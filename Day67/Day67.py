# =========================================================
#             STRONG PASSWORD GENERATOR
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Sinh password mạnh bằng Python
#
# Chức năng:
#   ✓ Sinh password mạnh ngẫu nhiên
#   ✓ Tùy chỉnh độ dài password
#   ✓ Hỗ trợ:
#       - Chữ hoa
#       - Chữ thường
#       - Số
#       - Ký tự đặc biệt
#   ✓ Đánh giá độ mạnh password
#   ✓ Tạo nhiều password cùng lúc
#   ✓ Lưu password vào file
#   ✓ Password pronounceable
#   ✓ Giao diện terminal hiện đại
#   ✓ Demo mode
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python password_generator.py
#
# =========================================================

from colorama import Fore, Style, init
import random
import string
import secrets
import math
import os
import time

init(autoreset=True)

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print(Fore.CYAN + "=" * 100)


def title(text):
    line()
    print(Fore.GREEN + Style.BRIGHT + text.center(100))
    line()


def pause():
    input(Fore.YELLOW + "\nNhấn ENTER để tiếp tục...")


# =========================================================
# FILE OUTPUT
# =========================================================

PASSWORD_FILE = "generated_passwords.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU PASSWORD GENERATOR")

    print(Fore.WHITE + """
Password Generator là công cụ dùng để:

   ✓ Sinh mật khẩu mạnh
   ✓ Tăng bảo mật tài khoản
   ✓ Chống brute-force
   ✓ Chống dictionary attack

=========================================================
PASSWORD MẠNH GỒM
=========================================================

✓ Chữ hoa
✓ Chữ thường
✓ Số
✓ Ký tự đặc biệt
✓ Độ dài lớn

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Email
✓ Facebook
✓ Banking
✓ WiFi
✓ Server
✓ Database
✓ Cloud

=========================================================
CHƯƠNG TRÌNH HỖ TRỢ
=========================================================

✓ Random Password
✓ Password Strength Checker
✓ Multiple Passwords
✓ Password Save
✓ Pronounceable Password
""")

    line()


# =========================================================
# ĐÁNH GIÁ PASSWORD
# =========================================================

def check_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(c.isupper() for c in password):
        score += 1

    if any(c.islower() for c in password):
        score += 1

    if any(c.isdigit() for c in password):
        score += 1

    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "YẾU", Fore.RED

    elif score <= 4:
        return "TRUNG BÌNH", Fore.YELLOW

    else:
        return "RẤT MẠNH", Fore.GREEN


# =========================================================
# TÍNH ENTROPY
# =========================================================

def calculate_entropy(password):

    charset = 0

    if any(c.islower() for c in password):
        charset += 26

    if any(c.isupper() for c in password):
        charset += 26

    if any(c.isdigit() for c in password):
        charset += 10

    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)

    entropy = len(password) * math.log2(charset)

    return round(entropy, 2)


# =========================================================
# SINH PASSWORD
# =========================================================

def generate_password(length,
                      upper=True,
                      lower=True,
                      digits=True,
                      symbols=True):

    characters = ""

    if upper:
        characters += string.ascii_uppercase

    if lower:
        characters += string.ascii_lowercase

    if digits:
        characters += string.digits

    if symbols:
        characters += string.punctuation

    if not characters:
        return None

    password = ''.join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return password


# =========================================================
# PASSWORD DỄ ĐỌC
# =========================================================

def generate_pronounceable(length=12):

    vowels = "aeiou"

    consonants = "bcdfghjklmnpqrstvwxyz"

    password = ""

    for i in range(length):

        if i % 2 == 0:
            password += random.choice(consonants)

        else:
            password += random.choice(vowels)

    password += str(random.randint(10, 99))
    password += random.choice("!@#$%")

    return password


# =========================================================
# HIỂN THỊ PASSWORD
# =========================================================

def display_password(password):

    strength, color = check_strength(password)

    entropy = calculate_entropy(password)

    line()

    print(Fore.GREEN + Style.BRIGHT +
          "\nPASSWORD ĐƯỢC TẠO\n")

    print(Fore.CYAN +
          f"Password : {password}")

    print(color +
          f"Strength : {strength}")

    print(Fore.YELLOW +
          f"Length   : {len(password)}")

    print(Fore.MAGENTA +
          f"Entropy  : {entropy} bits")

    line()


# =========================================================
# LƯU FILE
# =========================================================

def save_password(password):

    with open(PASSWORD_FILE,
              "a",
              encoding="utf-8") as f:

        f.write(password + "\n")


# =========================================================
# TẠO PASSWORD
# =========================================================

def create_password():

    clear()

    title("TẠO PASSWORD MẠNH")

    try:

        length = int(input(
            Fore.YELLOW +
            "Nhập độ dài password: "
        ))

    except:

        print(Fore.RED +
              "\nĐộ dài không hợp lệ.")

        pause()

        return

    upper = input(
        Fore.YELLOW +
        "Dùng chữ HOA? (y/n): "
    ).lower() == 'y'

    lower = input(
        Fore.YELLOW +
        "Dùng chữ thường? (y/n): "
    ).lower() == 'y'

    digits = input(
        Fore.YELLOW +
        "Dùng số? (y/n): "
    ).lower() == 'y'

    symbols = input(
        Fore.YELLOW +
        "Dùng ký tự đặc biệt? (y/n): "
    ).lower() == 'y'

    print(Fore.CYAN +
          "\nĐang sinh password...")

    time.sleep(1)

    password = generate_password(
        length,
        upper,
        lower,
        digits,
        symbols
    )

    if password:

        display_password(password)

        save = input(
            Fore.YELLOW +
            "\nLưu password? (y/n): "
        )

        if save.lower() == 'y':

            save_password(password)

            print(Fore.GREEN +
                  f"\nĐã lưu vào: {PASSWORD_FILE}")

    else:

        print(Fore.RED +
              "\nKhông có bộ ký tự nào được chọn.")

    pause()


# =========================================================
# TẠO NHIỀU PASSWORD
# =========================================================

def multiple_passwords():

    clear()

    title("SINH NHIỀU PASSWORD")

    try:

        count = int(input(
            Fore.YELLOW +
            "Số password: "
        ))

        length = int(input(
            Fore.YELLOW +
            "Độ dài: "
        ))

    except:

        print(Fore.RED +
              "\nInput không hợp lệ.")

        pause()

        return

    line()

    for i in range(count):

        password = generate_password(
            length
        )

        strength, color = check_strength(password)

        print(Fore.GREEN +
              f"\n[{i+1}] {password}")

        print(color +
              f"Strength: {strength}")

    line()

    pause()


# =========================================================
# PASSWORD DỄ NHỚ
# =========================================================

def pronounceable_menu():

    clear()

    title("PASSWORD DỄ NHỚ")

    password = generate_pronounceable()

    display_password(password)

    pause()


# =========================================================
# KIỂM TRA PASSWORD
# =========================================================

def analyze_password():

    clear()

    title("KIỂM TRA PASSWORD")

    password = input(
        Fore.YELLOW +
        "Nhập password cần kiểm tra: "
    )

    strength, color = check_strength(password)

    entropy = calculate_entropy(password)

    line()

    print(Fore.CYAN +
          f"\nPassword : {password}")

    print(color +
          f"Strength : {strength}")

    print(Fore.YELLOW +
          f"Entropy  : {entropy} bits")

    print(Fore.WHITE +
          f"Length   : {len(password)}")

    line()

    pause()


# =========================================================
# XEM PASSWORD ĐÃ LƯU
# =========================================================

def view_saved():

    clear()

    title("PASSWORD ĐÃ LƯU")

    if not os.path.exists(PASSWORD_FILE):

        print(Fore.RED +
              "\nChưa có password.")

    else:

        with open(PASSWORD_FILE,
                  "r",
                  encoding="utf-8") as f:

            content = f.read()

            if content.strip():

                print(Fore.GREEN +
                      "\n" + content)

            else:

                print(Fore.RED +
                      "\nFile trống.")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO PASSWORD GENERATOR")

    for i in range(5):

        password = generate_password(16)

        strength, color = check_strength(password)

        print(Fore.GREEN +
              f"\n[{i+1}] {password}")

        print(color +
              f"Strength: {strength}")

        time.sleep(0.5)

    pause()


# =========================================================
# GIẢI THÍCH PASSWORD
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH PASSWORD SECURITY")

    print(Fore.WHITE + """
=========================================================
1. PASSWORD MẠNH
=========================================================

Password mạnh gồm:
   ✓ Dài
   ✓ Random
   ✓ Đủ loại ký tự

=========================================================
2. BRUTE FORCE
=========================================================

Brute-force:
   ✓ Thử mọi password

=========================================================
3. DICTIONARY ATTACK
=========================================================

Dùng danh sách password phổ biến.

=========================================================
4. ENTROPY
=========================================================

Entropy:
   ✓ Độ ngẫu nhiên password

Entropy càng cao:
   ✓ Password càng mạnh

=========================================================
5. SPECIAL CHARACTERS
=========================================================

Ví dụ:
   ! @ # $ % ^ & *

=========================================================
6. PASSWORD MANAGER
=========================================================

Dùng để:
   ✓ Lưu password an toàn

=========================================================
7. KHUYẾN NGHỊ
=========================================================

✓ Dùng >= 12 ký tự
✓ Không dùng tên riêng
✓ Không dùng ngày sinh
✓ Không reuse password

=========================================================
8. MFA / 2FA
=========================================================

2FA:
   ✓ Tăng bảo mật tài khoản
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("STRONG PASSWORD GENERATOR")

        print(Fore.CYAN + """
[1] Giới thiệu Password Generator
[2] Sinh password mạnh
[3] Sinh nhiều password
[4] Password dễ nhớ
[5] Kiểm tra độ mạnh password
[6] Xem password đã lưu
[7] Demo mode
[8] Giải thích bảo mật password
[0] Thoát
""")

        choice = input(
            Fore.YELLOW +
            "Nhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            create_password()

        elif choice == '3':

            multiple_passwords()

        elif choice == '4':

            pronounceable_menu()

        elif choice == '5':

            analyze_password()

        elif choice == '6':

            view_saved()

        elif choice == '7':

            demo_mode()

        elif choice == '8':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Password Generator.

Kiến thức đạt được:
   ✓ Password Security
   ✓ Entropy
   ✓ Brute-force
   ✓ Random Password
   ✓ Secure Authentication
""")

            break

        else:

            print(Fore.RED +
                  "Lựa chọn không hợp lệ!")

            time.sleep(1)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        menu()

    except KeyboardInterrupt:

        print(Fore.RED +
              "\n\nĐã thoát chương trình.")
