import oqs
import binascii

class PQCEngine:
    """
    Handles ML-DSA (Dilithium) operations for the A2A Ledger.
    Standard: NIST FIPS 204
    """
    def __init__(self, alg_name="Dilithium2"):
        self.alg_name = alg_name

    def generate_keypair(self):
        """Generates a Post-Quantum Public and Private Key."""
        with oqs.Signature(self.alg_name) as signer:
            public_key = signer.generate_keypair()
            private_key = signer.export_secret_key()
            return binascii.hexlify(public_key).decode(), binascii.hexlify(private_key).decode()

    def sign_transaction(self, private_key_hex, data):
        """Signs a transaction payload with a 2400+ byte signature."""
        private_key = binascii.unhexlify(private_key_hex)
        with oqs.Signature(self.alg_name) as signer:
            signer.import_secret_key(private_key)
            signature = signer.sign(data.encode())
            return binascii.hexlify(signature).decode()

    def verify_signature(self, public_key_hex, data, signature_hex):
        """Verifies the integrity of the PQC signature."""
        public_key = binascii.unhexlify(public_key_hex)
        signature = binascii.unhexlify(signature_hex)
        with oqs.Signature(self.alg_name) as verifier:
            try:
                return verifier.verify(data.encode(), signature, public_key)
            except:
                return False
