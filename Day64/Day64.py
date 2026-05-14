# =========================================================
#              WIFI ANALYZER ĐƠN GIẢN - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : WiFi Analyzer
#
# Chức năng:
#   ✓ Quét mạng WiFi xung quanh
#   ✓ Hiển thị SSID
#   ✓ Hiển thị Signal Strength
#   ✓ Hiển thị BSSID
#   ✓ Hiển thị Channel
#   ✓ Hiển thị Security
#   ✓ Đánh giá chất lượng WiFi
#   ✓ Giao diện terminal hiện đại
#   ✓ Demo mode an toàn
#
# =========================================================
# HỖ TRỢ HỆ ĐIỀU HÀNH
# =========================================================
#
# ✓ Windows
# ✓ Linux
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
# python wifi_analyzer.py
#
# =========================================================

from colorama import Fore, Style, init
import subprocess
import platform
import random
import time
import os
import re

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

    title("GIỚI THIỆU WIFI ANALYZER")

    print(Fore.WHITE + """
WiFi Analyzer là công cụ dùng để:

   ✓ Quét WiFi xung quanh
   ✓ Phân tích tín hiệu WiFi
   ✓ Kiểm tra độ mạnh sóng
   ✓ Kiểm tra channel WiFi
   ✓ Kiểm tra bảo mật WiFi

=========================================================
THÔNG TIN HIỂN THỊ
=========================================================

✓ SSID
✓ BSSID
✓ Signal Strength
✓ Channel
✓ Security

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Tối ưu WiFi
✓ Chọn channel tốt
✓ Debug WiFi
✓ Network Monitoring
✓ Học Wireless Networking

=========================================================
LƯU Ý
=========================================================

Chương trình:
   ✓ Chỉ đọc thông tin public
   ✓ Không hack WiFi
   ✓ Không truy cập trái phép
""")

    line()


# =========================================================
# ĐÁNH GIÁ TÍN HIỆU
# =========================================================

def signal_quality(signal):

    if signal >= 80:
        return "RẤT MẠNH"

    elif signal >= 60:
        return "TỐT"

    elif signal >= 40:
        return "TRUNG BÌNH"

    else:
        return "YẾU"


# =========================================================
# VẼ THANH SÓNG
# =========================================================

def draw_signal_bar(signal):

    bars = int(signal / 5)

    return "█" * bars


# =========================================================
# QUÉT WIFI WINDOWS
# =========================================================

def scan_windows():

    wifi_list = []

    try:

        output = subprocess.check_output(
            ["netsh", "wlan", "show", "networks",
             "mode=bssid"],
            encoding="utf-8",
            errors="ignore"
        )

        ssids = re.findall(r"SSID\s\d+\s:\s(.*)", output)

        signals = re.findall(r"Signal\s+:\s(\d+)%", output)

        channels = re.findall(r"Channel\s+:\s(\d+)", output)

        auths = re.findall(r"Authentication\s+:\s(.*)", output)

        for i in range(len(ssids)):

            wifi = {
                "ssid": ssids[i].strip(),
                "signal": int(signals[i]) if i < len(signals) else 0,
                "channel": channels[i] if i < len(channels) else "?",
                "security": auths[i] if i < len(auths) else "Unknown",
                "bssid": "N/A"
            }

            wifi_list.append(wifi)

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi scan WiFi:\n{e}")

    return wifi_list


# =========================================================
# QUÉT WIFI LINUX
# =========================================================

def scan_linux():

    wifi_list = []

    try:

        output = subprocess.check_output(
            ["nmcli", "-f",
             "SSID,SIGNAL,CHAN,SECURITY",
             "device", "wifi"],
            encoding="utf-8"
        )

        lines = output.split("\n")[1:]

        for line_data in lines:

            if line_data.strip():

                parts = line_data.split()

                if len(parts) >= 4:

                    ssid = parts[0]

                    signal = int(parts[-3])

                    channel = parts[-2]

                    security = parts[-1]

                    wifi = {
                        "ssid": ssid,
                        "signal": signal,
                        "channel": channel,
                        "security": security,
                        "bssid": "N/A"
                    }

                    wifi_list.append(wifi)

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi scan WiFi:\n{e}")

    return wifi_list


# =========================================================
# HIỂN THỊ WIFI
# =========================================================

def display_wifi_list(wifi_list):

    clear()

    title("KẾT QUẢ PHÂN TÍCH WIFI")

    if not wifi_list:

        print(Fore.RED +
              "\nKhông tìm thấy WiFi.")

        pause()

        return

    for index, wifi in enumerate(wifi_list, start=1):

        quality = signal_quality(
            wifi["signal"]
        )

        line()

        print(Fore.GREEN +
              f"\n[{index}] {wifi['ssid']}")

        print(Fore.CYAN +
              f"BSSID   : {wifi['bssid']}")

        print(Fore.YELLOW +
              f"Signal  : {wifi['signal']}%")

        print(Fore.GREEN +
              f"Quality : {quality}")

        print(Fore.WHITE +
              f"Channel : {wifi['channel']}")

        print(Fore.MAGENTA +
              f"Security: {wifi['security']}")

        print(Fore.GREEN +
              "\nSignal Bar:")

        print(draw_signal_bar(
            wifi["signal"]
        ))

    line()

    print(Fore.GREEN + Style.BRIGHT +
          f"\nTìm thấy {len(wifi_list)} mạng WiFi")

    pause()


# =========================================================
# WIFI SCAN THẬT
# =========================================================

def real_scan():

    system = platform.system().lower()

    if system == "windows":

        wifi_list = scan_windows()

    elif system == "linux":

        wifi_list = scan_linux()

    else:

        print(Fore.RED +
              "\nHệ điều hành chưa hỗ trợ.")

        pause()

        return

    display_wifi_list(wifi_list)


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO WIFI ANALYZER")

    fake_wifi = [
        {
            "ssid": "Home_WiFi",
            "signal": 92,
            "channel": 6,
            "security": "WPA2",
            "bssid": "AA:BB:CC:11:22:33"
        },

        {
            "ssid": "Coffee_Shop",
            "signal": 55,
            "channel": 11,
            "security": "Open",
            "bssid": "DD:EE:FF:44:55:66"
        },

        {
            "ssid": "Office_Network",
            "signal": 74,
            "channel": 1,
            "security": "WPA3",
            "bssid": "77:88:99:AA:BB:CC"
        }
    ]

    display_wifi_list(fake_wifi)


# =========================================================
# GIẢI THÍCH WIFI
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH WIFI ANALYZER")

    print(Fore.WHITE + """
=========================================================
1. SSID
=========================================================

SSID là tên mạng WiFi.

Ví dụ:
   ✓ Home_WiFi
   ✓ CoffeeShop

=========================================================
2. BSSID
=========================================================

BSSID là MAC Address của Access Point.

Ví dụ:
   AA:BB:CC:11:22:33

=========================================================
3. SIGNAL STRENGTH
=========================================================

Độ mạnh tín hiệu WiFi.

100%:
   ✓ Sóng mạnh

0%:
   ✓ Không có sóng

=========================================================
4. CHANNEL
=========================================================

WiFi hoạt động trên channel.

2.4GHz:
   ✓ Channel 1-13

5GHz:
   ✓ Nhiều channel hơn

=========================================================
5. SECURITY
=========================================================

Các loại bảo mật:
   ✓ WPA2
   ✓ WPA3
   ✓ Open

=========================================================
6. WIFI INTERFERENCE
=========================================================

Nhiều WiFi cùng channel:
   ✓ Gây nhiễu

=========================================================
7. ỨNG DỤNG WIFI ANALYZER
=========================================================

✓ Chọn channel tốt
✓ Kiểm tra sóng WiFi
✓ Debug mạng
✓ Monitoring
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("WIFI ANALYZER TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu WiFi Analyzer
[2] Quét WiFi thật
[3] Demo mode
[4] Giải thích chi tiết
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

            real_scan()

        elif choice == '3':

            demo_mode()

        elif choice == '4':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng WiFi Analyzer.

Kiến thức đạt được:
   ✓ SSID
   ✓ BSSID
   ✓ Signal Strength
   ✓ Channel
   ✓ WiFi Security
   ✓ Wireless Networking
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
