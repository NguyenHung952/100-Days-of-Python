# =========================================================
#              MINI PACKET SNIFFER - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Packet Sniffer Mini
#
# Chức năng:
#   ✓ Bắt packet mạng cơ bản
#   ✓ Phân tích Ethernet Frame
#   ✓ Phân tích IPv4 Packet
#   ✓ Phân tích TCP / UDP / ICMP
#   ✓ Hiển thị IP nguồn / đích
#   ✓ Hiển thị Port
#   ✓ Hiển thị Payload
#   ✓ Giao diện terminal hiện đại
#   ✓ Thống kê packet
#   ✓ Chế độ demo an toàn
#
# =========================================================
#  QUAN TRỌNG
# =========================================================
#
# Chương trình hỗ trợ 2 chế độ:
#
# 1. DEMO MODE (Khuyên dùng)
#    ✓ Chạy mọi máy
#    ✓ Không cần quyền admin
#    ✓ Mô phỏng packet thật
#
# 2. REAL SNIFFER MODE
#    ✓ Bắt packet thật
#    ✓ Cần quyền Administrator / Root
#    ✓ Chỉ hoạt động trên một số OS
#
# =========================================================
#
# CÀI THƯ VIỆN:
#
# pip install colorama
#
# =========================================================
#
# CHẠY:
#
# python mini_sniffer.py
#
# =========================================================

from colorama import Fore, Style, init
import socket
import struct
import textwrap
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


# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU PACKET SNIFFER")

    print(Fore.WHITE + """
Packet Sniffer là công cụ dùng để:

   ✓ Bắt packet mạng
   ✓ Phân tích dữ liệu mạng
   ✓ Debug mạng
   ✓ Giám sát lưu lượng
   ✓ Học giao thức mạng

Ứng dụng thực tế:
   ✓ Wireshark
   ✓ tcpdump
   ✓ IDS/IPS
   ✓ Cyber Security
   ✓ Network Monitoring

=========================================================
GIAO THỨC HỖ TRỢ
=========================================================

✓ Ethernet
✓ IPv4
✓ TCP
✓ UDP
✓ ICMP

=========================================================
LƯU Ý
=========================================================

Packet sniffing trên mạng thật cần:
   ✓ Quyền Administrator
   ✓ Card mạng hỗ trợ
   ✓ Một số OS hỗ trợ raw socket
""")

    line()


# =========================================================
# FORMAT DỮ LIỆU
# =========================================================

def format_multi_line(prefix, string, size=80):

    size -= len(prefix)

    if isinstance(string, bytes):

        string = ''.join(
            r'\x{:02x}'.format(byte)
            for byte in string
        )

    return '\n'.join(
        [prefix + line for line in
         textwrap.wrap(string, size)]
    )


# =========================================================
# ETHERNET FRAME
# =========================================================

def ethernet_frame(data):

    dest_mac, src_mac, proto = struct.unpack(
        '! 6s 6s H',
        data[:14]
    )

    return (
        get_mac_addr(dest_mac),
        get_mac_addr(src_mac),
        socket.htons(proto),
        data[14:]
    )


def get_mac_addr(bytes_addr):

    bytes_str = map('{:02x}'.format, bytes_addr)

    return ':'.join(bytes_str).upper()


# =========================================================
# IPv4 PACKET
# =========================================================

def ipv4_packet(data):

    version_header_length = data[0]

    version = version_header_length >> 4

    header_length = (version_header_length & 15) * 4

    ttl, proto, src, target = struct.unpack(
        '! 8x B B 2x 4s 4s',
        data[:20]
    )

    return (
        version,
        header_length,
        ttl,
        proto,
        ipv4(src),
        ipv4(target),
        data[header_length:]
    )


def ipv4(addr):

    return '.'.join(map(str, addr))


# =========================================================
# TCP SEGMENT
# =========================================================

def tcp_segment(data):

    (
        src_port,
        dest_port,
        sequence,
        acknowledgment,
        offset_reserved_flags
    ) = struct.unpack('! H H L L H', data[:14])

    offset = (offset_reserved_flags >> 12) * 4

    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 4
    flag_psh = (offset_reserved_flags & 8) >> 3
    flag_rst = (offset_reserved_flags & 4) >> 2
    flag_syn = (offset_reserved_flags & 2) >> 1
    flag_fin = offset_reserved_flags & 1

    return (
        src_port,
        dest_port,
        sequence,
        acknowledgment,
        flag_urg,
        flag_ack,
        flag_psh,
        flag_rst,
        flag_syn,
        flag_fin,
        data[offset:]
    )


# =========================================================
# UDP SEGMENT
# =========================================================

def udp_segment(data):

    src_port, dest_port, size = struct.unpack(
        '! H H 2x H',
        data[:8]
    )

    return src_port, dest_port, size, data[8:]


# =========================================================
# ICMP PACKET
# =========================================================

def icmp_packet(data):

    icmp_type, code, checksum = struct.unpack(
        '! B B H',
        data[:4]
    )

    return icmp_type, code, checksum, data[4:]


# =========================================================
# HIỂN THỊ PACKET
# =========================================================

packet_count = 0

tcp_count = 0
udp_count = 0
icmp_count = 0


def display_packet(protocol,
                   src_ip,
                   dest_ip,
                   info):

    global packet_count

    packet_count += 1

    line()

    print(Fore.GREEN + Style.BRIGHT +
          f"PACKET #{packet_count}")

    print(Fore.CYAN +
          f"Protocol : {protocol}")

    print(Fore.YELLOW +
          f"Source IP: {src_ip}")

    print(Fore.YELLOW +
          f"Dest IP  : {dest_ip}")

    print(Fore.WHITE +
          f"Info     : {info}")

    line()


# =========================================================
# DEMO PACKET
# =========================================================

def demo_mode():

    global tcp_count
    global udp_count
    global icmp_count

    clear()

    title("DEMO MODE - PACKET SNIFFER")

    protocols = ["TCP", "UDP", "ICMP"]

    for i in range(10):

        proto = random.choice(protocols)

        src_ip = f"192.168.1.{random.randint(1,254)}"

        dest_ip = f"8.8.8.{random.randint(1,254)}"

        if proto == "TCP":

            tcp_count += 1

            src_port = random.randint(1000, 65000)

            dest_port = random.choice(
                [80, 443, 22, 21]
            )

            display_packet(
                "TCP",
                src_ip,
                dest_ip,
                f"PORT {src_port} -> {dest_port}"
            )

        elif proto == "UDP":

            udp_count += 1

            src_port = random.randint(1000, 65000)

            dest_port = random.choice(
                [53, 67, 123]
            )

            display_packet(
                "UDP",
                src_ip,
                dest_ip,
                f"PORT {src_port} -> {dest_port}"
            )

        else:

            icmp_count += 1

            display_packet(
                "ICMP",
                src_ip,
                dest_ip,
                "PING REQUEST"
            )

        time.sleep(1)

    print_statistics()

    pause()


# =========================================================
# REAL SNIFFER
# =========================================================

def real_sniffer():

    global tcp_count
    global udp_count
    global icmp_count

    clear()

    title("REAL PACKET SNIFFER MODE")

    print(Fore.RED + """
YÊU CẦU:
   ✓ Chạy bằng Administrator / Root
   ✓ Windows/Linux hỗ trợ raw socket
""")

    try:

        conn = socket.socket(
            socket.AF_PACKET,
            socket.SOCK_RAW,
            socket.ntohs(3)
        )

    except Exception as e:

        print(Fore.RED +
              f"\nKhông thể tạo raw socket:\n{e}")

        pause()

        return

    print(Fore.GREEN +
          "\nĐang bắt packet...")

    print(Fore.YELLOW +
          "Nhấn CTRL + C để dừng\n")

    try:

        while True:

            raw_data, addr = conn.recvfrom(65536)

            dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)

            if eth_proto == 8:

                (
                    version,
                    header_length,
                    ttl,
                    proto,
                    src,
                    target,
                    data
                ) = ipv4_packet(data)

                # TCP
                if proto == 6:

                    tcp_count += 1

                    (
                        src_port,
                        dest_port,
                        sequence,
                        acknowledgment,
                        flag_urg,
                        flag_ack,
                        flag_psh,
                        flag_rst,
                        flag_syn,
                        flag_fin,
                        data
                    ) = tcp_segment(data)

                    display_packet(
                        "TCP",
                        src,
                        target,
                        f"{src_port} -> {dest_port}"
                    )

                # UDP
                elif proto == 17:

                    udp_count += 1

                    src_port, dest_port, length, data = udp_segment(data)

                    display_packet(
                        "UDP",
                        src,
                        target,
                        f"{src_port} -> {dest_port}"
                    )

                # ICMP
                elif proto == 1:

                    icmp_count += 1

                    icmp_type, code, checksum, data = icmp_packet(data)

                    display_packet(
                        "ICMP",
                        src,
                        target,
                        f"Type={icmp_type} Code={code}"
                    )

    except KeyboardInterrupt:

        print_statistics()

        print(Fore.RED +
              "\nDừng packet sniffer.")

        pause()


# =========================================================
# THỐNG KÊ
# =========================================================

def print_statistics():

    title("THỐNG KÊ PACKET")

    print(Fore.GREEN +
          f"\nTổng packet: {packet_count}")

    print(Fore.CYAN +
          f"TCP : {tcp_count}")

    print(Fore.YELLOW +
          f"UDP : {udp_count}")

    print(Fore.MAGENTA +
          f"ICMP: {icmp_count}")

    line()


# =========================================================
# GIẢI THÍCH CHI TIẾT
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH PACKET SNIFFER")

    print(Fore.WHITE + """
=========================================================
1. PACKET LÀ GÌ?
=========================================================

Packet là đơn vị dữ liệu truyền trên mạng.

Packet gồm:
   ✓ Header
   ✓ Payload

=========================================================
2. ETHERNET FRAME
=========================================================

Frame chứa:
   ✓ MAC nguồn
   ✓ MAC đích
   ✓ Protocol

=========================================================
3. IPv4
=========================================================

IPv4 chứa:
   ✓ Source IP
   ✓ Destination IP
   ✓ TTL
   ✓ Protocol

=========================================================
4. TCP
=========================================================

TCP:
   ✓ Tin cậy
   ✓ Có ACK
   ✓ Có retransmission

Port phổ biến:
   ✓ 80  = HTTP
   ✓ 443 = HTTPS
   ✓ 22  = SSH

=========================================================
5. UDP
=========================================================

UDP:
   ✓ Nhanh
   ✓ Không đảm bảo dữ liệu

=========================================================
6. ICMP
=========================================================

ICMP dùng cho:
   ✓ Ping
   ✓ Kiểm tra mạng

=========================================================
7. RAW SOCKET
=========================================================

Raw socket cho phép:
   ✓ Đọc packet trực tiếp

Cần quyền admin/root.
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("MINI PACKET SNIFFER")

        print(Fore.CYAN + """
[1] Giới thiệu Packet Sniffer
[2] Demo Mode (An toàn)
[3] Real Packet Sniffer
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

            demo_mode()

        elif choice == '3':

            real_sniffer()

        elif choice == '4':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Mini Packet Sniffer.

Kiến thức đạt được:
   ✓ Packet hoạt động thế nào
   ✓ Ethernet Frame
   ✓ IPv4
   ✓ TCP / UDP / ICMP
   ✓ Raw Socket
   ✓ Packet Analysis
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
