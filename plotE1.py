import csv

def plotxy(Results,fieldnames):
    colours = ['b','r','b','r']
    location = [3,3,2,2,1,2]
    lcount = 0
    LocationSorted1 = []
    LocationSorted2 = []
    Labels = {'MaxStrain':'Tensile Strain','MinStrain':'Compressive Strain','MaxStress':'Tensile Stress [GPa]','MinStress':'Compressive Stress [GPa]'}
    import matplotlib.pyplot as plt
    import numpy as np
    
##    ax1 = fig.add_subplot(len(fieldnames[1:-2]),1,i+1)
    for i,v in enumerate(fieldnames[1:-2]):
        count = 0
        fig = plt.figure(figsize=(8.5,3.5))
        ax1 = fig.add_subplot(1,1,1)
        for Odb in Results.keys():
            try:
                MinLocalG = min(Results[Odb]['Gold']['CentroidPerpendicular'])
            except:
                MinLocalG=10000000
            try:
                MinLocalP =min(Results[Odb]['Polymer']['CentroidPerpendicular'])
            except:
                MinLocalP=10000000
            MinLocal = min(MinLocalG,MinLocalP)
            print(MinLocal)
            LocationSorted1= [(Results[Odb]['Gold']['CentroidPerpendicular'][i]-MinLocal) for i in range(len(Results[Odb]['Gold']['CentroidPerpendicular']))]
            LocationSorted2 = [(Results[Odb]['Polymer']['CentroidPerpendicular'][i]-MinLocal) for i in range(len(Results[Odb]['Polymer']['CentroidPerpendicular']))]
            MaxPrincipSorted1 = Results[Odb]['Gold'][v]
            MaxPrincipSorted2 = Results[Odb]['Polymer'][v]
            print(str(Odb))
            print('Gold')
            try:
                print(max(MaxPrincipSorted1))
            except:
                pass
            try:        
                print(min(MaxPrincipSorted1))
            except:
                pass
            print('Polymer')
            try:
                print(min(MaxPrincipSorted2))
            except:
                pass
            try:
                print(max(MaxPrincipSorted2))
            except:
                pass
            try:
                print("average "+ v + ' in Gold: '+ str((sum(MaxPrincipSorted1)/len(MaxPrincipSorted1))))
                print("range "+ v + ' in Gold: '+ str((max(MaxPrincipSorted1)-min(MaxPrincipSorted1))))
            except:
                pass
            try:
                print("average "+ v + ' in Polymer: '+ str((sum(MaxPrincipSorted2)/len(MaxPrincipSorted2))))
                print("range "+ v + ' in Polymer: '+ str((max(MaxPrincipSorted2)-min(MaxPrincipSorted2))))
            except:
                pass
            
            if v == 'MaxStress' or v == 'MinStress':
                MaxPrincipSorted1 = [MaxPrincipSorted1[i]*10**(-9) for i in range(len(MaxPrincipSorted1))]
                MaxPrincipSorted2 = [MaxPrincipSorted2[i]*10**(-9) for i in range(len(MaxPrincipSorted2))]
            if Odb == 'PBCCompositeXComp':
                label1 = 'gold - composite'
                label2 = 'polymer - composite'
            else:
                label1 = 'gold - homogeneous'
                label2 = 'polymer - homogeneous'
##            print(label1)
##            print(label2)
            if MaxPrincipSorted1 !=[]:
                print('LocationSorted1: min')
                print(max(LocationSorted1))
                if MaxPrincipSorted2 == []:
                    LocationSorted1.append(547.81813)
                    MaxPrincipSorted1.append(MaxPrincipSorted1[0])
                    ax1.plot(LocationSorted1,MaxPrincipSorted1,c = colours[count-2],linewidth=7,label = label1)   
                else:
                    ax1.scatter(LocationSorted1,MaxPrincipSorted1,c = colours[count],s = 250, label = label1)
                count += 1
                
            if MaxPrincipSorted2 !=[]:
                if MaxPrincipSorted1 == []:
                    LocationSorted2.append(547.81813)
                    MaxPrincipSorted2.append(MaxPrincipSorted2[0])
                    ax1.plot(LocationSorted2,MaxPrincipSorted2,c = colours[count-2], linestyle= '--',linewidth=7, label = label2)
                else:
                    ax1.scatter(LocationSorted2,MaxPrincipSorted2,c = colours[count],s = 250, label = label2)
                count += 1
            if v == 'MaxStress' or v == 'MinStress':    
                plt.axis([-50, 600,-5,5])
                plt.yticks(np.arange(-5,5,1))
            else:
                plt.axis([-50, 600,-0.2,0.2])
                plt.yticks(np.arange(-0.2,0.2,0.05))
                      
            plt.xlabel('Position along RVE [nm]',size = 20)
            plt.ylabel(Labels[v],size = 20)
            plt.setp(ax1.get_xticklabels(), fontsize=18)
            plt.setp(ax1.get_yticklabels(), fontsize=18)
            plt.legend(prop={'size':15},loc = location[lcount])
            plt.subplots_adjust(left = 0.08, bottom = 0.09, right=0.96, top=0.93)
            
            
        plt.show()
        lcount = lcount+1
    
fieldnames = ['CentroidPerpendicular','MaxStrain','MinStrain','MaxStress','MinStress','Element','Material']
Odbs =['PBCCompositeXTen', 'HomogeneousGoldTenX','HomogeneousPolymerTenX']
##Odbs = ['/SUBCComposite', '/SUBCHomogenousGold','/SUBCHomogenousPolymer']
Results = {}
for OdbName in Odbs:
    if OdbName==Odbs[0]:
        Filename = '/home/cerecam/Desktop/PBCSims/'
    else:
        Filename = '/home/cerecam/Documents/NpgRVE/'
    vals = open(Filename + OdbName + '.csv','r')
    reader = csv.DictReader(vals, fieldnames = fieldnames)

    fieldoutputsLIST1 = {}
    fieldoutputsLIST2 = {}
    for i in fieldnames:
        fieldoutputsLIST1[i] = []
        fieldoutputsLIST2[i] = []
    line = 1
    for row in reader:
        line +=1
        if line >2:
            for i in fieldnames[:-2]:
                if row['Material'] == '0':
                    fieldoutputsLIST1[i].append(float(row[i]))
                if row['Material'] == '1':
                    fieldoutputsLIST2[i].append(float(row[i]))
    MatFieldOutputs = {'Gold':fieldoutputsLIST1,'Polymer':fieldoutputsLIST2}
    Results[OdbName] = MatFieldOutputs
    vals.close
#print(Results.keys())
plotxy(Results,fieldnames)
