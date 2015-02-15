'''
Created on my MAC Feb 15, 2015-5:24:04 PM
What I do:
I am the unitest script for ext svm multi class classification
What's my input:
a text data, each line is segmented texts. utf-8 format
What's my output:
the class:weight vector for corresponding lines
@author: chenyanxiong
'''


import site
import math
site.addsitedir('/Users/chenyanxiong/workspace/cxZhitu')
from cxBasic.Conf import cxConfC
from MultiClassClassifier.ExtSVMMultiClassifier import ExtSVMMultiClassifierC

import sys

if 2 != len(sys.argv):
    print 'I classify a given segged text.'
    ExtSVMMultiClassifierC.ShowConf()
    print 'in=raw data (segmented)\nout=(best_class_id weight_in_each_class)\n'
    sys.exit()
    
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')

Classifier = ExtSVMMultiClassifierC(sys.argv[1])
Classifier.ClassifyData(InName, OutName, ReadRes=False)
print 'finished'
