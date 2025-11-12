
# Ticket Granting Server (TGS) for Kerberos Simulation

from crypto_utils import (
    decrypt_object,
    encrypt_object,
    generate_session_key,
    current_timestamp,
    is_fresh
)

import json

# Sample Data

# Shared keys only known to the servers

TGS_MASTER_KEY = b"TGS_MASTER_SECRET_123"
SERVICE_MASTER_KEYS = {
    "fileserver": b"FILE_SERVER_SECRET_456",
    "mailserver": b"MAIL_SERVER_SECRET_789"
}



# Validate Ticket Granting Ticket (TGT)

def validate_tgt(tgt_hex: str):
    "Decrypt and validate the TGT using TGS master key"
    try:
        tgt = decrypt_object(tgt_hex, TGS_MASTER_KEY)
    except Exception as e:
        print("[TGS] Invalid TGT decryption:", e)
        return None

    if current_timestamp() > tgt["expiry"]:
        print("[TGS] TGT expired.")
        return None

    return tgt



# Validate Authenticator

def validate_authenticator(auth_hex: str, session_key: str, username: str):
    "Decrypt and verify the Authenticator (timestamp freshness, matching username)"
    try:
        auth = decrypt_object(auth_hex, bytes.fromhex(session_key))
    except Exception as e:
        print("[TGS] Invalid authenticator decryption:", e)
        return None

    if auth["user"] != username:
        print("[TGS] Username mismatch in Authenticator.")
        return None

    if not is_fresh(auth["timestamp"]):
        print("[TGS] Authenticator expired ")
        return None

    return auth



# Create Service Ticket

def create_service_ticket(username: str, service: str, session_key_c_s: str, validity: int = 300):
    "Create a service ticket encrypted with the service's master key"
    ticket_data = {
        "user": username,
        "session_key": session_key_c_s,
        "timestamp": current_timestamp(),
        "expiry": current_timestamp() + validity
    }

    key = SERVICE_MASTER_KEYS.get(service)
    if not key:
        print(f"[TGS] Service request denied: {service}")
        return None

    encrypted_ticket = encrypt_object(ticket_data, key)
    return encrypted_ticket



# TGS Main Function

def kerberos_tgs_request(tgt_hex: str, auth_hex: str, service: str):
    "Simulate a TGS exchange: validates TGT along with Authenticator and issues a Service Ticket"
    print(f"\n[TGS] Received request for service: {service}")

    # Validate TGT
    tgt = validate_tgt(tgt_hex)
    if not tgt:
        print("[TGS] Invalid or expired TGT.")
        return None

    # Validate Authenticator
    auth = validate_authenticator(auth_hex, tgt["session_key"], tgt["user"])
    if not auth:
        print("[TGS] Authenticator validation failed.")
        return None

    # Generate Client-Service Session Key
    session_key_c_s = generate_session_key()
    print(f"[TGS] Generated Client–Service Session Key: {session_key_c_s}")

    # Create Service Ticket (encrypted with Service Key)
    service_ticket = create_service_ticket(tgt["user"], service, session_key_c_s)
    if not service_ticket:
        return None
    print("[TGS] Created Service Ticket for", service)

    # Create response (Service Ticket along with encrypted session key for client)
    response_to_client = {
        "service_ticket": service_ticket,
        "enc_session_key": encrypt_object({"session_key": session_key_c_s}, bytes.fromhex(tgt["session_key"]))
    }

    print("[TGS] Sending Service Ticket and encrypted session key to client\n")
    return response_to_client



# Testing 

if __name__ == "__main__":
    

    # Sample input to test
    tgt_sample = input("Enter sample TGT (hex): ").strip()
    auth_sample = input("Enter sample Authenticator (hex): ").strip()
    service_name = input("Enter requested service (fileserver/mailserver): ").strip()

    response = kerberos_tgs_request(tgt_sample, auth_sample, service_name)
    if response:
        print(json.dumps(response, indent=4))
