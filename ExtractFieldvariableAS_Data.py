"""
abaqus viewer noGui=/home/cerecam/Desktop/GIT/PhD_PyhtonScripts/ExtractFieldvariableAS_Data.py
"""


import numpy as np
import csv,math
import sys,os
from odbAccess import openOdb

currentwd = '/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42'
outputwd = currentwd
filename = sys.argv[-1]
odbfile = 'NPG_58_42_Standard' 
EArray = {}
if odbfile[0]!='/':
    odbfile = '/'+odbfile
odbname = str(currentwd)+str(odbfile)+'.odb'
odb = openOdb(odbname)
stepKey = odb.steps.keys()
steps = odb.steps[stepKey[-1]]
frame_val = steps.frames[-1]
myinstance = odb.rootAssembly.instances[odb.rootAssembly.instances.keys()[0]]
ELEC = frame_val.fieldOutputs['NT11']
for count,label in enumerate(ELEC.values):
    EArray[str(ELEC.values[count].nodeLabel)] = ELEC.values[count].dataDouble
odb.close()

LineValuesNode = []
LineValuesE = []
Topline = range(567,573)
Topline.append(10)
Topline.extend(range(301,327))
Topline.append(2)
Topline.extend(range(43,49))
Topline.append(3)
Midline = [496,6760,6734,6708,6682,6656,6630,287,3224,3198,3172,3146,3120,3094,
           3068,3042,3016,2990,2964,2938,2912,2886,2860,2834,2808,2782,2756,
           2730,2704,2678,2652,2626,2600,2574,29,597,623,649,675,701,727,62]
##print >> sys.__stdout__, str(CArray['10'])
LineValuesNode = []
LineValuesE = []
for val in Midline:
    np.array(LineValuesNode.append([int(val)]))
    try:
        np.array(LineValuesE.append(float(EArray[str(val)])))
    except KeyError:
        np.array(LineValuesE.append(0.0))
np.savetxt((str(currentwd)+'/Results/'+str(filename)+'Elec.csv'),np.c_[LineValuesNode,LineValuesE], delimiter=",")
