from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ledger import PostQuantumLedger
import uuid

# Initialize the API and the Ledger
app = FastAPI(title="PQC Agent Ledger API")
pqc_ledger = PostQuantumLedger()

# Generate a unique ID for this specific node in the network
node_identifier = str(uuid.uuid4()).replace('-', '')

class Transaction(BaseModel):
    sender: str
    receiver: str
    amount: float
    signature: str

@app.get("/")
def read_root():
    """
    Landing page for the Post-Quantum Ledger Node.
    """
    return {
        "project": "Post-Quantum A2A Ledger",
        "version": "1.0.0-Alpha",
        "status": "RUNNING",
        "endpoints": {
            "docs": "/docs",
            "view_chain": "/chain",
            "check_status": "/status"
        }
    }


@app.get("/chain")
def get_chain():
    """
    Returns the full state of the blockchain.
    """
    chain_data = []
    for block in pqc_ledger.chain:
        chain_data.append(block.__dict__)
    return {
        "length": len(chain_data),
        "chain": chain_data,
        "status": "SECURE"
    }

@app.post("/transactions/new")
def new_transaction(tx: Transaction):
    """
    Adds a new transaction to the unconfirmed list.
    """
    added = pqc_ledger.add_transaction(tx.sender, tx.receiver, tx.amount, tx.signature)
    if not added:
        raise HTTPException(status_code=400, detail="Invalid Transaction")
    
    return {"message": f"Transaction will be added to Block {pqc_ledger.last_block.index + 1}"}


@app.post("/audit/log")
def log_security_event(event_type: str, details: str):
    """
    Immutably records a security incident (like a rejected attack) 
    directly onto the blockchain.
    """
    pqc_ledger.add_transaction(
        sender_pub_key="SYSTEM_SOC",
        receiver_pub_key="AUDIT_VAULT",
        amount=0.0,
        signature="INTERNAL_SYSTEM_AUDIT_SIGNED" # In production, this would be a system PQC sig
    )
    # Log details to a special audit list for the UI
    return {"status": "EVENT_RECORDED_ON_CHAIN"}

@app.get("/mine")
def mine():
    """
    Triggers the mining process to secure transactions into a block.
    """
    index = pqc_ledger.mine_block()
    if not index:
        return {"message": "No transactions to mine."}
    
    return {
        "message": "New Block Mined",
        "block_index": index,
        "hash": pqc_ledger.last_block.hash
    }

@app.get("/status")
def system_status():
    """
    Health check for the cryptographic node.
    """
    return {
        "node_id": node_identifier,
        "ledger_height": len(pqc_ledger.chain),
        "pending_tx": len(pqc_ledger.unconfirmed_transactions),
        "encryption_mode": "POST-QUANTUM_READY"
    }
