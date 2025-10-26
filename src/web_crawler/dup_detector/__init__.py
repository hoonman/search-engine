import hashlib
import time


'''
The exact duplicate link detector class.
we will be using these concepts to build this:
* checksum technique
* 

have a set for storing checksums we have already seem.
'''
class ExactDupDetector:
    def __init__(self):
        self.seen_checksum = set()

    