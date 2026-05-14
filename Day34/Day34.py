# =========================================================
#                RFID READER SYSTEM - PYTHON
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống đọc RFID bằng Python với giao diện hiện đại
#
# Chức năng:
#   • Đọc UID thẻ RFID
#   • Hiển thị trạng thái RFID realtime
#   • Nhật ký quét thẻ
#   • Mô phỏng RFID trên Windows
#   • Hỗ trợ Raspberry Pi + RC522
#   • Dashboard hiện đại
#   • Lưu lịch sử quét
#   • Chế độ Auto Scan
#   • Kiểm tra Access Control
#
# =========================================================
# PHẦN CỨNG HỖ TRỢ
# =========================================================
#
# • Raspberry Pi
# • RFID RC522
# • RFID Tag/Card 13.56MHz
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# Raspberry Pi:
#
# pip install mfrc522
# pip install spidev
# pip install RPi.GPIO
#
# =========================================================
# ENABLE SPI
# =========================================================
#
# sudo raspi-config
#
# Interface Options
# -> SPI
# -> Enable
#
# =========================================================
# KẾT NỐI RC522
# =========================================================
#
# RC522     -> Raspberry Pi
#
# SDA       -> GPIO8  (CE0)
# SCK       -> GPIO11
# MOSI      -> GPIO10
# MISO      -> GPIO9
# IRQ       -> Không dùng
# GND       -> GND
# RST       -> GPIO25
# 3.3V      -> 3.3V
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python rfid_reader.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import random
import time

# =========================================================
# RFID IMPORT
# =========================================================

SIMULATION_MODE = False

try:

    from mfrc522 import SimpleMFRC522

    import RPi.GPIO as GPIO

except:

    SIMULATION_MODE = True

# =========================================================
# RFID INIT
# =========================================================

if not SIMULATION_MODE:

    try:

        reader = SimpleMFRC522()

        RFID_READY = True

    except:

        RFID_READY = False

else:

    RFID_READY = False

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
# DANH SÁCH UID HỢP LỆ
# =========================================================

AUTHORIZED_CARDS = [
    "123456789",
    "987654321",
    "456789123"
]

# =========================================================
# CLASS APP
# =========================================================

class RFIDApp:

    def __init__(self, root):

        self.root = root

        self.root.title("RFID READER SYSTEM")

        self.root.geometry("1500x850")

        self.root.configure(bg=BG)

        self.auto_scan_running = False

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="📡 RFID READER SYSTEM",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống đọc RFID bằng Python",
            font=("Arial", 11),
            fg="#94a3b8",
            bg=BG
        )

        subtitle.pack()

        # ================================================
        # MAIN FRAME
        # ================================================

        main = tk.Frame(root, bg=BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # ================================================
        # LEFT PANEL
        # ================================================

        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # ================================================
        # RIGHT PANEL
        # ================================================

        right = tk.Frame(main, bg=BG, width=350)
        right.pack(side="right", fill="y", padx=15)

        # ================================================
        # STATUS CARD
        # ================================================

        status_card = tk.Frame(left, bg=CARD)
        status_card.pack(fill="x", pady=10)

        tk.Label(
            status_card,
            text="📌 TRẠNG THÁI RFID",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        if SIMULATION_MODE:

            status_text = "🟡 SIMULATION MODE"
            status_color = YELLOW

        elif RFID_READY:

            status_text = "🟢 RFID READY"
            status_color = GREEN

        else:

            status_text = "🔴 RFID ERROR"
            status_color = RED

        self.status_label = tk.Label(
            status_card,
            text=status_text,
            font=("Arial", 26, "bold"),
            fg=status_color,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        # ================================================
        # RFID DATA CARD
        # ================================================

        rfid_card = tk.Frame(left, bg=CARD)
        rfid_card.pack(fill="x", pady=10)

        tk.Label(
            rfid_card,
            text="🏷 THÔNG TIN RFID",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.uid_label = tk.Label(
            rfid_card,
            text="UID: ---",
            font=("Consolas", 24, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.uid_label.pack(pady=10)

        self.access_label = tk.Label(
            rfid_card,
            text="ACCESS: WAITING",
            font=("Arial", 20, "bold"),
            fg=YELLOW,
            bg=CARD
        )

        self.access_label.pack(pady=10)

        # ================================================
        # RFID HISTORY
        # ================================================

        history_card = tk.Frame(left, bg=CARD)
        history_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            history_card,
            text="📜 LỊCH SỬ QUÉT THẺ",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.history_box = tk.Text(
            history_card,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 11)
        )

        self.history_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ================================================
        # CONTROL PANEL
        # ================================================

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
            text="QUÉT RFID",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.scan_rfid
        )

        scan_btn.pack(pady=10)

        auto_btn = tk.Button(
            control_card,
            text="AUTO SCAN",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.toggle_auto_scan
        )

        auto_btn.pack(pady=10)

        clear_btn = tk.Button(
            control_card,
            text="XÓA LOG",
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.clear_logs
        )

        clear_btn.pack(pady=10)

        # ================================================
        # SYSTEM INFO
        # ================================================

        info_card = tk.Frame(right, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="⚙ THÔNG TIN HỆ THỐNG",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        info_text = f"""
• RFID Module: RC522
• Communication: SPI
• Frequency: 13.56MHz
• Python GUI: Tkinter
• Simulation Mode:
  {"ON" if SIMULATION_MODE else "OFF"}
"""

        tk.Label(
            info_card,
            text=info_text,
            justify="left",
            font=("Consolas", 10),
            fg="#22c55e",
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        # ================================================
        # LOG SYSTEM
        # ================================================

        log_card = tk.Frame(right, bg=CARD)
        log_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            log_card,
            text="📋 NHẬT KÝ HỆ THỐNG",
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

        self.write_log("Khởi động RFID System.")

        if SIMULATION_MODE:

            self.write_log(
                "Không phát hiện RC522 -> Simulation Mode."
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
    # RFID SCAN
    # =====================================================

    def scan_rfid(self):

        self.write_log("Đang quét RFID...")

        # ================================================
        # SIMULATION MODE
        # ================================================

        if SIMULATION_MODE:

            fake_uid = str(
                random.randint(
                    100000000,
                    999999999
                )
            )

            time.sleep(1)

            self.process_card(fake_uid)

            return

        # ================================================
        # REAL RFID
        # ================================================

        try:

            self.write_log(
                "Đưa thẻ RFID lại gần..."
            )

            uid, text = reader.read()

            self.process_card(str(uid))

        except Exception as e:

            self.write_log(str(e))

    # =====================================================
    # PROCESS CARD
    # =====================================================

    def process_card(self, uid):

        self.uid_label.config(
            text=f"UID: {uid}"
        )

        current_time = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        # Access Check
        if uid in AUTHORIZED_CARDS:

            self.access_label.config(
                text="🟢 ACCESS GRANTED",
                fg=GREEN
            )

            access = "GRANTED"

            self.write_log(
                f"Access Granted -> UID={uid}"
            )

        else:

            self.access_label.config(
                text="🔴 ACCESS DENIED",
                fg=RED
            )

            access = "DENIED"

            self.write_log(
                f"Access Denied -> UID={uid}"
            )

        # Save History
        self.history_box.insert(
            tk.END,
            f"[{current_time}] "
            f"UID={uid} "
            f"| ACCESS={access}\n"
        )

        self.history_box.see(tk.END)

    # =====================================================
    # AUTO SCAN
    # =====================================================

    def toggle_auto_scan(self):

        if not self.auto_scan_running:

            self.auto_scan_running = True

            self.write_log(
                "Bắt đầu Auto Scan."
            )

            thread = threading.Thread(
                target=self.auto_scan_loop
            )

            thread.daemon = True

            thread.start()

        else:

            self.auto_scan_running = False

            self.write_log(
                "Dừng Auto Scan."
            )

    # =====================================================
    # AUTO LOOP
    # =====================================================

    def auto_scan_loop(self):

        while self.auto_scan_running:

            self.scan_rfid()

            time.sleep(3)

    # =====================================================
    # CLEAR LOG
    # =====================================================

    def clear_logs(self):

        self.history_box.delete(
            "1.0",
            tk.END
        )

        self.write_log(
            "Đã xóa lịch sử RFID."
        )

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("RFID READER SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    if SIMULATION_MODE:

        print("⚠ Simulation Mode")

    else:

        print("✅ RC522 READY")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = RFIDApp(root)

    root.mainloop()

    # Cleanup GPIO
    if not SIMULATION_MODE:

        GPIO.cleanup()
