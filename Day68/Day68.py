# =========================================================
#              FILE ENCRYPT / DECRYPT TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mã hóa & giải mã file bằng AES-256
#
# Chức năng:
#   ✓ Mã hóa file AES-256
#   ✓ Giải mã file AES-256
#   ✓ Password-based encryption
#   ✓ Hỗ trợ file lớn
#   ✓ Kiểm tra hash SHA256
#   ✓ Hiển thị thông tin file
#   ✓ Kiểm tra integrity
#   ✓ Giao diện terminal hiện đại
#   ✓ Demo mode
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pycryptodome colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python file_encryptor.py
#
# =========================================================

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from colorama import Fore, Style, init

import hashlib
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
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU FILE ENCRYPTION")

    print(Fore.WHITE + """
File Encryption Tool dùng để:

   ✓ Bảo vệ file
   ✓ Chống truy cập trái phép
   ✓ Bảo mật dữ liệu cá nhân
   ✓ Secure Backup

=========================================================
THUẬT TOÁN SỬ DỤNG
=========================================================

✓ AES-256 CBC
✓ PBKDF2
✓ SHA256

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Secure Storage
✓ Cloud Backup
✓ USB Encryption
✓ File Sharing
✓ Corporate Security

=========================================================
CHƯƠNG TRÌNH HỖ TRỢ
=========================================================

✓ Encrypt File
✓ Decrypt File
✓ File Hash
✓ Integrity Check
✓ Password-based Encryption

=========================================================
LƯU Ý
=========================================================

✓ Không quên password
✓ Password mạnh
✓ Backup file gốc
""")

    line()


# =========================================================
# TẠO KEY
# =========================================================

def generate_key(password, salt):

    return PBKDF2(
        password,
        salt,
        dkLen=32
    )


# =========================================================
# SHA256 FILE
# =========================================================

def file_hash(filename):

    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# =========================================================
# FILE INFO
# =========================================================

def file_info(filename):

    try:

        size = os.path.getsize(filename)

        print(Fore.CYAN +
              f"\nTên file : {filename}")

        print(Fore.YELLOW +
              f"Kích thước: {size} bytes")

        print(Fore.GREEN +
              f"SHA256   : {file_hash(filename)}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")


# =========================================================
# MÃ HÓA FILE
# =========================================================

def encrypt_file():

    clear()

    title("MÃ HÓA FILE AES-256")

    filename = input(
        Fore.YELLOW +
        "Nhập file cần mã hóa: "
    )

    if not os.path.exists(filename):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    try:

        print(Fore.CYAN +
              "\nĐang đọc file...")

        with open(filename, "rb") as f:

            data = f.read()

        salt = get_random_bytes(16)

        key = generate_key(password, salt)

        cipher = AES.new(
            key,
            AES.MODE_CBC
        )

        encrypted = cipher.encrypt(
            pad(data, AES.block_size)
        )

        output_file = filename + ".enc"

        with open(output_file, "wb") as f:

            f.write(salt)
            f.write(cipher.iv)
            f.write(encrypted)

        print(Fore.GREEN +
              f"\nĐã mã hóa file: {output_file}")

        file_info(output_file)

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi mã hóa:\n{e}")

    pause()


# =========================================================
# GIẢI MÃ FILE
# =========================================================

def decrypt_file():

    clear()

    title("GIẢI MÃ FILE AES-256")

    filename = input(
        Fore.YELLOW +
        "Nhập file .enc: "
    )

    if not os.path.exists(filename):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    try:

        with open(filename, "rb") as f:

            salt = f.read(16)

            iv = f.read(16)

            encrypted = f.read()

        key = generate_key(password, salt)

        cipher = AES.new(
            key,
            AES.MODE_CBC,
            iv
        )

        decrypted = unpad(
            cipher.decrypt(encrypted),
            AES.block_size
        )

        output_file = "decrypted_" + \
                      os.path.basename(
                          filename.replace(".enc", "")
                      )

        with open(output_file, "wb") as f:

            f.write(decrypted)

        print(Fore.GREEN +
              f"\nĐã giải mã file: {output_file}")

        file_info(output_file)

    except Exception as e:

        print(Fore.RED +
              "\nGiải mã thất bại!")

        print(Fore.RED +
              "Sai password hoặc file lỗi.")

    pause()


# =========================================================
# HASH CHECK
# =========================================================

def compare_hash():

    clear()

    title("KIỂM TRA FILE HASH")

    file1 = input(
        Fore.YELLOW +
        "Nhập file thứ nhất: "
    )

    file2 = input(
        Fore.YELLOW +
        "Nhập file thứ hai: "
    )

    try:

        hash1 = file_hash(file1)

        hash2 = file_hash(file2)

        line()

        print(Fore.CYAN +
              f"\nHash File 1:\n{hash1}")

        print(Fore.CYAN +
              f"\nHash File 2:\n{hash2}")

        if hash1 == hash2:

            print(Fore.GREEN +
                  "\n✓ Hai file giống nhau")

        else:

            print(Fore.RED +
                  "\n✗ Hai file khác nhau")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# FILE INFO MENU
# =========================================================

def file_info_menu():

    clear()

    title("THÔNG TIN FILE")

    filename = input(
        Fore.YELLOW +
        "Nhập tên file: "
    )

    if os.path.exists(filename):

        file_info(filename)

    else:

        print(Fore.RED +
              "\nFile không tồn tại.")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO FILE ENCRYPTION")

    demo_file = "demo.txt"

    with open(demo_file,
              "w",
              encoding="utf-8") as f:

        f.write("HELLO AES FILE ENCRYPTION")

    print(Fore.GREEN +
          f"\nĐã tạo file demo: {demo_file}")

    password = "123456"

    print(Fore.YELLOW +
          f"Password demo: {password}")

    time.sleep(1)

    # Encrypt
    try:

        with open(demo_file, "rb") as f:

            data = f.read()

        salt = get_random_bytes(16)

        key = generate_key(password, salt)

        cipher = AES.new(
            key,
            AES.MODE_CBC
        )

        encrypted = cipher.encrypt(
            pad(data, AES.block_size)
        )

        enc_file = demo_file + ".enc"

        with open(enc_file, "wb") as f:

            f.write(salt)
            f.write(cipher.iv)
            f.write(encrypted)

        print(Fore.GREEN +
              f"\nĐã mã hóa: {enc_file}")

    except Exception as e:

        print(Fore.RED + str(e))

    pause()


# =========================================================
# GIẢI THÍCH AES
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH FILE ENCRYPTION")

    print(Fore.WHITE + """
=========================================================
1. AES-256
=========================================================

AES:
   Advanced Encryption Standard

256-bit:
   ✓ Rất mạnh

=========================================================
2. CBC MODE
=========================================================

CBC:
   Cipher Block Chaining

=========================================================
3. IV
=========================================================

Initialization Vector:
   ✓ Random
   ✓ Tăng bảo mật

=========================================================
4. PBKDF2
=========================================================

Tạo key mạnh từ password.

=========================================================
5. SHA256
=========================================================

Hash dùng để:
   ✓ Kiểm tra integrity

=========================================================
6. ENCRYPTION
=========================================================

Plaintext -> Ciphertext

=========================================================
7. DECRYPTION
=========================================================

Ciphertext -> Plaintext

=========================================================
8. PASSWORD SECURITY
=========================================================

✓ Password mạnh
✓ Không reuse password
✓ Backup password

=========================================================
9. ỨNG DỤNG
=========================================================

✓ Secure File Storage
✓ Cloud Encryption
✓ USB Protection
✓ Enterprise Security
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("FILE ENCRYPT / DECRYPT TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu File Encryption
[2] Mã hóa file
[3] Giải mã file
[4] Kiểm tra hash file
[5] Xem thông tin file
[6] Demo mode
[7] Giải thích AES/File Encryption
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

            encrypt_file()

        elif choice == '3':

            decrypt_file()

        elif choice == '4':

            compare_hash()

        elif choice == '5':

            file_info_menu()

        elif choice == '6':

            demo_mode()

        elif choice == '7':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng File Encryption Tool.

Kiến thức đạt được:
   ✓ AES-256
   ✓ File Encryption
   ✓ CBC Mode
   ✓ SHA256
   ✓ Integrity Check
   ✓ Secure Storage
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
