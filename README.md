Title- Implementation of a Simplified Kerberos Authentication Protocol Using Python

Overview:

This project is a simplified implementation of the Kerberos authentication protocol developed using Python, demonstrating the core principles of Kerberos including the secure user authentication, ticket-based access control, and session key exchange through manual implementation and without using any third-party cryptographic libraries.

Kerberos Authentication protocol is basically a network authentication protocol which is used in Windows in order to strengthen the security predominantly for the client-server applications by including symmetric cryptography to encrypt tickets and sending them over only for a limited ammount of time instead of only passwords and also a thirdy party source for the authentication of client to services in  secure manner.

The main components of the Kerberos system:

i. Authentication Server (AS)

ii. Ticket Granting Server (TGS)

iii. Service Server (Resource Server)

iv. Client

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
1. Authentication Phase (Authentication Server)

Initially, the Client submits the username and password to the Authentication Server.

Then, the Server will verify the entered credentials and issues a Ticket Granting Ticket which will be encrypted with the TGS master key.

Now, the Authentication Server sends back a Ticket Granting Ticket and a Session Key(Client-Ticket granting server), which is encrypted with a key derived from the client’s password.

2. Ticket Granting Phase (TGS)

After the client receives the Ticket granting ticket and the session key, this TGT and an Authenticator (encrypted with the Client–TGS Session Key) is sent to the Ticket granting server.

Ticket Granting Server will validate both and then issues:

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


