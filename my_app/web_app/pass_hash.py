import hashlib

def hash_password(password: str):
    password_bytes = password.encode('utf-8')
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return hashed


