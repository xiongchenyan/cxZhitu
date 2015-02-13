'''
I classify docs to multi class.
classes include:
    training: (done by directly call command on svm file)
    CV on SVM file:
        input: svm data + svm light location + output dir + a list of C's
        output: acc + C in 5 fold CV
    classification:
        input: 
            a file or list of lines, each line: [word word word]
            word->id mapping dict
            class->id mapping dict
        output: {class:weight} (in json format)
         
'''