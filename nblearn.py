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
    class_vocabulary = [] # list of lists, separate list of vocabulary words for each class

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
            
            # if the class vocabulary has not been initialized, create a new vocabulary list
            if len(class_vocabulary) <= class_index:
                temp_array = []
                class_vocabulary.append(temp_array)
                first_word_and_text = text.split(' ', 1)
                first_word = first_word_and_text[0]
                text = first_word_and_text[1]
                new_word = Word(first_word.lower())
                class_vocabulary[class_index].append(new_word)
                print class_vocabulary[class_index]

            for word in text.split(' '):
                word = word.lower()
                matches = filter(lambda x: match_string(word, x.text), class_vocabulary[class_index]) # store all matching words in matches
                    
                # if the word is not already in the class' vocabulary, add it
                if not matches:
                    new_word = Word(word)
                    class_vocabulary[class_index].append(new_word)
                elif word not in matches:
                    new_word = Word(word)
                    class_vocabulary[class_index].append(new_word)
                else:
                    class_vocabulary[class_index].incr()











train()
