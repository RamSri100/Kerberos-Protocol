# Kerberos-Protocol
# Simplified Kerberos Authentication Protocol Implementation using Python

This project is a simplified educational implementation of the Kerberos authentication protocol using Python.  
It demonstrates the core principles of Kerberos: secure authentication, ticket-based access, session keys, and trusted third-party verification.  
All cryptographic logic (key derivation, encryption, ticket creation, session key handling, etc.) is **implemented manually**, without using any built-in or third-party cryptographic libraries, in accordance with project requirements.

---

 Project Objectives
- Understand and implement the Kerberos authentication workflow.
- Demonstrate secure access using Ticket Granting Tickets (TGTs) and Service Tickets.
- Build a working AS → TGS → Service Server communication system.
- Implement encryption, decryption, key generation, and timestamp validation **from scratch**.
- Provide a functional end-to-end simulation using Python.

---

Overview of Kerberos Protocol

Kerberos is a network authentication protocol that uses symmetric-key cryptography and a trusted third party to authenticate clients to services securely.

Core components included in this project:

1. **Authentication Server (AS)**  
   - Verifies user credentials  
   - Issues the Ticket Granting Ticket (TGT)  
   - Issues the Client–TGS session key  

2. **Ticket Granting Server (TGS)**  
   - Validates the TGT  
   - Issues Service Tickets  
   - Issues the Client–Service session key  

3. **Service Server**  
   - Validates the Service Ticket  
   - Validates the client’s authenticator  
   - Grants access to protected resources  

4. **Client**  
   - Initiates login  
   - Requests TGT and Service Ticket  
   - Generates authenticators  
   - Accesses the requested service  



Tools & Technologies

### Programming
- **Python 3.9+**

### Servers (implemented as Python modules)
- `server_as.py` – Authentication Server  
- `server_tgs.py` – Ticket Granting Server  
- `server_service.py` – Resource Server  
- `client.py` – Kerberos Client Program  

### Manual Cryptography
Stored in `crypto_utils.py`:
- XOR-based encryption/decryption (custom implementation)  
- Custom key derivation using SHA-256 (standard library)  
- Hex encoding/decoding  
- Timestamp generation and freshness validation  

### Storage
- In-memory dictionaries for users and service keys
- JSON-encoded encrypted tickets

No external cryptographic libraries were used.

---
Workflow: AS → TGS → Service Server

### Step 1: Authentication Server (AS)
- Client sends username & password
- AS verifies user
- AS returns:
  - **TGT** (encrypted with TGS master key)
  - **Client–TGS session key** (encrypted with password-derived key)

### Step 2: Ticket Granting Server (TGS)
- Client sends TGT + Authenticator
- TGS validates TGT and Authenticator
- TGS returns:
  - **Service Ticket**
  - **Client–Service session key** (encrypted with Client–TGS key)

### Step 3: Service Server
- Client sends Service Ticket + Authenticator
- Service validates both
- Access is granted to the protected resource

---

Expected Output

After running `client.py` the output should show:

- Successful login via AS  
- Valid TGT  
- Valid Service Ticket  
- Valid Client–Service session key  
- Successful access to service  

How to Run

 1. Activate virtual environment
venv\Scripts\activate # Windows
source venv/bin/activate # Linux/macOS

shell
Copy code

2. Run the client
python client.py

shell
Copy code

3. Enter:
username: alice
password: Passw0rdA1
service: fileserver
