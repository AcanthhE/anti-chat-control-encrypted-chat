# Anti-chat-control-encrypted-chat (made by AcanthE 🇫🇷)
provide a program to use to encrypt et decode a message for counter chat control UE 🇪🇺

# FileCrypto (AES-256)

A lightweight and highly secure text encryption tool written in Python. It allows you to encrypt and decrypt messages directly inside a local text file without relying on any external or third-party servers.

Designed to ensure complete communication privacy against mass surveillance and automated scanning.

---

## Features

* **AES-256-GCM Encryption:** World military standard. Includes message authentication to detect any tampering or data corruption.
* **Seed / Password Protection:** Key derivation via `PBKDF2HMAC` (600,000 iterations) makes brute-force attacks computationally infeasible.
* **In-Place File Processing:** The script reads, encrypts (or decrypts), and replaces content directly inside the `.txt` file.
* **Dynamic Security:** A fresh random salt and nonce are generated on every run. Encrypting the exact same text twice produces completely different outputs, preventing pattern recognition.

---

### Instructions & Usage
1. Create the Input File (message.txt)

Create a text file structured as follows:

```
MODE: true
CLE: YourUniqueSeedOrPassword
MESSAGE:
Write your confidential message here...
```

* MODE: true -> Set to encrypt the text.
* MODE: false -> Set to decrypt the text.
* CLE: Your secret key/seed (shared only between you and the recipient).
* MESSAGE: The payload to process.

2. Run the Script

Execute the script by passing your text file as an argument:
Bash

`python script.py message.txt`

3. Execution Result

    The message.txt file is modified directly in place.
    The raw message is replaced by a Base64-encoded encrypted string.
    MODE automatically toggles to false to prepare for subsequent decryption.
    To decrypt: Run the exact same command (python script.py message.txt) again.

Is it truly unbreakable?

Yes. Unlike legacy ciphers (Caesar, basic XOR) or common misconceptions:

  Zero Patterns: The encrypted output is indistinguishable from mathematical white noise.
  Text Length: Whether your message is 3 words or 50 pages long, security remains at maximum strength.
  Cracking: Without the exact key, cracking the cipher would take billions of years using current supercomputers.

## Prerequisites

Install the official Python cryptography library:

```bash
pip install cryptography
