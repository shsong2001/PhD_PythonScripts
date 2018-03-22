# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 12:04:48 2018

abaqus python /home/cerecam/Desktop/GIT/PhD_PyhtonScripts/WriteOdbVUELFromOdb.py

This script creates a 3D odb for a model that contains user defined elements.
It creates the following field outputs:
    - Displacement (U1,U2.U3, Magnitude) [NODAL]
    - Strain (E11,E22,E33,E12,E23,E13, Mises, Max/Mid and Min Principal ) [GAUSS POINT]
    - Stress (S11,S22,S33,S12,S23,S13, Mises, Max/Mid and Min Principal ) [GAUSS POINT]
    - Concentration (Co) [NODAL]
    - Electric Potential [GAUSS POINT]

Inputs to consider/change:
    - materialNames (list of strings of material names)
    - MatE (list of floats of Young's modulus of materials in materialNames)
    - Matmu (list of floats of Poisson's ratio of materials in materialNames)
    - cwd (current working directory i.e. where old odb and relevant .inp files are found and where new odb will be saved)
    - OldOdbName (odb of user definied elements)
    - ElementFiles (list of strings of location [cwd + filename] of input files containing each material elements nodal connectivity)
    - odbpath (path to and odb name of new odb to be created)
    - numIntervals (number of intervals that a display/frame must be created min=1 [one at beginning and on at analysisTime])
    
@author: cerecam_E Griffiths
"""
##
# import abaqus libraries
from odbAccess import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *
import numpy as np

# import python libraries
import sys,time,csv,os

def StressStrain(Ele_Con, Node_Vals):
    GpCord = [0.25, 0.25, 0.25]
    Wt = 1.0
    QuadPnts = 1.0/6.0
    
    xi1=GpCord[0]
    xi2=GpCord[1]
    xi3=GpCord[2]
    pNN = [1.0-xi1-xi2-xi3, xi1, xi2, xi3]
    dNdXi1 = [-1.0, 1.0, 0.0, 0.0]
    dNdXi2 = [-1.0, 0.0, 1.0, 0.0]
    dNdXi3 = [-1.0, 0.0, 0.0, 1.0]
    dNdX1 = [0.0, 0.0, 0.0, 0.0]
    dNdX2 = [0.0, 0.0, 0.0, 0.0]
    dNdX3 = [0.0, 0.0, 0.0, 0.0]
    
    X1,X2,X3 = [],[],[]
    for node in Ele_Con:
        X1.append(Node_Vals[str(node)][0])
        X2.append(Node_Vals[str(node)][1])
        X3.append(Node_Vals[str(node)][2])
        
    
    dX1dxi1=np.dot(X1,dNdXi1)
    dX1dxi2=np.dot(X1,dNdXi2)
    dX1dxi3=np.dot(X1,dNdXi3)
    
    dX2dxi1=np.dot(X2,dNdXi1)
    dX2dxi2=np.dot(X2,dNdXi2)
    dX2dxi3=np.dot(X2,dNdXi3)
    
    dX3dxi1=np.dot(X3,dNdXi1)
    dX3dxi2=np.dot(X3,dNdXi2)
    dX3dxi3=np.dot(X3,dNdXi3)
    
    detJ = dX1dxi1*dX2dxi2*dX3dxi3 + dX2dxi1*dX3dxi2*dX1dxi3 + dX3dxi1*dX1dxi2*dX2dxi3 - dX1dxi3*dX2dxi2*dX3dxi1 - dX2dxi3*dX3dxi2*dX1dxi1 - dX3dxi3*dX1dxi2*dX2dxi1
    
    for nn in range(4):
        dNdX1[nn] = 1.0/detJ*( (dX2dxi2*dX3dxi3-dX3dxi2*dX2dxi3)*dNdXi1[nn] + 
                        (dX3dxi1*dX2dxi3-dX2dxi1*dX3dxi3)*dNdXi2[nn] + 
                        (dX2dxi1*dX3dxi2-dX3dxi1*dX2dxi2)*dNdXi3[nn] )
        dNdX2[nn] = 1.0/detJ*( (dX3dxi2*dX1dxi3-dX1dxi2*dX3dxi3)*dNdXi1[nn] +
                        (dX1dxi1*dX3dxi3-dX3dxi1*dX1dxi3)*dNdXi2[nn] +
                        (dX3dxi1*dX1dxi2-dX1dxi1*dX3dxi2)*dNdXi3[nn] )
        dNdX3[nn] = 1.0/detJ*( (dX1dxi2*dX2dxi3-dX2dxi2*dX1dxi3)*dNdXi1[nn] +
                        (dX2dxi1*dX1dxi3-dX1dxi1*dX2dxi3)*dNdXi2[nn] +
                        (dX1dxi1*dX2dxi2-dX2dxi1*dX1dxi2)*dNdXi3[nn] )
                        
    return dNdX1,dNdX2,dNdX3, pNN

#
#########################################################
# Opening old odb file (pure VUEL file) to get nodal data:
#########################################################
#
materialNames = ["Polymer", "Gold"]
MatE = [1.951,77.71]
Matmu = [0.3,0.44]

# File names and locations for old odb
cwd = '/home/cerecam/Dropbox/PhD/PythonCodes/'
OldOdbName = 'TestCase2.odb'
ElementFiles = [cwd + 'UserElements.inp',
                cwd +'GoldElements.inp'] # Files with element connectivity description
                
# Accessing necessary objects in old odb                
oldOdb=openOdb(cwd+OldOdbName)
assembly = oldOdb.rootAssembly
instance= assembly.instances
myinstance = assembly.instances[instance.keys()[0]]
steps = oldOdb.steps[oldOdb.steps.keys()[-1]]
lastframe = steps.frames[-1]
analysisTime = steps.frames[-1].frameValue
FieldOutputs = lastframe.fieldOutputs

# node data read from old odb file
nodeData = []
nodeDict = {}
for nodes in myinstance.nodes:
    intnode = (nodes.label, nodes.coordinates[0],nodes.coordinates[1],nodes.coordinates[2]) # Tuple of node data (node no., node x-coord, y-coord, z-coord)
    nodeDict[str(nodes.label)] = (nodes.coordinates[0],nodes.coordinates[1],nodes.coordinates[2]) 
    nodeData.append(intnode)
    del intnode

# Creates an ODB
odbpath = cwd+'/Cube_PythonWritten.odb'
odb = Odb(name='Model-1', analysisTitle = "ODB created by python script",
          description = "using python scripting to create an odb for showing VUEL data from a previous odb with no visualization elements",
          path = odbpath)
          
for num, mat in enumerate(materialNames):
    # Creates materials
    Material = odb.Material(name=mat)
    Material.Elastic(table=( (MatE[num], Matmu[num]),))
    #polymerMaterial.Density(table=(  (1.47E-6),0))
                  
    # Create sections
    section1 = odb.HomogeneousSolidSection(name=mat,
                                           material=mat)

# MODEL data:
part1 = odb.Part(name='Part-1', embeddedSpace=THREE_D, type=DEFORMABLE_BODY)    

part1.addNodes(nodeData=tuple(nodeData), nodeSetName='All_NODES') # add nodes to part

# Get element node-connectivity of old odb from .inp files and add to new odb part
EleList= []
Ele_Con_Dict = {}
for num, Fname in enumerate(ElementFiles):
    elementData1 = []
    Efile = open(Fname)
    for line in Efile:
        if line[0] == '*': # remove first line if element def present (i.e *element,type=...)
            break
        else:
            newarray = map(int,line.split(',')) # Read first line and convert string to a list of integers
            elementData1.append(tuple(newarray))
            Ele_Con_Dict[newarray[0]] = [newarray[1:],num] 
            EleList.append(newarray[0])             
            del newarray
    elementData1 = tuple(elementData1)
    Efile.close()
    part1.addElements(elementData=elementData1, type='C3D4', elementSetName=materialNames[num]) # add elements to part
EleList = sorted(EleList) # List of elements in ascending order

#print >> sys.__stdout__, str(len(EleList))
#a=b
# Instance the part
instance1= odb.rootAssembly.Instance(name='I_Cube', object=part1)

## FIELD DATA: 
# Field data extraction from .odb file
# Data must be written as a tuple (tuple of data), if SCALAR tuple of data written as (scalar,); 
#                                                              else if VECTOR (data1,data2,data3);
#                                                              else if TENSOR ((11,22,33,12,13,23),(...))

# Creating step and frame:

step1 = odb.Step(name = 'Step-1',
                 description = 'First step with displacement applied',
                 domain = TIME, timePeriod = 1.0)

numIntervals = 1
frequency = analysisTime/numIntervals 
FrameTime = 0.0

DispDataDict = {}
DispNodesDict = {}
TempDataDict = {}
TempNodesDict = {}
FieldValueDataDict = {}
FieldValueEleDict = {}
Efinal, S_totfinal = {}, {}
S_mechfinal, S_chemfinal, S_elecfinal = {}, {}, {}
count = 0

#ELecFile = 'ElecPotentialInitial.inp'
#ElecF = open(ElecFile,'r')
#ElecData = [0]*len(nodeData)
#for line in ElecF:
#    newarray = map(float,line.split(','))
#    ElecData[int(newarray[0][4:])] = newarray[1]
for MultiFrame in steps.frames:
#for MultiFrame in [steps.frames[-1]]:
#    FrameTime= round(MultiFrame.frameValue,2)
    if round(MultiFrame.frameValue,2)==FrameTime:
        
        #########################################################################################
        #OLD ODB DATA EXTRACTION AND MANIPULATIONS
        #########################################################################################
        
        # Displacement data at nodes:                   
        Dispfield = MultiFrame.fieldOutputs['U'] # Extract disp field output object from old Odb
        DispData = []
        DispNodes = []
        for val in Dispfield.values:
            DispNodes.append(val.nodeLabel) # Node label list
            DispData.append(tuple(val.dataDouble)) # Data at node
        #Add values to dictionary elemtn with key= frameValue
        DispDataDict[round(MultiFrame.frameValue,3)]=tuple(DispData)
        DispNodesDict[round(MultiFrame.frameValue,3)] = tuple(DispNodes)
        
       # Temperature data at nodes:
        Tempfield = MultiFrame.fieldOutputs['NT11']    # Extract Temperature fieldOutput object from old Odb
        TempData = []
        TempNodes = []
        for val in Tempfield.values:
            TempNodes.append(val.nodeLabel) # Node label list
            TempData.append(tuple([val.dataDouble,]))# Data at node
        TempDataDict[round(MultiFrame.frameValue,3)]=tuple(TempData)
        TempNodesDict[round(MultiFrame.frameValue,3)] = tuple(TempNodes)
#         # Elec data at Gauss point:
#        FieldValue = MultiFrame.fieldOutputs['FV1']    # Extract Temperature fieldOutput object from old Odb
#        FieldValueData = []
#        FieldValueEle = []
#        for val in FieldValue.values:
#            FieldValueEle.append(val.elementLabel-500000) # Element label list
#            FieldValueData.append(tuple([val.data,]))# Data at Gauss point
#            
#        FieldValueDataDict[round(MultiFrame.frameValue,3)]=tuple(FieldValueData)
#        FieldValueEleDict[round(MultiFrame.frameValue,3)] = tuple(FieldValueEle)
    
        Ee, Ss, Ee_principal, Ss_principal, V_mises = [],[],[],[],[]
        Ss_mech, Ss_chem, Ss_elec, Ss_tot = [], [], [], []
        
##################### MATERIAL PARAMETERS #############################

        e_r = 1.0E3
        e_zero = 8.854E-12
        F = 9.6485337E+04
        Z = -1.0
        k = 5.0E+01
        csat = 1.2E-3
        elements = []
        Mat = -1
        for Ele_Label in EleList:
            
            Mat = Ele_Con_Dict[Ele_Label][1]    # Material of specified element
            Ele_con = Ele_Con_Dict[Ele_Label][0] # Nodal connectivity of current element
            
            ## Elastic material parameters            
            Gmod =  0.5*MatE[Mat]/(1.0+Matmu[Mat])
            lam = (MatE[Mat]*Matmu[Mat])/((1.0+Matmu[Mat])*(1.0-2.0*Matmu[Mat]))
        
            Node_Vals = {}
#            Elec_Ele_Data = {}
            for i in Ele_con:    # Creates dictionary (key = node label) of nodal coordinates (X,Y,Z) for element in question (Ele_Con[0])
                Node_Vals[str(i)] = nodeDict[str(i)] 
#                Elec_Ele_Data[str(i)] = ElecData[int(i)]
        
            dNdX1,dNdX2,dNdX3, pNN = StressStrain(Ele_con, Node_Vals) # Function defining shape functions and there derivatives
            H = [0.0,0.0,0.0]
            Conc_gp = 0.0
            ElecField = [0.0,0.0,0.0]
            Tarray = []
            for x,y in enumerate(Ele_con):
                Uarray = DispData[int(y)-1]
                H = H + np.outer(Uarray,np.array([dNdX1[x],dNdX2[x],dNdX3[x]])) # Grad(U)
                if materialNames[Mat].lower() == 'polymer':               
                    Tarray.append(float(TempDataDict[round(MultiFrame.frameValue,3)][int(y)-1][0]))
                    
                else:
                    Tarray.append(csat)
#                a=b    
                
#                ElecField = ElecField - ((/dNdX1[x],dNdX2[x],dNdX3[x]/))*Elec_Ele_Data[y]
            Conc_gp =  np.dot(np.array(pNN),np.array(Tarray))
            
#            ElecDisp = np.array(e_zero*E_r*ElecField)
            Qf = F*((Z*Conc_gp+(csat)))
            
            if Ele_Label == 120:
                print >> sys.__stdout__, str(Tarray)
                print >> sys.__stdout__, str(Tarray)
            E = 0.5*(np.transpose(H)+H)   # Strain calculation at Gauss point 
#            if Ele_Label == 11150:
#                print >> sys.__stdout__, str(E)
                
            S_mech = 2.0*Gmod*E+lam*np.trace(E)*np.eye(3)  # Mecahnical stress calculation at Gauss point
            S_chem = -((k*Qf)/Z)*np.eye(3)  # Chemical Stress calculation at Gauss point
            
#            S_elec = 1.0/(e_zero*e_r)(*(np.outer(ElecDisp,ElecDisp)) - 0.5*(np.dot(ElecDisp,ElecDisp))*np.eye(3))
            S_elec = np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
            S_total = S_mech+S_chem+S_elec
            
            Ee.append(tuple(E.flatten()[[0,4,8,1,2,5]]))    # create vector format of strain data ('E11','E22','E33','E12','E13','E23')           
            Ss_mech.append(tuple(S_mech.flatten()[[0,4,8,1,2,5]]))   # create vector format of strain data ('S11','S22','S33','S12','S13','S23')
            Ss_chem.append(tuple(S_chem.flatten()[[0,4,8,1,2,5]]))  
            Ss_elec.append(tuple(S_elec.flatten()[[0,4,8,1,2,5]])) 
            Ss_tot.append(tuple(S_total.flatten()[[0,4,8,1,2,5]])) 
        # Store data for frame in question              
        Efinal[round(MultiFrame.frameValue,3)] = tuple(Ee)
#        print >> sys.__stdout__, str(Efinal)
        S_mechfinal[round(MultiFrame.frameValue,3)] = tuple(Ss_mech)
        S_chemfinal[round(MultiFrame.frameValue,3)] = tuple(Ss_chem) 
        S_elecfinal[round(MultiFrame.frameValue,3)] = tuple(Ss_elec)
        S_totfinal[round(MultiFrame.frameValue,3)] = tuple(Ss_tot)
        
        #########################################################################################
        #NEW ODB FIELD DATA CREATION
        #########################################################################################
        count +=1
        # Creation of displacement, cocentration, stress and strain field at n=numIntervals frames       
        frame=step1.Frame(incrementNumber=count,
                             frameValue=FrameTime,
                             description='Results at time :\t '+str(FrameTime)+'s' ) # Creation of new frame
        # Add fieldoutput object to new odb  
        newField3 = frame.FieldOutput(name='E',
                                       description='Small strain at gauss points', 
                                       type=TENSOR_3D_FULL, 
                                       componentLabels=('E11','E22','E33','E12','E13','E23'),
                                       validInvariants=(MISES,MAX_PRINCIPAL,MID_PRINCIPAL,MIN_PRINCIPAL)) # Creation of new field otput object called 'STRAIN'
       
       # Add strain field                                       
        newField3.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleList),
                          data=Efinal[round(FrameTime,3)])
                          
        # Add fieldoutput object to new odb                 
        newField4 = frame.FieldOutput(name='S',
                                       description='Total stress at gauss points', 
                                       type=TENSOR_3D_FULL, 
                                       componentLabels=('S11','S22','S33','S12','S13','S23'),
                                       validInvariants=(MISES,MAX_PRINCIPAL,MID_PRINCIPAL,MIN_PRINCIPAL))# Creation of new field otput object called 'STRESS'
        # Add Total stress field                               
        newField4.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleList),
                          data=S_totfinal[round(FrameTime,3)]) 

        # Add data to fieldoutput object                          
        newField5 = frame.FieldOutput(name='S_m',
                                       description='Mechanical stress at gauss points', 
                                       type=TENSOR_3D_FULL, 
                                       componentLabels=('Sm11','Sm22','Sm33','Sm12','Sm13','Sm23'),
                                       validInvariants=(MISES,MAX_PRINCIPAL,MID_PRINCIPAL,MIN_PRINCIPAL))# Creation of new field otput object called 'STRESS'
        # Add mechanical stress field                               
        newField5.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleList),
                          data=S_mechfinal[round(FrameTime,3)])

        # Add data to fieldoutput object                          
        newField6 = frame.FieldOutput(name='S_c',
                                       description='Chemical stress at gauss points', 
                                       type=TENSOR_3D_FULL, 
                                       componentLabels=('Sc11','Sc22','Sc33','Sc12','Sc13','Sc23'),
                                       validInvariants=(MISES,MAX_PRINCIPAL,MID_PRINCIPAL,MIN_PRINCIPAL))# Creation of new field otput object called 'STRESS'
        # Add chemical stress field                               
        newField6.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleList),
                          data=S_chemfinal[round(FrameTime,3)])                 

        # Add data to fieldoutput object                          
        newField7 = frame.FieldOutput(name='S_e',
                           description='Electrical stress at gauss points', 
                           type=TENSOR_3D_FULL, 
                           componentLabels=('Se11','Se22','Se33','Se12','Se13','Se23'),
                           validInvariants=(MISES,MAX_PRINCIPAL,MID_PRINCIPAL,MIN_PRINCIPAL))# Creation of new field otput object called 'STRESS'

        # Add electrical stress field                              
        newField7.addData(position=INTEGRATION_POINT,
                          instance=instance1,
                          labels=tuple(EleList),
                          data=S_elecfinal[round(FrameTime,3)])                    
                         
        # Add fieldoutput object to new odb
        newField = frame.FieldOutput(name='U',
                                     description='Displacements', 
                                     type=VECTOR,
                                     validInvariants=(MAGNITUDE,)) # Creation of new field otput object called 'U'
        # Add data to fieldoutput object
        newField.addData(position=NODAL,
                          instance=instance1,
                          labels=DispNodesDict[round(FrameTime,3)],
                          data=DispDataDict[round(FrameTime,3)])
        step1.setDefaultField(newField)
        
        # Add fieldoutput object to new odb
        newField2 = frame.FieldOutput(name='Co',
                                      description='Concentration', 
                                      type=SCALAR) # Creation of new field otput object called 'CONCENTRATION'
        # Add data to fieldoutput object
        newField2.addData(position=NODAL,
                          instance=instance1,
                          labels=TempNodesDict[round(FrameTime,3)],
                          data=TempDataDict[round(FrameTime,3)])
        
#        # Add fieldoutput object to new odb
#        newField5 = frame.FieldOutput(name='EP',
#                                     description='Electric potential', 
#                                     type=SCALAR)
#        # Add data to fieldoutput object
#        newField5.addData(position=INTEGRATION_POINT,
#                          instance=instance1,
#                          labels=FieldValueEleDict[round(FrameTime,3)],
#                          data=FieldValueDataDict[round(FrameTime,3)])
                          
        step1.setDefaultField(newField2)
        print >> sys.__stdout__, ('Displacement, temperature, electric potential, stress and strain  tensors created at '+str(FrameTime) + 's')
        
        FrameTime += frequency

oldOdb.close()
odb.save()
odb.close()