"""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PyhtonScripts/ExtractFieldvariableAE_Data.py
"""


import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

currentwd = '/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/58_42'
outputwd = currentwd
Jobname = 'NPG_58_42'
#filename = sys.argv[-1]
if Jobname[0]!='/':
    Jobname = '/'+Jobname
odbfile = Jobname 
CArray = {}
UArray = {}
odbname = str(currentwd)+str(odbfile)+'.odb'
print >> sys.__stdout__, odbname
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
CONCEN = frame_val.fieldOutputs['NT11']
U = frame_val.fieldOutputs['U']
#print >> sys.__stdout__, str(CONCEN.values[1])
for count,label in enumerate(CONCEN.values):
    CArray[str(CONCEN.values[count].nodeLabel)] = CONCEN.values[count].dataDouble
for count,label in enumerate(U.values):
    UArray[str(U.values[count].nodeLabel)] = U.values[count].dataDouble
##NodeNum = np.array([ x.nodeLabel for x in CONCEN.values])
##CONCEN_Array = np.array([ round(float(CONCENvals.dataDouble),15) for CONCENvals in CONCEN.values]) 
##ELEC_Array = np.array([ round(float(ELECvals.dataDouble),15) for ELECvals in ELEC.values])
##U_Array = np.array([ Uvals.dataDouble for Uvals in U.values])
odb.close()

LineValuesNode = []
LineValuesC = []
LineValuesU1 = []
LineValuesU2 = []
LineValuesU3 = []

##FineMeshLine = [1211, 11167, 11141, 11115, 11089, 11063, 11037, 1022, 8827, 8801, 750, 6435, 6409, 721, 10335, 10309,
##                612, 5551, 5525, 547, 5291, 5265, 302, 2899, 2873, 273, 5343, 5317, 58, 1314, 1340, 85, 8854, 8880,
##                8906, 8932, 8958, 8984, 1055]
MidLine = [496,6760,6734,6708,6682,6656,6630,287,3224,3198,3172,3146,3120,3094,
           3068,3042,3016,2990,2964,2938,2912,2886,2860,2834,2808,2782,2756,
           2730,2704,2678,2652,2626,2600,2574,29,597,623,649,675,701,727,62]
#print >> sys.__stdout__, str(len(CArray))     
for val in MidLine:
    np.array(LineValuesNode.append([int(val)]))
    try:
        np.array(LineValuesC.append(float(CArray[str(val)])))
    except KeyError:
        np.array(LineValuesC.append(0.0))
    np.array(LineValuesU1.append(float(UArray[str(val)][0])))
    np.array(LineValuesU2.append(float(UArray[str(val)][1])))
    np.array(LineValuesU3.append(float(UArray[str(val)][2])))
##print >> sys.__stdout__, str()
np.savetxt((str(currentwd)+'/Results'+str(odbfile)+'DispConc.csv'),np.c_[LineValuesNode,LineValuesC,LineValuesU1,LineValuesU2,LineValuesU3], delimiter=",")
##np.savetxt((str(currentwd)+'/Results/'+str(odbfile)+'Results_PNPonly.csv'),np.c_[LineValuesNode,LineValuesC], delimiter=",")
    
