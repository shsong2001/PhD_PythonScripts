"""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PyhtonScripts/ExtractFieldvariableAE_2_AS.py 
"""


import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

currentwd = '/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42'
outputwd = currentwd

#JobnameFile = open('/home/cerecam/Desktop/AbqJob2.txt','r')
#Jobname = str(JobnameFile.readlines()[0])
#JobnameFile.close()
#Jobname = Jobname.strip()
Jobname = 'NPG_58_42'
if Jobname[0]!='/':
    Jobname = '/'+Jobname
odbfile = Jobname
FileOut = '/Concentrationfield'
FO = 'NT11'

print >> sys.__stdout__, ('Extracting Values from '+currentwd+odbfile)

odbname = str(currentwd)+str(odbfile)+'.odb'
Tempf = open(str(outputwd)+str(FileOut)+".inp", 'w')
##Elecf = open(str(outputwd)+"ElecPotentialfield_AE.inp", 'w')
##p = open(str(outputwd)+"/CheckTimemarks.inp", 'w')
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
CONCEN = frame_val.fieldOutputs[FO]
##ELEC = frame_val.fieldOutputs['FV1']
NodeNum = np.array([ x.nodeLabel for x in CONCEN.values])
CONCEN_Array = np.array([ round(float(CONCENvals.dataDouble),15) for CONCENvals in CONCEN.values]) 
##ELEC_Array = np.array([ round(float(ELECvals.data),15) for ELECvals in ELEC.values]) 

for count,i in enumerate(NodeNum):
    Tempf.write('I_CUBE.'+str(i)+',\t'+str(CONCEN_Array[count])+'\n')

Tempf.close()
odb.close()
print >> sys.__stdout__, ('Concentration field extraction SUCCESSFUL')
