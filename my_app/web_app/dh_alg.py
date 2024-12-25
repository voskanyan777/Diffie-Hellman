import base64
import random

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import unpad, pad


class DHAlgorithm:
    def __init__(self):
        self.p = int(
            "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD"
            "3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A63A3620FFFFFFFFFFFFFFFF",
            16)
        self.g = 2
        self.server_private_b = random.randint(1, self.p - 1)  # b
        self.shared_private_key = None  # K
        self.server_public_key = None  # B

    def public_key(self):
        self.server_public_key = pow(self.g, self.server_private_b, self.p)

    @property
    def shared_key(self):
        return self.shared_private_key

    @shared_key.setter
    def shared_key(self, client_public_key):
        self.shared_private_key = pow(client_public_key, self.server_private_b, self.p)


def evp_key_iv(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16):
    """Реконструирует ключ и IV из пароля и соли по алгоритму OpenSSL EVP."""
    d = d_i = b''
    while len(d) < key_len + iv_len:
        d_i = MD5.new(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def decrypt_message(encrypted_message: str, private_key: str):
    # Декодируем из Base64
    decoded_data = base64.b64decode(encrypted_message)

    private_key = b"%b" % str(private_key).encode()

    # Проверяем и убираем префикс "Salted__" (если он есть)
    assert decoded_data[:8] == b"Salted__"  # Префикс
    salt = decoded_data[8:16]  # Соль
    ciphertext = decoded_data[16:]  # Шифротекст

    # Реконструируем ключ (примерно) на основе соли (если известна схема генерации)
    # Для этого нужно знать, как ключ генерировался. В CryptoJS часто используется PBKDF2.

    # Генерируем ключ и IV
    key, iv = evp_key_iv(private_key, salt)

    # Расшифровываем данные
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted_data.decode()

def encrypt_message(message: str, private_key: str):
    # Преобразуем приватный ключ в байты
    private_key = b"%b" % str(private_key).encode()

    # Генерируем соль (random 8 байт)
    salt = bytes([random.randint(0, 255) for _ in range(8)])

    # Генерируем ключ и IV на основе приватного ключа и соли
    key, iv = evp_key_iv(private_key, salt)

    # Создаем шифратор AES с режимом CBC
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Паддинг для соответствия блочному размеру AES
    padded_message = pad(message.encode(), AES.block_size)

    # Шифруем данные
    encrypted_data = cipher.encrypt(padded_message)

    # Конкатенируем "Salted__" + соль + шифротекст
    encrypted_message = b"Salted__" + salt + encrypted_data

    # Кодируем в Base64
    return base64.b64encode(encrypted_message).decode()
