# ============================================================
#   APP HỌC MÃ NHỊ PHÂN
# ============================================================
#
# PHIÊN BẢN:
#   Binary Learning App 2026
#
# CHỨC NĂNG:
#   ✓ Học hệ nhị phân
#   ✓ Chuyển Decimal sang Binary
#   ✓ Chuyển Binary sang Decimal
#   ✓ Quiz mã nhị phân
#   ✓ Random bài tập
#   ✓ Theo dõi điểm số
#   ✓ Logging hệ thống
#   ✓ Giao diện terminal hiện đại
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Học logic số cơ bản
#
# CÔNG NGHỆ:
#   - Python
#   - Rich Terminal UI
#   - Binary Conversion Logic
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python binary_learning_app.py
#
# ============================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import random
import datetime
import os

# ============================================================
# CONSOLE
# ============================================================

console = Console()

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "binary_learning_log.txt"

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔══════════════════════════════════════════════╗
║           BINARY LEARNING SYSTEM            ║
║             MODERN EDITION 2026             ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Học mã nhị phân
✓ Decimal ↔ Binary
✓ Quiz hệ nhị phân
✓ Random bài tập
✓ Tính điểm tự động
✓ Logging hệ thống

[yellow]KIẾN THỨC:[/yellow]

- Binary Number
- Decimal Conversion
- Logic Digital
- Bit & Byte
- ASCII Binary

"""

    console.print(

        Panel(

            intro_text,

            title="BINARY APP",

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
# DECIMAL -> BINARY
# ============================================================

def decimal_to_binary():

    try:

        number = int(

            input(
                "\n🔢 Nhập số Decimal: "
            )

        )

        binary = bin(number)[2:]

        console.print(
            f"\n✅ Binary: [bold green]{binary}[/bold green]"
        )

        write_log(
            f"DECIMAL_TO_BINARY: {number} -> {binary}"
        )

    except:

        console.print(
            "\n[bold red]❌ Giá trị không hợp lệ![/bold red]"
        )

# ============================================================
# BINARY -> DECIMAL
# ============================================================

def binary_to_decimal():

    try:

        binary = input(
            "\n💻 Nhập Binary: "
        )

        decimal = int(binary, 2)

        console.print(
            f"\n✅ Decimal: [bold green]{decimal}[/bold green]"
        )

        write_log(
            f"BINARY_TO_DECIMAL: {binary} -> {decimal}"
        )

    except:

        console.print(
            "\n[bold red]❌ Binary không hợp lệ![/bold red]"
        )

# ============================================================
# HIỂN THỊ BẢNG BINARY
# ============================================================

def show_binary_table():

    table = Table(title="BẢNG MÃ NHỊ PHÂN")

    table.add_column(
        "Decimal",
        style="cyan"
    )

    table.add_column(
        "Binary",
        style="green"
    )

    for i in range(16):

        table.add_row(

            str(i),

            bin(i)[2:]

        )

    console.print(table)

# ============================================================
# QUIZ MODE
# ============================================================

def quiz_mode():

    console.print(
        "\n[bold yellow]QUIZ MODE[/bold yellow]"
    )

    score = 0

    total_questions = 5

    for question in range(total_questions):

        # ====================================================
        # RANDOM
        # ====================================================

        decimal_number = random.randint(1, 31)

        correct_binary = bin(decimal_number)[2:]

        console.print("\n" + "=" * 50)

        console.print(
            f"\n❓ Chuyển Decimal sang Binary:"
        )

        console.print(
            f"\n[bold cyan]{decimal_number}[/bold cyan]"
        )

        user_answer = input(
            "\n✍ Binary: "
        )

        # ====================================================
        # KIỂM TRA
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
                f"\n💡 Đáp án đúng: {correct_binary}"
            )

        write_log(
            f"QUIZ: {decimal_number}"
        )

    # ========================================================
    # ĐIỂM
    # ========================================================

    final_score = round(

        (score / total_questions) * 10,

        2

    )

    console.print("\n" + "=" * 50)

    console.print(
        f"\n🎯 ĐIỂM SỐ: {final_score}/10"
    )

    console.print(
        f"\n✅ ĐÚNG: {score}/{total_questions}"
    )

    console.print("=" * 50)

# ============================================================
# ASCII MODE
# ============================================================

def ascii_binary_mode():

    try:

        text = input(
            "\n⌨ Nhập ký tự: "
        )

        console.print(
            "\n[bold cyan]ASCII Binary:[/bold cyan]"
        )

        for char in text:

            binary = format(
                ord(char),
                '08b'
            )

            console.print(
                f"\n{char} -> {binary}"
            )

        write_log(
            f"ASCII_BINARY: {text}"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Lỗi:[/bold red] {e}"
        )

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "=" * 50)

    print("MENU:")

    print("1. Decimal -> Binary")
    print("2. Binary -> Decimal")
    print("3. Quiz Binary")
    print("4. Bảng Binary")
    print("5. ASCII Binary")
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
            # DECIMAL -> BINARY
            # =================================================

            if choice == "1":

                decimal_to_binary()

            # =================================================
            # BINARY -> DECIMAL
            # =================================================

            elif choice == "2":

                binary_to_decimal()

            # =================================================
            # QUIZ
            # =================================================

            elif choice == "3":

                quiz_mode()

            # =================================================
            # TABLE
            # =================================================

            elif choice == "4":

                show_binary_table()

            # =================================================
            # ASCII
            # =================================================

            elif choice == "5":

                ascii_binary_mode()

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
