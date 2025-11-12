# crypto_utils.py
# This file contains simple encryption, decryption, and helper functions


import hashlib
import json
import os
import time
import binascii



# Key Derivation

def derive_key_from_password(password: str) -> bytes:
    "Derive a 32-byte key from a password using SHA-256"
    return hashlib.sha256(password.encode()).digest()



# XOR-based Encryption/Decryption

def xor_bytes(data: bytes, key: bytes) -> bytes:
    "Simple XOR cipher for demonstration (symmetric)"
    result = bytearray()
    for i, b in enumerate(data):
        result.append(b ^ key[i % len(key)])
    return bytes(result)



# Encrypt/Decrypt JSON Objects

def encrypt_object(obj, key: bytes) -> str:
    "Serialize object to JSON, XOR-encrypt, and hex-encode"
    raw = json.dumps(obj).encode()
    cipher = xor_bytes(raw, key)
    return binascii.hexlify(cipher).decode()


def decrypt_object(hex_str: str, key: bytes):
    "Hex-decode, XOR-decrypt, and parse JSON object"
    cipher = binascii.unhexlify(hex_str)
    plain = xor_bytes(cipher, key)
    return json.loads(plain.decode())



# Session Key Generator

def generate_session_key(length: int = 16) -> str:
    "Generate a random hex-encoded session key"
    return binascii.hexlify(os.urandom(length)).decode()



# Timestamp Helper

def current_timestamp() -> int:
    return int(time.time())


def is_fresh(timestamp: int, window: int = 120) -> bool:
    "Check if timestamp is within allowed freshness window (seconds)"
    return abs(int(time.time()) - int(timestamp)) <= window



# Testing the functions 

if __name__ == "__main__":
    password = "mysecret"
    key = derive_key_from_password(password)
    data = {"user": "alice", "session_key": generate_session_key(), "time": current_timestamp()}

    enc = encrypt_object(data, key)
    print("Encrypted (hex):", enc)

    dec = decrypt_object(enc, key)
    print("Decrypted:", dec)
