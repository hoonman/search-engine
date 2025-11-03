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

    def compute_checksum(self, content, mode='sha256'):
        if isinstance(content, str):
            content = content.encode('utf-8')
        if mode == 'sha256':
            return hashlib.sha256(content).hexdigest()
        elif mode == 'blake2b':
            return hashlib.blake2b(content).hexdigest()
    

    def is_exact_duplicate(self, content):
        curr_checksum = self.compute_checksum(content, 'blake2b')
        if curr_checksum in self.seen_checksum:
            return True
        self.seen_checksum.add(curr_checksum)
        return False


class SimDupDector:
    def __init__(self):
        pass