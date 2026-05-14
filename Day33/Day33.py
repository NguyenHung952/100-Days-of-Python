# =========================================================
#               SPI COMMUNICATION SIMULATOR
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống mô phỏng giao tiếp SPI bằng Python
#
# Chức năng:
#   • Mô phỏng SPI Master / Slave
#   • Gửi dữ liệu SPI realtime
#   • Hiển thị MOSI / MISO
#   • Mô phỏng Clock SPI
#   • Dashboard hiện đại
#   • Nhật ký hệ thống
#   • Biểu đồ truyền dữ liệu
#   • Chế độ Auto Transfer
#   • Hỗ trợ Simulation Mode
#
# =========================================================
# ỨNG DỤNG
# =========================================================
#
# • Học giao tiếp SPI
# • Mô phỏng Embedded Systems
# • Raspberry Pi SPI
# • ESP32 SPI
# • Arduino SPI
# • Đồ án IoT
# • Driver cảm biến SPI
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install matplotlib
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python spi_simulator.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import random
import time

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
# CLASS SPI APP
# =========================================================

class SPISimulator:

    def __init__(self, root):

        self.root = root

        self.root.title("SPI COMMUNICATION SIMULATOR")

        self.root.geometry("1500x850")

        self.root.configure(bg=BG)

        self.running = False

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="🔄 SPI COMMUNICATION SIMULATOR",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Mô phỏng giao tiếp SPI bằng Python",
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
            text="📌 TRẠNG THÁI SPI",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.status_label = tk.Label(
            status_card,
            text="🟢 SPI READY",
            font=("Arial", 26, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        # ================================================
        # SIGNAL CARD
        # ================================================

        signal_card = tk.Frame(left, bg=CARD)
        signal_card.pack(fill="x", pady=10)

        tk.Label(
            signal_card,
            text="📡 TÍN HIỆU SPI",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.mosi_label = tk.Label(
            signal_card,
            text="MOSI: 00000000",
            font=("Consolas", 18, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.mosi_label.pack(anchor="w", padx=20, pady=5)

        self.miso_label = tk.Label(
            signal_card,
            text="MISO: 00000000",
            font=("Consolas", 18, "bold"),
            fg=BLUE,
            bg=CARD
        )

        self.miso_label.pack(anchor="w", padx=20, pady=5)

        self.clock_label = tk.Label(
            signal_card,
            text="CLOCK: LOW",
            font=("Arial", 16, "bold"),
            fg=YELLOW,
            bg=CARD
        )

        self.clock_label.pack(anchor="w", padx=20, pady=10)

        self.cs_label = tk.Label(
            signal_card,
            text="CS: HIGH",
            font=("Arial", 16, "bold"),
            fg=RED,
            bg=CARD
        )

        self.cs_label.pack(anchor="w", padx=20, pady=10)

        # ================================================
        # DATA CARD
        # ================================================

        data_card = tk.Frame(left, bg=CARD)
        data_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            data_card,
            text="📊 SPI DATA TRANSFER",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.data_box = tk.Text(
            data_card,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 11)
        )

        self.data_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ================================================
        # GRAPH CARD
        # ================================================

        graph_card = tk.Frame(left, bg=CARD)
        graph_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            graph_card,
            text="📈 SPI CLOCK GRAPH",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.figure = Figure(figsize=(7, 2), dpi=100)

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("SPI Clock Signal")

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_card
        )

        self.canvas.get_tk_widget().pack(
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

        send_btn = tk.Button(
            control_card,
            text="GỬI DỮ LIỆU",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.transfer_data
        )

        send_btn.pack(pady=10)

        auto_btn = tk.Button(
            control_card,
            text="AUTO TRANSFER",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.toggle_auto_transfer
        )

        auto_btn.pack(pady=10)

        clear_btn = tk.Button(
            control_card,
            text="XÓA DỮ LIỆU",
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.clear_data
        )

        clear_btn.pack(pady=10)

        # ================================================
        # SPI INFO
        # ================================================

        info_card = tk.Frame(right, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="⚙ THÔNG TIN SPI",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        info_text = """
• Protocol: SPI
• Mode: Full Duplex
• Clock: Simulated
• Data Size: 8-bit
• MOSI: Master Out
• MISO: Master In
• CS: Chip Select
• SCK: Serial Clock
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
        # LOG CARD
        # ================================================

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

        self.write_log("Khởi động SPI Simulator.")

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
    # SPI TRANSFER
    # =====================================================

    def transfer_data(self):

        # Random 8-bit data
        mosi = random.randint(0, 255)
        miso = random.randint(0, 255)

        mosi_bin = format(mosi, "08b")
        miso_bin = format(miso, "08b")

        self.mosi_label.config(
            text=f"MOSI: {mosi_bin}"
        )

        self.miso_label.config(
            text=f"MISO: {miso_bin}"
        )

        self.cs_label.config(
            text="CS: LOW",
            fg=GREEN
        )

        self.write_log(
            f"SPI Transfer Start | MOSI={mosi_bin}"
        )

        # Simulate SPI Clock
        clock_data = []

        for i in range(8):

            self.clock_label.config(
                text="CLOCK: HIGH",
                fg=GREEN
            )

            clock_data.append(1)

            self.root.update()

            time.sleep(0.1)

            self.clock_label.config(
                text="CLOCK: LOW",
                fg=YELLOW
            )

            clock_data.append(0)

            self.root.update()

            time.sleep(0.1)

        self.cs_label.config(
            text="CS: HIGH",
            fg=RED
        )

        current_time = datetime.now().strftime("%H:%M:%S")

        self.data_box.insert(
            tk.END,
            f"[{current_time}] "
            f"MOSI={mosi_bin} "
            f"| MISO={miso_bin}\n"
        )

        self.data_box.see(tk.END)

        self.write_log(
            "SPI Transfer Complete."
        )

        self.update_graph(clock_data)

    # =====================================================
    # UPDATE GRAPH
    # =====================================================

    def update_graph(self, data):

        self.ax.clear()

        self.ax.plot(data)

        self.ax.set_ylim(-0.5, 1.5)

        self.ax.set_title("SPI Clock Signal")

        self.canvas.draw()

    # =====================================================
    # AUTO TRANSFER
    # =====================================================

    def toggle_auto_transfer(self):

        if not self.running:

            self.running = True

            self.write_log(
                "Bắt đầu Auto Transfer."
            )

            thread = threading.Thread(
                target=self.auto_transfer_loop
            )

            thread.daemon = True

            thread.start()

        else:

            self.running = False

            self.write_log(
                "Dừng Auto Transfer."
            )

    # =====================================================
    # AUTO LOOP
    # =====================================================

    def auto_transfer_loop(self):

        while self.running:

            self.transfer_data()

            time.sleep(2)

    # =====================================================
    # CLEAR DATA
    # =====================================================

    def clear_data(self):

        self.data_box.delete(
            "1.0",
            tk.END
        )

        self.write_log(
            "Đã xóa dữ liệu SPI."
        )

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SPI COMMUNICATION SIMULATOR")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    print("✅ Simulation Mode")
    print("✅ Full Duplex SPI")
    print("✅ MOSI / MISO Simulation")
    print("✅ Clock Signal Simulation")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = SPISimulator(root)

    root.mainloop()
