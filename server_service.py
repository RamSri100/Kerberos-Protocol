
# Service Server for Kerberos Simulation

from crypto_utils import (
    decrypt_object,
    encrypt_object,
    current_timestamp,
    is_fresh
)

import json


# Configuration


SERVICE_MASTER_KEYS = {
    "fileserver": b"FILE_SERVER_SECRET_456",
    "mailserver": b"MAIL_SERVER_SECRET_789"
}



# Validate Service Ticket

def validate_service_ticket(ticket_hex: str, service: str):
    "Decrypt service ticket using service master key"
    key = SERVICE_MASTER_KEYS.get(service)
    if not key:
        print(f"[SERVICE] Unknown service requested: {service}")
        return None

    try:
        ticket = decrypt_object(ticket_hex, key)
    except Exception as e:
        print("[SERVICE] Invalid Service Ticket:", e)
        return None

    if current_timestamp() > ticket["expiry"]:
        print("[SERVICE] Service Ticket expired.")
        return None

    return ticket



# Validate Authenticator

def validate_authenticator(auth_hex: str, session_key_c_s: str, username: str):
    "Check timestamp and matching username"
    try:
        auth = decrypt_object(auth_hex, bytes.fromhex(session_key_c_s))
    except Exception as e:
        print("[SERVICE] Failed to decrypt authenticator:", e)
        return None

    if auth["user"] != username:
        print("[SERVICE] Username mismatch in Authenticator.")
        return None

    if not is_fresh(auth["timestamp"]):
        print("[SERVICE] Authenticator timestamp invalid or replayed.")
        return None

    return auth



# Main Function

def kerberos_service_request(service_ticket_hex: str, authenticator_hex: str, service: str):
    "Simulate the client accessing a resource"
    print(f"\n[SERVICE] Access request for: {service}")

    # Validate Service Ticket
    ticket = validate_service_ticket(service_ticket_hex, service)
    if not ticket:
        print("[SERVICE] Invalid Service Ticket.")
        return None

    username = ticket["user"]
    session_key_c_s = ticket["session_key"]

    # Validate Authenticator
    auth = validate_authenticator(authenticator_hex, session_key_c_s, username)
    if not auth:
        print("[SERVICE] Authenticator validation failed.")
        return None

    print("[SERVICE] Authentication successful!")
    print(f"[SERVICE] User '{username}' granted access to {service}.\n")

    data = f"This is the data for the {service}. Welcome, {username}!"

    return {"message": data}



# Testing 

if __name__ == "__main__":
    
    service = input("Enter service name (fileserver/mailserver): ").strip()
    ticket_hex = input("Enter Service Ticket (hex): ").strip()
    auth_hex = input("Enter Authenticator (hex): ").strip()

    result = kerberos_service_request(ticket_hex, auth_hex, service)
    if result:
        print(json.dumps(result, indent=4))
