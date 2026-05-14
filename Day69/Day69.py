# =========================================================
#          BRUTE-FORCE LOG DETECTION TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Phát hiện brute-force từ log hệ thống
#
# Chức năng:
#   ✓ Phân tích log đăng nhập
#   ✓ Phát hiện brute-force attack
#   ✓ Phân tích IP đáng ngờ
#   ✓ Thống kê failed login
#   ✓ Cảnh báo IP nguy hiểm
#   ✓ Tìm top attacker IP
#   ✓ Xuất báo cáo bảo mật
#   ✓ Demo mode tích hợp
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# LOG HỖ TRỢ
# =========================================================
#
# ✓ SSH Log
# ✓ Linux Auth Log
# ✓ Apache Login Log
# ✓ FTP Log
# ✓ Windows Login Log
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
# python brute_force_detector.py
#
# =========================================================

from colorama import Fore, Style, init
from collections import Counter
import re
import random
import datetime
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
# BIẾN TOÀN CỤC
# =========================================================

loaded_logs = []

REPORT_FILE = "security_report.txt"

FAILED_KEYWORDS = [
    "failed",
    "invalid",
    "authentication failure",
    "login failed",
    "access denied"
]

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU BRUTE-FORCE DETECTOR")

    print(Fore.WHITE + """
Brute-force Detector là công cụ dùng để:

   ✓ Phát hiện tấn công brute-force
   ✓ Phân tích failed login
   ✓ Giám sát bảo mật hệ thống
   ✓ Tìm IP đáng ngờ
   ✓ Hỗ trợ SOC/SIEM

=========================================================
BRUTE-FORCE ATTACK LÀ GÌ?
=========================================================

Là hình thức:
   ✓ Thử password liên tục
   ✓ Đoán tài khoản
   ✓ Tấn công SSH/FTP/Web Login

=========================================================
DẤU HIỆU NHẬN BIẾT
=========================================================

✓ Nhiều failed login
✓ Một IP thử nhiều lần
✓ Login bất thường

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ SOC Monitoring
✓ SIEM
✓ Server Security
✓ Blue Team
✓ Incident Response
""")

    line()


# =========================================================
# LOAD FILE LOG
# =========================================================

def load_log_file():

    global loaded_logs

    clear()

    title("LOAD SECURITY LOG")

    filename = input(
        Fore.YELLOW +
        "Nhập file log: "
    )

    try:

        with open(filename,
                  "r",
                  encoding="utf-8",
                  errors="ignore") as f:

            loaded_logs = f.readlines()

        print(Fore.GREEN +
              f"\nĐã load "
              f"{len(loaded_logs)} dòng log.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi đọc file:\n{e}")

    pause()


# =========================================================
# DEMO LOG
# =========================================================

def generate_demo_logs():

    global loaded_logs

    loaded_logs.clear()

    ips = [
        "192.168.1.10",
        "192.168.1.20",
        "45.12.22.11",
        "103.55.77.88",
        "8.8.8.8"
    ]

    messages = [
        "Failed password for admin",
        "Invalid login attempt",
        "Authentication failure",
        "Access denied",
        "Login success"
    ]

    for _ in range(120):

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        ip = random.choice(ips)

        # Tăng xác suất brute-force
        if random.randint(1, 100) <= 70:

            message = random.choice(
                messages[:-1]
            )

        else:

            message = "Login success"

        log = (
            f"{timestamp} "
            f"{ip} "
            f"{message}"
        )

        loaded_logs.append(log)

    print(Fore.GREEN +
          "\nĐã tạo demo security log.")

    pause()


# =========================================================
# HIỂN THỊ LOG
# =========================================================

def show_logs():

    clear()

    title("HIỂN THỊ SECURITY LOG")

    if not loaded_logs:

        print(Fore.RED +
              "\nChưa có log.")

        pause()

        return

    for log in loaded_logs[:100]:

        lower = log.lower()

        if any(k in lower for k in FAILED_KEYWORDS):

            print(Fore.RED + log)

        else:

            print(Fore.GREEN + log)

    pause()


# =========================================================
# PHÂN TÍCH FAILED LOGIN
# =========================================================

def analyze_failed_login():

    clear()

    title("PHÂN TÍCH FAILED LOGIN")

    failed_count = 0

    for log in loaded_logs:

        lower = log.lower()

        if any(k in lower for k in FAILED_KEYWORDS):

            failed_count += 1

            print(Fore.RED + log)

    line()

    print(Fore.YELLOW +
          f"\nTổng failed login: {failed_count}")

    pause()


# =========================================================
# TOP ATTACKER IP
# =========================================================

def top_attacker_ips():

    clear()

    title("TOP ATTACKER IP")

    ip_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'

    attacker_ips = []

    for log in loaded_logs:

        lower = log.lower()

        if any(k in lower for k in FAILED_KEYWORDS):

            ips = re.findall(
                ip_pattern,
                log
            )

            attacker_ips.extend(ips)

    counter = Counter(attacker_ips)

    line()

    print(Fore.RED +
          "\nTOP IP ĐÁNG NGỜ\n")

    for ip, count in counter.most_common(10):

        color = Fore.GREEN

        if count >= 10:
            color = Fore.RED

        elif count >= 5:
            color = Fore.YELLOW

        print(color +
              f"{ip:<20} "
              f"{count} failed attempts")

    line()

    pause()


# =========================================================
# PHÁT HIỆN BRUTE-FORCE
# =========================================================

def detect_bruteforce():

    clear()

    title("PHÁT HIỆN BRUTE-FORCE")

    ip_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'

    attacker_ips = []

    for log in loaded_logs:

        lower = log.lower()

        if any(k in lower for k in FAILED_KEYWORDS):

            ips = re.findall(
                ip_pattern,
                log
            )

            attacker_ips.extend(ips)

    counter = Counter(attacker_ips)

    found = False

    for ip, count in counter.items():

        if count >= 5:

            found = True

            print(Fore.RED +
                  Style.BRIGHT +
                  f"\n⚠ BRUTE-FORCE DETECTED")

            print(Fore.YELLOW +
                  f"IP Address : {ip}")

            print(Fore.RED +
                  f"Attempts   : {count}")

            if count >= 20:

                print(Fore.RED +
                      "Risk Level : CRITICAL")

            elif count >= 10:

                print(Fore.YELLOW +
                      "Risk Level : HIGH")

            else:

                print(Fore.CYAN +
                      "Risk Level : MEDIUM")

            line()

    if not found:

        print(Fore.GREEN +
              "\nKhông phát hiện brute-force.")

    pause()


# =========================================================
# XUẤT BÁO CÁO
# =========================================================

def export_report():

    clear()

    title("XUẤT SECURITY REPORT")

    try:

        ip_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'

        attacker_ips = []

        failed_count = 0

        for log in loaded_logs:

            lower = log.lower()

            if any(k in lower for k in FAILED_KEYWORDS):

                failed_count += 1

                ips = re.findall(
                    ip_pattern,
                    log
                )

                attacker_ips.extend(ips)

        counter = Counter(attacker_ips)

        with open(REPORT_FILE,
                  "w",
                  encoding="utf-8") as f:

            f.write("SECURITY REPORT\n")
            f.write("=" * 50 + "\n\n")

            f.write(
                f"Tổng log: {len(loaded_logs)}\n"
            )

            f.write(
                f"Failed login: {failed_count}\n\n"
            )

            f.write("TOP ATTACKER IP\n\n")

            for ip, count in counter.most_common(10):

                f.write(
                    f"{ip} : "
                    f"{count} attempts\n"
                )

        print(Fore.GREEN +
              f"\nĐã xuất report: {REPORT_FILE}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# GIẢI THÍCH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH BRUTE-FORCE DETECTION")

    print(Fore.WHITE + """
=========================================================
1. BRUTE-FORCE ATTACK
=========================================================

Kẻ tấn công:
   ✓ Thử nhiều password
   ✓ Đoán tài khoản

=========================================================
2. FAILED LOGIN
=========================================================

Là login thất bại.

Ví dụ:
   ✓ Sai password
   ✓ Sai username

=========================================================
3. INDICATORS OF ATTACK
=========================================================

✓ Nhiều failed login
✓ Một IP thử liên tục
✓ Login bất thường

=========================================================
4. SIEM
=========================================================

SIEM:
   Security Information and Event Management

=========================================================
5. SOC
=========================================================

SOC:
   Security Operation Center

=========================================================
6. RISK LEVEL
=========================================================

LOW:
   ✓ Ít failed login

HIGH:
   ✓ Nhiều failed login

CRITICAL:
   ✓ Brute-force mạnh

=========================================================
7. CÁCH PHÒNG CHỐNG
=========================================================

✓ MFA
✓ Strong Password
✓ Fail2Ban
✓ Firewall
✓ Account Lockout

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Linux SSH Security
✓ Web Login Protection
✓ SIEM Monitoring
✓ Incident Response
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("BRUTE-FORCE LOG DETECTOR")

        print(Fore.CYAN + """
[1] Giới thiệu Brute-force Detector
[2] Load file log
[3] Tạo demo log
[4] Hiển thị log
[5] Phân tích failed login
[6] Top attacker IP
[7] Phát hiện brute-force
[8] Xuất security report
[9] Giải thích chi tiết
[0] Thoát
""")

        print(Fore.GREEN +
              f"\nLoaded Logs: {len(loaded_logs)}")

        choice = input(
            Fore.YELLOW +
            "\nNhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            load_log_file()

        elif choice == '3':

            generate_demo_logs()

        elif choice == '4':

            show_logs()

        elif choice == '5':

            analyze_failed_login()

        elif choice == '6':

            top_attacker_ips()

        elif choice == '7':

            detect_bruteforce()

        elif choice == '8':

            export_report()

        elif choice == '9':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Brute-force Detector.

Kiến thức đạt được:
   ✓ Brute-force Attack
   ✓ Failed Login Analysis
   ✓ SIEM Concepts
   ✓ SOC Monitoring
   ✓ Security Analysis
   ✓ Incident Detection
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
