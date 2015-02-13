'''
Created on my MAC Feb 12, 2015-10:30:49 PM
What I do:
Partition input training data to k fold, line by line
What's my input:
a file
What's my output:
k * 2 file, each one for one fold
@author: chenyanxiong
'''


import random

def CVPartition(InName,OutPre,k=5):
    lTrainFoldOut = []
    lTestFoldOut = []
    for i in range(k):
        lTrainFoldOut.append(open(OutPre + '_train_%d' %(i),'w'))
        lTestFoldOut.append(open(OutPre + '_test_%d' %(i),'w'))
        
    for line in open(InName):
        r = random.randint(0,4)
        line = line.strip()
        for i in range(k):
            if i == r:
                print >> lTestFoldOut[i],line
            else:
                print >> lTrainFoldOut[i],line
                
    return