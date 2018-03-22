# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:25:54 2018

@author: cerecam
"""
cwd = '/home/cerecam/Desktop/Npg_Comp_Model_73_27/73_27/'
NodeFile = 'Nodes.inp'
Mat0File = 'GoldElements_Con.inp'
Mat1File = 'PolymerElements_Con.inp'
projectName = 'Periodic_NPG_73_27'
Instancename = 'i_cube'


import numpy as np
readf = open(cwd +NodeFile,'r') # All nodes with coordinates
writef = open(cwd + 'Nodes_'+str(projectName) + '.txt','w')
nodes = {}
readf.readline()
for line in readf:
    newarray = map(float,line.split(','))
    writef.write(str(newarray[1:]).strip('[').strip(']')+'\n')
readf.close()
writef.close()

ElementSets1 = []
ElementSets2 = []
readf = open(cwd + Mat0File,'r') # All nodes with coordinates
elements = [0]*(54511)
for line in readf:
    newarray = map(int,line.split(','))
    elements[newarray[0]] = newarray[1:]
    ElementSets1.append(newarray[0])
#    writef.write(str(newarray[1:]).strip('[').strip(']')+'\n')
readf.close()

readf = open(cwd + Mat1File,'r') # All nodes with coordinates
for line in readf:
    newarray = map(int,line.split(','))
    elements[newarray[0]] = newarray[1:]
    ElementSets2.append(newarray[0])
readf.close()

elements=elements[1:]
writef = open(cwd + 'Elements_'+projectName + '.txt','w')
for i in elements:
    writef.write(str(i).strip('[').strip(']')+'\n')
writef.close()

ElementSets1.sort()
ElementSets2.sort()
#
#ElementSets1 = list(np.arange(1,20225+1))
#ElementSets2 = (list(np.arange(20226,39184+1)))
ElementSets = [ElementSets1, ElementSets2]
writef = open(cwd + 'Element_Sets_' + projectName + '.txt','w')
for i in ElementSets:
    for x in range(0,len(i),10):
        writef.write(str(i[x:x+11]).strip('[').strip(']')+'\n')
    writef.write('\n')
writef.close()