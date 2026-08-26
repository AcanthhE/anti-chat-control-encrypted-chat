# Anti-chat-control-encrypted-chat (made by AcanthE 🇫🇷)
provide a program to use to encrypt et decode a message for counter chat control EU 🇪🇺

# FileCrypto (AES-256)

A lightweight and highly secure text encryption tool written in Python. It allows you to encrypt and decrypt messages directly inside a local text file without relying on any external or third-party servers.

Designed to ensure complete communication privacy against mass surveillance and automated scanning.

# Local Encrypted Message Tool

A small, fully offline desktop app to encrypt and decrypt text messages using **AES-256-GCM** with a password-derived key. Designed to ensure complete communication privacy against mass surveillance and automated scanning without relying on external servers, telemetry, or network calls.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## Features

- **AES-256-GCM encryption:** World military standard with message authentication (tamper detection).
- **PBKDF2HMAC key derivation:** (600,000 iterations) makes brute-forcing computationally infeasible.
- **Dynamic security:** Fresh random salt and nonce on every run. Encrypting the exact same text twice produces completely different outputs.
- **Graphical Interface (GUI):** Simple, responsive dark-themed window with zero hidden controls.
- **CLI / File-based Processing:** Native compatibility with raw `.txt` file processing (`MODE:` / `KEY:` / `MESSAGE:` format).
- **Standalone executable:** Can be compiled into a portable single-file application.

## Project Structure

```text

.
├── prim v1/
│   ├── README.md          # Dedicated documentation for using it
│   ├── script.py          # Standalone CLI / text-file script
│   └── secret.txt         # Text to encode / decode
├── utils/
│   ├── Makefile           # Automation shortcuts (install / run / build)
│   ├── README.md          # Dedicated documentation for the CLI tool
│   ├── crypto_app.py      # Graphical interface + core crypto logic
│   └── requirements.txt   # Python dependencies
└── README.md
