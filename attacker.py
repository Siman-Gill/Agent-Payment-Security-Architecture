import requests
import time
import hashlib

API_URL = "http://127.0.0.1:8000"

def launch_attack():
    print("⚠️ INITIALIZING QUANTUM-VULNERABLE INJECTION ATTACK...")
    
    # Simulate a legacy "weak" signature (ECDSA-style placeholder)
    weak_signature = hashlib.sha256(b"vulnerable_data").hexdigest()
    
    payload = {
        "sender": "MALICIOUS_ACTOR_01",
        "receiver": "Agent_Alpha",
        "amount": 9999.0,
        "signature": weak_signature # This will fail PQC verification
    }

    try:
        response = requests.post(f"{API_URL}/transactions/new", json=payload)
        if response.status_code == 400:
            print("🛡️ ATTACK DEFLECTED: Node rejected non-PQC transaction.")
        else:
            print("❌ SECURITY BREACH: Vulnerable transaction accepted.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        launch_attack()
        time.sleep(10)
