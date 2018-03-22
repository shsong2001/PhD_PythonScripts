"""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PyhtonScripts/ExtractFieldvariableCSV.py  
"""


import numpy as np
##from log import abqPrint
import csv,math
import sys,os

from odbAccess import openOdb

currentwd = '/home/cerecam/Desktop/Npg_Comp_Model_73_27/73_27'
odbfile  = 'NPG_73_27_Standard'
#FileOut = '/DispConc/LinearConcentration'
FileOut = '/ElecPotentials'
InstanceName = 'RVE.'
FO = 'NT11'
if odbfile[0]!='/':
    odbfile = '/'+odbfile
print >> sys.__stdout__, ('Extracting Values from '+currentwd+odbfile)

odbname = str(currentwd)+str(odbfile)+'.odb'
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
CONCEN = frame_val.fieldOutputs[FO]
NodeNum = np.array([ x.nodeLabel for x in CONCEN.values])       # numpy array containing node numbers
CONCEN_Array = np.array([ round(float(CONCENvals.dataDouble),15) for CONCENvals in CONCEN.values])    #numpy array containing concentrations at each node

np.savetxt((str(currentwd)+str(FileOut)+".csv"),CONCEN_Array, delimiter=",")
InitialFile=open(str(currentwd)+str(FileOut)+"Initial_RVE.inp", 'w')
ElecFieldFile = open(str(currentwd)+str(FileOut)+"_RVE.inp", 'w')
count = 0
for i in NodeNum:
    InitialFile.write(InstanceName+str(i)+',\t'+str(CONCEN_Array[count])+'\n')
    ElecFieldFile.write(InstanceName+str(i)+',\t'+str(CONCEN_Array[count])+'\n')
    count+=1


InitialFile.close()
ElecFieldFile.close()
odb.close()
print >> sys.__stdout__, ('Electric field extraction SUCCESSFUL')
