#! /usr/bin/env python

from __future__ import division
import sys
from math import log

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
        self.vocabulary = dict()
        self.vocabulary_size = 0
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

    #print "Loading model..."
    with open(model_filename) as f:
        # read the vocabulary size
        line = f.readline()
        tokens = line.split(' ')
        vocabulary_size = int(tokens[0])
        
        # read the total number of words
        line = f.readline()
        tokens = line.split(' ')
        total_words = int(tokens[0])
        
        # read the number of classes
        line = f.readline()
        tokens = line.split(' ')
        num_classes = int(tokens[0])
        
        # read the number of documents
        line = f.readline()
        tokens = line.split(' ')
        num_documents = int(tokens[0])
        
        for x in range(0, num_classes):
            # read the class names and store the class info
            line = f.readline()
            tokens = line.split(' ')
            new_class = Classification(tokens[0])
            new_class.frequency = int(tokens[1])
            new_class.total_words = int(tokens[2])
            new_class.vocabulary_size = int(tokens[3])
            classes.append(new_class)
            #print tokens[0]
            #print tokens[2]
        
        for class_type in classes:
            for word_in_model in range(0, class_type.vocabulary_size):
                line = f.readline()
                tokens = line.split(' ')
                class_type.vocabulary[tokens[0]] = int(tokens[1])


    #print "Model loaded. Classifying..."

    with open(test_filename) as f:
        for line in f:
            p_classes = []
            for class_type in classes:
                p_word_given_class = 0
                p_word_given_not_class = 0
                #print num_documents
                p_class = class_type.frequency/num_documents
                p_not_class = (num_documents - class_type.frequency)/num_documents
                #print "{0} p_class = {1}".format(class_type.name, p_class)
                for word in line.split(' '):
                    num_appearances = 0
                    num_words = 0
                    if word in class_type.vocabulary:
                        p_word_given_class += log((class_type.vocabulary[word] + 1)/(class_type.total_words + vocabulary_size))
                    else:
                        p_word_given_class += log(1/(class_type.total_words + vocabulary_size))
                    
                    #print "     {0} p_wgc = {1}".format(word, p_word_given_class)

                    for class_type2 in classes:
                        if class_type2 == class_type:
                            continue
                    
                        if word in class_type2.vocabulary:
                            num_appearances += class_type2.vocabulary[word]
                        
                        num_words += class_type2.total_words
            
                    p_word_given_not_class += log((num_appearances + 1)/(num_words + vocabulary_size))

                # calculate probability for this class
                #print "p_wgc = {0} p_wgnc = {1}".format(p_word_given_class, p_word_given_not_class)
                p_class_given_document = 1 - ((0.5 * p_word_given_class)/((0.5 * p_word_given_class) + (0.5 * p_word_given_not_class)))
                #p_class_given_document = (p_class * p_word_given_class)/((p_class * p_word_given_class) + (p_not_class * p_word_given_not_class))
                p_classes.append(p_class_given_document)
                #print p_class_given_document

            classified = 0
            #print "Scoring!"
            #print line

            #print "Size p_classes = {0}".format(len(p_classes))
            for score in p_classes:
                #print classes[p_classes.index(score)].name
                #print score
                if score > p_classes[classified]:
                    classified = p_classes.index(score)
                    #print "Updated score!"
                    #print classes[p_classes.index(score)].name

            print "Classified as {0}".format(classes[classified].name)


classify()