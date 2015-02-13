'''
Created on Feb 12, 2014 22:01:09 PM
@author: cx


This is the main class used to classify textual document/ad text

what I do:
I call external SVM (SVMLight) multi class classifier
and pretrained models to classify text
what's my input:
    SVM classifier path
    SVM pre trained model path
    SVM term hash dict (pickle dump of term->id)
    term df dict (pickle dump of term->Df)
    text to classify
    middirectory to dump data
what's my output:
    lhClass, the Score of each text belong to classes, [{class id: weight}], one item for each input line
'''

import site
import math
site.addsitedir('/Users/chenyanxiong/workspace/cxZhitu')

from cxBasic.Conf import cxConfC
import pickle,json
import random
import subprocess
import os
import shutil
class ExtSVMMultiClassifierC(object):
    def __init__(self,ConfIn = ""):
        self.Init()
        if "" != ConfIn:
            self.SetConf(ConfIn)
    
    def Init(self):
        self.SVMClassPath = "/Users/chenyanxiong/Dropbox/zhitu/DocumentClassification/SVMLIGHT/svm_multiclass_classify"
        self.SVMModel = '/Users/chenyanxiong/Dropbox/zhitu/DocumentClassification/SVMLIGHT/SogouModel'
        self.TempDir = '/Users/chenyanxiong/Dropbox/zhitu/DocumentClassification/SogouWorkdir/temp/'
        self.TermHashName = "/Users/chenyanxiong/Dropbox/zhitu/DocumentClassification/SogouWorkdir/SogouWordIdDict"
        self.hTermDF = {}
        self.TermDFName = '/Users/chenyanxiong/Dropbox/zhitu/DocumentClassification/SogouWorkdir/SogouDF'
        self.hTermId = {}
        self.ThisTempName = ""   #the temp name for each file
        
    def SetConf(self, ConfIn):
        self.conf = cxConfC()
        self.SVMClassPath = self.conf.GetConf('svmpath', self.SVMClassPath)
        self.SVMModel = self.conf.GetConf('svmmodel', self.SVMModel)
        self.TempDir = self.conf.GetConf('tempdir', self.TempDir) + '/'
        
        if not os.path.exists(self.TempDir):
            print "creating dir [%s]" %(self.TempDir)
            os.makedirs(self.TempDir)
        self.TermHashName = self.conf.GetConf('termhashin',self.TermHashName)
        self.hTermId = pickle.load(open(self.TermHashName))
        self.TermDFName = self.conf.GetConf('termdfin', self.TermDFName)
        
    @staticmethod
    def ShowConf():
        print "conf:\nsvmpath=(svm_multiclass_classify location)\nsvmmodel=(pre trained svm model)\ntempdir=(an temporary dir to work in)\ntermhashin=\n(the hash id dict of term)termdfin=\n(the term df (term id -> df))"
        
        
    def TransferTextToSVMFormat(self,text):
        lTerm = text.split()
        hFeature = {}
        DocCnt = self.hTermDF['DocCnt']
        for term in lTerm:
            if not term in self.hTermId:
                continue
            key = self.hTermId[term]
            DF = self.hTermDF[term]
            Idf = math.log(DocCnt / DF)
            if not key in hFeature:
                hFeature[key] = Idf
            else:
                hFeature[key] += Idf
        
        lFItem = hFeature.items()
        
        lFItem.sort(key=lambda item:item[0])
        lF = ['%d:%f' %(item[0],item[1]) for item in lFItem]
        res = '1 ' + ' '.join(lF)
        return res
    
    def GenerateTempName(self):
        name = "tmp_%d" %(random.randint(0,100000))
        while os.path.exists(name):
            name = "tmp_%d" %(random.randint(0,100000))
        self.ThisTempName = self.TempDir + '/' + name
        return self.ThisTempName
    
    def MakeSVMData(self,Data):
        out = open(self.ThisTempName,'w')
        if type(Data) == list:
            for text in Data:
                print >>out,self.TransferTextToSVMFormat(text)
        if type(Data) == str:
            for text in open(Data):
                text = text.strip()
                print >>out,self.TransferTextToSVMFormat(text)
        out.close()
        
        
    def Predict(self):
        self.PredictOut=self.ThisTempName + '_pred'
        lCmd = [self.SVMClassPath,self.ThisTempName,self.SVMModel,self.PredictOut]
        print 'svm running: %s' %(json.dumps(lCmd))
        subprocess.check_output(lCmd)
        print "reading predicted output from [%s]" %(self.PredictOut)
        lLines = open(self.PredictOut).readlines()
        lLines = [line.strip() for line in lLines if line.strip() != ""]
        lClass = [line.split()[0] for line in lLines]
        llProb = [[float(weight) for weight in line.split()[1:]] for line in lLines]
        del lLines[:]
        return lClass,llProb
    
    def Clean(self):
        shutil.rmtree(self.ThisTempName)
        shutil.rmtree(self.PredictOut)
        
        
    def ClassifyData(self,Data):
        '''
        Data can be a list, [segmented text]
        or a InName, each line is segmented text
        return lhClass
            one hClass for each line: {class id:float weight}
        '''
        #use utf-8 encoding
        self.GenerateTempName()
        self.MakeSVMData(Data)
        lClass,llProb = self.Predict()
#         self.Clean()
        lhClass = []
        for i in range(len(lClass)):
            lhClass.append(dict(zip(lClass,llProb[i])))
        return lhClass
    
        
         
        
    

