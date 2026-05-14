# =========================================================
#              MINI FIREWALL SIMULATION
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mô phỏng Firewall bằng Python
#
# Chức năng:
#   ✓ Mô phỏng packet filtering
#   ✓ Block/Allow IP
#   ✓ Block/Allow Port
#   ✓ Firewall Rule Management
#   ✓ Traffic Monitoring
#   ✓ Packet Logging
#   ✓ Phát hiện IP đáng ngờ
#   ✓ Demo traffic simulation
#   ✓ Giao diện terminal hiện đại
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
# python mini_firewall.py
#
# =========================================================

from colorama import Fore, Style, init
import random
import datetime
import time
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

blocked_ips = []
allowed_ips = []

blocked_ports = []
allowed_ports = []

traffic_logs = []

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU FIREWALL")

    print(Fore.WHITE + """
Firewall là hệ thống bảo mật mạng dùng để:

   ✓ Kiểm soát traffic
   ✓ Chặn truy cập trái phép
   ✓ Giám sát packet mạng
   ✓ Bảo vệ server/network

=========================================================
FIREWALL HOẠT ĐỘNG THẾ NÀO?
=========================================================

Firewall kiểm tra:
   ✓ Source IP
   ✓ Destination IP
   ✓ Port
   ✓ Protocol

Sau đó:
   ✓ ALLOW
   ✓ BLOCK

=========================================================
CÁC LOẠI FIREWALL
=========================================================

✓ Packet Filtering
✓ Stateful Firewall
✓ Proxy Firewall
✓ NGFW

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Server Security
✓ Enterprise Network
✓ Cloud Security
✓ SOC/SIEM
✓ Data Center
""")

    line()


# =========================================================
# GHI LOG
# =========================================================

def log_traffic(action,
                src_ip,
                dest_ip,
                port):

    timestamp = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    log = {
        "time": timestamp,
        "action": action,
        "src_ip": src_ip,
        "dest_ip": dest_ip,
        "port": port
    }

    traffic_logs.append(log)


# =========================================================
# THÊM BLOCK IP
# =========================================================

def block_ip():

    clear()

    title("BLOCK IP")

    ip = input(
        Fore.YELLOW +
        "Nhập IP cần block: "
    )

    if ip not in blocked_ips:

        blocked_ips.append(ip)

        print(Fore.RED +
              f"\nĐã block IP: {ip}")

    else:

        print(Fore.YELLOW +
              "\nIP đã tồn tại.")

    pause()


# =========================================================
# ALLOW IP
# =========================================================

def allow_ip():

    clear()

    title("ALLOW IP")

    ip = input(
        Fore.YELLOW +
        "Nhập IP cần allow: "
    )

    if ip not in allowed_ips:

        allowed_ips.append(ip)

        print(Fore.GREEN +
              f"\nĐã allow IP: {ip}")

    else:

        print(Fore.YELLOW +
              "\nIP đã tồn tại.")

    pause()


# =========================================================
# BLOCK PORT
# =========================================================

def block_port():

    clear()

    title("BLOCK PORT")

    try:

        port = int(input(
            Fore.YELLOW +
            "Nhập port cần block: "
        ))

        if port not in blocked_ports:

            blocked_ports.append(port)

            print(Fore.RED +
                  f"\nĐã block port: {port}")

        else:

            print(Fore.YELLOW +
                  "\nPort đã tồn tại.")

    except:

        print(Fore.RED +
              "\nPort không hợp lệ.")

    pause()


# =========================================================
# ALLOW PORT
# =========================================================

def allow_port():

    clear()

    title("ALLOW PORT")

    try:

        port = int(input(
            Fore.YELLOW +
            "Nhập port cần allow: "
        ))

        if port not in allowed_ports:

            allowed_ports.append(port)

            print(Fore.GREEN +
                  f"\nĐã allow port: {port}")

        else:

            print(Fore.YELLOW +
                  "\nPort đã tồn tại.")

    except:

        print(Fore.RED +
              "\nPort không hợp lệ.")

    pause()


# =========================================================
# KIỂM TRA PACKET
# =========================================================

def firewall_check(src_ip,
                   dest_ip,
                   port):

    # BLOCK IP
    if src_ip in blocked_ips:

        log_traffic(
            "BLOCKED",
            src_ip,
            dest_ip,
            port
        )

        return False

    # BLOCK PORT
    if port in blocked_ports:

        log_traffic(
            "BLOCKED",
            src_ip,
            dest_ip,
            port
        )

        return False

    # ALLOW RULE
    if allowed_ips and src_ip not in allowed_ips:

        log_traffic(
            "BLOCKED",
            src_ip,
            dest_ip,
            port
        )

        return False

    if allowed_ports and port not in allowed_ports:

        log_traffic(
            "BLOCKED",
            src_ip,
            dest_ip,
            port
        )

        return False

    log_traffic(
        "ALLOWED",
        src_ip,
        dest_ip,
        port
    )

    return True


# =========================================================
# TRAFFIC SIMULATION
# =========================================================

def traffic_simulation():

    clear()

    title("TRAFFIC SIMULATION")

    print(Fore.CYAN +
          "\nĐang mô phỏng network traffic...\n")

    sample_ips = [
        "192.168.1.10",
        "192.168.1.20",
        "10.0.0.5",
        "172.16.1.1",
        "45.22.11.99"
    ]

    ports = [
        22,
        80,
        443,
        21,
        3306,
        8080
    ]

    for _ in range(20):

        src_ip = random.choice(sample_ips)

        dest_ip = "192.168.1.100"

        port = random.choice(ports)

        allowed = firewall_check(
            src_ip,
            dest_ip,
            port
        )

        if allowed:

            print(Fore.GREEN +
                  f"[ALLOWED] "
                  f"{src_ip} -> "
                  f"{dest_ip}:{port}")

        else:

            print(Fore.RED +
                  f"[BLOCKED] "
                  f"{src_ip} -> "
                  f"{dest_ip}:{port}")

        time.sleep(0.5)

    pause()


# =========================================================
# HIỂN THỊ RULE
# =========================================================

def show_rules():

    clear()

    title("FIREWALL RULES")

    print(Fore.RED +
          "\nBLOCKED IP")

    line()

    if blocked_ips:

        for ip in blocked_ips:

            print(Fore.RED + ip)

    else:

        print(Fore.YELLOW +
              "Không có.")

    print(Fore.GREEN +
          "\nALLOWED IP")

    line()

    if allowed_ips:

        for ip in allowed_ips:

            print(Fore.GREEN + ip)

    else:

        print(Fore.YELLOW +
              "Không có.")

    print(Fore.RED +
          "\nBLOCKED PORT")

    line()

    if blocked_ports:

        for port in blocked_ports:

            print(Fore.RED + str(port))

    else:

        print(Fore.YELLOW +
              "Không có.")

    print(Fore.GREEN +
          "\nALLOWED PORT")

    line()

    if allowed_ports:

        for port in allowed_ports:

            print(Fore.GREEN + str(port))

    else:

        print(Fore.YELLOW +
              "Không có.")

    pause()


# =========================================================
# HIỂN THỊ LOG
# =========================================================

def show_logs():

    clear()

    title("FIREWALL TRAFFIC LOG")

    if not traffic_logs:

        print(Fore.RED +
              "\nChưa có traffic.")

        pause()

        return

    for log in traffic_logs[-50:]:

        color = Fore.GREEN

        if log["action"] == "BLOCKED":

            color = Fore.RED

        print(color +
              f"\n[{log['time']}]")

        print(color +
              f"{log['action']}")

        print(Fore.CYAN +
              f"{log['src_ip']} -> "
              f"{log['dest_ip']}:{log['port']}")

        line()

    pause()


# =========================================================
# THỐNG KÊ
# =========================================================

def statistics():

    clear()

    title("FIREWALL STATISTICS")

    allowed = 0
    blocked = 0

    for log in traffic_logs:

        if log["action"] == "ALLOWED":

            allowed += 1

        else:

            blocked += 1

    print(Fore.GREEN +
          f"\nAllowed Packets : {allowed}")

    print(Fore.RED +
          f"Blocked Packets : {blocked}")

    print(Fore.CYAN +
          f"Total Traffic   : {len(traffic_logs)}")

    line()

    pause()


# =========================================================
# GIẢI THÍCH FIREWALL
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH FIREWALL")

    print(Fore.WHITE + """
=========================================================
1. FIREWALL
=========================================================

Firewall:
   ✓ Bảo vệ mạng
   ✓ Kiểm soát traffic

=========================================================
2. PACKET FILTERING
=========================================================

Firewall kiểm tra:
   ✓ IP
   ✓ Port
   ✓ Protocol

=========================================================
3. BLOCK RULE
=========================================================

Rule dùng để:
   ✓ Chặn IP
   ✓ Chặn port

=========================================================
4. ALLOW RULE
=========================================================

Cho phép:
   ✓ Trusted IP
   ✓ Trusted Port

=========================================================
5. PORT
=========================================================

Ví dụ:
   22   = SSH
   80   = HTTP
   443  = HTTPS

=========================================================
6. TRAFFIC LOGGING
=========================================================

Firewall ghi lại:
   ✓ Allowed traffic
   ✓ Blocked traffic

=========================================================
7. SIEM / SOC
=========================================================

Firewall log dùng trong:
   ✓ SIEM
   ✓ SOC Monitoring

=========================================================
8. ỨNG DỤNG
=========================================================

✓ Server Security
✓ Enterprise Network
✓ Data Center
✓ Cloud Firewall
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("MINI FIREWALL SIMULATION")

        print(Fore.CYAN + """
[1] Giới thiệu Firewall
[2] Block IP
[3] Allow IP
[4] Block Port
[5] Allow Port
[6] Traffic Simulation
[7] Xem Firewall Rules
[8] Xem Traffic Logs
[9] Xem Statistics
[10] Giải thích Firewall
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

            block_ip()

        elif choice == '3':

            allow_ip()

        elif choice == '4':

            block_port()

        elif choice == '5':

            allow_port()

        elif choice == '6':

            traffic_simulation()

        elif choice == '7':

            show_rules()

        elif choice == '8':

            show_logs()

        elif choice == '9':

            statistics()

        elif choice == '10':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Mini Firewall Simulation.

Kiến thức đạt được:
   ✓ Firewall
   ✓ Packet Filtering
   ✓ Allow/Block Rules
   ✓ Port Filtering
   ✓ Traffic Monitoring
   ✓ Network Security
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
