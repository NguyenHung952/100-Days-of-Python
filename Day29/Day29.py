# =========================================================
#            THINGSPEAK DATA UPLOADER SYSTEM
# =========================================================
#
# Tên project :
#   Hệ thống gửi dữ liệu IoT lên ThingSpeak bằng Python
#
# Chức năng:
#   • Gửi dữ liệu cảm biến realtime lên ThingSpeak
#   • Dashboard giao diện hiện đại
#   • Mô phỏng cảm biến nhiệt độ / độ ẩm
#   • Hiển thị biểu đồ realtime
#   • Nhật ký hệ thống
#   • Trạng thái kết nối Internet
#   • Tự động gửi dữ liệu định kỳ
#   • Hỗ trợ ThingSpeak REST API
#
# Ứng dụng:
#   • Smart Home
#   • IoT Monitoring
#   • ESP32 / Raspberry Pi
#   • Đồ án IoT
#   • Hệ thống cảm biến môi trường
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install requests matplotlib
#
# =========================================================
# CÁCH DÙNG
# =========================================================
#
# BƯỚC 1:
#   Tạo tài khoản ThingSpeak:
#   https://thingspeak.com
#
# BƯỚC 2:
#   Tạo Channel mới
#
# BƯỚC 3:
#   Copy WRITE API KEY
#
# BƯỚC 4:
#   Thay API_KEY bên dưới
#
# BƯỚC 5:
#   Chạy:
#   python thingspeak_uploader.py
#
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import random
import time
import requests

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# =========================================================
# CẤU HÌNH THINGSPEAK
# =========================================================

API_KEY = "YOUR_WRITE_API_KEY"

THINGSPEAK_URL = "https://api.thingspeak.com/update"

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

class ThingSpeakApp:

    def __init__(self, root):

        self.root = root

        self.root.title("THINGSPEAK IOT SYSTEM")

        self.root.geometry("1400x800")

        self.root.configure(bg=BG)

        # ================================================
        # DỮ LIỆU BIỂU ĐỒ
        # ================================================

        self.temperature_data = []
        self.humidity_data = []

        self.time_data = []

        self.auto_running = False

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="☁ THINGSPEAK CLOUD IOT",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống gửi dữ liệu cảm biến lên Cloud",
            font=("Arial", 11),
            fg="#94a3b8",
            bg=BG
        )

        subtitle.pack()

        # ================================================
        # MAIN FRAME
        # ================================================

        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ================================================
        # LEFT PANEL
        # ================================================

        left_panel = tk.Frame(main_frame, bg=BG)
        left_panel.pack(side="left", fill="both", expand=True)

        # ================================================
        # RIGHT PANEL
        # ================================================

        right_panel = tk.Frame(main_frame, bg=BG, width=320)
        right_panel.pack(side="right", fill="y", padx=15)

        # ================================================
        # CARD NHIỆT ĐỘ
        # ================================================

        self.temp_card = tk.Frame(left_panel, bg=CARD)
        self.temp_card.pack(fill="x", pady=10)

        tk.Label(
            self.temp_card,
            text="🌡 NHIỆT ĐỘ",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.temp_value = tk.Label(
            self.temp_card,
            text="0 °C",
            font=("Arial", 32, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.temp_value.pack(pady=10)

        # ================================================
        # CARD ĐỘ ẨM
        # ================================================

        self.humid_card = tk.Frame(left_panel, bg=CARD)
        self.humid_card.pack(fill="x", pady=10)

        tk.Label(
            self.humid_card,
            text="💧 ĐỘ ẨM",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.humid_value = tk.Label(
            self.humid_card,
            text="0 %",
            font=("Arial", 32, "bold"),
            fg=BLUE,
            bg=CARD
        )

        self.humid_value.pack(pady=10)

        # ================================================
        # BIỂU ĐỒ REALTIME
        # ================================================

        graph_card = tk.Frame(left_panel, bg=CARD)
        graph_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            graph_card,
            text="📈 BIỂU ĐỒ REALTIME",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.figure = Figure(figsize=(8, 4), dpi=100)

        self.ax = self.figure.add_subplot(111)

        self.ax.set_title("Realtime Sensor Data")

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
        # THÔNG TIN HỆ THỐNG
        # ================================================

        info_card = tk.Frame(right_panel, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="THÔNG TIN HỆ THỐNG",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.status_label = tk.Label(
            info_card,
            text="🔴 CHƯA KẾT NỐI",
            font=("Arial", 11, "bold"),
            fg=RED,
            bg=CARD
        )

        self.status_label.pack(anchor="w", padx=15, pady=5)

        self.api_label = tk.Label(
            info_card,
            text=f"API KEY:\n{API_KEY}",
            font=("Arial", 10),
            fg=TEXT,
            bg=CARD,
            justify="left"
        )

        self.api_label.pack(anchor="w", padx=15, pady=10)

        # ================================================
        # NÚT ĐIỀU KHIỂN
        # ================================================

        button_card = tk.Frame(right_panel, bg=CARD)
        button_card.pack(fill="x", pady=10)

        tk.Label(
            button_card,
            text="ĐIỀU KHIỂN",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        send_btn = tk.Button(
            button_card,
            text="GỬI DỮ LIỆU",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            command=self.manual_send
        )

        send_btn.pack(pady=10)

        auto_btn = tk.Button(
            button_card,
            text="AUTO SEND",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            command=self.toggle_auto_send
        )

        auto_btn.pack(pady=10)

        # ================================================
        # LOG HỆ THỐNG
        # ================================================

        log_card = tk.Frame(right_panel, bg=CARD)
        log_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            log_card,
            text="NHẬT KÝ HỆ THỐNG",
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

        self.write_log("Khởi động hệ thống ThingSpeak.")

    # =====================================================
    # TẠO DỮ LIỆU GIẢ LẬP
    # =====================================================

    def generate_sensor_data(self):

        temperature = random.randint(25, 40)

        humidity = random.randint(50, 90)

        return temperature, humidity

    # =====================================================
    # GỬI LÊN THINGSPEAK
    # =====================================================

    def send_to_thingspeak(self, temperature, humidity):

        try:

            payload = {
                "api_key": API_KEY,
                "field1": temperature,
                "field2": humidity
            }

            response = requests.get(
                THINGSPEAK_URL,
                params=payload,
                timeout=5
            )

            if response.status_code == 200:

                self.status_label.config(
                    text="🟢 ĐÃ GỬI THÀNH CÔNG",
                    fg=GREEN
                )

                self.write_log(
                    f"Gửi dữ liệu thành công | Temp={temperature}°C | Humid={humidity}%"
                )

            else:

                self.status_label.config(
                    text="🔴 GỬI THẤT BẠI",
                    fg=RED
                )

                self.write_log("ThingSpeak response lỗi.")

        except Exception as e:

            self.status_label.config(
                text="🔴 MẤT KẾT NỐI INTERNET",
                fg=RED
            )

            self.write_log(str(e))

    # =====================================================
    # GỬI THỦ CÔNG
    # =====================================================

    def manual_send(self):

        temp, humid = self.generate_sensor_data()

        self.temp_value.config(text=f"{temp} °C")

        self.humid_value.config(text=f"{humid} %")

        self.send_to_thingspeak(temp, humid)

        self.update_graph(temp, humid)

    # =====================================================
    # AUTO SEND
    # =====================================================

    def toggle_auto_send(self):

        if not self.auto_running:

            self.auto_running = True

            self.write_log("Bắt đầu AUTO SEND.")

            thread = threading.Thread(
                target=self.auto_send_loop
            )

            thread.daemon = True
            thread.start()

        else:

            self.auto_running = False

            self.write_log("Dừng AUTO SEND.")

    # =====================================================
    # VÒNG LẶP AUTO SEND
    # =====================================================

    def auto_send_loop(self):

        while self.auto_running:

            temp, humid = self.generate_sensor_data()

            self.temp_value.config(text=f"{temp} °C")

            self.humid_value.config(text=f"{humid} %")

            self.send_to_thingspeak(temp, humid)

            self.update_graph(temp, humid)

            # ThingSpeak giới hạn ~15s/update
            time.sleep(15)

    # =====================================================
    # UPDATE GRAPH
    # =====================================================

    def update_graph(self, temp, humid):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.temperature_data.append(temp)

        self.humidity_data.append(humid)

        self.time_data.append(current_time)

        # Giới hạn dữ liệu
        self.temperature_data = self.temperature_data[-10:]
        self.humidity_data = self.humidity_data[-10:]
        self.time_data = self.time_data[-10:]

        self.ax.clear()

        self.ax.plot(
            self.time_data,
            self.temperature_data,
            marker='o',
            label='Temperature'
        )

        self.ax.plot(
            self.time_data,
            self.humidity_data,
            marker='o',
            label='Humidity'
        )

        self.ax.legend()

        self.ax.set_title("Realtime Sensor Data")

        self.canvas.draw()

    # =====================================================
    # GHI LOG
    # =====================================================

    def write_log(self, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            tk.END,
            f"[{current_time}] {message}\n"
        )

        self.log_box.see(tk.END)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ThingSpeakApp(root)

    root.mainloop()
