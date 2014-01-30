#! /usr/bin/env python

import sys
import re

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
        self.unique_words = 0
        self.vocabulary = dict()
        self.total_words = 0

    #def add_to_vocabulary(self, word):
    #       self.vocabulary.append(word)
    #       self.unique_words += 1

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
    
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes
    total_unique_words = 0 # number of unique words in the training set'
    total_words = 0 # number of words in the training set

    print "Beginning training..."
    with open(training_filename) as f:
        for line in f:
            class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
            classname = class_and_text[0]
            text = class_and_text[1]
            
            # search for the class in the list of possible classes
            class_index = -1
            for c in classes:
                if classname == c.name:
                    class_index = classes.index(c)
                    #class_matches = filter(lambda x: match_string(classname, x.name), classes)
            
            if class_index == -1:
                new_class = Classification(classname)
                classes.append(new_class)
                class_index = classes.index(new_class) # get the index of the class so we add the features to the correct index
            
            # increment the frequency of the class
            classes[class_index].incr_frequency()

            for word in text.split(' '):
                if (word == "") or (word == " "):
                    continue
                
                # increment the number of words in the class
                classes[class_index].incr_total_words()
                total_words += 1
                word_is_unique = True
                
                if word in classes[class_index].vocabulary:
                    classes[class_index].vocabulary[word] += 1 # increment the frequency of the existing word
                    word_is_unique = False
                else:
                    for c in classes:
                        if word in c.vocabulary:
                            word_is_unique = False
                                
                    classes[class_index].vocabulary[word] = 1 # add the new word to the dictionary and set the frequency to 1

                # increment the number of total words in the training set
                if word_is_unique:
                    total_unique_words += 1
                    print total_unique_words


    # Generate the classification model
    model_file = open(model_filename, 'w')
    model_file.write("vocabulary_size={0}\n".format(total_unique_words))
    model_file.write("number_of_classes={0}\n".format(len(classes)))

    total_documents = 0
    for class_type in classes:
        total_documents += class_type.frequency
    model_file.write("number_of_documents={0}\n".format(total_documents))


    for class_type in classes:
        model_file.write("class_name={0} class_frequency={1} class_unique_words={2} class_total_words={3}\n".format(class_type.name, class_type.frequency, class_type.unique_words, class_type.total_words))

    for class_type in classes:
        model_file.write("class_name_{0}_vocabulary\n".format(class_type.name))
        for word in class_type.vocabulary:
            model_file.write("word={0} word_frequency={1}\n".format(word, class_type.vocabulary[word]))




train()
