'''
Created on my MAC Feb 10, 2015-11:21:37 PM
What I do:
I generate SVM format training data from RawClassTrainingData(class\t word word)
word with df <= 1 is discarded
word weights is tf * log(DocCnt/DF)

What's my input:
    RawClassTraining Data: class \t word word word...
    DF from the RawClassTraining data
What's my output:
    svm format training data
    class->class id (pickle)
    word->word id (pickle)
@author: chenyanxiong
'''

import site
site.addsitedir('/Users/chenyanxiong/workspace/cxZhitu')
import sys
from cxBasic.Conf import cxConfC
import math
import os
import pickle


def TransferOneLine(text,hWordDF,hWordHash,hClassHash,ClassName = ""):
    '''
    I transfer one line of raw training data
    hWordDF: input df cnt dict
    hWordHash: to update word hash   | will modify
    hClassHash: to update class hash | will modify
    '''
    
    lW = text.split()
    if ClassName != "":
        if not ClassName in hClassHash:
            hClassHash[ClassName] = len(hClassHash) + 1
        ClassId = hClassHash[ClassName]
    else:
        ClassId = 0
    DocCnt = hWordDF['DocCnt']
    hW = {}
    for w in lW:
        if len(w) < 4:
            #single term discarded
            continue
        if not w in hWordDF:
            continue
        df = hWordDF[w]
        if df < 5:   #rare word discarded
            continue
        if not w in hW:
            hW[w] = 1
        else:
            hW[w] += 1
    hWordIdWeight = {}
    for key,score in hW.items():
        score *= math.log(DocCnt / float(hWordDF[key]))
        if not key in hWordHash:
            hWordHash[key] = len(hWordHash) + 1
        WordId = hWordHash[key]
        hWordIdWeight[WordId] = score
    
    
        
    lFeature = hWordIdWeight.items()
    lFeature.sort(key=lambda item:item[0])
    lFeatureStr = ["%d:%f" %(item[0],item[1]) for item in lFeature]
    
    res = '%d %s' %(ClassId,' '.join(lFeatureStr))
    return res
    

if 2 != len(sys.argv):
    print 'I transfer raw data to svm format'
    print 'in=\nout=\nworddfdict=\nwordiddict=\nclassiddict=\n'        
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
WordDfIn = conf.GetConf('worddfdict')
WordIdIn = conf.GetConf('wordiddict')
ClassIdIn = conf.GetConf('classiddict')

hWordDF = pickle.load(open(WordDfIn))
hWordHash = {}
hClassHash = {}
if os.path.exists(WordIdIn):
    hWordHash = pickle.load(open(WordIdIn))
if os.path.exists(ClassIdIn):
    hWordHash = pickle.load(open(ClassIdIn))
    
    
out = open(OutName,'w')
cnt = 0
for line in open(InName):
    line = line.strip()
    vCol = line.split('\t')
    if len(vCol) < 2:
        continue
    ClassName,text = vCol[:2]
    print >> out, TransferOneLine(text, hWordDF, hWordHash, hClassHash,ClassName)
    cnt += 1
    if 0 == (cnt % 1000):
        print 'processed [%d] line' %(cnt)


out.close()
print 'svm format transferred'
print 'feature dim: %d\nclass dim: %d'%(len(hWordHash),len(hClassHash))
pickle.dump(hWordHash,open(WordIdIn,'w'))
print 'word hash dumped'
pickle.dump(hClassHash,open(ClassIdIn,'w'))
print 'class hash dumped'

print 'finished'
        




    