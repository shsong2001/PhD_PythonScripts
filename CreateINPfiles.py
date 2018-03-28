# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:00:08 2018

@author: cerecam
"""

import numpy as np
##from log import abqPrint
import csv,math
import sys,os

filenameR='/home/cerecam/Desktop/Models/HalfSize_LowRes_58/NodePhase.txt'
readf = open(filenameR,'r')
filenameW1 = '/home/cerecam/Desktop/Models/HalfSize_LowRes_58/Nodes.inp'
writef1 = open(filenameW1,'w')
count = 1
for line in readf:
    writef1.write(str(count)+',\t'+line)
    count += 1
readf.close()
writef1.close()

filenameR='/home/cerecam/Desktop/Models/HalfSize_LowRes_58/ElemPhase.txt'
readf = open(filenameR,'r')
filenameW1 = '/home/cerecam/Desktop/Models/HalfSize_LowRes_58/Elements1.inp'
writef1 = open(filenameW1,'w')
filenameW2 = '/home/cerecam/Desktop/Models/HalfSize_LowRes_58/Elements2.inp'
writef2 = open(filenameW2,'w')
count = 1
for line in readf:
    if count<(329931+1):
        writef1.write(str(count)+',\t'+line)
    else:        
        writef2.write(str(count)+',\t'+line)
    count += 1
readf.close()
writef1.close()
writef2.close()
    
filenameR='/home/cerecam/Desktop/Models/HalfSize_LowRes_58/NodePhase.txt'
readf = open(filenameR,'r')
filenameW1 = '/home/cerecam/Desktop/Models/HalfSize_LowRes_58/Nodes1.inp'
writef1 = open(filenameW1,'w')
filenameW2 = '/home/cerecam/Desktop/Models/HalfSize_LowRes_58/Nodes2.inp'
writef2 = open(filenameW2,'w')
count = 1
for line in readf:
    if count<(83499+1):
        writef1.write(str(count)+',\t'+line)
    else:        
        writef2.write(str(count)+',\t'+line)
    count += 1
readf.close()
writef1.close()
writef2.close()    
