
# Authentication Server (AS) for Kerberos simulation

from crypto_utils import (
    derive_key_from_password,
    encrypt_object,
    generate_session_key,
    current_timestamp
)

import json

# Sample Data (shared only with the TGS)

TGS_MASTER_KEY = b"TGS_MASTER_SECRET_123"  

# User database (for demo)

USER_DB = {
    "alice": "Passw0rdA1",
    "bob": "PassC0deB1"
}



# Authentication Logic

def authenticate_user(username: str, password: str):
    "Check if the username and password are valid"
    if username in USER_DB and USER_DB[username] == password:
        return True
    return False



# TGT Creation

def create_tgt(username: str, session_key: str, validity: int = 300):
    "Create a Ticket Granting Ticket (TGT)"
    tgt_data = {
        "user": username,
        "session_key": session_key,
        "timestamp": current_timestamp(),
        "expiry": current_timestamp() + validity
    }
    # Encrypt TGT using TGS master key (bytes)
    encrypted_tgt = encrypt_object(tgt_data, TGS_MASTER_KEY)
    return encrypted_tgt



# Authentication Server Main Function

def kerberos_as_request(username: str, password: str):
    "Simulate a Kerberos AS exchange"
    print(f"\n[AS] Received authentication request for the user: {username}")

    # Validation of user
    if not authenticate_user(username, password):
        print("[AS] Authentication failed ")
        return None

    # Generate session key for client TGS
    session_key_c_tgs = generate_session_key()
    print(f"[AS] Generated session key (Client–TGS): {session_key_c_tgs}")

    # Create Ticket Granting Ticket (TGT)
    tgt = create_tgt(username, session_key_c_tgs)
    print("[AS] Created encrypted Ticket Granting Ticket (TGT)")

    # Encrypt session key using client password-derived key
    client_key = derive_key_from_password(password)
    enc_session_key = encrypt_object({"session_key": session_key_c_tgs}, client_key)

    # Create response
    response = {
        "tgt": tgt,
        "enc_session_key": enc_session_key
    }

    print("[AS] Sending TGT and encrypted session key to the client\n")
    return response



# Testing 

if __name__ == "__main__":
    # Simulate user login
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    response = kerberos_as_request(username, password)
    if response:
        print(json.dumps(response, indent=4))
