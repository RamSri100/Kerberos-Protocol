# Kerberos-Protocol
# Simplified Kerberos Authentication Protocol Implementation using Python

Overview:

This project is a simplified educational implementation of the Kerberos authentication protocol using Python.
It demonstrates the core principles of Kerberos — secure user authentication, ticket-based access control, and session key exchange — implemented manually without relying on any cryptographic libraries such as cryptography, pycrypto, or openssl.

The project simulates the three primary entities of the Kerberos system:

Authentication Server (AS)

Ticket Granting Server (TGS)

Service Server (Resource Server)

Client

---

 Project Objectives:
- Understand and implement the Kerberos authentication workflow.
- Demonstrate secure access using Ticket Granting Tickets (TGTs) and Service Tickets.
- Build a working AS → TGS → Service Server communication system.
- Implement manual cryptographic logic for encryption, decryption, and key derivation
- Reinforce information security principles — authentication, confidentiality, and freshness validation
- Provide a functional end-to-end simulation using Python.

---

Structure:
kerberos-sim/
│
├── client.py               → Simulates the Kerberos client workflow
├── server_as.py            → Authentication Server (AS)
├── server_tgs.py           → Ticket Granting Server (TGS)
├── server_service.py       → Resource/Service Server
├── crypto_utils.py         → Custom-built encryption, decryption, key derivation
├── .gitignore              → Ignored files (venv, __pycache__)
└── README.md               → Documentation file


---

Approach:
1. Authentication Phase (AS)

Client sends username and password to the Authentication Server.

AS verifies credentials and issues a Ticket Granting Ticket (TGT) encrypted with the TGS master key.

AS sends back:

The TGT

The Client–TGS Session Key, encrypted with a key derived from the client’s password.

2. Ticket Granting Phase (TGS)

Client sends TGT and an Authenticator (encrypted with the Client–TGS Session Key) to the TGS.

TGS validates both and issues:

A Service Ticket (encrypted with the service’s master key)

A Client–Service Session Key, encrypted with the Client–TGS Session Key.

3. Service Access Phase (Resource Server)

Client sends the Service Ticket and an Authenticator (encrypted with the Client–Service Session Key) to the Service Server.

Server decrypts, validates, and grants access to the protected resource.

---------
Challenges:
Understanding Kerberos ticket flow (AS → TGS → Service)- Studied real Kerberos packet flow and simplified it logically
Avoiding crypto libraries- Implemented XOR cipher and key derivation manually
Ticket & timestamp validation-Created reusable helper functions for freshness verification
Managing multiple keys-Used consistent JSON structures and hex-encoding for clarity
Organizing modules-Divided each stage into separate Python files for modular clarity

---------


---------

How to Run:

Step 1: Clone the repository
git clone https://github.com/RamSri100/Kerberos-Protocol.git
cd Kerberos-Protocol

🧩 Step 2: Create and activate virtual environment
py -m venv venv
venv\Scripts\activate

🧩 Step 3: (Optional) Install Flask
pip install flask


(Flask is not required for this command-line version but can be used later for web simulation.)

🧩 Step 4: Run the client to test the full Kerberos workflow
python client.py


Then enter:

Username: alice
Password: password123
Service: fileserver

✅ Expected Output

You should see:

=== KERBEROS CLIENT START ===
[AS] Authentication successful...
[TGS] Generated Service Ticket...
[SERVICE] Authentication successful!
=== SERVICE RESPONSE ===
This is protected data for fileserver. Welcome, alice!


service: fileserver

--------------

References

MIT Kerberos Protocol Overview

William Stallings, Cryptography and Network Security, 8th Edition

Python Official Documentation – hashlib, os

SEED Labs – Kerberos Authentication Lab (for conceptual guidance)


