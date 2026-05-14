# ============================================================
#   BỘ CHUYỂN ĐỔI ASCII ↔ BINARY
# ============================================================
#
# PHIÊN BẢN:
#   ASCII Binary Converter 2026
#
# CHỨC NĂNG:
#   ✓ ASCII sang Binary
#   ✓ Binary sang ASCII
#   ✓ Hiển thị bảng ASCII
#   ✓ Chuyển đổi realtime
#   ✓ Logging hệ thống
#   ✓ Giao diện terminal hiện đại
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Học mã nhị phân
#   ✓ Học mã ASCII
#   ✓ Quiz mini ASCII
#
# CÔNG NGHỆ:
#   - Python
#   - Rich Terminal UI
#   - Binary Encoding
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python ascii_binary_converter.py
#
# ============================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import datetime
import os
import random

# ============================================================
# CONSOLE
# ============================================================

console = Console()

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "ascii_binary_log.txt"

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔══════════════════════════════════════════════╗
║         ASCII ↔ BINARY CONVERTER            ║
║            MODERN EDITION 2026              ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ ASCII → Binary
✓ Binary → ASCII
✓ ASCII Table
✓ Mini Quiz
✓ Logging System
✓ Realtime Conversion

[yellow]KIẾN THỨC:[/yellow]

- ASCII Encoding
- Binary Encoding
- Character Conversion
- Digital Signal
- Bit & Byte

"""

    console.print(

        Panel(

            intro_text,

            title="ASCII BINARY SYSTEM",

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
# ASCII -> BINARY
# ============================================================

def ascii_to_binary():

    try:

        text = input(
            "\n⌨ Nhập văn bản ASCII: "
        )

        console.print(
            "\n[bold cyan]KẾT QUẢ BINARY:[/bold cyan]"
        )

        binary_result = []

        for char in text:

            binary = format(
                ord(char),
                '08b'
            )

            binary_result.append(binary)

            console.print(
                f"\n{char} -> [bold green]{binary}[/bold green]"
            )

        final_binary = " ".join(binary_result)

        print("\n" + "=" * 60)

        print("FULL BINARY:")

        print(final_binary)

        print("=" * 60)

        write_log(
            f"ASCII_TO_BINARY: {text}"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Lỗi:[/bold red] {e}"
        )

# ============================================================
# BINARY -> ASCII
# ============================================================

def binary_to_ascii():

    try:

        binary_input = input(
            "\n💻 Nhập Binary (cách nhau bằng dấu cách): "
        )

        binary_list = binary_input.split()

        text = ""

        console.print(
            "\n[bold cyan]KẾT QUẢ ASCII:[/bold cyan]"
        )

        for binary in binary_list:

            ascii_char = chr(
                int(binary, 2)
            )

            text += ascii_char

            console.print(
                f"\n{binary} -> [bold green]{ascii_char}[/bold green]"
            )

        print("\n" + "=" * 60)

        print("FULL ASCII:")

        print(text)

        print("=" * 60)

        write_log(
            f"BINARY_TO_ASCII: {binary_input}"
        )

    except Exception as e:

        console.print(
            "\n[bold red]❌ Binary không hợp lệ![/bold red]"
        )

# ============================================================
# ASCII TABLE
# ============================================================

def show_ascii_table():

    table = Table(title="ASCII TABLE")

    table.add_column(
        "ASCII",
        style="cyan"
    )

    table.add_column(
        "Decimal",
        style="green"
    )

    table.add_column(
        "Binary",
        style="yellow"
    )

    # ========================================================
    # A-Z
    # ========================================================

    for code in range(65, 91):

        char = chr(code)

        binary = format(
            code,
            '08b'
        )

        table.add_row(

            char,

            str(code),

            binary

        )

    console.print(table)

# ============================================================
# QUIZ MODE
# ============================================================

def quiz_mode():

    console.print(
        "\n[bold yellow]ASCII QUIZ MODE[/bold yellow]"
    )

    score = 0

    total_questions = 5

    for i in range(total_questions):

        # ====================================================
        # RANDOM ASCII
        # ====================================================

        random_char = random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

        correct_binary = format(
            ord(random_char),
            '08b'
        )

        print("\n" + "=" * 50)

        console.print(
            f"\n❓ Binary của ký tự:"
        )

        console.print(
            f"\n[bold cyan]{random_char}[/bold cyan]"
        )

        user_answer = input(
            "\n✍ Binary: "
        )

        # ====================================================
        # CHECK
        # ====================================================

        if user_answer == correct_binary:

            console.print(
                "\n[bold green]✅ Chính xác![/bold green]"
            )

            score += 1

        else:

            console.print(
                "\n[bold red]❌ Sai![/bold red]"
            )

            console.print(
                f"\n💡 Đáp án: {correct_binary}"
            )

        write_log(
            f"QUIZ: {random_char}"
        )

    # ========================================================
    # SCORE
    # ========================================================

    final_score = round(

        (score / total_questions) * 10,

        2

    )

    print("\n" + "=" * 50)

    print(f"\n🎯 ĐIỂM SỐ: {final_score}/10")

    print(f"\n✅ ĐÚNG: {score}/{total_questions}")

    print("=" * 50)

# ============================================================
# GIẢI THÍCH ASCII
# ============================================================

def show_ascii_info():

    info = """

ASCII (American Standard Code for Information Interchange)

- Là bảng mã ký tự chuẩn
- Mỗi ký tự có mã số riêng
- Máy tính lưu ký tự dưới dạng binary

Ví dụ:

A = 65 = 01000001
B = 66 = 01000010

1 byte = 8 bit

"""

    console.print(

        Panel(

            info,

            title="ASCII INFORMATION",

            border_style="green"

        )

    )

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "=" * 50)

    print("MENU:")

    print("1. ASCII -> Binary")
    print("2. Binary -> ASCII")
    print("3. ASCII Table")
    print("4. ASCII Quiz")
    print("5. ASCII Information")
    print("6. Thoát")

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
            # ASCII -> BINARY
            # =================================================

            if choice == "1":

                ascii_to_binary()

            # =================================================
            # BINARY -> ASCII
            # =================================================

            elif choice == "2":

                binary_to_ascii()

            # =================================================
            # TABLE
            # =================================================

            elif choice == "3":

                show_ascii_table()

            # =================================================
            # QUIZ
            # =================================================

            elif choice == "4":

                quiz_mode()

            # =================================================
            # INFO
            # =================================================

            elif choice == "5":

                show_ascii_info()

            # =================================================
            # EXIT
            # =================================================

            elif choice == "6":

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
