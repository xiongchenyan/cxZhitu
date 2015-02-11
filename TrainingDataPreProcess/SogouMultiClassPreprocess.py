'''
Created on my MAC Feb 10, 2015-10:38:48 PM
What I do:
I preprocess sogou multiclass classification data
I read through all .txt files in given dir
    transfer the gb2312->utf-8
    segment
    output to target file
What's my input:
    sogou data dir
What's my output:
    a single file:
        class label\t [term]
@author: chenyanxiong
'''

import site
site.addsitedir('/Users/chenyanxiong/workspace/cxZhitu')
import sys
from pyltp import Segmentor
import os
from cxBasic.Conf import cxConfC
import ntpath

def WalkDir(InDir):
    lFName = []
    for dirname,dirnames,filenames in os.walk(InDir):
        for filename in filenames:
            lFName.append(dirname + "/" + filename)
    return lFName

def ProcessOneFile(fname,WordCutter):
    lLines = open(fname).read().splitlines()
    lRes = []
    lPath = fname.split('/')
    ClassName = lPath[-2]
    for line in lLines:
        try:
            line = line.decode('gb2312').encode('utf-8')
        except UnicodeDecodeError,UnicodeEncodeError:
            continue
        
        lWord = WordCutter.segment(line)
        lRes.append(ClassName + '\t' + ' '.join(lWord))
    return lRes


def Process(InDir,OutName,ModelPath):
    WordCutter = Segmentor()
    WordCutter.load(ModelPath)
    print 'word cutter loaded'
    lFName = WalkDir(InDir)
    out = open(OutName,'w')
    for fname in lFName:
        print 'processing ' + fname
        lRes = ProcessOneFile(fname, WordCutter)
        if [] != lRes:
            print >> out,'\n'.join(lRes)
    out.close()
    print 'done'


if 2 != len(sys.argv):
    print 'I preprocess sogou multiclass classification data, conf:\nsogoudir=\nout=\ncwsmodel='
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InDir = conf.GetConf('sogoudir')
OutName = conf.GetConf('out')
ModelPath = conf.GetConf('cwsmodel')

Process(InDir,OutName,ModelPath)



    