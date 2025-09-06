from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
import hashlib

app = FastAPI(title="Blockchain Fruit Tracking")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Blockchain Classes
# -------------------

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode())
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, str(datetime.now()), {"info": "Genesis Block"}, "0")
        self.chain.append(genesis_block)

    def add_block(self, data):
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = str(datetime.now())
        previous_hash = previous_block.hash
        new_block = Block(index, timestamp, data, previous_hash)
        self.chain.append(new_block)
        return new_block

    def get_chain(self):
        return self.chain

    def get_fruit_history(self, fruit_id):
        history = []
        for block in self.chain:
            if isinstance(block.data, dict) and block.data.get("fruit_id") == fruit_id:
                history.append({
                    "index": block.index,
                    "timestamp": block.timestamp,
                    "data": block.data,
                    "hash": block.hash,
                    "previous_hash": block.previous_hash
                })
        return history

# Initialize blockchain
blockchain = Blockchain()

# -------------------
# FastAPI Models
# -------------------

class Fruit(BaseModel):
    fruit_id: str
    name: str
    location: str
    status: str

# -------------------
# FastAPI Endpoints
# -------------------

@app.post("/add_fruit/")
async def add_fruit(fruit: Fruit):
    new_block = blockchain.add_block(fruit.dict())
    return {"message": f"Fruit added to blockchain at block {new_block.index}"}

@app.get("/get_fruit_history/{fruit_id}")
async def get_fruit_history(fruit_id: str):
    history = blockchain.get_fruit_history(fruit_id)
    return {"history": history}

@app.get("/get_chain/")
async def get_chain():
    chain_data = []
    for block in blockchain.get_chain():
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash
        })
    return {"length": len(chain_data), "chain": chain_data}
