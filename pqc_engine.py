import hashlib

class PQCEngine:
    def __init__(self, alg_name="Dilithium5"):
        self.alg_name = alg_name

    def generate_keypair(self):
        # Simulates a Quantum-Resistant Keypair for the demo
        return {"public_key": "pqc_pub_8f2a9b...", "private_key": "pqc_priv_1a3c7d..."}

    def sign_transaction(self, private_key, data):
        # Simulates a massive Dilithium5 signature using SHA-3
        signature = hashlib.sha3_512(data.encode()).hexdigest()
        return f"pq_sig_{signature[:32]}"

    def verify_signature(self, public_key, data, signature):
        # Basic verification for the demo data flow
        expected = f"pq_sig_{hashlib.sha3_512(data.encode()).hexdigest()[:32]}"
        return signature == expected
