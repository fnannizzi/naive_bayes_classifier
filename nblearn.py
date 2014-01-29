#! /usr/bin/env python

import sys
import re

# class to store information used in the model
class Word:
    def __init__(self, t):
        self.text = t
        self.frequency = 1
        self.probability = 0

    def incr(self):
        self.frequency += 1

class Classification:
    def __init__(self, name):
        self.name = name
        self.frequency = 1
        self.unique_words = 0
        self.vocabulary = []
        self.total_words = 0

    def add_to_vocabulary(self, word):
        self.vocabulary.append(word)
        self.unique_words += 1

    def incr_frequency(self):
        self.frequency += 1

    def incr_total_words(self):
        self.total_words += 1


# function to match strings exactly
def match_string(word, text):
    boundary = "\\b"
    pattern = re.compile(boundary + re.escape(text) + boundary)
    if pattern.match(re.escape(word)):
        return True
    else:
        return False


def train():

    print "Beginning training..."
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes
    total_unique_words = 0 # number of unique words in the training set

    with open(training_filename) as f:
        for line in f:
            class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
            classname = class_and_text[0]
            text = class_and_text[1]
            
            # if the class is a new one, add it to the list of possible classes
            class_matches = filter(lambda x: match_string(classname, x.name), classes)
            if not class_matches:
                new_class = Classification(classname)
                classes.append(new_class)
            
            # get the index of the class so we add the features to the correct index
            class_index = classes.index(new_class)
            
            # increment the frequency of the class
            classes[class_index].incr_frequency()
            
            # if the class vocabulary has not been initialized, create a new vocabulary list
            if len(classes[class_index].vocabulary) == 0:
                first_word_and_text = text.split(' ', 1)
                first_word = first_word_and_text[0]
                text = first_word_and_text[1]
                new_word = Word(first_word.lower())
                classes[class_index].vocabulary.append(new_word)

            for word in text.split(' '):
                # increment the number of words in the class
                classes[class_index].incr_total_words()
                word = word.lower()
                word_is_unique = True
                
                for c in classes:
                    matches = filter(lambda x: match_string(word, x.text), c.vocabulary) # store all matching words in matches
                    
                    if not matches:
                        if c == classes[class_index]: # if the word is not already in the class' vocabulary, add it
                            new_word = Word(word)
                            classes[class_index].vocabulary.append(new_word)
                    elif word not in matches:
                        if c == classes[class_index]: # if the word is not already in the class' vocabulary, add it
                            new_word = Word(word)
                            classes[class_index].vocabulary.append(new_word)
                    else:
                        classes[class_index].vocabulary[classes[class_index].vocabulary.index(word)].incr() # increment the frequency of the existing word
                        word_is_unique = False

                # increment the number of total words in the training set
                if word_is_unique:
                    total_unique_words += 1












train()
