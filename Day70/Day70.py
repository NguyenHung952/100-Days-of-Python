# =========================================================
#              OTP AUTHENTICATION SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Hệ thống xác thực OTP bằng Python
#
# Chức năng:
#   ✓ Sinh OTP ngẫu nhiên
#   ✓ OTP hết hạn theo thời gian
#   ✓ Xác thực OTP
#   ✓ Giới hạn số lần nhập sai
#   ✓ OTP dạng số hoặc chữ
#   ✓ Mô phỏng gửi OTP Email/SMS
#   ✓ Lưu lịch sử OTP
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
# python otp_system.py
#
# =========================================================

from colorama import Fore, Style, init
import secrets
import string
import time
import datetime
import hashlib
import os

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
# BIẾN TOÀN CỤC
# =========================================================

current_otp = None
otp_expire = None
otp_attempts = 0

MAX_ATTEMPTS = 3

OTP_HISTORY_FILE = "otp_history.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU OTP AUTHENTICATION")

    print(Fore.WHITE + """
OTP = One Time Password

OTP là mã xác thực chỉ dùng 1 lần.

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Banking
✓ Facebook
✓ Google
✓ Email
✓ MFA/2FA
✓ E-commerce

=========================================================
OTP GIÚP
=========================================================

✓ Tăng bảo mật
✓ Chống đánh cắp tài khoản
✓ Chống brute-force
✓ Xác thực người dùng

=========================================================
CÁC LOẠI OTP
=========================================================

✓ SMS OTP
✓ Email OTP
✓ App OTP
✓ Time-based OTP

=========================================================
CHƯƠNG TRÌNH HỖ TRỢ
=========================================================

✓ Generate OTP
✓ Verify OTP
✓ OTP Expiration
✓ OTP Retry Limit
✓ OTP Logging
""")

    line()


# =========================================================
# GHI LOG
# =========================================================

def write_log(text):

    with open(OTP_HISTORY_FILE,
              "a",
              encoding="utf-8") as f:

        f.write(text + "\n")


# =========================================================
# SINH OTP
# =========================================================

def generate_otp(length=6,
                 otp_type="number"):

    if otp_type == "number":

        chars = string.digits

    elif otp_type == "alpha":

        chars = string.ascii_uppercase

    else:

        chars = (
            string.ascii_uppercase +
            string.digits
        )

    otp = ''.join(
        secrets.choice(chars)
        for _ in range(length)
    )

    return otp


# =========================================================
# HASH OTP
# =========================================================

def hash_otp(otp):

    return hashlib.sha256(
        otp.encode()
    ).hexdigest()


# =========================================================
# TẠO OTP
# =========================================================

def create_otp():

    global current_otp
    global otp_expire
    global otp_attempts

    clear()

    title("SINH OTP")

    try:

        length = int(input(
            Fore.YELLOW +
            "Độ dài OTP: "
        ))

    except:

        print(Fore.RED +
              "\nĐộ dài không hợp lệ.")

        pause()

        return

    print(Fore.CYAN + """
1. OTP số
2. OTP chữ
3. OTP hỗn hợp
""")

    choice = input(
        Fore.YELLOW +
        "Chọn loại OTP: "
    )

    if choice == '1':

        otp_type = "number"

    elif choice == '2':

        otp_type = "alpha"

    else:

        otp_type = "mixed"

    otp = generate_otp(
        length,
        otp_type
    )

    current_otp = otp

    otp_attempts = 0

    expire_seconds = 60

    otp_expire = time.time() + expire_seconds

    clear()

    title("OTP GENERATED")

    print(Fore.GREEN + Style.BRIGHT +
          f"\nOTP: {otp}")

    print(Fore.YELLOW +
          f"Hết hạn sau: {expire_seconds} giây")

    print(Fore.CYAN +
          f"OTP Hash: {hash_otp(otp)}")

    # LOG
    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    write_log(
        f"[{timestamp}] OTP Generated: {otp}"
    )

    print(Fore.GREEN +
          f"\nĐã lưu log: {OTP_HISTORY_FILE}")

    pause()


# =========================================================
# VERIFY OTP
# =========================================================

def verify_otp():

    global current_otp
    global otp_attempts

    clear()

    title("XÁC THỰC OTP")

    if current_otp is None:

        print(Fore.RED +
              "\nChưa tạo OTP.")

        pause()

        return

    # CHECK EXPIRE
    if time.time() > otp_expire:

        print(Fore.RED +
              "\nOTP đã hết hạn!")

        current_otp = None

        pause()

        return

    while otp_attempts < MAX_ATTEMPTS:

        user_otp = input(
            Fore.YELLOW +
            "\nNhập OTP: "
        )

        otp_attempts += 1

        if user_otp == current_otp:

            print(Fore.GREEN +
                  Style.BRIGHT +
                  "\n✓ OTP CHÍNH XÁC")

            timestamp = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            write_log(
                f"[{timestamp}] OTP VERIFIED SUCCESS"
            )

            current_otp = None

            pause()

            return

        else:

            remaining = MAX_ATTEMPTS - otp_attempts

            print(Fore.RED +
                  "\n✗ OTP SAI")

            print(Fore.YELLOW +
                  f"Còn {remaining} lần thử")

    print(Fore.RED +
          Style.BRIGHT +
          "\nOTP BỊ KHÓA!")

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    write_log(
        f"[{timestamp}] OTP FAILED"
    )

    current_otp = None

    pause()


# =========================================================
# MÔ PHỎNG GỬI OTP
# =========================================================

def send_otp_simulation():

    clear()

    title("MÔ PHỎNG GỬI OTP")

    if current_otp is None:

        print(Fore.RED +
              "\nChưa tạo OTP.")

        pause()

        return

    target = input(
        Fore.YELLOW +
        "Nhập Email/SĐT giả lập: "
    )

    print(Fore.CYAN +
          "\nĐang gửi OTP...")

    time.sleep(2)

    print(Fore.GREEN +
          f"\nĐã gửi OTP tới: {target}")

    print(Fore.YELLOW +
          "(Mô phỏng - không gửi thật)")

    pause()


# =========================================================
# KIỂM TRA OTP STATUS
# =========================================================

def otp_status():

    clear()

    title("OTP STATUS")

    if current_otp is None:

        print(Fore.RED +
              "\nKhông có OTP active.")

    else:

        remaining = int(
            otp_expire - time.time()
        )

        if remaining < 0:
            remaining = 0

        print(Fore.GREEN +
              f"\nOTP hiện tại: {current_otp}")

        print(Fore.YELLOW +
              f"Còn hạn: {remaining} giây")

        print(Fore.CYAN +
              f"Số lần thử: {otp_attempts}/{MAX_ATTEMPTS}")

    pause()


# =========================================================
# XEM LOG
# =========================================================

def view_logs():

    clear()

    title("OTP LOG HISTORY")

    if not os.path.exists(OTP_HISTORY_FILE):

        print(Fore.RED +
              "\nChưa có log.")

    else:

        with open(OTP_HISTORY_FILE,
                  "r",
                  encoding="utf-8") as f:

            content = f.read()

            print(Fore.GREEN +
                  "\n" + content)

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("OTP DEMO MODE")

    otp = generate_otp(
        6,
        "mixed"
    )

    print(Fore.GREEN +
          f"\nGenerated OTP: {otp}")

    print(Fore.CYAN +
          f"OTP Hash: {hash_otp(otp)}")

    print(Fore.YELLOW +
          "\nMô phỏng gửi OTP...")

    time.sleep(2)

    print(Fore.GREEN +
          "OTP Sent Successfully")

    pause()


# =========================================================
# GIẢI THÍCH OTP
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH OTP AUTHENTICATION")

    print(Fore.WHITE + """
=========================================================
1. OTP LÀ GÌ?
=========================================================

OTP:
   One Time Password

=========================================================
2. OTP DÙNG ĐỂ
=========================================================

✓ Xác thực người dùng
✓ MFA/2FA
✓ Tăng bảo mật

=========================================================
3. OTP EXPIRATION
=========================================================

OTP chỉ dùng trong thời gian ngắn.

Ví dụ:
   ✓ 30 giây
   ✓ 60 giây

=========================================================
4. MFA / 2FA
=========================================================

MFA:
   Multi-Factor Authentication

=========================================================
5. BRUTE-FORCE PROTECTION
=========================================================

Giới hạn số lần nhập OTP.

=========================================================
6. HASHING
=========================================================

SHA256 dùng để:
   ✓ Bảo vệ OTP

=========================================================
7. SMS / EMAIL OTP
=========================================================

OTP thường gửi qua:
   ✓ SMS
   ✓ Email
   ✓ Authenticator App

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Banking
✓ Google Authenticator
✓ Facebook
✓ E-commerce
✓ VPN Login
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("OTP AUTHENTICATION SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu OTP
[2] Sinh OTP
[3] Xác thực OTP
[4] Mô phỏng gửi OTP
[5] Kiểm tra OTP status
[6] Xem OTP log
[7] Demo mode
[8] Giải thích OTP
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

            create_otp()

        elif choice == '3':

            verify_otp()

        elif choice == '4':

            send_otp_simulation()

        elif choice == '5':

            otp_status()

        elif choice == '6':

            view_logs()

        elif choice == '7':

            demo_mode()

        elif choice == '8':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng OTP Authentication System.

Kiến thức đạt được:
   ✓ OTP
   ✓ MFA / 2FA
   ✓ OTP Expiration
   ✓ Authentication
   ✓ Brute-force Protection
   ✓ SHA256 Hashing
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
