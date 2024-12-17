import hashlib

def hash_password(password: str):
    # Преобразуем строку пароля в байты и хешируем с помощью SHA-256
    password_bytes = password.encode('utf-8')
    hashed = hashlib.sha256(password_bytes).hexdigest()  # Хеширование пароля
    return hashed


