import random
import string

def generate_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choices(characters, k=32))
    return token