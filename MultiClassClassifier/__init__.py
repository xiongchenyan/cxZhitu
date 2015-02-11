'''
I classify docs to multi class.
classes include:
    training:
        input: 
            label\t word word
            word->id mapping dict
        output: model + word id mapping (if updated) + class->id mapping
        by: calling svmlight's multi-class SVM
    classification:
        input: 
            word word word
            word->id mapping dict
            class->id mapping dict
        output: {class:weight} (in json format)
         
'''