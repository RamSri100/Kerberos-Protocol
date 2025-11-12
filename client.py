
# Kerberos Client Simulation 

from crypto_utils import (
    derive_key_from_password,
    decrypt_object,
    encrypt_object,
    current_timestamp
)

from server_as import kerberos_as_request
from server_tgs import kerberos_tgs_request
from server_service import kerberos_service_request

import json


# Create Authenticator 

def create_authenticator(username: str, session_key_hex: str):
    "Create an authenticator encrypted with the given session key"
    auth_data = {
        "user": username,
        "timestamp": current_timestamp()
    }
    # Convert session key hex to bytes
    return encrypt_object(auth_data, bytes.fromhex(session_key_hex))



# Kerberos Client Flow

def kerberos_client_flow(username: str, password: str, service: str):
    

    # Authenticate with AS (get TGT + session key)
    
    as_response = kerberos_as_request(username, password)
    if not as_response:
        print("[CLIENT] Authentication with AS failed.")
        return None

    # Decrypt session key (Client–TGS)
    client_key = derive_key_from_password(password)
    decrypted = decrypt_object(as_response["enc_session_key"], client_key)
    session_key_c_tgs = decrypted["session_key"]
    print(f"[CLIENT] Decrypted session key (Client–TGS): {session_key_c_tgs}")

    # Extract TGT
    tgt = as_response["tgt"]

    
    # Request Service Ticket from TGS
    
    authenticator_tgs = create_authenticator(username, session_key_c_tgs)
    print("[CLIENT] Created Authenticator for TGS")

    tgs_response = kerberos_tgs_request(tgt, authenticator_tgs, service)
    if not tgs_response:
        print("[CLIENT] TGS request failed.")
        return None

    # Decrypt Client–Service session key
    dec_for_client = decrypt_object(tgs_response["enc_session_key"], bytes.fromhex(session_key_c_tgs))
    session_key_c_s = dec_for_client["session_key"]
    print(f"[CLIENT] Decrypted session key (Client–Service): {session_key_c_s}")

    service_ticket = tgs_response["service_ticket"]

    
    # Contact the Service Server using the Service Ticket
    
    authenticator_service = create_authenticator(username, session_key_c_s)
    print("[CLIENT] Created Authenticator for Service Server")

    service_response = kerberos_service_request(service_ticket, authenticator_service, service)

    if not service_response:
        print("[CLIENT] Access denied")
        return None

    
    print(service_response["message"])
    return service_response



# Testing

if __name__ == "__main__":
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    service = input("Enter service (fileserver/mailserver): ").strip()

    kerberos_client_flow(username, password, service)
