#! /usr/bin/env python

import sys

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
        self.vocabulary = dict()
        self.total_words = 0
    
    def incr_frequency(self):
        self.frequency += 1
    
    def incr_total_words(self):
        self.total_words += 1

def classify():
    
    if len(sys.argv) > 2:
        model_filename = sys.argv[1]
        test_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a model filename and a test filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes

    print "Loading model..."
    with open(model_filename) as f:
        # read the vocabulary size
        line = f.readline()
        tokens = line.split(' ')
        vocabulary_size = tokens[0]
        
        # read the total number of words
        line = f.readline()
        tokens = line.split(' ')
        total_words = tokens[0]
        
        # read the number of classes
        line = f.readline()
        tokens = line.split(' ')
        num_classes = int(tokens[0])
        
        # read the number of documents
        line = f.readline()
        tokens = line.split(' ')
        num_documents = tokens[0]
        
        for x in range(0, num_classes):
            # read the class names and store the class info
            line = f.readline()
            tokens = line.split(' ')
            new_class = Classification(tokens[0])
            new_class.frequency = int(tokens[1])
            new_class.total_words = int(tokens[2])
            classes.append(new_class)
        
        for class_type in classes:
            for word_in_model in range(0, class_type.total_words):
                line = f.readline()
                tokens = line.split(' ')
                class_type.vocabulary[tokens[0]] = tokens[1]



classify()