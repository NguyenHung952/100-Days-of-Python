# ============================================================
#   THEO DÕI CPU RASPBERRY PI - PHIÊN BẢN HIỆN ĐẠI 2026
# ============================================================
# Tác dụng:
#   - Theo dõi nhiệt độ CPU Raspberry Pi
#   - Theo dõi tải CPU theo thời gian thực
#   - Theo dõi RAM
#   - Theo dõi xung nhịp CPU
#   - Theo dõi uptime hệ thống
#   - Giao diện terminal đẹp mắt
#   - Ghi log ra file CSV
#   - Cảnh báo quá nhiệt
#   - Hoạt động trên Raspberry Pi OS
#
# Yêu cầu:
#   pip install psutil rich
#
# Chạy:
#   python3 monitor_rpi.py
#
# Tác giả:
#   ChatGPT - Modern Raspberry Pi Monitor
# ============================================================

import os
import time
import csv
import psutil
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

# ============================================================
# KHỞI TẠO
# ============================================================

console = Console()

LOG_FILE = "raspberry_pi_cpu_log.csv"

# ============================================================
# GIỚI THIỆU CHƯƠNG TRÌNH
# ============================================================

def show_intro():
    intro_text = """
[bold cyan]
╔══════════════════════════════════════════════╗
║        THEO DÕI CPU RASPBERRY PI            ║
║          PHIÊN BẢN HIỆN ĐẠI 2026            ║
╚══════════════════════════════════════════════╝
[/bold cyan]

[green]CHỨC NĂNG:[/green]

✓ Theo dõi CPU theo thời gian thực
✓ Theo dõi nhiệt độ CPU
✓ Theo dõi RAM
✓ Theo dõi xung nhịp CPU
✓ Theo dõi uptime hệ thống
✓ Ghi log CSV
✓ Cảnh báo quá nhiệt
✓ Giao diện đẹp bằng Rich

[yellow]Nhấn CTRL + C để thoát[/yellow]
"""

    console.print(Panel(intro_text, title="GIỚI THIỆU", border_style="bright_blue"))


# ============================================================
# LẤY NHIỆT ĐỘ CPU
# ============================================================

def get_cpu_temperature():
    """
    Đọc nhiệt độ CPU Raspberry Pi
    """

    try:
        # Raspberry Pi OS thường có file này
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = float(f.read()) / 1000.0
            return round(temp, 1)

    except:
        return None


# ============================================================
# UPTIME HỆ THỐNG
# ============================================================

def get_uptime():
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time

    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)

    return f"{hours}h {minutes}m {seconds}s"


# ============================================================
# GHI FILE CSV
# ============================================================

def init_csv():
    """
    Tạo file CSV nếu chưa tồn tại
    """

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Thời gian",
                "CPU %",
                "RAM %",
                "Nhiệt độ",
                "Xung nhịp MHz"
            ])


def write_csv(cpu, ram, temp, freq):
    """
    Ghi dữ liệu vào CSV
    """

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cpu,
            ram,
            temp,
            freq
        ])


# ============================================================
# TẠO BẢNG GIAO DIỆN
# ============================================================

def create_dashboard():
    """
    Dashboard chính
    """

    table = Table(title="THEO DÕI CPU RASPBERRY PI", expand=True)

    table.add_column("Thông số", style="cyan", justify="left")
    table.add_column("Giá trị", style="green", justify="center")
    table.add_column("Trạng thái", style="magenta", justify="center")

    # ========================================================
    # CPU
    # ========================================================

    cpu_usage = psutil.cpu_percent(interval=0.5)

    if cpu_usage < 50:
        cpu_status = "TỐT"
    elif cpu_usage < 80:
        cpu_status = "CAO"
    else:
        cpu_status = "QUÁ TẢI"

    # ========================================================
    # RAM
    # ========================================================

    ram = psutil.virtual_memory()

    if ram.percent < 60:
        ram_status = "ỔN ĐỊNH"
    elif ram.percent < 85:
        ram_status = "CAO"
    else:
        ram_status = "NGUY HIỂM"

    # ========================================================
    # NHIỆT ĐỘ
    # ========================================================

    temp = get_cpu_temperature()

    if temp is not None:

        if temp < 60:
            temp_status = "MÁT"
        elif temp < 75:
            temp_status = "NÓNG"
        else:
            temp_status = "QUÁ NHIỆT"

    else:
        temp_status = "KHÔNG HỖ TRỢ"

    # ========================================================
    # XUNG NHỊP CPU
    # ========================================================

    freq = psutil.cpu_freq()

    if freq:
        current_freq = round(freq.current, 1)
    else:
        current_freq = 0

    # ========================================================
    # THÊM DỮ LIỆU VÀO BẢNG
    # ========================================================

    table.add_row("CPU Usage", f"{cpu_usage} %", cpu_status)

    table.add_row(
        "RAM Usage",
        f"{ram.percent} %",
        ram_status
    )

    if temp is not None:
        table.add_row(
            "CPU Temperature",
            f"{temp} °C",
            temp_status
        )
    else:
        table.add_row(
            "CPU Temperature",
            "Không xác định",
            temp_status
        )

    table.add_row(
        "CPU Frequency",
        f"{current_freq} MHz",
        "HOẠT ĐỘNG"
    )

    table.add_row(
        "CPU Cores",
        str(psutil.cpu_count()),
        "OK"
    )

    table.add_row(
        "Uptime",
        get_uptime(),
        "ONLINE"
    )

    # ========================================================
    # GHI LOG
    # ========================================================

    write_csv(cpu_usage, ram.percent, temp, current_freq)

    # ========================================================
    # CẢNH BÁO QUÁ NHIỆT
    # ========================================================

    warning = ""

    if temp is not None and temp >= 75:
        warning = "\n[bold red]⚠ CẢNH BÁO: CPU ĐANG QUÁ NHIỆT![/bold red]"

    # ========================================================
    # FOOTER
    # ========================================================

    footer = Text()
    footer.append("\nLog File: ", style="bold cyan")
    footer.append(LOG_FILE, style="bold yellow")

    footer.append("\nCập nhật mỗi giây", style="green")

    # ========================================================
    # PANEL CHÍNH
    # ========================================================

    panel = Panel.fit(
        table,
        title="[bold bright_green]Raspberry Pi Monitor[/bold bright_green]",
        subtitle=warning
    )

    return panel


# ============================================================
# MAIN
# ============================================================

def main():

    os.system("clear")

    show_intro()

    init_csv()

    console.print("\n[bold green]Khởi động hệ thống giám sát...[/bold green]\n")

    time.sleep(2)

    # ========================================================
    # LIVE DASHBOARD
    # ========================================================

    with Live(
        create_dashboard(),
        refresh_per_second=1,
        screen=True
    ) as live:

        while True:
            time.sleep(1)
            live.update(create_dashboard())


# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    try:
        main()

    except KeyboardInterrupt:

        console.print(
            "\n[bold red]Đã dừng chương trình theo dõi CPU Raspberry Pi[/bold red]"
        )

    except Exception as e:

        console.print(
            f"\n[bold red]Lỗi:[/bold red] {e}"
        )
