# =========================================================
#              GIAO TIẾP I2C BẰNG PYTHON
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống giao tiếp I2C hiện đại bằng Python
#
# Chức năng:
#   • Quét thiết bị I2C
#   • Đọc dữ liệu I2C
#   • Ghi dữ liệu I2C
#   • Monitor realtime
#   • Dashboard hiện đại
#   • Nhật ký hệ thống
#   • Hỗ trợ Raspberry Pi
#   • Chế độ giả lập Windows
#   • Hiển thị địa chỉ I2C
#
# =========================================================
# PHẦN CỨNG HỖ TRỢ
# =========================================================
#
# • Raspberry Pi
# • Arduino I2C Slave
# • ESP32 I2C
# • OLED SSD1306
# • LCD I2C
# • MPU6050
# • BMP280
# • ADS1115
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# Raspberry Pi:
#
# sudo apt install python3-smbus i2c-tools
#
# hoặc:
#
# pip install smbus2
#
# =========================================================
# ENABLE I2C TRÊN RASPBERRY PI
# =========================================================
#
# sudo raspi-config
#
# Interface Options
# -> I2C
# -> Enable
#
# =========================================================
# QUÉT I2C THỦ CÔNG
# =========================================================
#
# sudo i2cdetect -y 1
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python i2c_python.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import random
import time

# =========================================================
# IMPORT I2C
# =========================================================

SIMULATION_MODE = False

try:

    from smbus2 import SMBus

except:

    SIMULATION_MODE = True

# =========================================================
# I2C CONFIG
# =========================================================

I2C_BUS = 1

DEVICE_ADDRESS = 0x27

# =========================================================
# MÀU GIAO DIỆN
# =========================================================

BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#f8fafc"

GREEN = "#22c55e"
RED = "#ef4444"
BLUE = "#3b82f6"
YELLOW = "#facc15"

# =========================================================
# CLASS APP
# =========================================================

class I2CApp:

    def __init__(self, root):

        self.root = root

        self.root.title("I2C COMMUNICATION SYSTEM")

        self.root.geometry("1450x820")

        self.root.configure(bg=BG)

        self.running_monitor = False

        # =================================================
        # SMBUS
        # =================================================

        if not SIMULATION_MODE:

            try:

                self.bus = SMBus(I2C_BUS)

                self.i2c_ready = True

            except:

                self.i2c_ready = False

        else:

            self.i2c_ready = False

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="🔌 I2C COMMUNICATION DASHBOARD",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống giao tiếp I2C bằng Python",
            font=("Arial", 11),
            fg="#94a3b8",
            bg=BG
        )

        subtitle.pack()

        # =================================================
        # MAIN FRAME
        # =================================================

        main = tk.Frame(root, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # =================================================
        # LEFT PANEL
        # =================================================

        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # =================================================
        # RIGHT PANEL
        # =================================================

        right = tk.Frame(main, bg=BG, width=350)
        right.pack(side="right", fill="y", padx=15)

        # =================================================
        # STATUS CARD
        # =================================================

        status_card = tk.Frame(left, bg=CARD)
        status_card.pack(fill="x", pady=10)

        tk.Label(
            status_card,
            text="📌 TRẠNG THÁI I2C",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        if self.i2c_ready:

            status_text = "🟢 I2C READY"
            status_color = GREEN

        else:

            if SIMULATION_MODE:
                status_text = "🟡 SIMULATION MODE"
                status_color = YELLOW
            else:
                status_text = "🔴 I2C ERROR"
                status_color = RED

        self.status_label = tk.Label(
            status_card,
            text=status_text,
            font=("Arial", 24, "bold"),
            fg=status_color,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        self.bus_label = tk.Label(
            status_card,
            text=f"I2C BUS: {I2C_BUS}",
            font=("Arial", 12),
            fg=TEXT,
            bg=CARD
        )

        self.bus_label.pack(pady=5)

        self.addr_label = tk.Label(
            status_card,
            text=f"DEVICE ADDRESS: {hex(DEVICE_ADDRESS)}",
            font=("Arial", 12),
            fg=TEXT,
            bg=CARD
        )

        self.addr_label.pack(pady=5)

        # =================================================
        # DEVICE LIST
        # =================================================

        device_card = tk.Frame(left, bg=CARD)
        device_card.pack(fill="x", pady=10)

        tk.Label(
            device_card,
            text="📡 THIẾT BỊ I2C",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.device_list = tk.Listbox(
            device_card,
            height=8,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 11)
        )

        self.device_list.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # =================================================
        # DATA CARD
        # =================================================

        data_card = tk.Frame(left, bg=CARD)
        data_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            data_card,
            text="📊 DỮ LIỆU I2C",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.data_text = tk.Text(
            data_card,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 11)
        )

        self.data_text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # CONTROL PANEL
        # =================================================

        control_card = tk.Frame(right, bg=CARD)
        control_card.pack(fill="x", pady=10)

        tk.Label(
            control_card,
            text="🎮 ĐIỀU KHIỂN",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        scan_btn = tk.Button(
            control_card,
            text="QUÉT I2C",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.scan_i2c
        )

        scan_btn.pack(pady=10)

        read_btn = tk.Button(
            control_card,
            text="ĐỌC DỮ LIỆU",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.read_i2c
        )

        read_btn.pack(pady=10)

        write_btn = tk.Button(
            control_card,
            text="GHI DỮ LIỆU",
            bg=YELLOW,
            fg="black",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.write_i2c
        )

        write_btn.pack(pady=10)

        monitor_btn = tk.Button(
            control_card,
            text="START MONITOR",
            bg="#9333ea",
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.toggle_monitor
        )

        monitor_btn.pack(pady=10)

        # =================================================
        # LOG SYSTEM
        # =================================================

        log_card = tk.Frame(right, bg=CARD)
        log_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            log_card,
            text="📜 NHẬT KÝ HỆ THỐNG",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.log_box = tk.Text(
            log_card,
            bg="#111827",
            fg="#facc15",
            font=("Consolas", 10)
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.write_log("Khởi động hệ thống I2C.")

        if SIMULATION_MODE:

            self.write_log(
                "Không tìm thấy smbus2 -> chuyển sang Simulation Mode."
            )

    # =====================================================
    # WRITE LOG
    # =====================================================

    def write_log(self, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        log = f"[{current_time}] {message}"

        self.log_box.insert(
            tk.END,
            log + "\n"
        )

        self.log_box.see(tk.END)

        print(log)

    # =====================================================
    # SCAN I2C
    # =====================================================

    def scan_i2c(self):

        self.device_list.delete(0, tk.END)

        self.write_log("Bắt đầu quét I2C...")

        if SIMULATION_MODE:

            fake_devices = [
                "0x27 -> LCD I2C",
                "0x68 -> MPU6050",
                "0x76 -> BMP280",
                "0x3C -> OLED SSD1306"
            ]

            for dev in fake_devices:

                self.device_list.insert(
                    tk.END,
                    dev
                )

            self.write_log(
                "Quét I2C hoàn tất (Simulation)."
            )

            return

        try:

            found = False

            for address in range(128):

                try:

                    self.bus.read_byte(address)

                    self.device_list.insert(
                        tk.END,
                        f"Found Device: {hex(address)}"
                    )

                    found = True

                except:
                    pass

            if found:

                self.write_log(
                    "Đã phát hiện thiết bị I2C."
                )

            else:

                self.write_log(
                    "Không tìm thấy thiết bị I2C."
                )

        except Exception as e:

            self.write_log(str(e))

    # =====================================================
    # READ I2C
    # =====================================================

    def read_i2c(self):

        self.write_log("Đọc dữ liệu I2C...")

        if SIMULATION_MODE:

            value = random.randint(0, 255)

        else:

            try:

                value = self.bus.read_byte(
                    DEVICE_ADDRESS
                )

            except Exception as e:

                self.write_log(str(e))

                return

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.data_text.insert(
            tk.END,
            f"[{current_time}] READ: {value}\n"
        )

        self.data_text.see(tk.END)

        self.write_log(
            f"Đã đọc dữ liệu: {value}"
        )

    # =====================================================
    # WRITE I2C
    # =====================================================

    def write_i2c(self):

        value = random.randint(0, 255)

        self.write_log(
            f"Ghi dữ liệu {value} tới I2C..."
        )

        if not SIMULATION_MODE:

            try:

                self.bus.write_byte(
                    DEVICE_ADDRESS,
                    value
                )

            except Exception as e:

                self.write_log(str(e))

                return

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.data_text.insert(
            tk.END,
            f"[{current_time}] WRITE: {value}\n"
        )

        self.data_text.see(tk.END)

        self.write_log(
            "Ghi dữ liệu thành công."
        )

    # =====================================================
    # MONITOR
    # =====================================================

    def toggle_monitor(self):

        if not self.running_monitor:

            self.running_monitor = True

            self.write_log(
                "Bắt đầu realtime monitor."
            )

            thread = threading.Thread(
                target=self.monitor_loop
            )

            thread.daemon = True

            thread.start()

        else:

            self.running_monitor = False

            self.write_log(
                "Dừng realtime monitor."
            )

    # =====================================================
    # MONITOR LOOP
    # =====================================================

    def monitor_loop(self):

        while self.running_monitor:

            self.read_i2c()

            time.sleep(2)

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("I2C COMMUNICATION SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    if SIMULATION_MODE:

        print("⚠ Chạy ở Simulation Mode")

    else:

        print("✅ SMBUS2 READY")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = I2CApp(root)

    root.mainloop()
