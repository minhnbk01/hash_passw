from user_service import register_user, login_user

if __name__ == "__main__":
    print("=== BẮT ĐẦU TEST HỆ THỐNG BẢO MẬT ===")
    
    # 1. Test lỗi mật khẩu yếu
    register_user("hacker_01", "123", "0900000000", "hacker01@example.com")

    # 2. Test đăng ký thành công
    register_user("secure_user", "StrongPass!2024", "0912345678", "secureuser@example.com")
    # 3. Test đăng nhập thành công
    login_user("secure_user", "StrongPass!2024")
    # 4. Test đăng nhập thất bại (mật khẩu sai) 
    login_user("secure_user", "WrongPass!2024")
    # 5. Test đăng nhập thất bại (user không tồn tại)
    login_user("nonexistent_user", "AnyPass!2024")
    
    register_user("hacker_2", "H@cker1???'??", "0909090919", "hacker02@example.com")
    login_user("hacker_2", "H@cker1???'??")