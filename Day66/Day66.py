# =========================================================
#              AES DATA ENCRYPTION TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mã hóa dữ liệu bằng AES
#
# Chức năng:
#   ✓ Mã hóa dữ liệu AES-256
#   ✓ Giải mã dữ liệu AES
#   ✓ Sinh khóa bảo mật
#   ✓ Mã hóa file text
#   ✓ Lưu dữ liệu mã hóa
#   ✓ Hiển thị Base64
#   ✓ Password-based encryption
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
# python aes_encryptor.py
#
# =========================================================

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

from colorama import Fore, Style, init

import base64
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
# FILE OUTPUT
# =========================================================

OUTPUT_FILE = "encrypted_output.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU AES ENCRYPTION")

    print(Fore.WHITE + """
AES (Advanced Encryption Standard) là thuật toán
mã hóa đối xứng mạnh nhất hiện nay.

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ HTTPS
✓ VPN
✓ WiFi WPA2/WPA3
✓ Cloud Storage
✓ Banking
✓ Military
✓ Messaging App

=========================================================
AES HOẠT ĐỘNG THẾ NÀO?
=========================================================

AES dùng:
   ✓ Secret Key
   ✓ Block Cipher
   ✓ Symmetric Encryption

=========================================================
AES-256
=========================================================

AES-256:
   ✓ Khóa 256-bit
   ✓ Rất mạnh
   ✓ Gần như không brute-force được

=========================================================
CHƯƠNG TRÌNH NÀY HỖ TRỢ
=========================================================

✓ Encrypt Text
✓ Decrypt Text
✓ AES-256 CBC
✓ Password Key
✓ Base64 Encoding
""")

    line()


# =========================================================
# TẠO KEY TỪ PASSWORD
# =========================================================

def generate_key(password, salt):

    key = PBKDF2(
        password,
        salt,
        dkLen=32
    )

    return key


# =========================================================
# MÃ HÓA AES
# =========================================================

def encrypt_data(data, password):

    salt = get_random_bytes(16)

    key = generate_key(password, salt)

    cipher = AES.new(
        key,
        AES.MODE_CBC
    )

    encrypted = cipher.encrypt(
        pad(data.encode(), AES.block_size)
    )

    result = (
        salt +
        cipher.iv +
        encrypted
    )

    return base64.b64encode(result).decode()


# =========================================================
# GIẢI MÃ AES
# =========================================================

def decrypt_data(encrypted_data, password):

    raw = base64.b64decode(encrypted_data)

    salt = raw[:16]

    iv = raw[16:32]

    encrypted = raw[32:]

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

    return decrypted.decode()


# =========================================================
# HIỂN THỊ KEY HASH
# =========================================================

def show_password_hash(password):

    hashed = hashlib.sha256(
        password.encode()
    ).hexdigest()

    print(Fore.CYAN +
          "\nSHA256 Password Hash:")

    print(Fore.GREEN + hashed)


# =========================================================
# ENCRYPT MENU
# =========================================================

def encrypt_menu():

    clear()

    title("AES ENCRYPTION")

    data = input(
        Fore.YELLOW +
        "Nhập dữ liệu cần mã hóa: "
    )

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    print(Fore.CYAN +
          "\nĐang mã hóa dữ liệu...")

    time.sleep(1)

    encrypted = encrypt_data(
        data,
        password
    )

    line()

    print(Fore.GREEN + Style.BRIGHT +
          "\nDỮ LIỆU ĐÃ MÃ HÓA\n")

    print(Fore.CYAN +
          encrypted)

    show_password_hash(password)

    # SAVE FILE
    with open(OUTPUT_FILE,
              "w",
              encoding="utf-8") as f:

        f.write(encrypted)

    print(Fore.GREEN +
          f"\nĐã lưu file: {OUTPUT_FILE}")

    line()

    pause()


# =========================================================
# DECRYPT MENU
# =========================================================

def decrypt_menu():

    clear()

    title("AES DECRYPTION")

    encrypted = input(
        Fore.YELLOW +
        "Nhập dữ liệu mã hóa: "
    )

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    print(Fore.CYAN +
          "\nĐang giải mã dữ liệu...")

    time.sleep(1)

    try:

        decrypted = decrypt_data(
            encrypted,
            password
        )

        line()

        print(Fore.GREEN + Style.BRIGHT +
              "\nDỮ LIỆU GIẢI MÃ\n")

        print(Fore.WHITE +
              decrypted)

        line()

    except Exception as e:

        print(Fore.RED +
              "\nGiải mã thất bại!")

        print(Fore.RED +
              "Sai password hoặc dữ liệu lỗi.")

    pause()


# =========================================================
# MÃ HÓA FILE
# =========================================================

def encrypt_file():

    clear()

    title("AES FILE ENCRYPTION")

    filename = input(
        Fore.YELLOW +
        "Nhập file text: "
    )

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    try:

        with open(filename,
                  "r",
                  encoding="utf-8") as f:

            data = f.read()

        encrypted = encrypt_data(
            data,
            password
        )

        output = filename + ".aes"

        with open(output,
                  "w",
                  encoding="utf-8") as f:

            f.write(encrypted)

        print(Fore.GREEN +
              f"\nĐã mã hóa file: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# GIẢI MÃ FILE
# =========================================================

def decrypt_file():

    clear()

    title("AES FILE DECRYPTION")

    filename = input(
        Fore.YELLOW +
        "Nhập file .aes: "
    )

    password = input(
        Fore.YELLOW +
        "Nhập password: "
    )

    try:

        with open(filename,
                  "r",
                  encoding="utf-8") as f:

            encrypted = f.read()

        decrypted = decrypt_data(
            encrypted,
            password
        )

        output = "decrypted_output.txt"

        with open(output,
                  "w",
                  encoding="utf-8") as f:

            f.write(decrypted)

        print(Fore.GREEN +
              f"\nĐã giải mã file: {output}")

    except Exception as e:

        print(Fore.RED +
              "\nGiải mã thất bại!")

        print(Fore.RED + str(e))

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("AES DEMO MODE")

    data = "HELLO AES ENCRYPTION"

    password = "123456"

    print(Fore.WHITE +
          f"\nOriginal Data : {data}")

    print(Fore.WHITE +
          f"Password      : {password}")

    time.sleep(1)

    encrypted = encrypt_data(
        data,
        password
    )

    print(Fore.GREEN +
          "\nEncrypted Data:\n")

    print(Fore.CYAN +
          encrypted)

    time.sleep(1)

    decrypted = decrypt_data(
        encrypted,
        password
    )

    print(Fore.GREEN +
          "\nDecrypted Data:\n")

    print(Fore.WHITE +
          decrypted)

    pause()


# =========================================================
# GIẢI THÍCH AES
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH AES")

    print(Fore.WHITE + """
=========================================================
1. AES LÀ GÌ?
=========================================================

AES:
   Advanced Encryption Standard

=========================================================
2. SYMMETRIC ENCRYPTION
=========================================================

Cùng một key:
   ✓ Encrypt
   ✓ Decrypt

=========================================================
3. AES-256
=========================================================

Khóa:
   256-bit

Rất mạnh:
   ✓ Chính phủ
   ✓ Ngân hàng
   ✓ Military dùng

=========================================================
4. CBC MODE
=========================================================

CBC:
   Cipher Block Chaining

Ưu điểm:
   ✓ An toàn hơn ECB

=========================================================
5. IV
=========================================================

Initialization Vector:
   ✓ Random
   ✓ Tăng bảo mật

=========================================================
6. SALT
=========================================================

Salt dùng để:
   ✓ Chống rainbow table

=========================================================
7. BASE64
=========================================================

Base64 giúp:
   ✓ Hiển thị dữ liệu nhị phân dạng text

=========================================================
8. PBKDF2
=========================================================

PBKDF2:
   ✓ Tạo key mạnh từ password

=========================================================
9. ỨNG DỤNG
=========================================================

✓ HTTPS
✓ VPN
✓ WiFi
✓ Cloud Storage
✓ Secure Messaging
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("AES DATA ENCRYPTION TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu AES
[2] Mã hóa text
[3] Giải mã text
[4] Mã hóa file
[5] Giải mã file
[6] Demo mode
[7] Giải thích AES
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

            encrypt_menu()

        elif choice == '3':

            decrypt_menu()

        elif choice == '4':

            encrypt_file()

        elif choice == '5':

            decrypt_file()

        elif choice == '6':

            demo_mode()

        elif choice == '7':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng AES Encryption Tool.

Kiến thức đạt được:
   ✓ AES-256
   ✓ CBC Mode
   ✓ Encryption
   ✓ Decryption
   ✓ PBKDF2
   ✓ Base64
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
