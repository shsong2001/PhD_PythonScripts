# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:48:58 2017

@author: cerecam

abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PythonScriptsNOdeSetCreation.py
"""

def writefile(filename, values,nset, instanceName):
    # Creates file will heading '*Nset, nset='+str(nset)+', instance=RVE\n'
    # Writes first entry from list of lists given by values argument.
    F = open(filename,'w+')
    F.write('*Nset, nset='+str(nset)+', instance='+str(instanceName) + '\n')
    count = 1
    for val in values:   
        if count%14 == 0:
            F.write(str(val[0])+'\n')
            count +=1
        else:
            F.write(str(val[0])+', ')   
            count  += 1
            
    F.close()
    
def writefile2(filename, values,heading):
    # Creates file with heading 'heading'
    # Writes entries from list given by values argument.
    F = open(filename,'w')
    F.write(heading)
    count = 1
    for val in values:   
        if count%14 == 0:
            F.write(str(val)+'\n')
            count +=1
        else:
            F.write(str(val)+', ')   
            count  += 1
            
    F.close()
#    print >> sys.__stdout__, (str(filename)+' has been written with '+ str(len(values)))

import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

Dimensions = [(0.0,1.0),(0.0,1.0),(0.0,1.0)]
##############################################################
#INPUTS TO DEFINE!!!!!!!!!!!!!
currentwd = '/home/cerecam/Desktop/Voxel_models/2M_32x32x32'
outputwd = currentwd
filename = 'Voxel32'
odbfile = '/Voxel32' 
material1= 'Gold'
material2= 'Dummy'
instanceName = 'i_cube'
inputFile='Voxel32.inp'
##############################################################

odbname = str(currentwd)+str(odbfile)+'.odb'
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
Mat2NodeArray= []
Mat2Front = []
Mat2FrontEle = [1]
Mat2FrontEle1 = [1]
Mat2Back = []
Mat2BackEle = [1]
Mat2BackEle1 = [1]
Mat2Right = []
Mat2RightEle = [1]
Mat2RightEle1 = [1]
Mat2Left = []
Mat2LeftEle = [1]
Mat2LeftEle1 = [1]
Mat2Top = []
Mat2TopEle = [1]
Mat2TopEle1 = [1]
Mat2Bottom = []
Mat2BottomEle = [1]
Mat2BottomEle1 = [1]
for ele in myinstance.elementSets[material2.upper()].elements:
        Mat2NodeArray.extend(list(ele.connectivity))
#        conecF = 0
#        conecB = 0
#        conecL = 0
#        conecR = 0
#        conecT = 0
#        conecBot = 0
        for node in ele.connectivity:
            if round(myinstance.nodes[int(node)-1].coordinates[2],4)== Dimensions[2][1]:
#                 conecF +=1
                 Mat2Front.append(node)
#                 if conecF >2:
#                     if Mat2FrontEle[-1] != str(ele.label):
#                         Mat2FrontEle.append(str(int(ele.label)-500000))
#                         Mat2FrontEle1.append(str(int(ele.label)))
#                         Mat2FrontEle.sort()
#                         Mat2FrontEle1.sort()
#                     conecF = -1
            if round(myinstance.nodes[int(node)-1].coordinates[2],4)== Dimensions[2][0]:
#                 conecB +=1
                 Mat2Back.append(node)
#                 if conecB >2:
#                     if Mat2BackEle[-1] != str(int(ele.label)):
#                         Mat2BackEle.append(str(int(ele.label)-500000))
#                         Mat2BackEle1.append(str(int(ele.label)))
#                         Mat2BackEle.sort()
#                         Mat2BackEle1.sort()
#                     conecB = -1
            if round(myinstance.nodes[int(node)-1].coordinates[0],4)== Dimensions[0][1]:
#                 conecR +=1
                 Mat2Right.append(node)
#                 if conecR >2:
#                     if Mat2RightEle[-1] != str(int(ele.label)):
#                         Mat2RightEle.append(str(int(ele.label)-500000))
#                         Mat2RightEle1.append(str(int(ele.label)))
#                         Mat2RightEle.sort()
#                         Mat2RightEle1.sort()
#                     conecR = -1
            if round(myinstance.nodes[int(node)-1].coordinates[0],4)== Dimensions[0][0]:
#                 conecL +=1
                 Mat2Left.append(node)
#                 if conecL >2:
#                     if Mat2LeftEle[-1] != str(int(ele.label)):
#                         Mat2LeftEle.append(str(int(ele.label)-500000))
#                         Mat2LeftEle1.append(str(int(ele.label)))
#                         Mat2LeftEle.sort()
#                         Mat2LeftEle1.sort()
#                     conecL = -1
            if round(myinstance.nodes[int(node)-1].coordinates[1],4)== Dimensions[1][1]:
#                 conecT +=1
                 Mat2Top.append(node)
#                 if conecT >2:
#                     if Mat2TopEle[-1] != str(int(ele.label)):
#                         Mat2TopEle.append(str(int(ele.label)-500000))
#                         Mat2TopEle1.append(str(int(ele.label)))
#                         Mat2TopEle.sort()
#                         Mat2TopEle1.sort()
#                     conecT = -1
            if round(myinstance.nodes[int(node)-1].coordinates[1],4)== Dimensions[1][0]:
#                 conecBot +=1
                 Mat2Bottom.append(node)
#                 if conecBot >2:
#                     if Mat2BottomEle[-1] != str(int(ele.label)):
#                         Mat2BottomEle.append(str(int(ele.label)-500000))
#                         Mat2BottomEle1.append(str(int(ele.label)))
#                         Mat2BottomEle.sort()
#                         Mat2BottomEle1.sort()
#                     conecBot = -1

                     
Mat2NodeArray= sorted(list(set(Mat2NodeArray)))
print >> sys.__stdout__, ('Number of '+material2+' nodes: '+str(len(list(set(Mat2NodeArray)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on front: '+str(len(list(set(Mat2Front)))))
#print >> sys.__stdout__, ('Number of '+material2+' element on front: '+str(len(list(set(Mat2FrontEle)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on back: '+str(len(list(set(Mat2Back)))))
#print >> sys.__stdout__, ('Number of '+material2+' elements on back: '+str(len(list(set(Mat2BackEle)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on right: '+str(len(list(set(Mat2Right)))))
#print >> sys.__stdout__, ('Number of '+material2+' elements on right: '+str(len(list(set(Mat2RightEle)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on left: '+str(len(list(set(Mat2Left)))))
#print >> sys.__stdout__, ('Number of '+material2+' elements on left: '+str(len(list(set(Mat2LeftEle)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on top: '+str(len(list(set(Mat2Top)))))
#print >> sys.__stdout__, ('Number of '+material2+' elements on top: '+str(len(list(set(Mat2TopEle)))))
print >> sys.__stdout__, ('Number of '+material2+' nodes on bottom: '+str(len(list(set(Mat2Bottom)))))
#print >> sys.__stdout__, ('Number of '+material2+' elements on bottom: '+str(len(list(set(Mat2BottomEle)))))

#filename = 'nodeSets/Number'+material2+'EleSetFront.inp'
#F = open(filename,'w+')
#F.write(str(len(Mat2FrontEle)))
#F.close()
#
#filename ='nodeSets/Number'+material2+'EleSetBack.inp'
#F = open(filename,'w+')
#F.write(str(len(Mat2FrontEle)))
#F.close()

Mat1NodeArray = []

for ele in myinstance.elementSets[material1.upper()].elements:
    Mat1NodeArray.extend(list(ele.connectivity))
Mat1NodeArray = sorted(list(set(Mat1NodeArray)))
print >> sys.__stdout__, ('Number of '+material1+' nodes: '+str(len(Mat1NodeArray)))
Mat1LessMat2 = [GlessP for GlessP in Mat2NodeArray if GlessP not in Mat1NodeArray ]
Mat2LessMat1 = [PlessG for PlessG in Mat1NodeArray if PlessG not in Mat2NodeArray ]

    
#filename = currentwd+'/nodeSets/'+material1+'Node.inp'
#values = Mat1NodeArray
#heading = '*Nset, nset='+material1+'Nodes, instance='+str(instanceName) + '\n' 
#writefile2(filename, values,heading)

#filename = currentwd+'/nodeSets/'+material2+'NodeSet.inp'
#values = Mat2NodeArray
#heading = '*Nset, nset='+material2+'Nodes, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)

#filename = currentwd+'/nodeSets/'+material2+'NodeSetFront.inp'
#values = Mat2Front
#heading = '*Nset, nset='+material2+'Nodes_Front, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)

#filename = currentwd+'/nodeSets/'+material2+'NodeSetBack.inp'
#values = Mat2Back
#heading = '*Nset, nset='+material2+'Nodes_Back, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)

#filename = currentwd+'/nodeSets/'+material2+'EleSetFront.inp'
#values = Mat2FrontEle
#heading = '*Elset, elset= '+material2+'Ele_Front, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)
#with open((str(currentwd)+'/nodeSets/'+material2+'EleSetFront.csv'),'wb') as csvfile:
#    elewriter = csv.writer(csvfile,delimiter = ',')
#    elewriter.writerow(values)
#filename = currentwd+'/nodeSets/'+material2+'EleSetFront1.inp'
#values = Mat2FrontEle1
#heading = '*Elset, elset= '+material2+'Ele_Front, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)
#
#filename = currentwd+'/nodeSets/'+material2+'EleSetBack.inp'
#values = Mat2BackEle
#heading = '*Elset, elset='+material2+'Ele_Back, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)
#with open((str(currentwd)+'/nodeSets/'+material2+'EleSetBack.csv'),'wb') as csvfile:
#    elewriter = csv.writer(csvfile,delimiter = ',')
#    elewriter.writerow(values)
#filename = currentwd+'/nodeSets/'+material2+'EleSetBack1.inp'
#values = Mat2BackEle1
#heading = '*Elset, elset='+material2+'Ele_Back1, instance='+str(instanceName) + '\n'
#writefile2(filename, values,heading)

RightFull, LeftFull, Right, Left, Top, Bottom, Front, Back = [], [], [], [], [], [], [], []

R_T_F, L_T_F, R_Bot_F, L_Bot_F = [],[],[],[]
R_T_B, L_T_B, R_Bot_B, L_Bot_B = [],[],[],[]
R_F, R_Bot, R_T, R_B = [],[],[],[]
L_F, L_Bot, L_T, L_B = [],[],[],[]
T_F, T_B, Bot_F, Bot_B = [],[],[],[]
BottomFull, TopFull, FrontFull, BackFull, RightFull, LeftFull = [],[],[],[],[],[]

nodeArray = myinstance.nodes
filename2 = 'nodeSets/SingleNodeSet.inp'
F2 = open(filename2,'w+')
for count,val in enumerate(myinstance.nodes):
    F2.write('*NSET, nset=RVE_'+ str(val.label) + ', instance='+str(instanceName) + '\n'+ str(val.label) + '\n' )
    R, L, T, Bot, F, B =0,0,0,0,0,0

    if round(val.coordinates[0],4) == Dimensions[0][1]:
        RightFull.append((val.label,val.coordinates))
        
        
    if round(val.coordinates[0],4) == Dimensions[0][0]:
        LeftFull.append((val.label,val.coordinates))
        
    if (round(val.coordinates[0],4) >= Dimensions[0][0]) & (round(val.coordinates[0],4) <= Dimensions[0][1]):
        if round(val.coordinates[1],4) == Dimensions[1][1]:
            T=1
            TopFull.append((val.label,val.coordinates))
        if round(val.coordinates[1],4) == Dimensions[1][0]:
            Bot=1
            BottomFull.append((val.label,val.coordinates))
        if round(val.coordinates[2],4) == Dimensions[2][1]:
            F=1 
            FrontFull.append((val.label,val.coordinates))
        if round(val.coordinates[2],4) == Dimensions[2][0]:
            B=1
            BackFull.append((val.label,val.coordinates))
        if round(val.coordinates[0],4) == Dimensions[0][1]:
            R =1
            if T ==1:                
                if (F == 1):
                    R_T_F.append((val.label,val.coordinates))
                elif (B == 1):
                    R_T_B.append((val.label,val.coordinates))
                else:
                    R_T.append((val.label,val.coordinates))
                    
            elif Bot ==1:
                if (F == 1):
                    R_Bot_F.append((val.label,val.coordinates))
                elif (B == 1):
                    R_Bot_B.append((val.label,val.coordinates))
                else:
                    R_Bot.append((val.label,val.coordinates))
                
            elif F ==1:
                R_F.append((val.label,val.coordinates))
                
            elif B ==1:
                R_B.append((val.label,val.coordinates))
            else:
                Right.append((val.label,val.coordinates))    

        if round(val.coordinates[0],4) == Dimensions[0][0]:
            L =1
            if T ==1:                
                if (F == 1):
                    L_T_F.append((val.label,val.coordinates))
                elif (B == 1):
                    L_T_B.append((val.label,val.coordinates))
                else:
                    L_T.append((val.label,val.coordinates))
                    
            elif Bot ==1:
                if (F == 1):
                    L_Bot_F.append((val.label,val.coordinates))
                elif (B == 1):
                    L_Bot_B.append((val.label,val.coordinates))
                else:
                    L_Bot.append((val.label,val.coordinates))
                
            elif (F ==1):
                L_F.append((val.label,val.coordinates))
                
            elif B ==1:
                L_B.append((val.label,val.coordinates))
            else:
                Left.append((val.label,val.coordinates))
                
        if (T==1) and (L == 0) and (F == 0) and (B == 0) and (R ==0):
            Top.append((val.label,val.coordinates))
        if (Bot==1) and (L == 0) and (F == 0) and (B == 0) and (R ==0):
            Bottom.append((val.label,val.coordinates))
        if T ==1 and (F==1) and (L==0) and (R ==0):
            T_F.append((val.label,val.coordinates))
        if Bot ==1 and (F==1) and (L==0) and (R ==0):
            Bot_F.append((val.label,val.coordinates))
        if (F==1) and (L == 0) and (T == 0) and (Bot == 0) and (R ==0):
            Front.append((val.label,val.coordinates))
        if T ==1 and (B==1) and (L==0) and (R ==0):
            T_B.append((val.label,val.coordinates))
        if Bot ==1 and (B==1) and (L==0) and (R ==0):
            Bot_B.append((val.label,val.coordinates))
        if (B==1) and (L == 0) and (T == 0) and (Bot == 0) and (R ==0):
            Back.append((val.label,val.coordinates))
F2.close()
#        if str(val.label) == '4432':
#            print >> sys.__stdout__, (str(R)+str(L)+str(Bot)+str(T)+str(F)+str(B)+str(L)+str(R))
RightFull = sorted(RightFull, key=lambda x: x[1][1])
LeftFull = sorted(LeftFull, key=lambda x: x[1][1])
Right = sorted(Right, key=lambda x: x[1][1])
Left = sorted(Left, key=lambda x: x[1][1])
Top = sorted(Top, key=lambda x: x[1][1])
Bottom = sorted(Bottom, key=lambda x: x[1][1])
Back = sorted(Back, key=lambda x: x[1][1])
Front = sorted(Front, key=lambda x: x[1][1])
R_T = sorted(R_T, key=lambda x: x[1][1])
R_Bot = sorted(R_Bot, key=lambda x: x[1][1])
R_F = sorted(R_F, key=lambda x: x[1][1])
R_B = sorted(R_B, key=lambda x: x[1][1])
R_T_F = sorted(R_T_F, key=lambda x: x[1][1])
R_T_B = sorted(R_T_B, key=lambda x: x[1][1])
R_Bot_F = sorted(R_Bot_F, key=lambda x: x[1][1])
R_Bot_B = sorted(R_Bot_B, key=lambda x: x[1][1])
L_T = sorted(L_T, key=lambda x: x[1][1])
L_Bot = sorted(L_Bot, key=lambda x: x[1][1])
L_F = sorted(L_F, key=lambda x: x[1][1])
L_B = sorted(L_B, key=lambda x: x[1][1])
L_T_F = sorted(L_T_F, key=lambda x: x[1][1])
L_T_B = sorted(L_T_B, key=lambda x: x[1][1])
L_Bot_F = sorted(L_Bot_F, key=lambda x: x[1][1])
L_Bot_B = sorted(L_Bot_B, key=lambda x: x[1][1])
T_F = sorted(T_F, key=lambda x: x[1][1])
T_B = sorted(T_B, key=lambda x: x[1][1])
Bot_F = sorted(Bot_F, key=lambda x: x[1][1])
Bot_B = sorted(Bot_B, key=lambda x: x[1][1])
               
nodeSets = {'Right':Right,'Left':Left,'Top':Top,'Bottom':Bottom,'Back':Back,'Front':Front,
            'TopFULL':TopFull,'BottomFULL':BottomFull,'BackFULL':BackFull,'FrontFULL':FrontFull,'RightFULL':RightFull,'LeftFULL':LeftFull,
            'R_T':R_T,'R_Bot':R_Bot,'R_F':R_F,'R_B':R_B,'R_T_F':R_T_F,'R_T_B':R_T_B,'R_Bot_F':R_Bot_F,'R_Bot_B':R_Bot_B,
            'L_T':L_T,'L_Bot':L_Bot,'L_F':L_F,'L_B':L_B,'L_T_F':L_T_F,'L_T_B':L_T_B,'L_Bot_F':L_Bot_F,'L_Bot_B':L_Bot_B,
            'T_F' : T_F, 'T_B': T_B, 'Bot_F': Bot_F, 'Bot_B':Bot_B}
for key,value in nodeSets.items():
    filename = 'nodeSets/'+str(key)+'.inp'
    writefile(filename, value, key, instanceName)


SetNames = {material1+'Nodes':Mat1NodeArray,material2+'Nodes':Mat2NodeArray,material2+'Node_Front':Mat2Front,
            material2+'Node_Back':Mat2Back,material2+'Node_Right':Mat2Right,material2+'Node_Left':Mat2Left,
            material2+'Node_Top':Mat2Top,material2+'Node_Bottom':Mat2Bottom,
            material2+'_Less_'+material1+'Nodes':Mat1LessMat2,material1+'_Less_'+material2+'Nodes':Mat2LessMat1}
            

for key,vals in SetNames.items():
    filename = 'nodeSets/'+key+'.inp'
    values = list(set(vals[1:]))
    heading = '*Nset, nset='+key+', instance='+str(instanceName) + '\n' 
    writefile2(filename, values,heading)
    
###################################################
#Write new nsets to input file
###################################################
    
f = open('NodesetList.inp','w')
for key in nodeSets.keys():
    f.write('*INCLUDE, INPUT=nodeSets/'+key+'.inp\n')
for key in SetNames.keys():
    f.write('*INCLUDE, INPUT=nodeSets/'+key+'.inp\n')
f.close()