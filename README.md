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
├── client.py (Simulates the Kerberos client workflow)
├── server_as.py (Authentication Server (AS) )
├── server_tgs.py (Ticket Granting Server (TGS) )
├── server_service.py (Resource/Service Server) )
├── crypto_utils.py (Custom-built encryption, decryption, key derivation)
├── .gitignore (Includes (venv, __pycache__) )
└── README.md  (Documentation file )


---

Approach:
1. Authentication Phase (Authentication Server):

Initially, the Client submits the username and password to the Authentication Server.

Then, the Server will verify the entered credentials and issues a Ticket Granting Ticket which will be encrypted with the TGS master key.

Now, the Authentication Server sends back a Ticket Granting Ticket and a Session Key(Client-Ticket granting server), which is encrypted with a key derived from the client’s password.

2. Ticket Granting Phase (TGS):

After the client receives the Ticket granting ticket and the session key, this TGT and an Authenticator which is encrypted with the Client–TGS Session Key is sent to the Ticket granting server.

Then, the Ticket Granting Server will validate both and then issues a Service Ticket which is encrypted with the service’s master key and the Client–Service Session Key encrypted with the Client–TGS Session Key.

3. Service Access Phase (Resource Server):

In this phase, the Client sends the Service Ticket and the Authenticator which is encrypted with the Client–Service Session Key) to the Service Server.

Server decrypts, validates, and grants access to the protected resource.

---------
Challenges:
i.Understanding the working flow of Kerberos  (AS → TGS → Service).
ii.Avoiding the external cryptographic libraries.
iii.Ticket and timestamp validation.
iv.Management of multiple keys.
v.Organization of all the modules.

---------
Solutions:
i. Analyzed the true Kerberos packet flow in order to arrive at a logical simplification.
ii. Implemented the XOR cipher as well as the key derivation directly in python.
iii.Created reusable helper functions in the main python file for freshness verification.
iv.Used consistent JSON structures and hex-encoding technicques for management of the keys.
v.Divided every single stage into multiple Python files in order to acheive the modular clarity.

---------

How to Run:

Firstly, open command prompt and perform the initial setup:

Step 1: Creating the folder: kerberos-sim:
mkdir kerberos-sim
(All the python files have to be saved in this folder-under single environment).

The, changing the directory:
cd kerberos-sim

Step 2: Creating and activating the virtual environment
py -m venv venv
venv\Scripts\activate

Step 3: (Optional) Install Flask
pip install flask

(Flask is not required for this command-line version but can be used later for web simulation.)

Step 4: Check the installed files:

kerberos-sim>pip list

Step 4: Run the client to test the full Kerberos workflow
python client.py

Then enter:

Username: alice
Password: Passw0rdA1
Service: fileserver

--------------

References:

MIT Kerberos Protocol Overview

Python Official Documentation – hashlib, os

SEED Labs – Kerberos Authentication Lab (for conceptual guidance)


