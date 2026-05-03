import datetime
import json
from pqc_engine import PQCEngine

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, signature):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.signature = signature

    def to_dict(self):
        return {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "signature": self.signature
        }

class PostQuantumLedger:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.engine = PQCEngine()
        # Create genesis block
        self.create_block(previous_hash="0", signature="genesis_sig")

    def create_block(self, previous_hash, signature):
        block = Block(
            index=len(self.chain) + 1,
            transactions=self.pending_transactions,
            timestamp=str(datetime.datetime.now()),
            previous_hash=previous_hash,
            signature=signature
        )
        self.pending_transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount, agent_signature, public_key):
        # Verify the agent's PQC signature before adding to pending
        transaction_data = f"{sender}{receiver}{amount}"
        is_valid = self.engine.verify_signature(public_key, transaction_data, agent_signature)
        
        if is_valid:
            transaction = {
                "sender": sender,
                "receiver": receiver,
                "amount": amount,
                "signature": agent_signature,
                "status": "verified"
            }
            self.pending_transactions.append(transaction)
            return True
        return False

    def get_last_block(self):
        return self.chain[-1]

    def get_chain_data(self):
        return [block.to_dict() for block in self.chain]
