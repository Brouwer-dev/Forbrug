#!/usr/bin/python
from cryptography.fernet import Fernet

# One-time key generation
key = Fernet.generate_key()
with open("fernet.key", "wb") as key_file:
    key_file.write(key)