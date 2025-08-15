import os
import json
import re

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
        # get the raw_content line by line and parse the tokens line by line since doing it all at once is bad since it loads everything at once
        # break the line by whitespace and for each of these, filter out all the non-alphanumeric characters.
        # let's see the result after this.

        # choices:
        # lowercase, alphanumeric, what else should we keep? emails? dots? (for links), 
        # before normalizing, we should consider if we should filter the emails, links,

        with open(self.filepath, 'r') as f:
            for line in f:
                tokens = line.strip().split() # strips the first and last trailing whitespace and splits on any number of whitespace
                for i, token in enumerate(tokens):
                    tokens[i] = self.normalize_token(token)

                self.tokens.extend(tokens)

    def normalize_token(self, token):
        '''
        this function will take a single token as input and normalize it by:
        1. filter non-alphanumeric characters
        2. lowercase the characters
        3. unicode 
        '''
        token = token.casefold() 
        token = self.filter_alphanumeric(token)
        return token

    def filter_alphanumeric(self, token):
        # . / : 
        # - for dates
        # @ for emails
        return re.sub(r'[^a-z0-9\s]', ' ', token)

    # def filter_punctuations(self, token):

    def compute_word_frequencies(self):
        '''
        count the number of occurrences of each token in the tokens input list. 
        '''
        for token in self.tokens:
            if token in self.frequency_map:
                self.frequency_map[token] += 1
            else:
                self.frequency_map[token] = 1

    def print_frequencies(self):
        '''
        this method prints out the word frequency onto the command line interface. 
        print should be ordered by frequency.
        use alphabet ordering for tie breaks
        '''
        sorted_frequency_map = dict(sorted(self.frequency_map.items(), key=lambda x: x[1], reverse=True))
        for token, freq in sorted_frequency_map.items():
            print(f"{token} - {freq}")

    