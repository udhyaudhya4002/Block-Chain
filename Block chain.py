import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='1', proof=100)  # Genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_license_transaction(self, software_id, license_id, owner, license_key, status, expiry_date):
        self.current_transactions.append({
            'software_id': software_id,
            'license_id': license_id,
            'owner': owner,
            'license_key': license_key,
            'status': status,
            'expiry_date': expiry_date,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Instantiate the Blockchain
blockchain = Blockchain()

# Simulate mining a new block
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

# Adding a new license transaction
blockchain.new_license_transaction(
    software_id="SW001",
    license_id="LIC123456",
    owner="user_001",
    license_key="XYZ-ABC-123",
    status="active",
    expiry_date="2025-12-31"
)

# Forge the new block
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)
# Display the blockchain
print(json.dumps(blockchain.chain, indent=4))
