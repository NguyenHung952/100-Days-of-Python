# =========================================================
#            LOCAL NETWORK SCANNER - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Network Scanner Nội Bộ
#
# Chức năng:
#   ✓ Quét IP trong mạng LAN
#   ✓ Kiểm tra host online/offline
#   ✓ Scan port phổ biến
#   ✓ Hiển thị hostname
#   ✓ Hiển thị thời gian phản hồi
#   ✓ Giao diện terminal hiện đại
#   ✓ Thống kê thiết bị
#   ✓ Chế độ demo an toàn
#   ✓ Hoạt động Windows/Linux/Mac
#
# =========================================================
# YÊU CẦU
# =========================================================
#
# pip install colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python network_scanner.py
#
# =========================================================

from colorama import Fore, Style, init
import socket
import subprocess
import platform
import threading
import queue
import time
import random
import ipaddress
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

online_hosts = []
scan_count = 0

COMMON_PORTS = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-ALT"
}

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU NETWORK SCANNER")

    print(Fore.WHITE + """
Network Scanner là công cụ dùng để:

   ✓ Quét thiết bị trong mạng LAN
   ✓ Kiểm tra host online
   ✓ Kiểm tra port mở
   ✓ Kiểm tra dịch vụ mạng
   ✓ Học về networking

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Quản trị mạng
✓ Cyber Security
✓ Pentest nội bộ
✓ Kiểm tra server
✓ Giám sát hệ thống

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Ping Scan
✓ Port Scan
✓ Host Discovery
✓ Hostname Lookup

=========================================================
LƯU Ý
=========================================================

Chỉ sử dụng:
   ✓ Mạng của bạn
   ✓ Môi trường học tập
   ✓ Lab nội bộ

Không scan trái phép hệ thống người khác.
""")

    line()


# =========================================================
# LẤY LOCAL IP
# =========================================================

def get_local_ip():

    try:

        s = socket.socket(socket.AF_INET,
                          socket.SOCK_DGRAM)

        s.connect(("8.8.8.8", 80))

        ip = s.getsockname()[0]

        s.close()

        return ip

    except:

        return "127.0.0.1"


# =========================================================
# PING HOST
# =========================================================

def ping_host(ip):

    global scan_count

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", ip]

    try:

        start = time.time()

        output = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        response_time = round(
            (time.time() - start) * 1000,
            2
        )

        scan_count += 1

        if output.returncode == 0:

            try:

                hostname = socket.gethostbyaddr(ip)[0]

            except:

                hostname = "Unknown"

            online_hosts.append({
                "ip": ip,
                "hostname": hostname,
                "response": response_time
            })

            print(Fore.GREEN +
                  f"[ONLINE] {ip:<15} "
                  f"{hostname:<30} "
                  f"{response_time} ms")

    except:
        pass


# =========================================================
# PORT SCAN
# =========================================================

def scan_port(ip, port):

    try:

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.5)

        result = sock.connect_ex((ip, port))

        sock.close()

        if result == 0:

            service = COMMON_PORTS.get(
                port,
                "Unknown"
            )

            print(Fore.GREEN +
                  f"Port {port:<5} OPEN "
                  f"({service})")

    except:
        pass


# =========================================================
# QUÉT PORT
# =========================================================

def port_scan():

    clear()

    title("PORT SCANNER")

    ip = input(Fore.YELLOW +
               "Nhập IP cần scan: ")

    print(Fore.CYAN +
          "\nĐang scan port...\n")

    for port in COMMON_PORTS:

        scan_port(ip, port)

    line()

    pause()


# =========================================================
# QUÉT MẠNG LAN
# =========================================================

def network_scan():

    clear()

    title("NETWORK SCAN")

    local_ip = get_local_ip()

    print(Fore.GREEN +
          f"\nLocal IP: {local_ip}")

    network = ".".join(local_ip.split(".")[:-1]) + "."

    print(Fore.CYAN +
          f"Network: {network}0/24")

    print(Fore.YELLOW +
          "\nĐang quét mạng...\n")

    threads = []

    for i in range(1, 255):

        ip = network + str(i)

        t = threading.Thread(
            target=ping_host,
            args=(ip,)
        )

        threads.append(t)

        t.start()

    for t in threads:
        t.join()

    line()

    print(Fore.GREEN + Style.BRIGHT +
          f"\nTìm thấy {len(online_hosts)} host online")

    line()

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO NETWORK SCANNER")

    fake_devices = [
        ("192.168.1.1", "Router"),
        ("192.168.1.5", "Laptop"),
        ("192.168.1.10", "Smart TV"),
        ("192.168.1.15", "ESP32"),
        ("192.168.1.20", "Printer")
    ]

    print(Fore.CYAN +
          "\nĐang mô phỏng scan mạng...\n")

    time.sleep(1)

    for ip, device in fake_devices:

        response = round(
            random.uniform(1, 20),
            2
        )

        print(Fore.GREEN +
              f"[ONLINE] {ip:<15} "
              f"{device:<20} "
              f"{response} ms")

        time.sleep(0.7)

    line()

    print(Fore.GREEN + Style.BRIGHT +
          f"\nTìm thấy {len(fake_devices)} thiết bị")

    pause()


# =========================================================
# HIỂN THỊ HOST ONLINE
# =========================================================

def show_hosts():

    clear()

    title("DANH SÁCH HOST ONLINE")

    if not online_hosts:

        print(Fore.RED +
              "\nChưa có dữ liệu scan.")

    else:

        for index, host in enumerate(online_hosts, start=1):

            print(Fore.GREEN +
                  f"\n[{index}]")

            print(Fore.CYAN +
                  f"IP       : {host['ip']}")

            print(Fore.YELLOW +
                  f"Hostname : {host['hostname']}")

            print(Fore.WHITE +
                  f"Response : {host['response']} ms")

            line()

    pause()


# =========================================================
# GIẢI THÍCH CHI TIẾT
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH NETWORK SCANNER")

    print(Fore.WHITE + """
=========================================================
1. NETWORK SCANNING
=========================================================

Là quá trình:
   ✓ Tìm thiết bị trong mạng
   ✓ Kiểm tra host hoạt động

=========================================================
2. PING
=========================================================

Ping dùng ICMP.

Nếu host trả lời:
   ✓ Host online

=========================================================
3. PORT SCAN
=========================================================

Port scan kiểm tra:
   ✓ Dịch vụ đang mở

Ví dụ:
   80   = HTTP
   443  = HTTPS
   22   = SSH

=========================================================
4. HOSTNAME
=========================================================

Hostname là tên thiết bị.

Ví dụ:
   ✓ DESKTOP-PC
   ✓ SERVER01

=========================================================
5. SOCKET
=========================================================

Socket giúp:
   ✓ Kết nối mạng
   ✓ Kiểm tra port

=========================================================
6. THREADING
=========================================================

Thread giúp:
   ✓ Scan nhanh hơn
   ✓ Quét song song

=========================================================
7. RESPONSE TIME
=========================================================

Là thời gian phản hồi host.

Đơn vị:
   ms (milliseconds)

=========================================================
8. ỨNG DỤNG
=========================================================

✓ Network Admin
✓ Cyber Security
✓ Monitoring
✓ Device Discovery
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("LOCAL NETWORK SCANNER")

        print(Fore.CYAN + """
[1] Giới thiệu Network Scanner
[2] Scan mạng LAN thật
[3] Scan port
[4] Xem host online
[5] Demo mode
[6] Giải thích chi tiết
[0] Thoát
""")

        print(Fore.GREEN +
              f"\nLocal IP: {get_local_ip()}")

        choice = input(
            Fore.YELLOW +
            "\nNhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            online_hosts.clear()

            network_scan()

        elif choice == '3':

            port_scan()

        elif choice == '4':

            show_hosts()

        elif choice == '5':

            demo_mode()

        elif choice == '6':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Network Scanner.

Kiến thức đạt được:
   ✓ Ping Scan
   ✓ Port Scan
   ✓ Host Discovery
   ✓ Socket Programming
   ✓ Threading
   ✓ TCP/IP Networking
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
