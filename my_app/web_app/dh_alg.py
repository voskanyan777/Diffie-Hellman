import random


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
