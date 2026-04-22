import sys
from user_service import register_user, login_user
from password_service import add_password, get_passwords, get_password, update_password, delete_password
from security_utils import generate_strong_password
from virtual_keyboard import get_password_via_vk

def logged_in_menu(user_id):
    while True:
        print("\n=== QUẢN LÝ MẬT KHẨU ===")
        print("1. Xem danh sách dịch vụ đã lưu")
        print("2. Xem mật khẩu của một dịch vụ")
        print("3. Thêm mật khẩu mới")
        print("4. Cập nhật mật khẩu")
        print("5. Xóa mật khẩu")
        print("6. Đăng xuất")
        
        choice = input("Chọn chức năng (1-6): ")
        
        if choice == '1':
            get_passwords(user_id)
        elif choice == '2':
            service = input("Nhập tên dịch vụ: ")
            get_password(user_id, service)
        elif choice == '3':
            service = input("Nhập tên dịch vụ: ")
            username = input("Nhập tên tài khoản/email: ")
            gen_choice = input("Bạn muốn tự tạo mật khẩu mạnh? (y/n): ")
            if gen_choice.lower() == 'y':
                password = generate_strong_password()
                print(f"[i] Mật khẩu được tạo: {password}")
            else:
                vk_choice = input("Sử dụng Bàn phím ảo để chống keylogger? (y/n): ")
                if vk_choice.lower() == 'y':
                    password = get_password_via_vk("Nhập Mật Khẩu Dịch Vụ")
                    print("[i] Đã nhận mật khẩu từ Bàn phím ảo.")
                else:
                    password = input("Nhập mật khẩu: ")
            add_password(user_id, service, username, password)
        elif choice == '4':
            service = input("Nhập tên dịch vụ cần cập nhật: ")
            gen_choice = input("Bạn muốn tự tạo mật khẩu mạnh mới? (y/n): ")
            if gen_choice.lower() == 'y':
                password = generate_strong_password()
                print(f"[i] Mật khẩu mới được tạo: {password}")
            else:
                vk_choice = input("Sử dụng Bàn phím ảo để chống keylogger? (y/n): ")
                if vk_choice.lower() == 'y':
                    password = get_password_via_vk("Nhập Mật Khẩu Mới")
                    print("[i] Đã nhận mật khẩu từ Bàn phím ảo.")
                else:
                    password = input("Nhập mật khẩu mới: ")
            update_password(user_id, service, password)
        elif choice == '5':
            service = input("Nhập tên dịch vụ cần xóa: ")
            confirm = input(f"Bạn có chắc chắn muốn xóa '{service}'? (y/n): ")
            if confirm.lower() == 'y':
                delete_password(user_id, service)
        elif choice == '6':
            print("Đã đăng xuất.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

def main_menu():
    while True:
        print("\n=== HỆ THỐNG QUẢN LÝ MẬT KHẨU CÁ NHÂN ===")
        print("1. Đăng ký")
        print("2. Đăng nhập")
        print("3. Thoát")
        
        choice = input("Chọn chức năng (1-3): ")
        
        if choice == '1':
            username = input("Nhập username: ")
            vk_choice = input("Sử dụng Bàn phím ảo cho mật khẩu để chống keylogger? (y/n): ")
            if vk_choice.lower() == 'y':
                password = get_password_via_vk("Nhập Mật Khẩu Đăng Ký")
                print("[i] Đã nhận mật khẩu từ Bàn phím ảo.")
            else:
                password = input("Nhập password (ít nhất 8 ký tự, có hoa, thường, số, ký tự đặc biệt): ")
            phone = input("Nhập số điện thoại: ")
            email = input("Nhập email: ")
            register_user(username, password, phone, email)
        elif choice == '2':
            username = input("Nhập username: ")
            vk_choice = input("Sử dụng Bàn phím ảo cho mật khẩu để chống keylogger? (y/n): ")
            if vk_choice.lower() == 'y':
                password = get_password_via_vk("Nhập Mật Khẩu Đăng Nhập")
                print("[i] Đã nhận mật khẩu từ Bàn phím ảo.")
            else:
                password = input("Nhập password: ")
            user_id = login_user(username, password)
            if user_id:
                logged_in_menu(user_id)
        elif choice == '3':
            print("Tạm biệt!")
            sys.exit(0)
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main_menu()