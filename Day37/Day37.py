# =========================================================
#             SERVO CONTROL GUI SYSTEM
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống điều khiển Servo bằng Python GUI hiện đại
#
# Chức năng:
#   • Điều khiển Servo bằng Slider
#   • Hiển thị góc Servo realtime
#   • Dashboard hiện đại
#   • Simulation Mode
#   • Hỗ trợ Raspberry Pi GPIO
#   • Hỗ trợ PCA9685 Servo Driver
#   • Auto Sweep Servo
#   • Nhật ký hệ thống
#   • Servo Animation
#   • Preset góc Servo
#
# =========================================================
# HỖ TRỢ PHẦN CỨNG
# =========================================================
#
# • Raspberry Pi
# • SG90 Servo
# • MG996R Servo
# • PCA9685
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# Chạy Simulation Mode:
#
#   pip install matplotlib
#
# Raspberry Pi GPIO:
#
#   pip install gpiozero
#
# PCA9685:
#
#   pip install adafruit-circuitpython-servokit
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python servo_gui.py
#
# =========================================================
# KẾT NỐI SERVO GPIO
# =========================================================
#
# Servo      -> Raspberry Pi
#
# Đỏ         -> 5V
# Nâu/Đen    -> GND
# Cam/Vàng   -> GPIO18
#
# =========================================================

import tkinter as tk
from tkinter import ttk
from datetime import datetime

import threading
import time
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# =========================================================
# IMPORT GPIO / PCA9685
# =========================================================

SIMULATION_MODE = False

GPIO_READY = False

PCA9685_READY = False

# =========================================================
# GPIO SERVO
# =========================================================

try:

    from gpiozero import AngularServo

    servo = AngularServo(
        18,
        min_angle=0,
        max_angle=180
    )

    GPIO_READY = True

except:
    pass

# =========================================================
# PCA9685 SERVO
# =========================================================

try:

    from adafruit_servokit import ServoKit

    kit = ServoKit(channels=16)

    PCA9685_READY = True

except:
    pass

# =========================================================
# FALLBACK
# =========================================================

if not GPIO_READY and not PCA9685_READY:

    SIMULATION_MODE = True

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

class ServoGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("SERVO CONTROL GUI")

        self.root.geometry("1550x900")

        self.root.configure(bg=BG)

        self.current_angle = 90

        self.auto_mode = False

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="🎛 SERVO CONTROL DASHBOARD",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Điều khiển Servo bằng Python GUI",
            font=("Arial", 11),
            fg="#94a3b8",
            bg=BG
        )

        subtitle.pack()

        # ================================================
        # MAIN
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
            text="📌 TRẠNG THÁI SERVO",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        if SIMULATION_MODE:

            status = "🟡 SIMULATION MODE"
            color = YELLOW

        elif PCA9685_READY:

            status = "🟢 PCA9685 READY"
            color = GREEN

        elif GPIO_READY:

            status = "🟢 GPIO READY"
            color = GREEN

        else:

            status = "🔴 SERVO ERROR"
            color = RED

        self.status_label = tk.Label(
            status_card,
            text=status,
            font=("Arial", 24, "bold"),
            fg=color,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        # ================================================
        # ANGLE CARD
        # ================================================

        angle_card = tk.Frame(left, bg=CARD)
        angle_card.pack(fill="x", pady=10)

        tk.Label(
            angle_card,
            text="📐 GÓC SERVO",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.angle_label = tk.Label(
            angle_card,
            text="90°",
            font=("Arial", 50, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.angle_label.pack(pady=20)

        # ================================================
        # SLIDER
        # ================================================

        self.slider = tk.Scale(
            angle_card,
            from_=0,
            to=180,
            orient="horizontal",
            length=900,
            font=("Arial", 12),
            bg=CARD,
            fg=TEXT,
            troughcolor="#111827",
            highlightthickness=0,
            command=self.update_servo
        )

        self.slider.set(90)

        self.slider.pack(pady=20)

        # ================================================
        # SERVO VISUAL
        # ================================================

        graph_card = tk.Frame(left, bg=CARD)
        graph_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            graph_card,
            text="📊 SERVO VISUALIZATION",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.figure = Figure(
            figsize=(6, 5),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

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

        self.draw_servo_arm(90)

        # ================================================
        # CONTROL CARD
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

        auto_btn = tk.Button(
            control_card,
            text="AUTO SWEEP",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.toggle_auto_mode
        )

        auto_btn.pack(pady=10)

        center_btn = tk.Button(
            control_card,
            text="CENTER 90°",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=lambda: self.set_angle(90)
        )

        center_btn.pack(pady=10)

        zero_btn = tk.Button(
            control_card,
            text="SET 0°",
            bg=YELLOW,
            fg="black",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=lambda: self.set_angle(0)
        )

        zero_btn.pack(pady=10)

        max_btn = tk.Button(
            control_card,
            text="SET 180°",
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=lambda: self.set_angle(180)
        )

        max_btn.pack(pady=10)

        # ================================================
        # INFO CARD
        # ================================================

        info_card = tk.Frame(right, bg=CARD)
        info_card.pack(fill="x", pady=10)

        tk.Label(
            info_card,
            text="⚙ THÔNG TIN SERVO",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        info_text = f"""
• Servo Range: 0° -> 180°
• PWM Control
• GPIO18 Default
• PCA9685 Support
• Realtime GUI
• Auto Sweep Mode

Simulation:
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

        self.write_log("Khởi động Servo GUI System.")

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
    # UPDATE SERVO
    # =====================================================

    def update_servo(self, value):

        angle = int(value)

        self.current_angle = angle

        self.angle_label.config(
            text=f"{angle}°"
        )

        # ================================================
        # GPIO SERVO
        # ================================================

        try:

            if GPIO_READY:

                servo.angle = angle

            elif PCA9685_READY:

                kit.servo[0].angle = angle

        except Exception as e:

            self.write_log(str(e))

        self.draw_servo_arm(angle)

        self.write_log(
            f"Servo Angle = {angle}°"
        )

    # =====================================================
    # SET ANGLE
    # =====================================================

    def set_angle(self, angle):

        self.slider.set(angle)

        self.update_servo(angle)

    # =====================================================
    # DRAW SERVO
    # =====================================================

    def draw_servo_arm(self, angle):

        self.ax.clear()

        self.ax.set_xlim(-1.2, 1.2)

        self.ax.set_ylim(-1.2, 1.2)

        self.ax.set_aspect("equal")

        self.ax.set_title(
            f"Servo Angle = {angle}°"
        )

        rad = math.radians(angle)

        x = math.cos(rad)

        y = math.sin(rad)

        # Servo Arm
        self.ax.plot(
            [0, x],
            [0, y],
            linewidth=5
        )

        # Servo Center
        self.ax.plot(
            0,
            0,
            marker="o",
            markersize=12
        )

        self.canvas.draw()

    # =====================================================
    # AUTO MODE
    # =====================================================

    def toggle_auto_mode(self):

        if not self.auto_mode:

            self.auto_mode = True

            self.write_log(
                "Bắt đầu Auto Sweep."
            )

            thread = threading.Thread(
                target=self.auto_sweep
            )

            thread.daemon = True

            thread.start()

        else:

            self.auto_mode = False

            self.write_log(
                "Dừng Auto Sweep."
            )

    # =====================================================
    # AUTO SWEEP
    # =====================================================

    def auto_sweep(self):

        while self.auto_mode:

            for angle in range(0, 181, 5):

                if not self.auto_mode:
                    break

                self.slider.set(angle)

                self.update_servo(angle)

                time.sleep(0.05)

            for angle in range(180, -1, -5):

                if not self.auto_mode:
                    break

                self.slider.set(angle)

                self.update_servo(angle)

                time.sleep(0.05)

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SERVO CONTROL GUI SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    if SIMULATION_MODE:

        print("⚠ Simulation Mode")

    elif PCA9685_READY:

        print("✅ PCA9685 READY")

    elif GPIO_READY:

        print("✅ GPIO SERVO READY")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = ServoGUI(root)

    root.mainloop()
