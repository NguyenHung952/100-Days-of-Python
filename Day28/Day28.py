# =========================================================
# MQTT CHAT GIỮA 2 THIẾT BỊ
# =========================================================
#
# Tác giả     : ChatGPT
# Ngôn ngữ    : Python
# Giao diện   : Tkinter Modern UI
# Giao thức   : MQTT
#
# =========================================================
# CHỨC NĂNG
# =========================================================
#
# • Chat realtime giữa 2 thiết bị
# • Gửi và nhận tin nhắn MQTT
# • Hiển thị trạng thái kết nối
# • Giao diện hiện đại
# • Tự động reconnect
# • Nhật ký hệ thống
# • Hiển thị thời gian gửi tin
# • Hỗ trợ nhiều topic
# • Có thể mở 2 cửa sổ chat để test
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install paho-mqtt
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python mqtt_chat.py
#
# Sau đó:
# • Mở thêm 1 cửa sổ terminal
# • Chạy lại file lần 2
# • Đặt tên khác nhau
# • Chat realtime giữa 2 thiết bị
#
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import threading
import random

import paho.mqtt.client as mqtt


# =========================================================
# MQTT CONFIG
# =========================================================

BROKER = "broker.emqx.io"
PORT = 1883

# Có thể đổi topic để tạo phòng chat riêng
TOPIC = "smart_home/chat_room_01"

# =========================================================
# MÀU GIAO DIỆN
# =========================================================

BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#f8fafc"
GREEN = "#22c55e"
RED = "#ef4444"
BLUE = "#3b82f6"
GRAY = "#94a3b8"

# =========================================================
# CLASS MQTT CHAT
# =========================================================


class MQTTChatApp:

    def __init__(self, root):

        self.root = root
        self.root.title("MQTT CHAT - SMART DEVICE")
        self.root.geometry("1200x720")
        self.root.configure(bg=BG)

        # =================================================
        # THÔNG TIN USER
        # =================================================

        self.username = f"Device_{random.randint(1000,9999)}"

        self.client_id = f"python-mqtt-{random.randint(0,9999)}"

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="📡 MQTT CHAT REALTIME",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống chat giữa 2 thiết bị bằng MQTT",
            font=("Arial", 11),
            fg=GRAY,
            bg=BG
        )

        subtitle.pack()

        # =================================================
        # KHUNG CHÍNH
        # =================================================

        main_frame = tk.Frame(root, bg=BG)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # =================================================
        # LEFT PANEL
        # =================================================

        left_panel = tk.Frame(main_frame, bg=BG)
        left_panel.pack(side="left", fill="both", expand=True)

        # =================================================
        # RIGHT PANEL
        # =================================================

        right_panel = tk.Frame(main_frame, bg=BG, width=300)
        right_panel.pack(side="right", fill="y", padx=15)

        # =================================================
        # CHAT BOX
        # =================================================

        chat_frame = tk.Frame(left_panel, bg=CARD)
        chat_frame.pack(fill="both", expand=True)

        chat_title = tk.Label(
            chat_frame,
            text="💬 KHUNG CHAT MQTT",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        )

        chat_title.pack(anchor="w", padx=10, pady=10)

        self.chat_box = tk.Text(
            chat_frame,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 11),
            wrap="word"
        )

        self.chat_box.pack(fill="both", expand=True, padx=10, pady=10)

        # =================================================
        # INPUT MESSAGE
        # =================================================

        input_frame = tk.Frame(left_panel, bg=BG)
        input_frame.pack(fill="x", pady=10)

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 13),
            bg="#1e293b",
            fg="white",
            insertbackground="white"
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10),
            ipady=10
        )

        send_btn = tk.Button(
            input_frame,
            text="GỬI",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2,
            command=self.send_message
        )

        send_btn.pack(side="right")

        # =================================================
        # PANEL THÔNG TIN
        # =================================================

        info_card = tk.Frame(right_panel, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="THÔNG TIN THIẾT BỊ",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.user_label = tk.Label(
            info_card,
            text=f"👤 User: {self.username}",
            font=("Arial", 11),
            fg=TEXT,
            bg=CARD
        )

        self.user_label.pack(anchor="w", padx=15, pady=5)

        self.topic_label = tk.Label(
            info_card,
            text=f"📡 Topic:\n{TOPIC}",
            font=("Arial", 10),
            fg=TEXT,
            bg=CARD,
            justify="left"
        )

        self.topic_label.pack(anchor="w", padx=15, pady=5)

        # =================================================
        # TRẠNG THÁI MQTT
        # =================================================

        self.status_label = tk.Label(
            info_card,
            text="🔴 ĐANG KẾT NỐI MQTT...",
            font=("Arial", 11, "bold"),
            fg=RED,
            bg=CARD
        )

        self.status_label.pack(anchor="w", padx=15, pady=10)

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = tk.Frame(right_panel, bg=CARD)
        button_frame.pack(fill="x", pady=15)

        tk.Label(
            button_frame,
            text="ĐIỀU KHIỂN",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        clear_btn = tk.Button(
            button_frame,
            text="XÓA CHAT",
            bg=RED,
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2,
            command=self.clear_chat
        )

        clear_btn.pack(pady=10)

        reconnect_btn = tk.Button(
            button_frame,
            text="RECONNECT MQTT",
            bg=GREEN,
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            height=2,
            command=self.reconnect
        )

        reconnect_btn.pack(pady=10)

        # =================================================
        # LOG SYSTEM
        # =================================================

        self.log_card = tk.Frame(right_panel, bg=CARD)
        self.log_card.pack(fill="both", expand=True)

        tk.Label(
            self.log_card,
            text="NHẬT KÝ HỆ THỐNG",
            font=("Arial", 14, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.log_box = tk.Text(
            self.log_card,
            height=10,
            bg="#111827",
            fg="#facc15",
            font=("Consolas", 10)
        )

        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

        # =================================================
        # MQTT CLIENT
        # =================================================

        self.client = mqtt.Client(
            client_id=self.client_id
        )

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.connect_mqtt()

        self.write_log("Khởi động ứng dụng MQTT Chat.")

        # Enter để gửi tin nhắn
        self.message_entry.bind("<Return>", lambda e: self.send_message())

    # =====================================================
    # CONNECT MQTT
    # =====================================================

    def connect_mqtt(self):

        try:

            self.client.connect(BROKER, PORT)

            thread = threading.Thread(
                target=self.client.loop_forever
            )

            thread.daemon = True
            thread.start()

        except Exception as e:

            messagebox.showerror(
                "MQTT ERROR",
                str(e)
            )

    # =====================================================
    # MQTT CONNECT CALLBACK
    # =====================================================

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:

            self.status_label.config(
                text="🟢 MQTT ĐÃ KẾT NỐI",
                fg=GREEN
            )

            self.client.subscribe(TOPIC)

            self.write_log("Kết nối MQTT thành công.")
            self.write_chat(
                "SYSTEM",
                "Đã kết nối MQTT Broker."
            )

        else:

            self.status_label.config(
                text="🔴 MQTT LỖI KẾT NỐI",
                fg=RED
            )

    # =====================================================
    # NHẬN TIN NHẮN
    # =====================================================

    def on_message(self, client, userdata, msg):

        try:

            message = msg.payload.decode()

            # Không hiện tin nhắn của chính mình
            if not message.startswith(self.username):

                sender, content = message.split(":", 1)

                self.write_chat(sender, content)

                self.write_log(
                    f"Nhận tin nhắn từ {sender}"
                )

        except:
            pass

    # =====================================================
    # MẤT KẾT NỐI
    # =====================================================

    def on_disconnect(self, client, userdata, rc):

        self.status_label.config(
            text="🔴 MQTT ĐÃ NGẮT",
            fg=RED
        )

        self.write_log("Mất kết nối MQTT.")

    # =====================================================
    # GỬI TIN NHẮN
    # =====================================================

    def send_message(self):

        message = self.message_entry.get().strip()

        if message == "":
            return

        full_message = f"{self.username}: {message}"

        self.client.publish(
            TOPIC,
            full_message
        )

        self.write_chat(
            "TÔI",
            message
        )

        self.write_log("Đã gửi tin nhắn.")

        self.message_entry.delete(0, tk.END)

    # =====================================================
    # HIỂN THỊ CHAT
    # =====================================================

    def write_chat(self, sender, message):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.chat_box.insert(
            tk.END,
            f"[{current_time}] {sender}: {message}\n"
        )

        self.chat_box.see(tk.END)

    # =====================================================
    # GHI LOG
    # =====================================================

    def write_log(self, text):

        current_time = datetime.now().strftime("%H:%M:%S")

        self.log_box.insert(
            tk.END,
            f"[{current_time}] {text}\n"
        )

        self.log_box.see(tk.END)

    # =====================================================
    # XÓA CHAT
    # =====================================================

    def clear_chat(self):

        self.chat_box.delete("1.0", tk.END)

        self.write_log("Đã xóa khung chat.")

    # =====================================================
    # RECONNECT
    # =====================================================

    def reconnect(self):

        try:

            self.client.reconnect()

            self.write_log("Đang reconnect MQTT...")

        except Exception as e:

            self.write_log(str(e))


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MQTTChatApp(root)

    root.mainloop()
