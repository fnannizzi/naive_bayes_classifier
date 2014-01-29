#! /usr/bin/env python

import sys
import re

class Feature:
    def __init__(self, val):
        self.value = val
        self.frequency = 0
        self.probability = 0

def match_string(word, value):
    boundary = "\\b"
    pattern = re.compile(boundary + value + boundary)
    if pattern.match(word):
        return true
    else:
        return false

def train():

    print "Beginning training..."
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes
    class_features = [] # list of lists, separate list of features for each class

    with open(training_filename) as f:
        for line in f:
            class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
            classname = class_and_text[0]
            text = class_and_text[1]
            
            # if the class is a new one, add it to the list of possible classes
            if classname not in classes:
                classes.append(classname)
            
            # get the index of the class so we add the features to the correct index
            class_index = classes.index(classname)
            
            for word in text.split(' '):
                matches = filter(lambda x: match_string(word, x.value), class_features) # store all matching words in matches
                print matchesgit










train()
