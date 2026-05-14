# ============================================================
#   HỆ THỐNG SINH ĐỀ QUIZ ĐIỆN TỬ
# ============================================================
#
# PHIÊN BẢN:
#   Electronics Quiz Generator 2026
#
# CHỨC NĂNG:
#   ✓ Sinh đề quiz điện tử tự động
#   ✓ Trộn câu hỏi ngẫu nhiên
#   ✓ Trộn đáp án
#   ✓ Hiển thị đáp án đúng
#   ✓ Xuất file TXT
#   ✓ Logging hệ thống
#   ✓ Giao diện terminal hiện đại
#   ✓ Quiz Arduino / Raspberry Pi
#   ✓ Quiz linh kiện điện tử
#   ✓ Quiz IoT cơ bản
#
# CÔNG NGHỆ:
#   - Python
#   - Random Quiz Generator
#   - Electronics Knowledge Base
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python electronics_quiz_generator.py
#
# ============================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import random
import os
import datetime

# ============================================================
# CONSOLE
# ============================================================

console = Console()

# ============================================================
# THƯ MỤC OUTPUT
# ============================================================

OUTPUT_FOLDER = "quiz_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "quiz_generator_log.txt"

# ============================================================
# DATABASE CÂU HỎI
# ============================================================

quiz_database = [

    {
        "question": "Arduino là gì?",

        "choices": [

            "Vi điều khiển",
            "Điện trở",
            "Tụ điện",
            "Cảm biến"

        ],

        "answer": "Vi điều khiển"
    },

    {
        "question": "LED là linh kiện gì?",

        "choices": [

            "Diode phát quang",
            "Transistor",
            "Relay",
            "Biến trở"

        ],

        "answer": "Diode phát quang"
    },

    {
        "question": "GPIO dùng trên thiết bị nào?",

        "choices": [

            "Raspberry Pi",
            "RAM",
            "Ổ cứng",
            "CPU"

        ],

        "answer": "Raspberry Pi"
    },

    {
        "question": "PWM dùng để làm gì?",

        "choices": [

            "Điều khiển tốc độ",
            "Lưu dữ liệu",
            "Sạc pin",
            "Đo nhiệt độ"

        ],

        "answer": "Điều khiển tốc độ"
    },

    {
        "question": "Relay dùng để?",

        "choices": [

            "Đóng cắt điện",
            "Lưu điện",
            "Khuếch đại âm thanh",
            "Đo khoảng cách"

        ],

        "answer": "Đóng cắt điện"
    },

    {
        "question": "I2C gồm mấy dây?",

        "choices": [

            "2 dây",
            "4 dây",
            "6 dây",
            "8 dây"

        ],

        "answer": "2 dây"
    },

    {
        "question": "Điện trở có đơn vị là gì?",

        "choices": [

            "Ohm",
            "Volt",
            "Ampere",
            "Watt"

        ],

        "answer": "Ohm"
    },

    {
        "question": "Cảm biến HC-SR04 dùng để?",

        "choices": [

            "Đo khoảng cách",
            "Đo nhiệt độ",
            "Đo ánh sáng",
            "Đo điện áp"

        ],

        "answer": "Đo khoảng cách"
    }

]

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔══════════════════════════════════════════════╗
║      ELECTRONICS QUIZ GENERATOR AI          ║
║          MODERN EDITION 2026                ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Sinh đề quiz điện tử
✓ Trộn đáp án tự động
✓ Xuất file TXT
✓ Quiz Arduino
✓ Quiz Raspberry Pi
✓ Quiz IoT
✓ Logging hệ thống

[yellow]HỖ TRỢ:[/yellow]

- Arduino
- Raspberry Pi
- IoT
- Sensor
- Relay
- PWM
- I2C

"""

    console.print(

        Panel(

            intro_text,

            title="QUIZ GENERATOR",

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

        file.write(f"[{timestamp}] {message}\n")

# ============================================================
# SINH QUIZ
# ============================================================

def generate_quiz(number_of_questions):

    # ========================================================
    # RANDOM CÂU HỎI
    # ========================================================

    questions = random.sample(

        quiz_database,

        min(number_of_questions, len(quiz_database))

    )

    quiz_text = ""

    answer_text = ""

    # ========================================================
    # HEADER
    # ========================================================

    quiz_text += (
        "========================================\n"
    )

    quiz_text += (
        "        ĐỀ QUIZ ĐIỆN TỬ AI\n"
    )

    quiz_text += (
        "========================================\n\n"
    )

    # ========================================================
    # DUYỆT CÂU HỎI
    # ========================================================

    for index, item in enumerate(questions):

        question = item["question"]

        choices = item["choices"]

        correct_answer = item["answer"]

        # ====================================================
        # TRỘN ĐÁP ÁN
        # ====================================================

        shuffled_choices = choices.copy()

        random.shuffle(shuffled_choices)

        # ====================================================
        # HIỂN THỊ
        # ====================================================

        quiz_text += (
            f"Câu {index+1}: {question}\n"
        )

        labels = ["A", "B", "C", "D"]

        correct_label = ""

        for i, choice in enumerate(shuffled_choices):

            quiz_text += (
                f"{labels[i]}. {choice}\n"
            )

            if choice == correct_answer:

                correct_label = labels[i]

        quiz_text += "\n"

        answer_text += (
            f"Câu {index+1}: {correct_label}\n"
        )

    # ========================================================
    # ĐÁP ÁN
    # ========================================================

    quiz_text += (
        "\n========================================\n"
    )

    quiz_text += (
        "              ĐÁP ÁN\n"
    )

    quiz_text += (
        "========================================\n\n"
    )

    quiz_text += answer_text

    return quiz_text

# ============================================================
# SAVE FILE
# ============================================================

def save_quiz(content):

    filename = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S_quiz.txt"
    )

    filepath = os.path.join(

        OUTPUT_FOLDER,

        filename

    )

    with open(filepath, "w", encoding="utf-8") as file:

        file.write(content)

    return filepath

# ============================================================
# HIỂN THỊ DATABASE
# ============================================================

def show_database_table():

    table = Table(title="DATABASE QUIZ")

    table.add_column(
        "STT",
        style="cyan"
    )

    table.add_column(
        "Chủ đề",
        style="green"
    )

    topics = [

        "Arduino",
        "LED",
        "GPIO",
        "PWM",
        "Relay",
        "I2C",
        "Điện trở",
        "Cảm biến"

    ]

    for index, topic in enumerate(topics):

        table.add_row(

            str(index + 1),

            topic

        )

    console.print(table)

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    show_database_table()

    while True:

        try:

            print("\n" + "=" * 50)

            print("MENU:")

            print("1. Sinh đề quiz")
            print("2. Xem số lượng câu hỏi")
            print("3. Thoát")

            print("=" * 50)

            choice = input(
                "\n👉 Nhập lựa chọn: "
            )

            # =================================================
            # GENERATE QUIZ
            # =================================================

            if choice == "1":

                number = int(

                    input(
                        "\n📘 Số câu hỏi: "
                    )

                )

                quiz_content = generate_quiz(
                    number
                )

                filepath = save_quiz(
                    quiz_content
                )

                console.print(

                    "\n[bold green]✅ Đã sinh đề thành công![/bold green]"

                )

                console.print(
                    f"\n📁 File: {filepath}"
                )

                # =============================================
                # PREVIEW
                # =============================================

                print("\n" + "-" * 60)

                print(quiz_content)

                print("-" * 60)

                # =============================================
                # LOG
                # =============================================

                write_log(
                    f"Generated Quiz: {filepath}"
                )

            # =================================================
            # SHOW DATABASE
            # =================================================

            elif choice == "2":

                console.print(

                    f"\n📚 Tổng câu hỏi: {len(quiz_database)}"

                )

            # =================================================
            # EXIT
            # =================================================

            elif choice == "3":

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
                "\n[bold red]Đã dừng chương trình[/bold red]"
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
