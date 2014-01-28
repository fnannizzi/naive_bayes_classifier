#! /usr/bin/env python

import sys
import re

class Feature:
    def __init__(self, val):
        self.value = val
        self.frequency = 0
        self.probability = 0

def match_string(word, value):
    regex = 


def train():

    print "Beginning training..."
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)


    features = []

    with open(training_filename) as f:
        for line in f:
            for word in line.split():
                matches = filter(lambda x: match_string(word, x.value), features) # store all matching words in matches





train()
