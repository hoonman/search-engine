import os
import json

class Tokenizer:
    def __init__(self, filepath):
        self.tokens = []
        self.frequency_map = {}
        self.filepath = filepath

    def tokenize(self):
        '''
        this function takes filepath as input. reads this text file in the filepath and returns a list of tokens in the file.
        a token is a sequence of alphanumeric characters independent of capitalization. ex) Apple vs. apple
        we cannot use NLTK 
        '''

        # steps: 
        # lets use with open(filepath, 'r') to read the HTML / PDF file
        # lets focus on text files first. and come up with cases along the way
        #`get the raw_content line by line and parse the tokens line by line since doing it all at once is bad since it loads everything at once
        # break the line by whitespace and for each of these, filter out all the non-alphanumeric characters.
        # let's see the result after this.

        with open(self.filepath, 'r') as f:
            for line in f:
                print("line: ", line)
                tokens = line.split(' ')
                print("tokens: ", tokens)
        pass

    def compute_word_frequencies(self, tokens):
        '''
        count the number of occurrences of each token in the tokens input list. 
        '''
        pass

    def print(self, frequency_map):
        '''
        this method prints out the word frequency onto the command line interface. 
        print should be ordered by frequency.
        use alphabet ordering for tie breaks
        '''
        for token, freq in frequency_map.items():
            print(f"{token} - {freq}")
            print("\n")

    