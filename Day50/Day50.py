# ============================================================
#   CHATBOT KỸ THUẬT ĐIỆN TỬ
# ============================================================
#
# PHIÊN BẢN:
#   Electronics AI Chatbot 2026
#
# CHỨC NĂNG:
#   ✓ Chatbot kỹ thuật điện tử
#   ✓ Tư vấn Arduino
#   ✓ Tư vấn Raspberry Pi
#   ✓ Tư vấn cảm biến
#   ✓ Tính điện trở
#   ✓ Tính định luật Ohm
#   ✓ Giải thích linh kiện điện tử
#   ✓ Logging lịch sử chat
#   ✓ Terminal UI hiện đại
#   ✓ Chat AI cơ bản offline
#
# CÔNG NGHỆ:
#   - Python
#   - Rule-based AI
#   - Electronics Knowledge Base
#
# CÀI ĐẶT:
#
#   pip install rich
#
# CHẠY:
#
#   python electronics_chatbot.py
#
# THOÁT:
#
#   gõ:
#   thoát
#
# ============================================================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import math
import datetime

# ============================================================
# CONSOLE
# ============================================================

console = Console()

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "electronics_chatbot_log.txt"

# ============================================================
# KIẾN THỨC ĐIỆN TỬ
# ============================================================

knowledge_base = {

    "arduino":
        "Arduino là nền tảng vi điều khiển phổ biến cho IoT và robot.",

    "raspberry pi":
        "Raspberry Pi là máy tính mini hỗ trợ Linux và AI.",

    "led":
        "LED là diode phát quang cần điện trở hạn dòng.",

    "điện trở":
        "Điện trở dùng để hạn dòng và chia điện áp.",

    "tụ điện":
        "Tụ điện dùng để lưu trữ năng lượng điện.",

    "transistor":
        "Transistor dùng để khuếch đại hoặc đóng cắt.",

    "relay":
        "Relay là công tắc điều khiển bằng điện.",

    "cảm biến":
        "Cảm biến dùng để đo nhiệt độ, ánh sáng, khoảng cách...",

    "servo":
        "Servo motor có thể điều khiển góc quay chính xác.",

    "i2c":
        "I2C là giao tiếp 2 dây SDA và SCL.",

    "spi":
        "SPI là giao tiếp tốc độ cao dùng MOSI MISO SCK.",

    "uart":
        "UART là giao tiếp serial TX RX.",

    "pwm":
        "PWM dùng để điều khiển tốc độ động cơ hoặc độ sáng LED."

}

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    intro_text = """

[bold cyan]
╔════════════════════════════════════════════╗
║      CHATBOT KỸ THUẬT ĐIỆN TỬ AI          ║
║          MODERN EDITION 2026              ║
╚════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Hỏi đáp Arduino
✓ Hỏi đáp Raspberry Pi
✓ Kiến thức cảm biến
✓ Tính điện trở LED
✓ Tính định luật Ohm
✓ Chat AI điện tử
✓ Logging lịch sử

[yellow]Ví dụ:[/yellow]

- Arduino là gì
- LED là gì
- tính điện trở led
- tính định luật ohm
- relay là gì
- pwm là gì

[red]Gõ 'thoát' để kết thúc[/red]
"""

    console.print(
        Panel(
            intro_text,
            title="ELECTRONICS AI CHATBOT",
            border_style="bright_blue"
        )
    )

# ============================================================
# GHI LOG
# ============================================================

def write_log(user, bot):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(
            f"[{timestamp}] USER: {user}\n"
        )

        file.write(
            f"[{timestamp}] BOT : {bot}\n\n"
        )

# ============================================================
# CHAT RESPONSE
# ============================================================

def chatbot_response(message):

    message = message.lower()

    # ========================================================
    # OHM LAW
    # ========================================================

    if "định luật ohm" in message:

        return (
            "Định luật Ohm: U = I x R\n"
            "U: điện áp (Volt)\n"
            "I: dòng điện (Ampere)\n"
            "R: điện trở (Ohm)"
        )

    # ========================================================
    # TÍNH ĐIỆN TRỞ LED
    # ========================================================

    elif "tính điện trở led" in message:

        return (
            "Công thức:\n"
            "R = (Vcc - Vled) / I\n"
            "Ví dụ:\n"
            "5V LED đỏ 2V 20mA:\n"
            "R = (5 - 2) / 0.02 = 150 Ohm"
        )

    # ========================================================
    # TÍNH ĐIỆN ÁP
    # ========================================================

    elif "tính điện áp" in message:

        return (
            "Công thức điện áp:\n"
            "U = I x R"
        )

    # ========================================================
    # TÍNH DÒNG ĐIỆN
    # ========================================================

    elif "tính dòng điện" in message:

        return (
            "Công thức dòng điện:\n"
            "I = U / R"
        )

    # ========================================================
    # TÍNH ĐIỆN TRỞ
    # ========================================================

    elif "tính điện trở" in message:

        return (
            "Công thức điện trở:\n"
            "R = U / I"
        )

    # ========================================================
    # KIẾN THỨC
    # ========================================================

    for keyword in knowledge_base:

        if keyword in message:

            return knowledge_base[keyword]

    # ========================================================
    # CHÀO
    # ========================================================

    if (
        "xin chào" in message
        or
        "hello" in message
    ):

        return (
            "Xin chào. Tôi là chatbot kỹ thuật điện tử."
        )

    # ========================================================
    # KHÔNG HIỂU
    # ========================================================

    return (
        "Xin lỗi, tôi chưa có dữ liệu cho câu hỏi này."
    )

# ============================================================
# HIỂN THỊ BẢNG KIẾN THỨC
# ============================================================

def show_help_table():

    table = Table(title="KIẾN THỨC HỖ TRỢ")

    table.add_column(
        "Chủ đề",
        style="cyan"
    )

    table.add_column(
        "Mô tả",
        style="green"
    )

    table.add_row(
        "Arduino",
        "Vi điều khiển IoT"
    )

    table.add_row(
        "Raspberry Pi",
        "Mini Computer"
    )

    table.add_row(
        "LED",
        "Diode phát quang"
    )

    table.add_row(
        "Relay",
        "Đóng cắt thiết bị"
    )

    table.add_row(
        "PWM",
        "Điều khiển xung"
    )

    console.print(table)

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    show_help_table()

    while True:

        try:

            user_message = input(
                "\n👤 Bạn: "
            )

            # =================================================
            # THOÁT
            # =================================================

            if user_message.lower() == "thoát":

                console.print(
                    "\n[bold red]Tạm biệt![/bold red]"
                )

                break

            # =================================================
            # RESPONSE
            # =================================================

            bot_response = chatbot_response(
                user_message
            )

            console.print(
                f"\n🤖 Bot: {bot_response}"
            )

            # =================================================
            # LOG
            # =================================================

            write_log(
                user_message,
                bot_response
            )

        except KeyboardInterrupt:

            console.print(
                "\n[bold red]Đã dừng chatbot[/bold red]"
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
