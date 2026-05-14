# ============================================================
#   BỘ MÃ HÓA HAMMING CODE
# ============================================================
#
# PHIÊN BẢN:
#   Hamming Code Encoder 2026
#
# CHỨC NĂNG:
#   ✓ Mã hóa Hamming Code
#   ✓ Phát hiện lỗi bit
#   ✓ Sửa lỗi 1 bit
#   ✓ Binary Encoder
#   ✓ Binary Decoder
#   ✓ Error Detection
#   ✓ Logging hệ thống
#   ✓ Terminal UI hiện đại
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Học truyền dữ liệu số
#
# CÔNG NGHỆ:
#   - Python
#   - Hamming Code Algorithm
#   - Error Correction
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python hamming_code_system.py
#
# ============================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import datetime

# ============================================================
# CONSOLE
# ============================================================

console = Console()

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "hamming_code_log.txt"

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔══════════════════════════════════════════════╗
║           HAMMING CODE SYSTEM               ║
║            MODERN EDITION 2026              ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Hamming Encoder
✓ Hamming Decoder
✓ Error Detection
✓ Error Correction
✓ Binary Transmission
✓ Data Protection
✓ Logging System

[yellow]KIẾN THỨC:[/yellow]

- Digital Communication
- Error Detection
- Error Correction
- Binary Data
- Data Transmission

"""

    console.print(

        Panel(

            intro_text,

            title="HAMMING CODE",

            border_style="bright_blue"

        )

    )

# ============================================================
# GHI LOG
# ============================================================

def write_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(
            f"[{timestamp}] {message}\n"
        )

# ============================================================
# KIỂM TRA BINARY
# ============================================================

def is_binary(data):

    return all(bit in "01" for bit in data)

# ============================================================
# TÍNH PARITY BIT
# ============================================================

def calculate_parity_bits(data):

    m = len(data)

    r = 0

    while (2 ** r) < (m + r + 1):

        r += 1

    return r

# ============================================================
# ENCODE HAMMING
# ============================================================

def encode_hamming(data):

    if not is_binary(data):

        return None

    data = list(data)

    m = len(data)

    r = calculate_parity_bits(data)

    total_length = m + r

    encoded = ['0'] * total_length

    # ========================================================
    # CHÈN DATA BIT
    # ========================================================

    j = 0

    for i in range(1, total_length + 1):

        if (i & (i - 1)) != 0:

            encoded[i - 1] = data[j]

            j += 1

    # ========================================================
    # TÍNH PARITY
    # ========================================================

    for i in range(r):

        parity_position = 2 ** i

        parity = 0

        for j in range(1, total_length + 1):

            if j & parity_position:

                parity ^= int(encoded[j - 1])

        encoded[parity_position - 1] = str(parity)

    return ''.join(encoded)

# ============================================================
# DETECT ERROR
# ============================================================

def detect_error(data):

    n = len(data)

    r = 0

    while (2 ** r) < n:

        r += 1

    error_position = 0

    # ========================================================
    # CHECK PARITY
    # ========================================================

    for i in range(r):

        parity_position = 2 ** i

        parity = 0

        for j in range(1, n + 1):

            if j & parity_position:

                parity ^= int(data[j - 1])

        if parity != 0:

            error_position += parity_position

    return error_position

# ============================================================
# FIX ERROR
# ============================================================

def fix_error(data, error_position):

    data = list(data)

    if error_position > 0:

        index = error_position - 1

        data[index] = (

            '1' if data[index] == '0'

            else

            '0'

        )

    return ''.join(data)

# ============================================================
# ENCODER MODE
# ============================================================

def encoder_mode():

    try:

        data = input(
            "\n💻 Nhập binary data: "
        )

        if not is_binary(data):

            console.print(
                "\n[bold red]❌ Chỉ nhập 0 và 1![/bold red]"
            )

            return

        encoded = encode_hamming(data)

        console.print(
            f"\n✅ Hamming Code:"
        )

        console.print(
            f"\n[bold green]{encoded}[/bold green]"
        )

        write_log(
            f"ENCODE: {data} -> {encoded}"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Lỗi:[/bold red] {e}"
        )

# ============================================================
# DECODER MODE
# ============================================================

def decoder_mode():

    try:

        data = input(
            "\n📡 Nhập Hamming Code: "
        )

        if not is_binary(data):

            console.print(
                "\n[bold red]❌ Chỉ nhập 0 và 1![/bold red]"
            )

            return

        error_position = detect_error(data)

        # ====================================================
        # KHÔNG LỖI
        # ====================================================

        if error_position == 0:

            console.print(
                "\n[bold green]✅ Không phát hiện lỗi[/bold green]"
            )

        # ====================================================
        # CÓ LỖI
        # ====================================================

        else:

            console.print(
                f"\n[bold red]❌ Lỗi tại bit: {error_position}[/bold red]"
            )

            fixed_data = fix_error(
                data,
                error_position
            )

            console.print(
                "\n✅ Dữ liệu sau sửa lỗi:"
            )

            console.print(
                f"\n[bold green]{fixed_data}[/bold green]"
            )

        write_log(
            f"DECODE: {data}"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Lỗi:[/bold red] {e}"
        )

# ============================================================
# DEMO MODE
# ============================================================

def demo_mode():

    console.print(
        "\n[bold yellow]HAMMING CODE DEMO[/bold yellow]"
    )

    data = "1011"

    encoded = encode_hamming(data)

    console.print(
        f"\n📘 Data gốc: [bold cyan]{data}[/bold cyan]"
    )

    console.print(
        f"\n✅ Encoded: [bold green]{encoded}[/bold green]"
    )

    # ========================================================
    # TẠO LỖI
    # ========================================================

    error_data = list(encoded)

    error_data[3] = (

        '1'

        if error_data[3] == '0'

        else

        '0'

    )

    error_data = ''.join(error_data)

    console.print(
        f"\n❌ Data lỗi: [bold red]{error_data}[/bold red]"
    )

    error_position = detect_error(
        error_data
    )

    console.print(
        f"\n⚠ Lỗi tại bit: {error_position}"
    )

    fixed_data = fix_error(
        error_data,
        error_position
    )

    console.print(
        f"\n✅ Sau sửa lỗi: [bold green]{fixed_data}[/bold green]"
    )

# ============================================================
# HIỂN THỊ THÔNG TIN
# ============================================================

def show_information():

    info = """

Hamming Code là kỹ thuật:

✓ Phát hiện lỗi bit
✓ Sửa lỗi 1 bit
✓ Bảo vệ dữ liệu truyền

Ứng dụng:

- RAM ECC
- Digital Communication
- Satellite Communication
- Network Data
- IoT System

Parity bit đặt tại:

1, 2, 4, 8, 16...

"""

    console.print(

        Panel(

            info,

            title="HAMMING THEORY",

            border_style="green"

        )

    )

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "=" * 50)

    print("MENU:")

    print("1. Encode Hamming Code")
    print("2. Decode & Detect Error")
    print("3. Demo Hamming")
    print("4. Hamming Information")
    print("5. Thoát")

    print("=" * 50)

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    while True:

        try:

            show_menu()

            choice = input(
                "\n👉 Nhập lựa chọn: "
            )

            # =================================================
            # ENCODE
            # =================================================

            if choice == "1":

                encoder_mode()

            # =================================================
            # DECODE
            # =================================================

            elif choice == "2":

                decoder_mode()

            # =================================================
            # DEMO
            # =================================================

            elif choice == "3":

                demo_mode()

            # =================================================
            # INFO
            # =================================================

            elif choice == "4":

                show_information()

            # =================================================
            # EXIT
            # =================================================

            elif choice == "5":

                console.print(
                    "\n[bold red]Tạm biệt![/bold red]"
                )

                break

            # =================================================
            # INVALID
            # =================================================

            else:

                console.print(
                    "\n[bold red]Lựa chọn không hợp lệ![/bold red]"
                )

        except KeyboardInterrupt:

            console.print(
                "\n[bold red]Đã dừng hệ thống[/bold red]"
            )

            break

        except Exception as e:

            console.print(
                f"\n[bold red]Lỗi:[/bold red] {e}"
            )

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
