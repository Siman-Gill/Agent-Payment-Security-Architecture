from pqc_engine import PQCEngine
import requests
import time

engine = PQCEngine()
API_URL = "http://127.0.0.1:8000"

# Generate PQC Identities for Agents
AGENT_KEYS = {name: engine.generate_keypair() for name in ["Alpha", "Beta", "Gamma"]}

def run_pqc_traffic():
    while True:
        sender_name = "Alpha"
        receiver_name = "Beta"
        pub_key, priv_key = AGENT_KEYS[sender_name]
        dest_pub, _ = AGENT_KEYS[receiver_name]
        
        amount = 125.50
        tx_data = f"{pub_key}{dest_pub}{amount}"
        
        # Create the massive PQC signature
        signature = engine.sign_transaction(priv_key, tx_data)
        
        payload = {
            "sender": pub_key,
            "receiver": dest_pub,
            "amount": amount,
            "signature": signature
        }
        
        requests.post(f"{API_URL}/transactions/new", json=payload)
        requests.get(f"{API_URL}/mine")
        time.sleep(5)
