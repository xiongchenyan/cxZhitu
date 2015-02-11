'''
Created on my MAC Feb 10, 2015-11:14:53 PM
What I do:
I count the df of word in segmented data
each line here is a doc (the raw training date from sogou)
What's my input:
raw train data from sogou
What's my output:
word:df 's pickle dump
@author: chenyanxiong
'''
import sys
import pickle

if 3 != len(sys.argv):
    print 'in + df dump out'
    sys.exit()
    
h = {}
cnt = 0
DocCnt = 0
for line in open(sys.argv[1]):
    DocCnt += 1
    lW = line.strip().split('\t')[-1].split()
    cnt += len(lW)
    for w in lW:
        if not w in h:
            h[w] = 1
        else:
            h[w] += 1
print 'total [%d] word with [%d] appearance' %(len(h),cnt) 
h['DocCnt'] = DocCnt           
out = open(sys.argv[2],'w')
pickle.dump(h,out)
out.close()
print 'dumped'