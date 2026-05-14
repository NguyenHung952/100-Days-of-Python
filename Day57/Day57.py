# =========================================================
#  MÔ PHỎNG CRC CHECKSUM HIỆN ĐẠI - PYTHON 3
# =========================================================
#  Tác giả : ChatGPT
#  Chủ đề  : Mô phỏng CRC (Cyclic Redundancy Check)
#  Mục tiêu:
#     - Giải thích CRC trực quan
#     - Mô phỏng từng bước chia nhị phân XOR
#     - Tạo checksum CRC
#     - Kiểm tra lỗi dữ liệu
#     - Giao diện terminal đẹp, hiện đại
#     - Menu đầy đủ chức năng
#
#  Yêu cầu:
#     pip install colorama
#
#  Chạy:
#     python crc_simulator.py
#
# =========================================================

from colorama import Fore, Style, init
import time
import random
import os

init(autoreset=True)

# =========================================================
# HÀM GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input(Fore.YELLOW + "\nNhấn ENTER để tiếp tục...")


def line():
    print(Fore.CYAN + "=" * 70)


def title(text):
    line()
    print(Fore.GREEN + Style.BRIGHT + text.center(70))
    line()


def loading(text="Đang xử lý"):
    print()
    for i in range(3):
        print(Fore.YELLOW + f"{text}{'.' * (i+1)}")
        time.sleep(0.3)


# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():
    clear()
    title("MÔ PHỎNG CRC CHECKSUM")

    print(Fore.WHITE + """
CRC (Cyclic Redundancy Check) là kỹ thuật phát hiện lỗi dữ liệu
được sử dụng rất nhiều trong:

   • Mạng máy tính
   • Ethernet
   • WiFi
   • Bluetooth
   • Ổ cứng
   • Truyền dữ liệu nhúng
   • Giao thức truyền thông

CRC hoạt động bằng cách:
   1. Chuyển dữ liệu thành bit nhị phân
   2. Chia XOR với đa thức sinh
   3. Lấy phần dư (remainder)
   4. Phần dư chính là CRC checksum

Khi nhận dữ liệu:
   • Nếu CRC đúng => dữ liệu OK
   • Nếu CRC sai => dữ liệu bị lỗi

Chương trình này sẽ mô phỏng:
   ✓ Tạo CRC
   ✓ Kiểm tra CRC
   ✓ Phát hiện lỗi
   ✓ Hiển thị từng bước XOR
""")

    line()


# =========================================================
# CHUYỂN ĐỔI
# =========================================================

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)


def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)


# =========================================================
# THUẬT TOÁN CRC
# =========================================================

def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def mod2div(dividend, divisor, show_steps=False):

    pick = len(divisor)

    temp = dividend[0:pick]

    if show_steps:
        print(Fore.CYAN + "\nBẮT ĐẦU CHIA MODULO-2")
        line()

    while pick < len(dividend):

        if show_steps:
            print(Fore.YELLOW + f"\nTemp hiện tại : {temp}")

        if temp[0] == '1':

            if show_steps:
                print(Fore.GREEN + f"XOR với       : {divisor}")

            temp = xor(divisor, temp) + dividend[pick]

        else:

            if show_steps:
                print(Fore.RED + f"XOR với       : {'0'*pick}")

            temp = xor('0'*pick, temp) + dividend[pick]

        if show_steps:
            print(Fore.WHITE + f"Kết quả XOR   : {temp}")

        pick += 1

    # Bước cuối
    if temp[0] == '1':
        temp = xor(divisor, temp)
    else:
        temp = xor('0'*pick, temp)

    remainder = temp

    if show_steps:
        line()
        print(Fore.MAGENTA + f"CRC remainder = {remainder}")

    return remainder


def encode_data(data, key, show_steps=False):

    appended_data = data + '0' * (len(key)-1)

    remainder = mod2div(appended_data, key, show_steps)

    codeword = data + remainder

    return codeword, remainder


def check_data(data, key):

    remainder = mod2div(data, key)

    return set(remainder) == {'0'}


# =========================================================
# MÔ PHỎNG LỖI
# =========================================================

def introduce_error(data):

    data = list(data)

    pos = random.randint(0, len(data)-1)

    data[pos] = '1' if data[pos] == '0' else '0'

    return ''.join(data), pos


# =========================================================
# CHỨC NĂNG 1
# =========================================================

def simulate_crc():

    clear()
    title("TẠO CRC CHECKSUM")

    text = input(Fore.YELLOW + "Nhập dữ liệu text: ")

    print()
    print(Fore.CYAN + "Các đa thức CRC phổ biến:")
    print("1. CRC-4  : 10011")
    print("2. CRC-8  : 101010101")
    print("3. CRC-16 : 11000000000000101")
    print("4. Tự nhập")

    choice = input(Fore.GREEN + "\nChọn: ")

    if choice == "1":
        key = "10011"

    elif choice == "2":
        key = "101010101"

    elif choice == "3":
        key = "11000000000000101"

    else:
        key = input("Nhập đa thức nhị phân: ")

    binary_data = text_to_binary(text)

    line()

    print(Fore.WHITE + f"\nText gốc      : {text}")
    print(Fore.WHITE + f"Dữ liệu binary: {binary_data}")
    print(Fore.WHITE + f"Generator Key : {key}")

    loading("Đang tạo CRC")

    codeword, crc = encode_data(binary_data, key, show_steps=True)

    line()

    print(Fore.GREEN + Style.BRIGHT + "\nKẾT QUẢ CRC")
    print(Fore.GREEN + f"\nCRC checksum : {crc}")
    print(Fore.GREEN + f"Codeword     : {codeword}")

    pause()


# =========================================================
# CHỨC NĂNG 2
# =========================================================

def verify_crc():

    clear()
    title("KIỂM TRA CRC")

    text = input(Fore.YELLOW + "Nhập dữ liệu text: ")

    key = input(Fore.YELLOW + "Nhập generator key: ")

    binary_data = text_to_binary(text)

    codeword, crc = encode_data(binary_data, key)

    line()

    print(Fore.GREEN + "\nDữ liệu gửi đi:")
    print(Fore.WHITE + f"Codeword: {codeword}")

    # Giả lập lỗi
    choice = input(
        Fore.YELLOW +
        "\nCó muốn giả lập lỗi truyền dữ liệu? (y/n): "
    )

    if choice.lower() == 'y':

        corrupted, pos = introduce_error(codeword)

        print(Fore.RED + f"\nLỗi xuất hiện tại bit vị trí: {pos}")
        print(Fore.RED + f"Dữ liệu lỗi: {corrupted}")

        result = check_data(corrupted, key)

        print()

        if result:
            print(Fore.GREEN + "Không phát hiện lỗi!")
        else:
            print(Fore.RED + Style.BRIGHT +
                  "CRC PHÁT HIỆN DỮ LIỆU BỊ LỖI!")

    else:

        result = check_data(codeword, key)

        print()

        if result:
            print(Fore.GREEN + Style.BRIGHT +
                  "CRC XÁC NHẬN DỮ LIỆU NGUYÊN VẸN")
        else:
            print(Fore.RED + "Dữ liệu lỗi!")

    pause()


# =========================================================
# CHỨC NĂNG 3
# =========================================================

def explain_crc():

    clear()
    title("GIẢI THÍCH CRC CHI TIẾT")

    print(Fore.WHITE + """
CRC sử dụng phép chia nhị phân modulo-2.

Khác với phép chia thông thường:
   • Không có nhớ
   • Không có mượn
   • Sử dụng XOR thay cho trừ

QUY TẮC XOR:
   0 XOR 0 = 0
   1 XOR 1 = 0
   1 XOR 0 = 1
   0 XOR 1 = 1

Ví dụ:
   Data      = 1101011011
   Generator = 10011

Bước thực hiện:
   1. Thêm các bit 0 vào cuối data
   2. XOR với generator
   3. Dịch sang phải
   4. Lặp lại đến hết
   5. Lấy remainder làm CRC

ƯU ĐIỂM CRC:
   ✓ Phát hiện lỗi mạnh
   ✓ Nhanh
   ✓ Hiệu quả cao
   ✓ Dùng trong thực tế rất nhiều

NHƯỢC ĐIỂM:
   ✗ Không sửa được lỗi
   ✗ Chỉ phát hiện lỗi
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("CRC CHECKSUM SIMULATOR")

        print(Fore.CYAN + """
[1] Giới thiệu CRC
[2] Tạo CRC checksum
[3] Kiểm tra CRC
[4] Giải thích CRC chi tiết
[5] Demo tự động
[0] Thoát
""")

        choice = input(Fore.YELLOW + "Nhập lựa chọn: ")

        if choice == '1':
            intro()
            pause()

        elif choice == '2':
            simulate_crc()

        elif choice == '3':
            verify_crc()

        elif choice == '4':
            explain_crc()

        elif choice == '5':
            auto_demo()

        elif choice == '0':

            clear()

            title("CẢM ƠN BẠN ĐÃ SỬ DỤNG")

            print(Fore.GREEN + """
Chương trình mô phỏng CRC đã kết thúc.

Kiến thức đạt được:
   ✓ CRC là gì
   ✓ Cách tạo checksum
   ✓ Cách kiểm tra lỗi
   ✓ XOR hoạt động thế nào
   ✓ CRC phát hiện lỗi ra sao
""")

            break

        else:
            print(Fore.RED + "Lựa chọn không hợp lệ!")
            time.sleep(1)


# =========================================================
# DEMO TỰ ĐỘNG
# =========================================================

def auto_demo():

    clear()

    title("DEMO CRC TỰ ĐỘNG")

    text = "HELLO"

    key = "10011"

    binary_data = text_to_binary(text)

    print(Fore.WHITE + f"\nText           : {text}")
    print(Fore.WHITE + f"Binary         : {binary_data}")
    print(Fore.WHITE + f"Generator Key  : {key}")

    loading("Đang mô phỏng")

    codeword, crc = encode_data(binary_data, key, show_steps=True)

    line()

    print(Fore.GREEN + f"\nCRC tạo được: {crc}")

    print(Fore.CYAN + "\nMô phỏng truyền dữ liệu...")

    time.sleep(1)

    corrupted, pos = introduce_error(codeword)

    print(Fore.RED + f"\nBit lỗi tại vị trí: {pos}")

    print(Fore.RED + f"Dữ liệu lỗi:")
    print(corrupted)

    result = check_data(corrupted, key)

    print()

    if result:
        print(Fore.GREEN + "Không phát hiện lỗi")
    else:
        print(Fore.RED + Style.BRIGHT +
              "CRC ĐÃ PHÁT HIỆN LỖI THÀNH CÔNG!")

    pause()


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:
        menu()

    except KeyboardInterrupt:
        print(Fore.RED + "\n\nĐã thoát chương trình.")
