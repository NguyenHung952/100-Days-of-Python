# =========================================================
#                PING MONITOR TOOL - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Ping Monitor & Network Latency Tool
#
# Chức năng:
#   ✓ Ping liên tục tới host
#   ✓ Theo dõi độ trễ mạng (Latency)
#   ✓ Theo dõi Packet Loss
#   ✓ Hiển thị trạng thái ONLINE/OFFLINE
#   ✓ Biểu đồ realtime terminal
#   ✓ Lưu log ping
#   ✓ Thống kê MIN/MAX/AVG
#   ✓ Giao diện terminal hiện đại
#   ✓ Hỗ trợ Windows/Linux/Mac
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
# python ping_monitor.py
#
# =========================================================

from colorama import Fore, Style, init
import subprocess
import platform
import time
import statistics
import datetime
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

ping_history = []

total_sent = 0
total_received = 0
total_lost = 0

log_file = "ping_logs.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU PING MONITOR TOOL")

    print(Fore.WHITE + """
Ping Monitor là công cụ dùng để:

   ✓ Kiểm tra kết nối mạng
   ✓ Theo dõi độ ổn định Internet
   ✓ Theo dõi latency
   ✓ Kiểm tra packet loss
   ✓ Giám sát server/network

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Network Monitoring
✓ Game Ping Check
✓ Server Monitoring
✓ ISP Troubleshooting
✓ DevOps
✓ Cyber Security

=========================================================
THÔNG TIN HIỂN THỊ
=========================================================

✓ Response Time (ms)
✓ Packet Loss
✓ ONLINE/OFFLINE
✓ Average Ping
✓ Max/Min Ping

=========================================================
PING HOẠT ĐỘNG THẾ NÀO?
=========================================================

Ping dùng giao thức ICMP:

   Client ---- ICMP Request ----> Host
   Client <-- ICMP Reply  ------- Host

Nếu host phản hồi:
   ✓ ONLINE

Nếu không phản hồi:
   ✓ OFFLINE
""")

    line()


# =========================================================
# GHI LOG
# =========================================================

def write_log(text):

    with open(log_file, "a", encoding="utf-8") as f:

        f.write(text + "\n")


# =========================================================
# PARSE PING TIME
# =========================================================

def extract_ping_time(output):

    keywords = ["time=", "time<", "TTL="]

    output = output.lower()

    try:

        if "time=" in output:

            part = output.split("time=")[1]

            value = ""

            for char in part:

                if char.isdigit() or char == '.':
                    value += char
                else:
                    break

            return float(value)

        elif "time<" in output:

            return 1.0

    except:
        pass

    return None


# =========================================================
# PING HOST
# =========================================================

def ping_host(host):

    global total_sent
    global total_received
    global total_lost

    system = platform.system().lower()

    param = "-n" if system == "windows" else "-c"

    command = ["ping", param, "1", host]

    total_sent += 1

    start = time.time()

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    elapsed = round((time.time() - start) * 1000, 2)

    timestamp = datetime.datetime.now().strftime(
        "%H:%M:%S"
    )

    if result.returncode == 0:

        total_received += 1

        ping_time = extract_ping_time(
            result.stdout
        )

        if ping_time is None:
            ping_time = elapsed

        ping_history.append(ping_time)

        log = (f"[{timestamp}] "
               f"ONLINE | {host} | "
               f"{ping_time} ms")

        write_log(log)

        return True, ping_time

    else:

        total_lost += 1

        log = (f"[{timestamp}] "
               f"OFFLINE | {host}")

        write_log(log)

        return False, None


# =========================================================
# THỐNG KÊ
# =========================================================

def statistics_info():

    if not ping_history:
        return None

    return {
        "min": round(min(ping_history), 2),
        "max": round(max(ping_history), 2),
        "avg": round(statistics.mean(ping_history), 2)
    }


# =========================================================
# BIỂU ĐỒ TERMINAL
# =========================================================

def draw_chart(ping):

    bars = int(min(ping / 2, 50))

    print(Fore.GREEN +
          "█" * bars +
          Fore.WHITE +
          f" {ping} ms")


# =========================================================
# MONITOR MODE
# =========================================================

def monitor():

    clear()

    title("PING MONITOR")

    host = input(
        Fore.YELLOW +
        "Nhập IP hoặc domain: "
    )

    interval = input(
        Fore.YELLOW +
        "Khoảng thời gian ping (giây): "
    )

    try:
        interval = float(interval)
    except:
        interval = 1

    clear()

    title("ĐANG GIÁM SÁT MẠNG")

    print(Fore.GREEN +
          f"\nTarget: {host}")

    print(Fore.YELLOW +
          f"Interval: {interval}s")

    print(Fore.CYAN +
          f"Log file: {log_file}")

    print(Fore.RED +
          "\nNhấn CTRL + C để dừng.\n")

    try:

        while True:

            online, ping = ping_host(host)

            timestamp = datetime.datetime.now().strftime(
                "%H:%M:%S"
            )

            if online:

                print(Fore.GREEN +
                      f"[{timestamp}] "
                      f"ONLINE  "
                      f"{ping} ms")

                draw_chart(ping)

            else:

                print(Fore.RED +
                      f"[{timestamp}] "
                      f"OFFLINE")

            stats = statistics_info()

            if stats:

                loss = round(
                    (total_lost / total_sent) * 100,
                    2
                )

                print(Fore.CYAN +
                      f"\nMIN={stats['min']} ms | "
                      f"MAX={stats['max']} ms | "
                      f"AVG={stats['avg']} ms | "
                      f"LOSS={loss}%")

            line()

            time.sleep(interval)

    except KeyboardInterrupt:

        print_summary()

        pause()


# =========================================================
# TỔNG KẾT
# =========================================================

def print_summary():

    clear()

    title("PING SUMMARY")

    print(Fore.GREEN +
          f"\nPackets Sent     : {total_sent}")

    print(Fore.GREEN +
          f"Packets Received : {total_received}")

    print(Fore.RED +
          f"Packets Lost     : {total_lost}")

    if total_sent > 0:

        loss = round(
            (total_lost / total_sent) * 100,
            2
        )

        print(Fore.YELLOW +
              f"Packet Loss      : {loss}%")

    stats = statistics_info()

    if stats:

        print(Fore.CYAN +
              f"\nMinimum Ping : {stats['min']} ms")

        print(Fore.CYAN +
              f"Maximum Ping : {stats['max']} ms")

        print(Fore.CYAN +
              f"Average Ping : {stats['avg']} ms")

    line()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    import random

    clear()

    title("DEMO MODE")

    print(Fore.CYAN +
          "\nĐang mô phỏng ping monitor...\n")

    for i in range(10):

        fake_ping = round(
            random.uniform(5, 120),
            2
        )

        print(Fore.GREEN +
              f"[ONLINE] google.com "
              f"{fake_ping} ms")

        draw_chart(fake_ping)

        time.sleep(0.7)

    print(Fore.GREEN +
          "\nDemo hoàn tất.")

    pause()


# =========================================================
# GIẢI THÍCH CHI TIẾT
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH PING MONITOR")

    print(Fore.WHITE + """
=========================================================
1. PING
=========================================================

Ping là công cụ kiểm tra:
   ✓ Kết nối mạng
   ✓ Độ trễ
   ✓ Packet loss

=========================================================
2. ICMP
=========================================================

Ping dùng giao thức:
   ICMP

=========================================================
3. LATENCY
=========================================================

Latency là thời gian phản hồi.

Đơn vị:
   milliseconds (ms)

=========================================================
4. PACKET LOSS
=========================================================

Packet loss là packet bị mất.

Ví dụ:
   ✓ Mạng yếu
   ✓ WiFi lỗi
   ✓ ISP lỗi

=========================================================
5. RESPONSE TIME
=========================================================

Ping thấp:
   ✓ Mạng tốt

Ping cao:
   ✓ Lag
   ✓ Mạng chậm

=========================================================
6. ỨNG DỤNG
=========================================================

✓ Monitoring
✓ Gaming
✓ Server Check
✓ Internet Test
✓ Network Debugging

=========================================================
7. SOCKET & ICMP
=========================================================

Hệ điều hành xử lý ICMP packet.

Lệnh ping:
   ✓ Gửi ICMP Echo Request
   ✓ Nhận ICMP Echo Reply
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("PING MONITOR TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu Ping Monitor
[2] Bắt đầu Monitor
[3] Demo mode
[4] Xem thống kê hiện tại
[5] Giải thích chi tiết
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

            monitor()

        elif choice == '3':

            demo_mode()

        elif choice == '4':

            print_summary()

            pause()

        elif choice == '5':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Ping Monitor Tool.

Kiến thức đạt được:
   ✓ Ping hoạt động thế nào
   ✓ ICMP
   ✓ Packet Loss
   ✓ Latency
   ✓ Network Monitoring
   ✓ Real-time Monitoring
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
