# =========================================================
#            NETWORK LOG ANALYZER - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Log Analyzer cho hệ thống mạng
#
# Chức năng:
#   ✓ Phân tích log mạng
#   ✓ Tìm ERROR / WARNING
#   ✓ Thống kê IP truy cập
#   ✓ Thống kê mức độ log
#   ✓ Tìm top IP xuất hiện nhiều
#   ✓ Tìm hoạt động bất thường
#   ✓ Xuất báo cáo
#   ✓ Giao diện terminal hiện đại
#   ✓ Demo mode tích hợp
#
# =========================================================
# HỖ TRỢ LOG
# =========================================================
#
# ✓ Syslog
# ✓ Firewall log
# ✓ Router log
# ✓ Server log
# ✓ Apache/Nginx log
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
# python log_analyzer.py
#
# =========================================================

from colorama import Fore, Style, init
from collections import Counter
import re
import os
import time
import random
import datetime

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

REPORT_FILE = "network_report.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU NETWORK LOG ANALYZER")

    print(Fore.WHITE + """
Log Analyzer là công cụ dùng để:

   ✓ Phân tích log hệ thống mạng
   ✓ Tìm lỗi hệ thống
   ✓ Theo dõi hoạt động mạng
   ✓ Phát hiện truy cập bất thường
   ✓ Giám sát bảo mật

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ SIEM
✓ SOC Monitoring
✓ Firewall Analysis
✓ Server Monitoring
✓ Cyber Security
✓ DevOps

=========================================================
THÔNG TIN PHÂN TÍCH
=========================================================

✓ ERROR
✓ WARNING
✓ INFO
✓ IP Address
✓ Failed Login
✓ Traffic Statistics

=========================================================
LOG PHỔ BIẾN
=========================================================

✓ Syslog
✓ Apache Access Log
✓ Nginx Log
✓ Firewall Log
✓ Router Log
""")

    line()


# =========================================================
# LOAD FILE LOG
# =========================================================

def load_log_file():

    global loaded_logs

    clear()

    title("LOAD LOG FILE")

    filename = input(
        Fore.YELLOW +
        "Nhập đường dẫn file log: "
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

    ips = [
        "192.168.1.10",
        "192.168.1.20",
        "10.0.0.5",
        "172.16.0.8",
        "8.8.8.8"
    ]

    levels = [
        "INFO",
        "WARNING",
        "ERROR"
    ]

    messages = [
        "User login success",
        "Connection timeout",
        "Firewall blocked packet",
        "Port scan detected",
        "DNS request",
        "Failed SSH login",
        "High bandwidth usage"
    ]

    loaded_logs.clear()

    for _ in range(100):

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        ip = random.choice(ips)

        level = random.choice(levels)

        message = random.choice(messages)

        log = (
            f"{timestamp} "
            f"{level} "
            f"{ip} "
            f"{message}"
        )

        loaded_logs.append(log)

    print(Fore.GREEN +
          "\nĐã tạo demo log thành công.")

    pause()


# =========================================================
# THỐNG KÊ LOG LEVEL
# =========================================================

def analyze_log_levels():

    clear()

    title("PHÂN TÍCH LOG LEVEL")

    if not loaded_logs:

        print(Fore.RED +
              "\nChưa có log.")

        pause()

        return

    levels = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in loaded_logs:

        for level in levels:

            if level in log:
                levels[level] += 1

    line()

    for level, count in levels.items():

        color = Fore.GREEN

        if level == "WARNING":
            color = Fore.YELLOW

        elif level == "ERROR":
            color = Fore.RED

        print(color +
              f"{level:<10}: {count}")

    line()

    pause()


# =========================================================
# PHÂN TÍCH IP
# =========================================================

def analyze_ips():

    clear()

    title("PHÂN TÍCH IP ADDRESS")

    if not loaded_logs:

        print(Fore.RED +
              "\nChưa có log.")

        pause()

        return

    ip_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'

    ips = []

    for log in loaded_logs:

        found = re.findall(ip_pattern, log)

        ips.extend(found)

    counter = Counter(ips)

    line()

    print(Fore.GREEN +
          "\nTOP IP XUẤT HIỆN NHIỀU\n")

    for ip, count in counter.most_common(10):

        print(Fore.CYAN +
              f"{ip:<20} {count} lần")

    line()

    pause()


# =========================================================
# TÌM ERROR
# =========================================================

def find_errors():

    clear()

    title("TÌM ERROR LOG")

    found = False

    for log in loaded_logs:

        if "ERROR" in log:

            print(Fore.RED + log)

            found = True

    if not found:

        print(Fore.GREEN +
              "\nKhông có ERROR.")

    pause()


# =========================================================
# TÌM WARNING
# =========================================================

def find_warning():

    clear()

    title("TÌM WARNING LOG")

    found = False

    for log in loaded_logs:

        if "WARNING" in log:

            print(Fore.YELLOW + log)

            found = True

    if not found:

        print(Fore.GREEN +
              "\nKhông có WARNING.")

    pause()


# =========================================================
# PHÁT HIỆN BẤT THƯỜNG
# =========================================================

def detect_suspicious():

    clear()

    title("PHÁT HIỆN HOẠT ĐỘNG BẤT THƯỜNG")

    keywords = [
        "failed",
        "blocked",
        "scan",
        "timeout"
    ]

    found = False

    for log in loaded_logs:

        lower = log.lower()

        for keyword in keywords:

            if keyword in lower:

                print(Fore.RED + log)

                found = True

                break

    if not found:

        print(Fore.GREEN +
              "\nKhông phát hiện bất thường.")

    pause()


# =========================================================
# XUẤT BÁO CÁO
# =========================================================

def export_report():

    clear()

    title("XUẤT BÁO CÁO")

    if not loaded_logs:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

        pause()

        return

    try:

        with open(REPORT_FILE,
                  "w",
                  encoding="utf-8") as f:

            f.write("NETWORK LOG REPORT\n")
            f.write("=" * 50 + "\n\n")

            f.write(
                f"Tổng log: {len(loaded_logs)}\n\n"
            )

            # LEVEL COUNT
            levels = {
                "INFO": 0,
                "WARNING": 0,
                "ERROR": 0
            }

            for log in loaded_logs:

                for level in levels:

                    if level in log:
                        levels[level] += 1

            f.write("LOG LEVEL STATISTICS\n")

            for level, count in levels.items():

                f.write(f"{level}: {count}\n")

            f.write("\n")

            # IP COUNT
            ip_pattern = r'(?:\d{1,3}\.){3}\d{1,3}'

            ips = []

            for log in loaded_logs:

                found = re.findall(
                    ip_pattern,
                    log
                )

                ips.extend(found)

            counter = Counter(ips)

            f.write("TOP IP ADDRESS\n")

            for ip, count in counter.most_common(10):

                f.write(f"{ip}: {count}\n")

        print(Fore.GREEN +
              f"\nĐã xuất báo cáo: {REPORT_FILE}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi xuất report:\n{e}")

    pause()


# =========================================================
# HIỂN THỊ LOG
# =========================================================

def show_logs():

    clear()

    title("HIỂN THỊ LOG")

    if not loaded_logs:

        print(Fore.RED +
              "\nChưa có log.")

    else:

        for log in loaded_logs[:50]:

            if "ERROR" in log:

                print(Fore.RED + log)

            elif "WARNING" in log:

                print(Fore.YELLOW + log)

            else:

                print(Fore.GREEN + log)

    pause()


# =========================================================
# GIẢI THÍCH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH LOG ANALYZER")

    print(Fore.WHITE + """
=========================================================
1. LOG LÀ GÌ?
=========================================================

Log là dữ liệu ghi lại hoạt động hệ thống.

=========================================================
2. INFO
=========================================================

Thông tin hoạt động bình thường.

=========================================================
3. WARNING
=========================================================

Cảnh báo:
   ✓ Có thể có vấn đề

=========================================================
4. ERROR
=========================================================

Lỗi hệ thống:
   ✓ Kết nối lỗi
   ✓ Timeout
   ✓ Authentication fail

=========================================================
5. IP ADDRESS
=========================================================

Địa chỉ thiết bị mạng.

Ví dụ:
   192.168.1.1

=========================================================
6. SUSPICIOUS ACTIVITY
=========================================================

Hoạt động đáng ngờ:
   ✓ Port scan
   ✓ Failed login
   ✓ Firewall block

=========================================================
7. SIEM
=========================================================

SIEM:
   Security Information and Event Management

Dùng để:
   ✓ Giám sát bảo mật
   ✓ Phân tích log
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("NETWORK LOG ANALYZER")

        print(Fore.CYAN + """
[1] Giới thiệu Log Analyzer
[2] Load file log
[3] Tạo demo log
[4] Hiển thị log
[5] Phân tích log level
[6] Phân tích IP
[7] Tìm ERROR
[8] Tìm WARNING
[9] Phát hiện bất thường
[10] Xuất báo cáo
[11] Giải thích chi tiết
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

            analyze_log_levels()

        elif choice == '6':

            analyze_ips()

        elif choice == '7':

            find_errors()

        elif choice == '8':

            find_warning()

        elif choice == '9':

            detect_suspicious()

        elif choice == '10':

            export_report()

        elif choice == '11':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Network Log Analyzer.

Kiến thức đạt được:
   ✓ Log Analysis
   ✓ Error Detection
   ✓ IP Analysis
   ✓ Suspicious Activity
   ✓ SIEM Concepts
   ✓ Network Monitoring
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
