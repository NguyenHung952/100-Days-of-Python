# =========================================================
#           HỆ THỐNG ĐIỂM DANH BẰNG QR CODE
# =========================================================
#
# MÔ TẢ:
# ---------------------------------------------------------
# Hệ thống điểm danh bằng QR Code sử dụng Python
#
# Chức năng:
#   • Quét QR Code realtime bằng camera
#   • Điểm danh tự động
#   • Lưu dữ liệu SQLite
#   • Hiển thị danh sách điểm danh
#   • Chống điểm danh trùng
#   • Dashboard hiện đại
#   • Xuất file CSV
#   • Chụp ảnh camera
#   • Nhật ký hệ thống
#   • Camera realtime OpenCV
#
# =========================================================
# CÀI THƯ VIỆN
# =========================================================
#
# pip install opencv-python pillow pandas
#
# =========================================================
# CHẠY CHƯƠNG TRÌNH
# =========================================================
#
# python qr_attendance.py
#
# =========================================================
#
# QR DEMO:
#
#   STUDENT001
#   STUDENT002
#   STUDENT003
#
# Có thể dùng điện thoại tạo QR:
# https://www.qr-code-generator.com/
#
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image, ImageTk

import cv2
from cv2 import QRCodeDetector

from datetime import datetime

import sqlite3
import pandas as pd

import threading
import os
import time

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
# DATABASE
# =========================================================

conn = sqlite3.connect("attendance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_id TEXT,

    date TEXT,

    time TEXT
)
""")

conn.commit()

# =========================================================
# CLASS APP
# =========================================================

class QRAttendanceApp:

    def __init__(self, root):

        self.root = root

        self.root.title("QR ATTENDANCE SYSTEM")

        self.root.geometry("1600x900")

        self.root.configure(bg=BG)

        # ================================================
        # CAMERA
        # ================================================

        self.cap = cv2.VideoCapture(0)

        self.detector = QRCodeDetector()

        self.running = False

        self.last_scan = ""

        # ================================================
        # HEADER
        # ================================================

        header = tk.Frame(root, bg=BG)
        header.pack(fill="x", pady=10)

        title = tk.Label(
            header,
            text="📷 QR ATTENDANCE SYSTEM",
            font=("Arial", 24, "bold"),
            fg=TEXT,
            bg=BG
        )

        title.pack()

        subtitle = tk.Label(
            header,
            text="Hệ thống điểm danh bằng QR Code",
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
        # LEFT
        # ================================================

        left = tk.Frame(main, bg=BG)
        left.pack(side="left", fill="both", expand=True)

        # ================================================
        # RIGHT
        # ================================================

        right = tk.Frame(main, bg=BG, width=380)
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
        # RESULT CARD
        # ================================================

        result_card = tk.Frame(left, bg=CARD)
        result_card.pack(fill="x", pady=10)

        tk.Label(
            result_card,
            text="🪪 KẾT QUẢ ĐIỂM DANH",
            font=("Arial", 16, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(anchor="w", padx=15, pady=10)

        self.result_label = tk.Label(
            result_card,
            text="WAITING FOR QR...",
            font=("Consolas", 18, "bold"),
            fg=GREEN,
            bg=CARD
        )

        self.result_label.pack(
            padx=20,
            pady=20
        )

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

        start_btn = tk.Button(
            control_card,
            text="START CAMERA",
            bg=GREEN,
            fg="white",
            font=("Arial", 12, "bold"),
            width=24,
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
            width=24,
            height=2,
            command=self.stop_camera
        )

        stop_btn.pack(pady=10)

        export_btn = tk.Button(
            control_card,
            text="EXPORT CSV",
            bg=BLUE,
            fg="white",
            font=("Arial", 12, "bold"),
            width=24,
            height=2,
            command=self.export_csv
        )

        export_btn.pack(pady=10)

        clear_btn = tk.Button(
            control_card,
            text="XÓA ĐIỂM DANH",
            bg=YELLOW,
            fg="black",
            font=("Arial", 12, "bold"),
            width=24,
            height=2,
            command=self.clear_attendance
        )

        clear_btn.pack(pady=10)

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
        # ATTENDANCE LIST
        # ================================================

        attendance_card = tk.Frame(right, bg=CARD)
        attendance_card.pack(fill="both", expand=True, pady=10)

        tk.Label(
            attendance_card,
            text="📋 DANH SÁCH ĐIỂM DANH",
            font=("Arial", 15, "bold"),
            fg=TEXT,
            bg=CARD
        ).pack(pady=10)

        self.attendance_box = tk.Text(
            attendance_card,
            bg="#111827",
            fg="#22c55e",
            font=("Consolas", 10)
        )

        self.attendance_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

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

        self.write_log("Khởi động QR Attendance System.")

        self.load_attendance()

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

        self.status_label.config(
            text="🟢 CAMERA RUNNING",
            fg=GREEN
        )

        self.write_log("Camera started.")

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
                continue

            # ============================================
            # QR DETECT
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

                if data != self.last_scan:

                    self.last_scan = data

                    self.mark_attendance(data)

            # ============================================
            # SHOW FRAME
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
    # MARK ATTENDANCE
    # =====================================================

    def mark_attendance(self, student_id):

        today = datetime.now().strftime("%d/%m/%Y")

        current_time = datetime.now().strftime("%H:%M:%S")

        # Check duplicate
        cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id=? AND date=?
        """, (student_id, today))

        result = cursor.fetchone()

        if result:

            self.result_label.config(
                text=f"⚠ ĐÃ ĐIỂM DANH:\n{student_id}",
                fg=YELLOW
            )

            self.write_log(
                f"Trùng điểm danh: {student_id}"
            )

            return

        # Insert database
        cursor.execute("""
        INSERT INTO attendance(student_id,date,time)
        VALUES(?,?,?)
        """, (
            student_id,
            today,
            current_time
        ))

        conn.commit()

        self.result_label.config(
            text=f"✅ ĐIỂM DANH THÀNH CÔNG:\n{student_id}",
            fg=GREEN
        )

        self.write_log(
            f"Điểm danh thành công: {student_id}"
        )

        self.load_attendance()

    # =====================================================
    # LOAD ATTENDANCE
    # =====================================================

    def load_attendance(self):

        self.attendance_box.delete(
            "1.0",
            tk.END
        )

        cursor.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        for row in rows:

            text = (
                f"ID={row[0]} | "
                f"STUDENT={row[1]} | "
                f"DATE={row[2]} | "
                f"TIME={row[3]}\n"
            )

            self.attendance_box.insert(
                tk.END,
                text
            )

    # =====================================================
    # EXPORT CSV
    # =====================================================

    def export_csv(self):

        cursor.execute("""
        SELECT * FROM attendance
        """)

        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "ID",
                "STUDENT_ID",
                "DATE",
                "TIME"
            ]
        )

        filename = datetime.now().strftime(
            "attendance_%Y%m%d_%H%M%S.csv"
        )

        df.to_csv(
            filename,
            index=False
        )

        self.write_log(
            f"Đã export CSV: {filename}"
        )

        messagebox.showinfo(
            "EXPORT",
            f"Đã lưu file:\n{filename}"
        )

    # =====================================================
    # CLEAR ATTENDANCE
    # =====================================================

    def clear_attendance(self):

        confirm = messagebox.askyesno(
            "CONFIRM",
            "Xóa toàn bộ dữ liệu điểm danh?"
        )

        if confirm:

            cursor.execute("""
            DELETE FROM attendance
            """)

            conn.commit()

            self.load_attendance()

            self.write_log(
                "Đã xóa dữ liệu điểm danh."
            )

    # =====================================================
    # CLOSE APP
    # =====================================================

    def on_close(self):

        self.running = False

        self.cap.release()

        conn.close()

        cv2.destroyAllWindows()

        self.root.destroy()

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("QR ATTENDANCE SYSTEM")
    print("=" * 60)

    print("\n📌 THÔNG TIN")

    print("✅ OpenCV QR Detection")
    print("✅ SQLite Attendance Database")
    print("✅ CSV Export")
    print("✅ Duplicate Check")
    print("✅ Webcam Support")

    print("\n🚀 KHỞI ĐỘNG HỆ THỐNG...\n")

    root = tk.Tk()

    app = QRAttendanceApp(root)

    root.protocol(
        "WM_DELETE_WINDOW",
        app.on_close
    )

    root.mainloop()
