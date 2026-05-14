# ============================================================
#   FLASHCARD HỌC TÍN HIỆU SỐ
# ============================================================
#
# PHIÊN BẢN:
#   Digital Signal Flashcard System 2026
#
# CHỨC NĂNG:
#   ✓ Flashcard học tín hiệu số
#   ✓ Hiển thị câu hỏi/đáp án
#   ✓ Chế độ học ngẫu nhiên
#   ✓ Quiz kiểm tra nhanh
#   ✓ Theo dõi điểm số
#   ✓ Logging lịch sử học
#   ✓ Giao diện terminal hiện đại
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Học logic số cơ bản
#   ✓ Học điện tử số
#
# CÔNG NGHỆ:
#   - Python
#   - Rich Terminal UI
#   - Flashcard Learning System
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python digital_signal_flashcard.py
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

LOG_FILE = "flashcard_log.txt"

# ============================================================
# FLASHCARD DATABASE
# ============================================================

flashcards = [

    {
        "question": "Tín hiệu số là gì?",
        "answer":
            "Tín hiệu số chỉ có các mức logic rời rạc như 0 và 1."
    },

    {
        "question": "Binary là gì?",
        "answer":
            "Binary là hệ đếm nhị phân chỉ dùng 0 và 1."
    },

    {
        "question": "AND Gate là gì?",
        "answer":
            "AND Gate chỉ xuất 1 khi tất cả input đều bằng 1."
    },

    {
        "question": "OR Gate là gì?",
        "answer":
            "OR Gate xuất 1 khi có ít nhất một input bằng 1."
    },

    {
        "question": "NOT Gate là gì?",
        "answer":
            "NOT Gate đảo logic: 0 thành 1, 1 thành 0."
    },

    {
        "question": "XOR Gate là gì?",
        "answer":
            "XOR Gate xuất 1 khi hai input khác nhau."
    },

    {
        "question": "Flip-Flop dùng để?",
        "answer":
            "Flip-Flop dùng để lưu trữ dữ liệu số."
    },

    {
        "question": "PWM là gì?",
        "answer":
            "PWM là kỹ thuật điều chế độ rộng xung."
    },

    {
        "question": "ADC là gì?",
        "answer":
            "ADC chuyển tín hiệu analog sang digital."
    },

    {
        "question": "DAC là gì?",
        "answer":
            "DAC chuyển tín hiệu digital sang analog."
    }

]

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔══════════════════════════════════════════════╗
║      DIGITAL SIGNAL FLASHCARD SYSTEM        ║
║            MODERN EDITION 2026              ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Flashcard tín hiệu số
✓ Quiz logic số
✓ Random Learning
✓ Score Tracking
✓ Logging System
✓ Terminal Dashboard

[yellow]CHỦ ĐỀ:[/yellow]

- Logic Gate
- Binary
- PWM
- ADC
- DAC
- Flip-Flop
- Digital Signal

"""

    console.print(

        Panel(

            intro_text,

            title="FLASHCARD AI",

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
# HIỂN THỊ DATABASE
# ============================================================

def show_topics():

    table = Table(title="DANH SÁCH CHỦ ĐỀ")

    table.add_column(
        "STT",
        style="cyan"
    )

    table.add_column(
        "Kiến thức",
        style="green"
    )

    topics = [

        "Binary",
        "Logic Gate",
        "PWM",
        "ADC",
        "DAC",
        "Flip-Flop",
        "Digital Signal"

    ]

    for index, topic in enumerate(topics):

        table.add_row(

            str(index + 1),

            topic

        )

    console.print(table)

# ============================================================
# FLASHCARD MODE
# ============================================================

def flashcard_mode():

    console.print(
        "\n[bold green]FLASHCARD MODE[/bold green]"
    )

    shuffled_cards = flashcards.copy()

    random.shuffle(shuffled_cards)

    for index, card in enumerate(shuffled_cards):

        question = card["question"]

        answer = card["answer"]

        console.print("\n" + "=" * 60)

        console.print(
            f"\n📘 Câu {index+1}:"
        )

        console.print(
            f"\n[bold cyan]{question}[/bold cyan]"
        )

        input(
            "\n👉 Nhấn ENTER để xem đáp án..."
        )

        console.print(
            f"\n✅ Đáp án:"
        )

        console.print(
            f"\n[bold green]{answer}[/bold green]"
        )

        write_log(
            f"FLASHCARD: {question}"
        )

# ============================================================
# QUIZ MODE
# ============================================================

def quiz_mode():

    console.print(
        "\n[bold yellow]QUIZ MODE[/bold yellow]"
    )

    score = 0

    shuffled_cards = flashcards.copy()

    random.shuffle(shuffled_cards)

    for index, card in enumerate(shuffled_cards):

        question = card["question"]

        answer = card["answer"]

        console.print("\n" + "=" * 60)

        console.print(
            f"\n❓ Câu {index+1}:"
        )

        console.print(
            f"\n[bold cyan]{question}[/bold cyan]"
        )

        user_answer = input(
            "\n✍ Nhập câu trả lời: "
        )

        # ====================================================
        # KIỂM TRA ĐƠN GIẢN
        # ====================================================

        if len(user_answer.strip()) > 3:

            score += 1

            console.print(
                "\n[bold green]✅ Đã ghi nhận câu trả lời[/bold green]"
            )

        else:

            console.print(
                "\n[bold red]❌ Câu trả lời quá ngắn[/bold red]"
            )

        console.print(
            f"\n💡 Đáp án tham khảo:"
        )

        console.print(
            f"\n[bold yellow]{answer}[/bold yellow]"
        )

        write_log(
            f"QUIZ: {question}"
        )

    # ========================================================
    # ĐIỂM
    # ========================================================

    final_score = round(

        (score / len(shuffled_cards)) * 10,

        2

    )

    console.print("\n" + "=" * 60)

    console.print(
        f"\n🎯 ĐIỂM SỐ: {final_score}/10"
    )

    console.print(
        f"\n✅ SỐ CÂU: {score}/{len(shuffled_cards)}"
    )

    console.print("=" * 60)

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "=" * 50)

    print("MENU:")

    print("1. Flashcard Mode")
    print("2. Quiz Mode")
    print("3. Xem chủ đề")
    print("4. Thoát")

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
            # FLASHCARD
            # =================================================

            if choice == "1":

                flashcard_mode()

            # =================================================
            # QUIZ
            # =================================================

            elif choice == "2":

                quiz_mode()

            # =================================================
            # TOPICS
            # =================================================

            elif choice == "3":

                show_topics()

            # =================================================
            # EXIT
            # =================================================

            elif choice == "4":

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
