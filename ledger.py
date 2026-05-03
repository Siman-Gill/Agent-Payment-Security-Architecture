import hashlib
import time
import json
from pqc_engine import PQCEngine

class Block:
    """
    Represents a single block in the A2A Micro-Ledger.
    """
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # List of dictionaries (A2A payments)
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        """
        Generates the SHA-256 hash of the block payload.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class PostQuantumLedger:
    """
    The core blockchain managing the autonomous agent transactions.
    """
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Generates the initial block in the chain.
        """
        genesis_block = Block(0, [], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    
    def add_transaction(self, sender_pub_key, receiver_pub_key, amount, signature):
    engine = PQCEngine()
    
    # Construct the data payload for verification
    tx_data = f"{sender_pub_key}{receiver_pub_key}{amount}"
    
    # CRITICAL: Verify the Post-Quantum Signature
    if engine.verify_signature(sender_pub_key, tx_data, signature):
        transaction = {
            "sender": sender_pub_key[:16] + "...", # Truncate for UI
            "receiver": receiver_pub_key[:16] + "...",
            "amount": amount,
            "signature_size": f"{len(signature) // 2} Bytes",
            "pqc_signature": signature # The massive payload
        }
        self.unconfirmed_transactions.append(transaction)
        return True
    return False    



    def mine_block(self):
        """
        Processes unconfirmed transactions into a new block.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          previous_hash=last_block.hash)

        # Simple Proof of Work (can be swapped for Proof of Authority later)
        proof = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.unconfirmed_transactions = []
        return new_block.index

    def proof_of_work(self, block, difficulty=2):
        """
        A basic PoW mechanism to simulate network consensus.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        block.hash = computed_hash
        return computed_hash


# --- Test Execution ---
if __name__ == "__main__":
    # 1. Initialize the startup's ledger
    network_ledger = PostQuantumLedger()

    # 2. Simulate autonomous agents submitting transactions
    print("Agent Alpha submitting transaction to Agent Beta...")
    network_ledger.add_transaction(
        sender="Agent_Alpha_PubKey", 
        receiver="Agent_Beta_PubKey", 
        amount=50, 
        signature="dummy_signature_data_for_now"
    )

    # 3. Mine the block to commit the transaction
    print("Mining new block...")
    network_ledger.mine_block()

    # 4. Output the ledger state
    print("\n--- Current Ledger State ---")
    for block in network_ledger.chain:
        print(f"Block {block.index} Hash: {block.hash}")
        print(f"Transactions: {block.transactions}\n")
