'''
Created on my MAC Feb 12, 2015-10:36:01 PM
What I do:
I CV svm
What's my input:
    SVMData, CV Range, work dir
What's my output:
    Accuracy for each C
@author: chenyanxiong
'''

import site
site.addsitedir('/Users/chenyanxiong/workspace/cxZhitu')

from cxBasic.Conf import cxConfC
from cxBasic.CVPartition import CVPartition
import subprocess
import json
import sys

class CrossValidateSVMC(object):
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
            
            
    def Init(self):
        self.DataIn = ""
        self.workdir = ""
        self.lC = []
        self.lCAcc = []
        self.SVMDir = "" #contain svm_multiclass_learn svm_multiclass_classify
        self.SVMTrain = ""
        self.SVMTest = ""
        
    def SetConf(self,ConfIn):
        self.conf = cxConfC(ConfIn)
        self.DataIn = self.conf.GetConf('in')
        self.workdir = self.conf.GetConf('workdir') + '/'
        self.SVMDir = self.conf.GetConf('svmdir') + '/'
        self.SVMTrain = self.SVMDir + '/svm_multiclass_learn'
        self.SVMTest = self.SVMDir + '/svm_multiclass_classify'
        self.lC = self.conf.GetConf('c',[1,10,100,1000,10000,100000])
        self.lC = [float(c) for c in self.lC]
        self.lCAcc = [0] * len(self.lC)
        
    @staticmethod
    def ShowConf():
        print "conf\nin=\nworkdir=\nsvmdir=\nc=1\t10\t100\t1000\t10000\t50000\t100000"
    
        
    def PrepareData(self):
        CVPartition(self.DataIn, self.workdir, 5)
        
    
    def SegTestAccFromSVMOut(self,OutStr):
        lLine = OutStr.split('\n')
        line = lLine[-1]
        vCol = line.split()
        Acc = vCol[4].strip("%")
        Acc = 1 - float(Acc) / 100.0
        print 'Acc [%f]' %(Acc)
        return Acc
        
    def ProcessOneFold(self,k):
        TrainName = self.workdir + '_train_%d' %(k)
        TestName = self.workdir + '_test_%d' %(k)
        for i in range(len(self.lC)):
            ModelName = TrainName + '_model_%f' %(self.lC[i])
            PreName = ModelName + '_pre'
            lTrainCmd = [self.SVMTrain, '-c','%f' %(self.lC[i]),TrainName,ModelName]
            print 'svm run ' + json.dumps(lTrainCmd)
            subprocess.check_output(lTrainCmd)
            lTestCmd = [self.SVMTest,TestName,ModelName,PreName]
            print 'svm test ' + json.dumps(lTestCmd)
            OutStr = subprocess.check_output(lTestCmd).strip()
            print OutStr
            self.lCAcc[i] += self.SegTestAccFromSVMOut(OutStr) / 5
        print '[%d fold done' %(k)
        return
        
    def Process(self):
        print 'start preparing data'
        self.PrepareData()
        print 'start CV'
        for k in range(5):
            self.ProcessOneFold(k)
        out = open(self.workdir + 'CVAcc','w')
        for c,Acc in zip(self.lC,self.lCAcc):
            print >>out, '%f\t%f' %(c,Acc)
        out.close()
        print 'finished'
        

if 2 != len(sys.argv):
    CrossValidateSVMC.ShowConf()
    sys.exit()
    
    
    
CVer = CrossValidateSVMC(sys.argv[1])
CVer.Process()