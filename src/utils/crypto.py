import os
from cryptography.fernet import Fernet


def load_key_from_env(env_var='CSV_ENC_KEY'):
    """Load base64 key from environment variable."""
    key = os.environ.get(env_var)
    if not key:
        return None
    return key.encode()


def decrypt_bytes(enc_bytes, key):
    f = Fernet(key)
    return f.decrypt(enc_bytes)


def encrypt_file(in_path, out_path, key):
    f = Fernet(key)
    with open(in_path, 'rb') as fin:
        data = fin.read()
    token = f.encrypt(data)
    with open(out_path, 'wb') as fout:
        fout.write(token)


def generate_key():
    return Fernet.generate_key()
