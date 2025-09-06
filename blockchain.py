import hashlib
import json
import time


class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.data = data  # dictionary
        self.timestamp = timestamp or time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(
            {
                "index": self.index,
                "previous_hash": self.previous_hash,
                "data": self.data,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        )
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", {"message": "Genesis Block"})

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            data=data,
        )
        self.chain.append(new_block)
        return new_block
