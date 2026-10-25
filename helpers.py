import random
import string

def generate_email():
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    return f"{name}@test.com"

def generate_password():
    return "123456"