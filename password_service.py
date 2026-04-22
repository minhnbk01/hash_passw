import mysql.connector
from config import DB_CONFIG
import security_utils

def add_password(user_id, service_name, account_username, plain_password):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Check if service already exists for user
        cursor.execute("SELECT id FROM passwords WHERE user_id = %s AND service_name = %s", (user_id, service_name))
        if cursor.fetchone():
            print(f"     [!] Bạn đã lưu mật khẩu cho dịch vụ '{service_name}' rồi.")
            return False

        encrypted_password = security_utils.encrypt_data(plain_password)
        
        query = "INSERT INTO passwords (user_id, service_name, account_username, encrypted_password) VALUES (%s, %s, %s, %s)"
        values = (user_id, service_name, account_username, encrypted_password)
        cursor.execute(query, values)
        conn.commit()
        print(f"     [+] Đã lưu mật khẩu cho dịch vụ '{service_name}' thành công.")
        return True
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_passwords(user_id):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT service_name, account_username FROM passwords WHERE user_id = %s", (user_id,))
        passwords = cursor.fetchall()
        
        if not passwords:
            print("     [i] Bạn chưa lưu mật khẩu nào.")
            return []
            
        print("\n--- DANH SÁCH DỊCH VỤ ĐÃ LƯU ---")
        for idx, pw in enumerate(passwords, 1):
            print(f"{idx}. {pw['service_name']} (Tài khoản: {pw['account_username']})")
        print("---------------------------------")
        return passwords
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_password(user_id, service_name):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT account_username, encrypted_password FROM passwords WHERE user_id = %s AND service_name = %s", (user_id, service_name))
        pw_entry = cursor.fetchone()
        
        if not pw_entry:
            print(f"     [!] Không tìm thấy dịch vụ '{service_name}'.")
            return None
            
        decrypted_password = security_utils.decrypt_data(pw_entry['encrypted_password'])
        print(f"\n[+] Thông tin dịch vụ: {service_name}")
        print(f"    Tài khoản: {pw_entry['account_username']}")
        print(f"    Mật khẩu:  ********")
        security_utils.copy_to_clipboard_with_scrub(decrypted_password)
        return decrypted_password
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return None
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_password(user_id, service_name, new_plain_password):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM passwords WHERE user_id = %s AND service_name = %s", (user_id, service_name))
        if not cursor.fetchone():
            print(f"     [!] Không tìm thấy dịch vụ '{service_name}'.")
            return False

        encrypted_password = security_utils.encrypt_data(new_plain_password)
        
        query = "UPDATE passwords SET encrypted_password = %s WHERE user_id = %s AND service_name = %s"
        values = (encrypted_password, user_id, service_name)
        cursor.execute(query, values)
        conn.commit()
        print(f"     [+] Đã cập nhật mật khẩu cho '{service_name}' thành công.")
        return True
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_password(user_id, service_name):
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM passwords WHERE user_id = %s AND service_name = %s", (user_id, service_name))
        if not cursor.fetchone():
            print(f"     [!] Không tìm thấy dịch vụ '{service_name}'.")
            return False

        query = "DELETE FROM passwords WHERE user_id = %s AND service_name = %s"
        cursor.execute(query, (user_id, service_name))
        conn.commit()
        print(f"     [+] Đã xóa dịch vụ '{service_name}' thành công.")
        return True
    except Exception as e:
        print(f"     [!] Lỗi Database: {e}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
