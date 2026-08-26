import sys
import os
import re
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

SALT_SIZE = 16
NONCE_SIZE = 12

def get_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
    )
    return kdf.derive(password.encode('utf-8'))

def encrypt(msg, password):
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = get_key(password, salt)
    
    aes = AESGCM(key)
    raw_cipher = aes.encrypt(nonce, msg.encode('utf-8'), None)
    
    data = salt + nonce + raw_cipher
    return base64.b64encode(data).decode('utf-8')

def decrypt(msg_b64, password):
    try:
        data = base64.b64decode(msg_b64.strip().encode('utf-8'))
        salt = data[:SALT_SIZE]
        nonce = data[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
        raw_cipher = data[SALT_SIZE + NONCE_SIZE:]
        
        key = get_key(password, salt)
        aes = AESGCM(key)
        plain = aes.decrypt(nonce, raw_cipher, None)
        
        return plain.decode('utf-8')
    except Exception:
        return "error : wrong key or corrupted data"

def run(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        m_mode = re.search(r'^MODE:\s*(true|false|1|0)', content, re.M | re.I)
        m_key = re.search(r'^KEY:\s*(.+)$', content, re.M)
        
        if not m_mode or not m_key:
            print("error : missing MODE or KEY")
            return

        is_enc = m_mode.group(1).lower() in ['true', '1']
        pwd = m_key.group(1).strip()

        parts = content.split("MESSAGE:", 1)
        if len(parts) < 2:
            print("error : missing MESSAGE tag")
            return

        msg = parts[1].strip()

        if is_enc:
            out_msg = encrypt(msg, pwd)
            new_mode = "false"
        else:
            out_msg = decrypt(msg, pwd)
            new_mode = "true"

        new_content = f"MODE: {new_mode}\nKEY: {pwd}\nMESSAGE:\n{out_msg}\n"

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print("done")

    except FileNotFoundError:
        print("error : file not found")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage : python script.py <file.txt>")
    else:
        run(sys.argv[1])