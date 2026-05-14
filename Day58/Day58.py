# =========================================================
#      MÔ PHỎNG TRUYỀN DỮ LIỆU UART HIỆN ĐẠI
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : UART Communication Simulator
#
# Chức năng:
#   ✓ Giới thiệu UART
#   ✓ Mô phỏng truyền UART từng bit
#   ✓ Hiển thị Start Bit / Data Bit / Stop Bit
#   ✓ Hỗ trợ Parity Bit
#   ✓ Mô phỏng lỗi truyền
#   ✓ Giải mã dữ liệu nhận
#   ✓ Giao diện Terminal đẹp hiện đại
#   ✓ Hoạt động hoàn toàn bằng Python
#
# Yêu cầu:
#   pip install colorama
#
# Chạy:
#   python uart_simulator.py
#
# =========================================================

from colorama import Fore, Style, init
import time
import random
import os

init(autoreset=True)

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print(Fore.CYAN + "=" * 80)


def title(text):
    line()
    print(Fore.GREEN + Style.BRIGHT + text.center(80))
    line()


def pause():
    input(Fore.YELLOW + "\nNhấn ENTER để tiếp tục...")


def loading(text="Đang xử lý"):
    for i in range(3):
        print(Fore.YELLOW + f"{text}{'.' * (i + 1)}")
        time.sleep(0.4)


# =========================================================
# GIỚI THIỆU UART
# =========================================================

def intro_uart():

    clear()

    title("GIỚI THIỆU UART")

    print(Fore.WHITE + """
UART = Universal Asynchronous Receiver Transmitter

UART là giao thức truyền dữ liệu nối tiếp rất phổ biến.

Ứng dụng:
   ✓ Arduino
   ✓ ESP32
   ✓ STM32
   ✓ Raspberry Pi
   ✓ GPS
   ✓ Bluetooth HC-05
   ✓ Module GSM
   ✓ Vi điều khiển

UART truyền dữ liệu theo từng bit.

Cấu trúc khung UART:

    START | DATA BITS | PARITY | STOP

Ví dụ:
    0 10101010 1 1

Ý nghĩa:
    • Start bit = 0
    • Data bits = dữ liệu
    • Parity = kiểm tra lỗi
    • Stop bit = 1

Đặc điểm:
   ✓ Không cần clock riêng
   ✓ Truyền đơn giản
   ✓ Dễ triển khai
   ✓ Phổ biến trong Embedded System
""")

    line()


# =========================================================
# CHUYỂN ĐỔI DỮ LIỆU
# =========================================================

def text_to_binary(text):

    result = []

    for char in text:
        result.append(format(ord(char), '08b'))

    return result


def binary_to_text(binary_list):

    text = ""

    for binary in binary_list:
        text += chr(int(binary, 2))

    return text


# =========================================================
# PARITY BIT
# =========================================================

def calculate_parity(data_bits, parity_type):

    ones = data_bits.count('1')

    if parity_type == "none":
        return ""

    elif parity_type == "even":

        return '0' if ones % 2 == 0 else '1'

    elif parity_type == "odd":

        return '1' if ones % 2 == 0 else '0'

    return ""


# =========================================================
# TẠO FRAME UART
# =========================================================

def create_uart_frame(data_bits,
                      parity="none",
                      stop_bits=1):

    start_bit = "0"

    parity_bit = calculate_parity(data_bits, parity)

    stop = "1" * stop_bits

    frame = start_bit + data_bits + parity_bit + stop

    return frame


# =========================================================
# HIỂN THỊ FRAME
# =========================================================

def display_uart_frame(frame,
                       data_length=8,
                       parity="none",
                       stop_bits=1):

    print()

    print(Fore.GREEN + Style.BRIGHT + "CẤU TRÚC UART FRAME\n")

    index = 0

    # Start bit
    print(Fore.RED + f"[START:{frame[index]}]", end=" ")
    index += 1

    # Data bits
    data_bits = frame[index:index + data_length]

    for bit in data_bits:
        print(Fore.CYAN + f"[DATA:{bit}]", end=" ")

    index += data_length

    # Parity
    if parity != "none":

        print(Fore.YELLOW +
              f"[PARITY:{frame[index]}]", end=" ")

        index += 1

    # Stop bits
    stop = frame[index:index + stop_bits]

    for bit in stop:
        print(Fore.GREEN + f"[STOP:{bit}]", end=" ")

    print("\n")


# =========================================================
# MÔ PHỎNG TRUYỀN BIT
# =========================================================

def simulate_transmission(frame, baud_rate):

    print(Fore.MAGENTA + Style.BRIGHT +
          "\nBẮT ĐẦU TRUYỀN UART\n")

    bit_time = 1 / baud_rate

    transmitted = ""

    for i, bit in enumerate(frame):

        print(Fore.WHITE +
              f"Bit {i+1:02d}: ", end="")

        if bit == '0':
            print(Fore.RED + f"{bit}")
        else:
            print(Fore.GREEN + f"{bit}")

        transmitted += bit

        time.sleep(min(bit_time, 0.2))

    return transmitted


# =========================================================
# GIẢ LẬP LỖI
# =========================================================

def inject_error(frame):

    frame = list(frame)

    pos = random.randint(0, len(frame)-1)

    frame[pos] = '1' if frame[pos] == '0' else '0'

    return ''.join(frame), pos


# =========================================================
# KIỂM TRA PARITY
# =========================================================

def check_parity(frame,
                 parity="none",
                 data_length=8):

    if parity == "none":
        return True

    data_bits = frame[1:1 + data_length]

    received_parity = frame[1 + data_length]

    calculated = calculate_parity(data_bits, parity)

    return received_parity == calculated


# =========================================================
# GIẢI MÃ FRAME
# =========================================================

def decode_uart_frame(frame,
                      parity="none",
                      data_length=8,
                      stop_bits=1):

    data_bits = frame[1:1 + data_length]

    return data_bits


# =========================================================
# CHỨC NĂNG MÔ PHỎNG UART
# =========================================================

def uart_simulation():

    clear()

    title("MÔ PHỎNG TRUYỀN UART")

    text = input(Fore.YELLOW +
                 "Nhập dữ liệu cần gửi: ")

    print()

    print(Fore.CYAN + "Các chế độ parity:")
    print("1. None")
    print("2. Even")
    print("3. Odd")

    choice = input(Fore.GREEN +
                   "\nChọn parity: ")

    if choice == "1":
        parity = "none"

    elif choice == "2":
        parity = "even"

    else:
        parity = "odd"

    baud_rate = int(input(
        Fore.YELLOW +
        "\nNhập baud rate (VD: 9600): "
    ))

    stop_bits = int(input(
        Fore.YELLOW +
        "Nhập số stop bit (1 hoặc 2): "
    ))

    clear()

    title("ĐANG MÔ PHỎNG UART")

    binaries = text_to_binary(text)

    all_received = []

    for index, binary in enumerate(binaries):

        print(Fore.WHITE +
              f"\nKý tự: {text[index]}")

        print(Fore.CYAN +
              f"Binary: {binary}")

        frame = create_uart_frame(
            binary,
            parity,
            stop_bits
        )

        display_uart_frame(
            frame,
            parity=parity,
            stop_bits=stop_bits
        )

        transmitted = simulate_transmission(
            frame,
            baud_rate
        )

        # Giả lập lỗi
        print()

        error_choice = input(
            Fore.YELLOW +
            "Có muốn giả lập lỗi bit? (y/n): "
        )

        if error_choice.lower() == 'y':

            transmitted, pos = inject_error(
                transmitted
            )

            print(Fore.RED +
                  f"\nLỗi xuất hiện tại bit {pos}")

            print(Fore.RED +
                  f"Frame lỗi: {transmitted}")

        # Kiểm tra parity
        valid = check_parity(
            transmitted,
            parity
        )

        print()

        if valid:
            print(Fore.GREEN +
                  Style.BRIGHT +
                  "Parity Check: HỢP LỆ")
        else:
            print(Fore.RED +
                  Style.BRIGHT +
                  "Parity Check: PHÁT HIỆN LỖI")

        decoded = decode_uart_frame(
            transmitted,
            parity,
            stop_bits=stop_bits
        )

        all_received.append(decoded)

        line()

    received_text = binary_to_text(all_received)

    print(Fore.GREEN + Style.BRIGHT +
          "\nDỮ LIỆU NHẬN ĐƯỢC")

    print(Fore.WHITE +
          f"\nText nhận: {received_text}")

    pause()


# =========================================================
# GIẢI THÍCH UART
# =========================================================

def explain_uart():

    clear()

    title("GIẢI THÍCH UART CHI TIẾT")

    print(Fore.WHITE + """
UART hoạt động theo nguyên lý truyền nối tiếp.

Mỗi bit được truyền lần lượt theo thời gian.

=========================================================
1. START BIT
=========================================================

Start bit luôn là:
   0

Mục đích:
   ✓ Báo hiệu bắt đầu truyền dữ liệu

=========================================================
2. DATA BITS
=========================================================

Thông thường:
   ✓ 5 bit
   ✓ 6 bit
   ✓ 7 bit
   ✓ 8 bit

Phổ biến nhất:
   8 bit

=========================================================
3. PARITY BIT
=========================================================

Dùng để kiểm tra lỗi đơn giản.

EVEN parity:
   Tổng số bit 1 phải CHẴN

ODD parity:
   Tổng số bit 1 phải LẺ

=========================================================
4. STOP BIT
=========================================================

Stop bit luôn là:
   1

Mục đích:
   ✓ Kết thúc frame UART

=========================================================
5. BAUD RATE
=========================================================

Là tốc độ truyền dữ liệu.

Ví dụ:
   ✓ 9600
   ✓ 115200
   ✓ 1Mbps

Hai thiết bị UART phải cùng baud rate.

=========================================================
6. ƯU ĐIỂM
=========================================================

✓ Đơn giản
✓ Rẻ
✓ Phổ biến
✓ Dễ debug

=========================================================
7. NHƯỢC ĐIỂM
=========================================================

✗ Chậm hơn SPI
✗ Chỉ point-to-point
✗ Không đồng bộ clock
""")

    pause()


# =========================================================
# DEMO TỰ ĐỘNG
# =========================================================

def auto_demo():

    clear()

    title("DEMO UART TỰ ĐỘNG")

    text = "UART"

    parity = "even"

    stop_bits = 1

    baud_rate = 9600

    print(Fore.WHITE + f"""
Text demo:
   {text}

Parity:
   {parity}

Baud Rate:
   {baud_rate}

Stop Bits:
   {stop_bits}
""")

    loading("Đang mô phỏng")

    binaries = text_to_binary(text)

    for binary in binaries:

        frame = create_uart_frame(
            binary,
            parity,
            stop_bits
        )

        display_uart_frame(
            frame,
            parity=parity,
            stop_bits=stop_bits
        )

        transmitted = simulate_transmission(
            frame,
            baud_rate
        )

        print(Fore.GREEN +
              f"\nFrame truyền: {transmitted}")

        line()

    print(Fore.GREEN + Style.BRIGHT +
          "\nDEMO UART HOÀN TẤT")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("UART COMMUNICATION SIMULATOR")

        print(Fore.CYAN + """
[1] Giới thiệu UART
[2] Mô phỏng truyền UART
[3] Giải thích UART chi tiết
[4] Demo tự động
[0] Thoát
""")

        choice = input(Fore.YELLOW +
                       "Nhập lựa chọn: ")

        if choice == '1':

            intro_uart()

            pause()

        elif choice == '2':

            uart_simulation()

        elif choice == '3':

            explain_uart()

        elif choice == '4':

            auto_demo()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng UART Simulator.

Kiến thức đạt được:
   ✓ UART là gì
   ✓ Start bit hoạt động thế nào
   ✓ Data bits
   ✓ Parity check
   ✓ Stop bit
   ✓ Baud rate
   ✓ Phát hiện lỗi truyền dữ liệu
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
