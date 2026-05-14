# =========================================================
#        MÔ PHỎNG TCP/IP CƠ BẢN HIỆN ĐẠI - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : TCP/IP Network Simulator
#
# Chức năng:
#   ✓ Giới thiệu TCP/IP
#   ✓ Mô phỏng gửi packet
#   ✓ Mô phỏng TCP 3-Way Handshake
#   ✓ Mô phỏng IP Address
#   ✓ Mô phỏng Port
#   ✓ Mô phỏng Router
#   ✓ Mô phỏng ACK
#   ✓ Mô phỏng mất packet
#   ✓ Hiển thị packet trực quan
#   ✓ Giao diện terminal hiện đại
#
# Yêu cầu:
#   pip install colorama
#
# Chạy:
#   python tcpip_simulator.py
#
# =========================================================

from colorama import Fore, Style, init
import random
import time
import os

init(autoreset=True)

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print(Fore.CYAN + "=" * 90)


def title(text):
    line()
    print(Fore.GREEN + Style.BRIGHT + text.center(90))
    line()


def pause():
    input(Fore.YELLOW + "\nNhấn ENTER để tiếp tục...")


def loading(text="Đang xử lý"):
    for i in range(3):
        print(Fore.YELLOW + f"{text}{'.' * (i+1)}")
        time.sleep(0.4)


# =========================================================
# GIỚI THIỆU TCP/IP
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU TCP/IP")

    print(Fore.WHITE + """
TCP/IP là bộ giao thức mạng quan trọng nhất hiện nay.

Nó là nền tảng của:
   ✓ Internet
   ✓ WiFi
   ✓ LAN
   ✓ Website
   ✓ Email
   ✓ Cloud Computing
   ✓ IoT
   ✓ Game Online

=========================================================
1. TCP (Transmission Control Protocol)
=========================================================

Nhiệm vụ:
   ✓ Đảm bảo dữ liệu đến đúng
   ✓ Kiểm tra lỗi
   ✓ Gửi lại packet bị mất
   ✓ Đúng thứ tự dữ liệu

TCP là giao thức:
   ✓ Tin cậy
   ✓ Có ACK
   ✓ Có Handshake

=========================================================
2. IP (Internet Protocol)
=========================================================

Nhiệm vụ:
   ✓ Định tuyến dữ liệu
   ✓ Xác định địa chỉ thiết bị

Ví dụ IP:
   192.168.1.10

=========================================================
3. TCP/IP STACK
=========================================================

   Application Layer
   Transport Layer (TCP)
   Internet Layer (IP)
   Network Access Layer

=========================================================
4. TCP 3-WAY HANDSHAKE
=========================================================

   Client ---- SYN ----> Server
   Client <-- SYN-ACK -- Server
   Client ---- ACK ----> Server

Sau đó mới truyền dữ liệu.
""")

    line()


# =========================================================
# TẠO IP
# =========================================================

def generate_ip():

    return ".".join(
        str(random.randint(1, 254))
        for _ in range(4)
    )


# =========================================================
# PACKET TCP/IP
# =========================================================

class Packet:

    def __init__(
        self,
        source_ip,
        dest_ip,
        source_port,
        dest_port,
        data,
        seq,
        ack,
        flag
    ):

        self.source_ip = source_ip
        self.dest_ip = dest_ip

        self.source_port = source_port
        self.dest_port = dest_port

        self.data = data

        self.seq = seq
        self.ack = ack

        self.flag = flag

    def display(self):

        print(Fore.GREEN + Style.BRIGHT +
              "\nTCP/IP PACKET")

        line()

        print(Fore.CYAN + f"Source IP     : {self.source_ip}")
        print(Fore.CYAN + f"Destination IP: {self.dest_ip}")

        print(Fore.YELLOW + f"Source Port   : {self.source_port}")
        print(Fore.YELLOW + f"Dest Port     : {self.dest_port}")

        print(Fore.WHITE + f"Sequence      : {self.seq}")
        print(Fore.WHITE + f"ACK           : {self.ack}")

        print(Fore.MAGENTA + f"Flag          : {self.flag}")

        print(Fore.GREEN + f"Data          : {self.data}")

        line()


# =========================================================
# THIẾT BỊ MẠNG
# =========================================================

class Device:

    def __init__(self, name):

        self.name = name
        self.ip = generate_ip()

    def info(self):

        print(Fore.GREEN +
              f"{self.name} - IP: {self.ip}")


# =========================================================
# TCP HANDSHAKE
# =========================================================

def tcp_handshake(client, server):

    clear()

    title("TCP 3-WAY HANDSHAKE")

    print(Fore.WHITE +
          f"\nClient: {client.ip}")

    print(Fore.WHITE +
          f"Server: {server.ip}")

    print()

    # STEP 1
    print(Fore.CYAN +
          "[1] Client gửi SYN")

    syn = Packet(
        client.ip,
        server.ip,
        5000,
        80,
        "SYN REQUEST",
        seq=100,
        ack=0,
        flag="SYN"
    )

    syn.display()

    time.sleep(1)

    # STEP 2
    print(Fore.YELLOW +
          "\n[2] Server trả SYN-ACK")

    syn_ack = Packet(
        server.ip,
        client.ip,
        80,
        5000,
        "SYN-ACK RESPONSE",
        seq=200,
        ack=101,
        flag="SYN-ACK"
    )

    syn_ack.display()

    time.sleep(1)

    # STEP 3
    print(Fore.GREEN +
          "\n[3] Client gửi ACK")

    ack = Packet(
        client.ip,
        server.ip,
        5000,
        80,
        "ACK",
        seq=101,
        ack=201,
        flag="ACK"
    )

    ack.display()

    print(Fore.GREEN + Style.BRIGHT +
          "\nKẾT NỐI TCP ĐÃ THIẾT LẬP THÀNH CÔNG")

    pause()


# =========================================================
# GỬI DỮ LIỆU TCP
# =========================================================

def send_data(client, server):

    clear()

    title("MÔ PHỎNG GỬI DỮ LIỆU TCP")

    message = input(
        Fore.YELLOW +
        "Nhập dữ liệu cần gửi: "
    )

    seq = random.randint(1000, 5000)

    packet = Packet(
        client.ip,
        server.ip,
        5000,
        80,
        message,
        seq,
        0,
        "PSH-ACK"
    )

    loading("Đang đóng gói packet")

    packet.display()

    print(Fore.CYAN +
          "\nĐang truyền packet qua router...")

    time.sleep(1)

    # Mô phỏng packet loss
    packet_loss = random.randint(1, 100)

    if packet_loss <= 25:

        print(Fore.RED + Style.BRIGHT +
              "\nPACKET BỊ MẤT!")

        print(Fore.YELLOW +
              "\nTCP sẽ gửi lại packet...")

        time.sleep(2)

        print(Fore.GREEN +
              "\nPacket retransmission SUCCESS")

    else:

        print(Fore.GREEN +
              "\nPacket đến server thành công")

    time.sleep(1)

    # ACK
    ack_packet = Packet(
        server.ip,
        client.ip,
        80,
        5000,
        "ACK RESPONSE",
        seq=9999,
        ack=seq + len(message),
        flag="ACK"
    )

    print(Fore.YELLOW +
          "\nServer gửi ACK")

    ack_packet.display()

    print(Fore.GREEN + Style.BRIGHT +
          "\nTRUYỀN DỮ LIỆU THÀNH CÔNG")

    pause()


# =========================================================
# MÔ PHỎNG ROUTER
# =========================================================

def router_simulation():

    clear()

    title("MÔ PHỎNG ROUTER")

    routers = [
        "Router A",
        "Router B",
        "Router C",
        "Router D"
    ]

    print(Fore.CYAN +
          "\nDữ liệu sẽ đi qua các router:\n")

    for router in routers:

        print(Fore.GREEN +
              f"Đang đi qua: {router}")

        time.sleep(1)

    print(Fore.GREEN + Style.BRIGHT +
          "\nPACKET ĐÃ ĐẾN ĐÍCH")

    pause()


# =========================================================
# GIẢI THÍCH TCP/IP
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH TCP/IP CHI TIẾT")

    print(Fore.WHITE + """
=========================================================
1. TCP
=========================================================

TCP đảm bảo:
   ✓ Đúng dữ liệu
   ✓ Đúng thứ tự
   ✓ Không mất dữ liệu

Cơ chế:
   ✓ Sequence Number
   ✓ ACK
   ✓ Retransmission

=========================================================
2. IP
=========================================================

IP giúp:
   ✓ Xác định địa chỉ
   ✓ Định tuyến packet

Ví dụ:
   8.8.8.8

=========================================================
3. PORT
=========================================================

Port dùng để xác định ứng dụng.

Ví dụ:
   80   = HTTP
   443  = HTTPS
   21   = FTP
   22   = SSH

=========================================================
4. PACKET
=========================================================

Packet gồm:
   ✓ Header
   ✓ Payload

=========================================================
5. ROUTER
=========================================================

Router định tuyến packet.

Packet có thể đi qua:
   ✓ Nhiều router
   ✓ Nhiều quốc gia
   ✓ Nhiều ISP

=========================================================
6. TCP ƯU ĐIỂM
=========================================================

✓ Tin cậy
✓ Kiểm tra lỗi
✓ Tự gửi lại

=========================================================
7. TCP NHƯỢC ĐIỂM
=========================================================

✗ Chậm hơn UDP
✗ Overhead cao

=========================================================
8. UDP KHÁC TCP
=========================================================

UDP:
   ✓ Nhanh
   ✗ Không đảm bảo dữ liệu

Ứng dụng:
   ✓ Livestream
   ✓ Game Online
   ✓ Voice Call
""")

    pause()


# =========================================================
# DEMO TỰ ĐỘNG
# =========================================================

def auto_demo():

    clear()

    title("AUTO DEMO TCP/IP")

    client = Device("CLIENT")
    server = Device("SERVER")

    print(Fore.GREEN +
          "\nTạo thiết bị thành công")

    client.info()
    server.info()

    time.sleep(1)

    # HANDSHAKE
    print(Fore.CYAN +
          "\nĐang thực hiện handshake...")

    time.sleep(1)

    print(Fore.GREEN +
          "\nSYN")

    time.sleep(1)

    print(Fore.YELLOW +
          "SYN-ACK")

    time.sleep(1)

    print(Fore.GREEN +
          "ACK")

    time.sleep(1)

    print(Fore.GREEN + Style.BRIGHT +
          "\nTCP CONNECTED")

    # Gửi packet
    packet = Packet(
        client.ip,
        server.ip,
        5000,
        80,
        "HELLO TCP/IP",
        1000,
        0,
        "PSH-ACK"
    )

    packet.display()

    print(Fore.CYAN +
          "\nPacket đang đi qua mạng...")

    time.sleep(2)

    print(Fore.GREEN +
          "\nServer nhận packet thành công")

    print(Fore.YELLOW +
          "\nServer gửi ACK")

    time.sleep(1)

    print(Fore.GREEN + Style.BRIGHT +
          "\nDEMO HOÀN TẤT")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    client = Device("CLIENT")
    server = Device("SERVER")

    while True:

        clear()

        title("TCP/IP NETWORK SIMULATOR")

        print(Fore.CYAN + """
[1] Giới thiệu TCP/IP
[2] Mô phỏng TCP Handshake
[3] Mô phỏng gửi dữ liệu TCP
[4] Mô phỏng Router
[5] Giải thích TCP/IP chi tiết
[6] Demo tự động
[0] Thoát
""")

        print(Fore.GREEN +
              f"\nClient IP : {client.ip}")

        print(Fore.GREEN +
              f"Server IP : {server.ip}")

        choice = input(
            Fore.YELLOW +
            "\nNhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            tcp_handshake(client, server)

        elif choice == '3':

            send_data(client, server)

        elif choice == '4':

            router_simulation()

        elif choice == '5':

            explain()

        elif choice == '6':

            auto_demo()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng TCP/IP Simulator.

Kiến thức đạt được:
   ✓ TCP hoạt động thế nào
   ✓ TCP Handshake
   ✓ ACK
   ✓ Packet
   ✓ Router
   ✓ IP Address
   ✓ Port
   ✓ Packet Loss
   ✓ Retransmission
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
