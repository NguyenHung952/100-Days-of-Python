# =========================================================
# SMART HOME - ĐIỀU KHIỂN RELAY THÔNG MINH
# Ngôn ngữ    : Python
# Giao diện   : Tkinter
# Chức năng   :
#   • Điều khiển 4 Relay
#   • Bật/Tắt toàn bộ thiết bị
#   • Hiển thị trạng thái thiết bị
#   • Đồng hồ thời gian thực
#   • Nhật ký hoạt động
#   • Giao diện hiện đại tiếng Việt
#
# Phù hợp:
#   • Đồ án IoT
#   • Raspberry Pi
#   • ESP32 + Relay
#   • Demo Smart Home
#
# Cài đặt:
#   pip install tk
#
# Chạy:
#   python smart_home_relay.py
# =========================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

# =========================================================
# CẤU HÌNH GIAO DIỆN
# =========================================================

BACKGROUND = "#0f172a"
CARD = "#1e293b"
TEXT = "#f8fafc"
GREEN = "#22c55e"
RED = "#ef4444"
BLUE = "#3b82f6"
YELLOW = "#eab308"

# =========================================================
# CLASS SMART HOME
# =========================================================

class SmartHomeApp:

    def __init__(self, root):

        self.root = root
        self.root.title("SMART HOME - ĐIỀU KHIỂN RELAY")
        self.root.geometry("1200x700")
        self.root.configure(bg=BACKGROUND)

        # =========================
        # DỮ LIỆU RELAY
        # =========================

        self.relays = {
            "Đèn phòng khách": False,
            "Quạt phòng ngủ": False,
            "Máy bơm nước": False,
            "Cửa tự động": False
        }

        # =========================
        # HEADER
        # =========================

        self.header = tk.Frame(root, bg=BACKGROUND)
        self.header.pack(fill="x", pady=10)

        self.title = tk.Label(
            self.header,
            text="🏠 SMART HOME RELAY CONTROL",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BACKGROUND
        )
        self.title.pack()

        self.subtitle = tk.Label(
            self.header,
            text="Hệ thống điều khiển relay thông minh bằng Python",
            font=("Arial", 11),
            fg="#94a3b8",
            bg=BACKGROUND
        )
        self.subtitle.pack()

        # =========================
        # THỜI GIAN
        # =========================

        self.clock_label = tk.Label(
            root,
            font=("Consolas", 14, "bold"),
            fg=YELLOW,
            bg=BACKGROUND
        )
        self.clock_label.pack(pady=5)

        self.update_clock()

        # =========================
        # KHUNG CHÍNH
        # =========================

        self.main_frame = tk.Frame(root, bg=BACKGROUND)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # =========================
        # LEFT PANEL
        # =========================

        self.left_panel = tk.Frame(self.main_frame, bg=BACKGROUND)
        self.left_panel.pack(side="left", fill="both", expand=True)

        # =========================
        # RIGHT PANEL
        # =========================

        self.right_panel = tk.Frame(self.main_frame, bg=BACKGROUND)
        self.right_panel.pack(side="right", fill="y", padx=20)

        # =========================
        # TẠO CARD RELAY
        # =========================

        self.buttons = {}
        self.status_labels = {}

        for name in self.relays:
            self.create_relay_card(name)

        # =========================
        # NÚT ĐIỀU KHIỂN NHANH
        # =========================

        self.control_frame = tk.Frame(self.right_panel, bg=CARD)
        self.control_frame.pack(fill="x", pady=10)

        tk.Label(
            self.control_frame,
            text="ĐIỀU KHIỂN NHANH",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        tk.Button(
            self.control_frame,
            text="BẬT TẤT CẢ",
            command=self.turn_all_on,
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.control_frame,
            text="TẮT TẤT CẢ",
            command=self.turn_all_off,
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        ).pack(pady=10)

        # =========================
        # THÔNG SỐ HỆ THỐNG
        # =========================

        self.info_frame = tk.Frame(self.right_panel, bg=CARD)
        self.info_frame.pack(fill="x", pady=20)

        tk.Label(
            self.info_frame,
            text="THÔNG TIN HỆ THỐNG",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.temp_label = tk.Label(
            self.info_frame,
            text=f"Nhiệt độ: {random.randint(25,35)}°C",
            font=("Arial", 12),
            fg=TEXT,
            bg=CARD
        )
        self.temp_label.pack(pady=5)

        self.humid_label = tk.Label(
            self.info_frame,
            text=f"Độ ẩm: {random.randint(50,80)}%",
            font=("Arial", 12),
            fg=TEXT,
            bg=CARD
        )
        self.humid_label.pack(pady=5)

        # =========================
        # NHẬT KÝ HOẠT ĐỘNG
        # =========================

        self.log_frame = tk.Frame(root, bg=CARD)
        self.log_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            self.log_frame,
            text="NHẬT KÝ HOẠT ĐỘNG",
            font=("Arial", 13, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=10, pady=5)

        self.log_text = tk.Text(
            self.log_frame,
            height=8,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 10)
        )
        self.log_text.pack(fill="x", padx=10, pady=10)

        self.write_log("Hệ thống Smart Home đã khởi động.")

    # =====================================================
    # TẠO CARD RELAY
    # =====================================================

    def create_relay_card(self, relay_name):

        card = tk.Frame(
            self.left_panel,
            bg=CARD,
            padx=20,
            pady=20
        )

        card.pack(fill="x", pady=10)

        title = tk.Label(
            card,
            text=relay_name,
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        )
        title.pack(anchor="w")

        status = tk.Label(
            card,
            text="TRẠNG THÁI: OFF",
            font=("Arial", 12, "bold"),
            fg=RED,
            bg=CARD
        )
        status.pack(anchor="w", pady=10)

        self.status_labels[relay_name] = status

        btn = tk.Button(
            card,
            text="BẬT",
            font=("Arial", 12, "bold"),
            bg=GREEN,
            fg="white",
            width=15,
            height=2,
            command=lambda n=relay_name: self.toggle_relay(n)
        )

        btn.pack(pady=10)

        self.buttons[relay_name] = btn

    # =====================================================
    # BẬT / TẮT RELAY
    # =====================================================

    def toggle_relay(self, relay_name):

        current = self.relays[relay_name]
        self.relays[relay_name] = not current

        if self.relays[relay_name]:

            self.status_labels[relay_name].config(
                text="TRẠNG THÁI: ON",
                fg=GREEN
            )

            self.buttons[relay_name].config(
                text="TẮT",
                bg=RED
            )

            self.write_log(f"{relay_name} đã được BẬT.")

        else:

            self.status_labels[relay_name].config(
                text="TRẠNG THÁI: OFF",
                fg=RED
            )

            self.buttons[relay_name].config(
                text="BẬT",
                bg=GREEN
            )

            self.write_log(f"{relay_name} đã được TẮT.")

    # =====================================================
    # BẬT TẤT CẢ
    # =====================================================

    def turn_all_on(self):

        for relay in self.relays:

            if not self.relays[relay]:
                self.toggle_relay(relay)

        self.write_log("Đã bật toàn bộ relay.")

    # =====================================================
    # TẮT TẤT CẢ
    # =====================================================

    def turn_all_off(self):

        for relay in self.relays:

            if self.relays[relay]:
                self.toggle_relay(relay)

        self.write_log("Đã tắt toàn bộ relay.")

    # =====================================================
    # GHI LOG
    # =====================================================

    def write_log(self, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.log_text.insert(
            tk.END,
            f"[{current_time}] {message}\n"
        )

        self.log_text.see(tk.END)

    # =====================================================
    # CẬP NHẬT ĐỒNG HỒ
    # =====================================================

    def update_clock(self):

        now = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

        self.clock_label.config(
            text=f"🕒 {now}"
        )

        self.root.after(1000, self.update_clock)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartHomeApp(root)

    root.mainloop()
