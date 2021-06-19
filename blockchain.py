#!/usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import sha256

# Function that encrypts arguments using sha256 encryption
def updateHash(*args):
    hashingText = ""; h = sha256()
    for arg in args:
        hashingText += str(arg)

    h.update(hashingText.encode('utf-8'))
    return h.hexdigest()

# Defines what a block object looks like
class Block():

    def __init__(self, number=0, previous_hash="0"*64, data=None, nonce=0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        return updateHash(self.previous_hash, self.number, self.data, self.nonce)

    def __str__(self):
        return str("Block #: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(self.number, self.hash(), self.previous_hash, self.data, self.nonce))

class Blockchain():
    difficulty = 2

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def remoe(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try:
            block.previous_hash = self.chain[-1].hash() # get the hash of the last block
        except IndexError:
            pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1

    # checks if hashes have 4 zeroes like we defined, and if the previous hash is equal to the actual previous hash
    # (makes sure no blocks are corrupted or changed)
    def isValid(self):
        for i in range(1, len(self.chain)):
            _previous = self.chain[i].previous_hash # get previous hash value
            _current = self.chain[i-1].hash() # re-hash previous data
            
            if _previous != _current: # check if those two are the same, if not block is corrupt
                return False

            if _current[:self.difficulty] != "0"*self.difficulty: # checks if the number of 0s is the same as the difficulty defined
                return False

        return True # otherwise, everything is A-okay!

def main():
    blockchain = Blockchain()
    database = ['hello', "what's up", 'hello' 'bye']

    num = 0
    for data in database:
        num += 1
        blockchain.mine(Block(num, data=data))

    for block in blockchain.chain:
        print(block)

    # ~ CORRUPTION TESTING ~   
    # blockchain.chain[0].data = "NOT THE RIGHT HASH" # if data is changed
    # blockchain.mine(blockchain.chain[2]) # if data is then remined to find a value that satisfied, still shows invalid because it does not fit in the chain

    print(blockchain.isValid())

if __name__ == '__main__':
    main()