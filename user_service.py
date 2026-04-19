import mysql.connector
from config import DB_CONFIG
import security_utils

def check_user_exists(username):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
        count = cursor.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def register_user(username, plain_password, phone_number,email):
    print(f"\n[*] Đang xử lý đăng ký cho user: {username}")

    if check_user_exists(username):
        print("     [!] User đã tồn tại.")
        return

    is_strong, msg = security_utils.check_password_strong(plain_password)
    if not is_strong:
        print(f"     [!] Lỗi: {msg}")
        return

    hashed_password = security_utils.hash_password(plain_password)
    encrypted_phone = security_utils.encrypt_data(phone_number)
    encrypted_email = security_utils.encrypt_data(email)

    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password_hash, encrypted_phone, encrypted_email) VALUES (%s, %s, %s, %s)"
        values = (username, hashed_password.decode('utf-8'), encrypted_phone, encrypted_email)
        cursor.execute(query, values)
        conn.commit()
        print("     [+] Đăng ký thành công")
    except mysql.connector.IntegrityError:
        print("     [!] User đã tồn tại.")
    except Exception as e:
        print(f"    [!] Lỗi hệ thống: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def login_user(username, plain_password):
    print(f"\n[*] Đang xử lý đăng nhập cho user: {username}")
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            print("     [!] Không tìm thấy người dùng")
            return

        if security_utils.verify_password(plain_password, user['password_hash']):
            print("[+] Đăng nhập thành công")
            decrypted_phone = security_utils.decrypt_data(user['encrypted_phone'])
            decrypted_email = security_utils.decrypt_data(user['encrypted_email'])
            print(f"    SĐT: {decrypted_phone}")
            print(f"    Email: {decrypted_email}")
        else:
            print("     [!] Sai mật khẩu")
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
