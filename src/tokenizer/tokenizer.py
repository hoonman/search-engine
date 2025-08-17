import os
import json
import re
import unicodedata
from ..config.config import tokenizer_config

class Tokenizer:
    def __init__(self, filepath):
        self.tokens = []
        self.frequency_map = {}
        self.filepath = filepath
        self.config = tokenizer_config

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

        with open(self.filepath, 'r', encoding='utf-8', buffering=8192) as f:
            for line in f:
                tokens = line.strip().split()
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
        token = self.unicode_normalize(token)
        return token

    def unicode_normalize(self, token):
        '''
        this function will take a token and perform a unicode normalization so that certain text that we parsed will be treated in normalized way instead of messy unnormalized cases.
        we can specify if we need to strip the accents or not.
        we will, by default, modify fullwidth/halfwidth chars into their respective default abstract character
        '''
        if self.config['strip_accent']:
            nfkd = unicodedata.normalize('NFKD', token)
            token = ''.join(char for char in nfkd if not unicodedata.combining(char))
        # NFC does not handle the fullwidth/halfwidth and ligatures
        # NFKC does! it will normalize ｃａｆｅ -> cafe but keeps accent.
        return unicodedata.normalize('NFKC', token)

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

    def get_frequency_map(self):
        return self.frequency_map

    