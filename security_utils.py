import re
import bcrypt
from cryptography.fernet import Fernet
from config import SECRET_KEY

cipher = Fernet(SECRET_KEY)

def check_password_strong(password):
    if not password:
        return False, "Password is required"
    if len(password) < 8 or len(password) > 72:
        return False, "Password must be at least 8 characters long and not exceed 72 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    return True, None

def hash_password(plain_password):
     return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt(rounds=16))

def verify_password(plain_password, hashed_password):
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def encrypt_data(data_string):
    return cipher.encrypt(data_string.encode('utf-8'))

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data).decode('utf-8')

import secrets
import string

def generate_strong_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>"
    while True:
        password = ''.join(secrets.choice(characters) for i in range(length))
        is_strong, _ = check_password_strong(password)
        if is_strong:
            return password