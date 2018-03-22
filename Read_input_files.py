# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:25:54 2018

@author: cerecam
"""

readf = open('/home/cerecam/Desktop/MesoporousSilica/Short/Nodes.inp','r') # All nodes with coordinates
writef = open('/home/cerecam/Desktop/MesoporousSilica/Short/Nodes_silica.txt','w')
nodes = {}
readf.readline()
for line in readf:
    newarray = map(float,line.split(','))
    writef.write(str(newarray[1:]).strip('[').strip(']')+'\n')
readf.close()
writef.close()

#readf = open('/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/Elements.inp','r') # All elements with connectivity in the model 
#elements = {}
#for line in readf:
#    newarray = map(int,line.split(','))    
#    elements[newarray[0]] = newarray
#readf.close()
#gold_elements = []
#polymer_elements = []
#
#readfg = open('/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/GoldElements.inp','r') # Elements within gold element set
##readfg.readline()
#for line in readfg:
#    newarray = map(int,line.split(',')[0:-1])    
#    gold_elements.extend(newarray)
#readfg.close()
#readfp = open('/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/PolymerElements.inp','r') # Elements within polymer element set
##readfp.readline()
#for line in readfp:
#    newarray = map(int,line.split(',')[0:-1])     
#    polymer_elements.extend(newarray)
#readfp.close()
#
#All_Elements = []
#All_Elements.extend(set(gold_elements))
#All_Elements.extend(set(polymer_elements))
#All_Elements.sort()
##elements.sort()
#count = -1
#for i in All_Elements:
#    count +=1
#    try:
#        elements[i]
#    except KeyError:
#        print(elements[i])
#        break
##
#write_gold = open('/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/GoldElements_Con.inp','w') # Connectivity of gold elements
#for i in sorted(gold_elements):
#    write_gold.write(str(elements[i]).strip('[').strip(']')+'\n')
#write_gold.close()
#
#write_polymer = open('/home/cerecam/Desktop/Npg_Comp_Model_58_42/58_42/PolymerElements_Con.inp','w') # Connectivity of gold elements
#for i in sorted(polymer_elements):
#    write_polymer.write(str(elements[i]).strip('[').strip(']')+'\n')   
#write_polymer.close()