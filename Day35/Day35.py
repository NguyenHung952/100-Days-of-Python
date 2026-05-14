# =========================================================
#            QR CODE CAMERA DETECTION SYSTEM
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống nhận diện QR Code bằng camera sử dụng Python
#
# Chức năng:
#   • Nhận diện QR Code realtime
#   • Camera trực tiếp
#   • Hiển thị nội dung QR
#   • Vẽ khung QR Detection
#   • Lưu lịch sử quét
#   • Dashboard hiện đại
#   • Chụp ảnh QR
#   • Nhật ký hệ thống
#   • Auto Scan
#   • Hỗ trợ Webcam / USB Camera
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install opencv-python
# pip install pillow
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python qr_camera.py
#
# =========================================================
#
# PHÍM TẮT:
#
#   Q -> Thoát camera
#   S -> Chụp ảnh
#
# =========================================================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from PIL import Image, ImageTk

import cv2
from cv2 import QRCodeDetector

from datetime import datetime

import threading
import time
import os

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
# CLASS QR APP
# =========================================================

class QRCodeApp:

    def __init__(self, root):

        self.root = root

        self.root.title("QR CODE CAMERA SYSTEM")

        self.root.geometry("1550x900")

        self.root.configure(bg=BG)

        # ================================================
        # CAMERA
        # ================================================

        self.cap = cv2.VideoCapture(0)

        self.detector = QRCodeDetector()

        self.running = False

        self.last_qr = ""

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="📷 QR CODE CAMERA DETECTION",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống nhận diện QR Code bằng Python + OpenCV",
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
        # CAMERA CARD
        # ================================================

        camera_card = tk.Frame(left, bg=CARD)
        camera_card.pack(fill="both", expand=True)

        tk.Label(
            camera_card,
            text="📸 CAMERA LIVE",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.camera_label = tk.Label(
            camera_card,
            bg="black"
        )

        self.camera_label.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ================================================
        # QR RESULT CARD
        # ================================================

        qr_card = tk.Frame(left, bg=CARD)
        qr_card.pack(fill="x", pady=10)

        tk.Label(
            qr_card,
            text="🔍 QR DETECTION RESULT",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.qr_label = tk.Label(
            qr_card,
            text="WAITING FOR QR...",
            font=("Consolas", 16, "bold"),
            fg=GREEN,
            bg=CARD,
            wraplength=1000,
            justify="left"
        )

        self.qr_label.pack(
            anchor="w",
            padx=20,
            pady=15
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

        start_btn = tk.Button(
            control_card,
            text="START CAMERA",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.start_camera
        )

        start_btn.pack(pady=10)

        stop_btn = tk.Button(
            control_card,
            text="STOP CAMERA",
            bg=RED,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.stop_camera
        )

        stop_btn.pack(pady=10)

        capture_btn = tk.Button(
            control_card,
            text="CHỤP ẢNH",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=22,
            height=2,
            command=self.capture_image
        )

        capture_btn.pack(pady=10)

        # ================================================
        # STATUS CARD
        # ================================================

        status_card = tk.Frame(right, bg=CARD)
        status_card.pack(fill="x", pady=10)

        tk.Label(
            status_card,
            text="📌 TRẠNG THÁI",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.status_label = tk.Label(
            status_card,
            text="🟢 CAMERA READY",
            font=("Arial", 18, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.status_label.pack(pady=15)

        # ================================================
        # HISTORY CARD
        # ================================================

        history_card = tk.Frame(right, bg=CARD)
        history_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            history_card,
            text="📜 LỊCH SỬ QR",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.history_box = tk.Text(
            history_card,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 10)
        )

        self.history_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

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

        self.write_log("Khởi động QR Camera System.")

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
    # START CAMERA
    # =====================================================

    def start_camera(self):

        if self.running:
            return

        self.running = True

        self.write_log("Camera started.")

        self.status_label.config(
            text="🟢 CAMERA RUNNING",
            fg=GREEN
        )

        thread = threading.Thread(
            target=self.camera_loop
        )

        thread.daemon = True

        thread.start()

    # =====================================================
    # STOP CAMERA
    # =====================================================

    def stop_camera(self):

        self.running = False

        self.status_label.config(
            text="🔴 CAMERA STOPPED",
            fg=RED
        )

        self.write_log("Camera stopped.")

    # =====================================================
    # CAMERA LOOP
    # =====================================================

    def camera_loop(self):

        while self.running:

            ret, frame = self.cap.read()

            if not ret:

                self.write_log(
                    "Không thể mở camera."
                )

                continue

            # ============================================
            # QR DETECTION
            # ============================================

            data, bbox, _ = self.detector.detectAndDecode(frame)

            if bbox is not None:

                points = bbox.astype(int)

                for i in range(len(points[0])):

                    pt1 = tuple(points[0][i])

                    pt2 = tuple(
                        points[0][(i + 1) % len(points[0])]
                    )

                    cv2.line(
                        frame,
                        pt1,
                        pt2,
                        (0, 255, 0),
                        3
                    )

            # ============================================
            # QR FOUND
            # ============================================

            if data:

                if data != self.last_qr:

                    self.last_qr = data

                    self.qr_label.config(
                        text=f"QR CONTENT:\n{data}"
                    )

                    current_time = datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )

                    self.history_box.insert(
                        tk.END,
                        f"[{current_time}] {data}\n"
                    )

                    self.history_box.see(tk.END)

                    self.write_log(
                        f"Phát hiện QR: {data}"
                    )

            # ============================================
            # FRAME -> TKINTER
            # ============================================

            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(frame)

            img = img.resize((1000, 650))

            imgtk = ImageTk.PhotoImage(image=img)

            self.camera_label.imgtk = imgtk

            self.camera_label.configure(
                image=imgtk
            )

            time.sleep(0.01)

    # =====================================================
    # CAPTURE IMAGE
    # =====================================================

    def capture_image(self):

        ret, frame = self.cap.read()

        if ret:

            if not os.path.exists("captures"):

                os.makedirs("captures")

            filename = datetime.now().strftime(
                "captures/qr_%Y%m%d_%H%M%S.jpg"
            )

            cv2.imwrite(
                filename,
                frame
            )

            self.write_log(
                f"Đã lưu ảnh: {filename}"
            )

            messagebox.showinfo(
                "CAPTURE",
                f"Đã lưu ảnh:\n{filename}"
            )

    # =====================================================
    # CLOSE APP
    # =====================================================

    def on_close(self):

        self.running = False

        self.cap.release()

        cv2.destroyAllWindows()

        self.root.destroy()

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("QR CODE CAMERA SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    print("✅ OpenCV QR Detection")
    print("✅ Webcam Support")
    print("✅ Realtime Detection")
    print("✅ QR Bounding Box")

    print("\n🚀 KHỞI ĐỘNG DASHBOARD...\n")

    root = tk.Tk()

    app = QRCodeApp(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.on_close
    )

    root.mainloop()
