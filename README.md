# anti-chat-control-encrypted-chat
provide a program to use to encrypt et decode a message for counter chat control UE

# FileCrypto (AES-256)

A lightweight, standalone, and highly secure text encryption tool written in Python. It allows you to encrypt and decrypt messages directly inside a local text file without relying on any external or third-party servers.

Designed to ensure complete communication privacy against mass surveillance and automated scanning.

---

## Features

* **AES-256-GCM Encryption:** World military standard. Includes message authentication to detect any tampering or data corruption.
* **Seed / Password Protection:** Key derivation via `PBKDF2HMAC` (600,000 iterations) makes brute-force attacks computationally infeasible.
* **In-Place File Processing:** The script reads, encrypts (or decrypts), and replaces content directly inside the `.txt` file.
* **Dynamic Security:** A fresh random salt and nonce are generated on every run. Encrypting the exact same text twice produces completely different outputs, preventing pattern recognition.

---

## Prerequisites

Install the official Python cryptography library:

```bash
pip install cryptography
