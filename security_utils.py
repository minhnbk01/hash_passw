import re
import bcrypt
import pyperclip
import threading
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

def clear_clipboard(original_text):
    if pyperclip.paste() == original_text:
        pyperclip.copy("")
        print("\n[i] Clipboard đã tự động xóa mật khẩu để bảo mật.")

def copy_to_clipboard_with_scrub(text, timeout=10):
    pyperclip.copy(text)
    print(f"\n[+] Đã sao chép mật khẩu vào clipboard an toàn.")
    print(f"    Vui lòng Paste (Ctrl+V) vào nơi cần thiết.")
    print(f"    Mật khẩu sẽ tự động bị xóa khỏi clipboard sau {timeout} giây.")
    timer = threading.Timer(timeout, clear_clipboard, args=(text,))
    timer.start()