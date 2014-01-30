#! /usr/bin/env python

import sys
import re

# class to store information used in the model
class Word:
    def __init__(self, t):
        self.text = t
        self.frequency = 1

    def incr(self):
        self.frequency += 1

class Classification:
    def __init__(self, name):
        self.name = name
        self.frequency = 0
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
            #print "Line:{0}\n".format(line)
            class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
            classname = class_and_text[0]
            text = class_and_text[1]
            print "Classname:{0}\n".format(classname)
            #print "Text:{0}\n".format(text)
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
                if (word == "") or (word == " "):
                    continue
                
                # increment the number of words in the class
                classes[class_index].incr_total_words()
                total_words += 1
                word = word.lower()
                word_is_unique = True
                
                word_index = -1
                for c in classes:
                    for w in c.vocabulary:
                        if(w.text == word):
                            word_index = c.vocabulary.index(w)
                            break
                
                    #matches = filter(lambda x: match_string(word, x.text), c.vocabulary) # store all matching words in matches
                    '''print "Matches for word={0}:".format(word)
                    for w in matches:
                        print "{0},".format(w)
                    print "\n"'''
                    
                    if word == "airlines":
                        print "HEY\n"
                    
                    if word_index == -1:
                        if c == classes[class_index]: # if the word is not already in the class' vocabulary, add it
                            new_word = Word(word)
                            classes[class_index].vocabulary.append(new_word)
                            #print "Added word={0}\n".format(word)
                            if word == "airlines":
                                print "ADDED\n"
                    else:
                        if c == classes[class_index]:
                            classes[class_index].vocabulary[word_index].incr() # increment the frequency of the existing word
                        
                        word_is_unique = False
                        if word == "airlines":
                            print "NOT ADDED\n"
                            print classes[class_index].vocabulary[word_index].frequency
                        #print "Word already exists={0}\n".format(word)

                # increment the number of total words in the training set
                if word_is_unique:
                    total_unique_words += 1
                    #print total_unique_words


    # Generate the classification model
    model_file = open(model_filename, 'w')
    model_file.write("vocabulary_size={0}\n".format(total_unique_words))
    model_file.write("number_of_classes={0}\n".format(len(classes)))

    total_documents = 0
    for class_type in classes:
        total_documents += class_type.frequency
    
    for class_type in classes:
        p_class = (class_type.frequency/total_documents)
        p_not_class = ((total_documents-class_type.frequency)/total_documents)
        model_file.write("class_name={0} p_class={1} p_not_class={2}\n".format(class_type.name, p_class, p_not_class))

    for class_type in classes:
        model_file.write("class_name_{0}_vocabulary\n".format(class_type.name))
        for word in class_type.vocabulary:
            p_word_given_class = (word.frequency + 1)/class_type.total_words
            p_word_given_not_class = 0
            for class_type2 in classes:
                if class_type2 == class_type:
                    continue
            
                p_word_given_not_class += class_type2.vocabulary[class_type2.vocabulary.index(word)].frequency

            p_word_given_not_class = (p_word_given_not_class + 1)/total_words
            model_file.write("word={0} p_word_given_class={1} p_word_given_not_class={2}\n".format(word.text, p_word_given_class, p_word_given_not_class))






train()
