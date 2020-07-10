import json
import time
from hashlib import sha256

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        """
        Constructor for the `Block` class.
        Parameters:
         - index: unique id of the block
         - transactions: list of transactions
         - timestamp: Time of generation of the block 
         - previous_hash: Hash of the previous block in chain
        """

        self.index         = index
        self.transactions  = transactions
        self.timestamp     = timestamp
        self.previous_hash = previous_hash


    def compute_hash(self):
        """
        Returns the hash of the block instance by first converting it into a json string
        """

        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    # difficulty of Proof of Work (PoW) algorithm
    difficulty = 2

    def __init__(self):
        """
        Constructor of the class Blockchain
        """
        self.unconfirmed_transactions =[] # data to get into chain
        self.chain = []
        self.create_genesis_block()
        

    def create_genesis_block(self):
        """
        Function to create first block in blockchain and append it to the chain.
        The block has index of 0, previous_hash of 0, and a valid hash.
        """
        genesis_block = Block(index=0, transactions=[], timestamp=time.time(), previous_hash="0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        """
        A method to return the most recent block in the chain. 
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Function that tries different values of the nonce to get a hash that satisfies our difficulty criteria
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'* Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_block(self, block, proof):
        """
        A function that adds the block to the chain after verification. 
        Steps in verification:
            1 - proof is valid
            2 - previous_hash referred in `block` and the hash of the latest block in the chain match
        """
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False

        if not self.is_valid_proof(block=block, block_hash=proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True


    def is_valid_proof(self, block, block_hash):
        """
        Check if block hash is valid hash of block and satisfies difficulty criteria
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Function serving as interface to adding the pending transactions to the blockchain. 
        This is accomplished by adding them to the block and figuring out proof of work
        """

        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(
            index=last_block.index + 1,
            transactions = self.unconfirmed_transactions,
            timestamp = time.time(),
            previous_hash = last_block.hash
        )
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
