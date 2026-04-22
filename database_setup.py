import mysql.connector
from config import DB_CONFIG

def setup_database():
    # Connect without database first to create it if it doesn't exist
    config_no_db = {k: v for k, v in DB_CONFIG.items() if k != 'database'}
    
    try:
        conn = mysql.connector.connect(**config_no_db)
        cursor = conn.cursor()
        
        db_name = DB_CONFIG.get('database', 'secure_app_db')
        
        # Create database
        print(f"[*] Đang tạo database '{db_name}' (nếu chưa có)...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        
        # Select database
        cursor.execute(f"USE {db_name}")
        
        # Create users table
        print("[*] Đang tạo bảng 'users' (nếu chưa có)...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                encrypted_phone BLOB,
                encrypted_email BLOB
            )
        """)
        
        # Create passwords table
        print("[*] Đang tạo bảng 'passwords' (nếu chưa có)...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                service_name VARCHAR(100) NOT NULL,
                account_username VARCHAR(100) NOT NULL,
                encrypted_password BLOB NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        print("[+] Thiết lập Database thành công!")
        
    except Exception as e:
        print(f"[!] Lỗi khi thiết lập Database: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_database()
