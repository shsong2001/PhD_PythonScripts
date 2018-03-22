Readf = open('/home/cerecam/Desktop/SUPG_tricks/UserElements.inp','r')
import numpy as np

user_eles = []
dummies = []

i = 0
for line in Readf:
    if line[0] == '*':
        pass
    else:
        newarray = map(int,line.split(','))
        user_eles.append(map(float,line.split(',')))
        newarray[0] = newarray[0]+500000
        dummies.append(newarray)

Readf.close()
Writef = open('/home/cerecam/Desktop/SUPG_tricks//DummyElements.inp','w')
number = 0
for x in dummies:
    Writef.write(str(x).strip(']').strip('[')+'\n')
    number+=1

Writef.close()
