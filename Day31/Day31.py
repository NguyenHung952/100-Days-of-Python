# =========================================================
#             ESP32 WEB SERVER - PYTHON TOOL
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống Web Server điều khiển ESP32 bằng Python
#
# Chức năng:
#   • Quét IP ESP32
#   • Gửi lệnh ON/OFF tới ESP32
#   • Dashboard hiện đại
#   • Điều khiển LED
#   • Hiển thị trạng thái thiết bị
#   • Nhật ký hệ thống
#   • Kiểm tra kết nối ESP32
#   • Chạy được trên Windows/Linux/macOS
#
# =========================================================
# PHẦN CỨNG
# =========================================================
#
# • ESP32 DevKit V1
# • LED nối GPIO2
#
# =========================================================
# ESP32 CODE (MicroPython)
# =========================================================
#
# File boot.py
#
# ---------------------------------------------------------
#
# import network
#
# ssid = "TEN_WIFI"
# password = "MATKHAU_WIFI"
#
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(ssid, password)
#
# while not wlan.isconnected():
#     pass
#
# print("WiFi Connected")
# print(wlan.ifconfig())
#
# ---------------------------------------------------------
#
# File main.py
#
# ---------------------------------------------------------
#
# from machine import Pin
# import socket
#
# led = Pin(2, Pin.OUT)
#
# html = """
# <!DOCTYPE html>
# <html>
# <head>
# <title>ESP32 WEB SERVER</title>
# </head>
# <body>
# <h1>ESP32 CONTROL</h1>
# <a href="/on"><button>ON</button></a>
# <a href="/off"><button>OFF</button></a>
# </body>
# </html>
# """
#
# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
#
# s = socket.socket()
# s.bind(addr)
# s.listen(1)
#
# print("Server running...")
#
# while True:
#
#     cl, addr = s.accept()
#
#     request = cl.recv(1024)
#
#     request = str(request)
#
#     if '/on' in request:
#         led.value(1)
#
#     if '/off' in request:
#         led.value(0)
#
#     cl.send(html)
#     cl.close()
#
# =========================================================
# CÀI THƯ VIỆN PYTHON
# =========================================================
#
# pip install requests flask tkinterweb
#
# =========================================================
# CHẠY PYTHON TOOL
# =========================================================
#
# python esp32_webserver.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import requests
import socket
import time

# =========================================================
# CẤU HÌNH
# =========================================================

ESP32_IP = "192.168.1.100"

PORT = 80

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

class ESP32WebServerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("ESP32 WEB SERVER CONTROL")

        self.root.geometry("1400x800")

        self.root.configure(bg=BG)

        self.led_state = False

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="🌐 ESP32 WEB SERVER",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Điều khiển ESP32 bằng Python Web Dashboard",
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
            text="📌 TRẠNG THÁI ESP32",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.status_label = tk.Label(
            status_card,
            text="🔴 CHƯA KẾT NỐI",
            font=("Arial", 22, "bold"),
            fg=RED,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        self.ip_label = tk.Label(
            status_card,
            text=f"ESP32 IP: {ESP32_IP}",
            font=("Arial", 12),
            fg=TEXT,
            bg=CARD
        )

        self.ip_label.pack(pady=5)

        # =================================================
        # LED CONTROL
        # =================================================

        led_card = tk.Frame(left, bg=CARD)
        led_card.pack(fill="x", pady=10)

        tk.Label(
            led_card,
            text="💡 ĐIỀU KHIỂN LED",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.led_status = tk.Label(
            led_card,
            text="LED OFF",
            font=("Arial", 28, "bold"),
            fg=RED,
            bg=CARD
        )

        self.led_status.pack(pady=20)

        btn_frame = tk.Frame(led_card, bg=CARD)
        btn_frame.pack(pady=20)

        on_btn = tk.Button(
            btn_frame,
            text="BẬT LED",
            bg=GREEN,
            fg="white",
            font=("Arial", 13, "bold"),
            width=15,
            height=2,
            command=self.turn_on
        )

        on_btn.pack(side="left", padx=10)

        off_btn = tk.Button(
            btn_frame,
            text="TẮT LED",
            bg=RED,
            fg="white",
            font=("Arial", 13, "bold"),
            width=15,
            height=2,
            command=self.turn_off
        )

        off_btn.pack(side="left", padx=10)

        # =================================================
        # SYSTEM INFO
        # =================================================

        info_card = tk.Frame(left, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="⚙ THÔNG TIN HỆ THỐNG",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.info_text = tk.Text(
            info_card,
            height=10,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 10)
        )

        self.info_text.pack(fill="x", padx=10, pady=10)

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
            text="KIỂM TRA ESP32",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.check_connection
        )

        scan_btn.pack(pady=10)

        refresh_btn = tk.Button(
            control_card,
            text="REFRESH STATUS",
            bg=YELLOW,
            fg="black",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.refresh_status
        )

        refresh_btn.pack(pady=10)

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
            fg="#22c55e",
            font=("Consolas", 10)
        )

        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

        # =================================================
        # AUTO MONITOR
        # =================================================

        monitor_thread = threading.Thread(
            target=self.auto_monitor
        )

        monitor_thread.daemon = True

        monitor_thread.start()

        self.write_log("Khởi động hệ thống ESP32 Web Server.")

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

        self.info_text.insert(
            tk.END,
            log + "\n"
        )

        self.info_text.see(tk.END)

        print(log)

    # =====================================================
    # CHECK CONNECTION
    # =====================================================

    def check_connection(self):

        try:

            response = requests.get(
                f"http://{ESP32_IP}",
                timeout=3
            )

            if response.status_code == 200:

                self.status_label.config(
                    text="🟢 ESP32 ONLINE",
                    fg=GREEN
                )

                self.write_log("ESP32 kết nối thành công.")

            else:

                self.status_label.config(
                    text="🔴 ESP32 OFFLINE",
                    fg=RED
                )

        except Exception as e:

            self.status_label.config(
                text="🔴 KHÔNG KẾT NỐI",
                fg=RED
            )

            self.write_log(str(e))

    # =====================================================
    # TURN ON
    # =====================================================

    def turn_on(self):

        try:

            requests.get(
                f"http://{ESP32_IP}/on",
                timeout=3
            )

            self.led_state = True

            self.led_status.config(
                text="🟢 LED ON",
                fg=GREEN
            )

            self.write_log("Đã bật LED ESP32.")

        except Exception as e:

            self.write_log(str(e))

    # =====================================================
    # TURN OFF
    # =====================================================

    def turn_off(self):

        try:

            requests.get(
                f"http://{ESP32_IP}/off",
                timeout=3
            )

            self.led_state = False

            self.led_status.config(
                text="🔴 LED OFF",
                fg=RED
            )

            self.write_log("Đã tắt LED ESP32.")

        except Exception as e:

            self.write_log(str(e))

    # =====================================================
    # REFRESH STATUS
    # =====================================================

    def refresh_status(self):

        self.check_connection()

        if self.led_state:

            self.led_status.config(
                text="🟢 LED ON",
                fg=GREEN
            )

        else:

            self.led_status.config(
                text="🔴 LED OFF",
                fg=RED
            )

        self.write_log("Refresh trạng thái hệ thống.")

    # =====================================================
    # AUTO MONITOR
    # =====================================================

    def auto_monitor(self):

        while True:

            self.check_connection()

            time.sleep(10)

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("ESP32 WEB SERVER SYSTEM")
    print("=" * 60)

    print("\n📌 HƯỚNG DẪN:")
    print("1. Flash MicroPython vào ESP32")
    print("2. Upload boot.py và main.py")
    print("3. Xem IP ESP32 trên Serial Monitor")
    print("4. Đổi ESP32_IP trong file Python")
    print("5. Chạy chương trình")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = ESP32WebServerApp(root)

    root.mainloop()
