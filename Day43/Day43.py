# ============================================================
#   SMART PARKING SIMULATION SYSTEM
# ============================================================
#
# PHIÊN BẢN:
#   Smart Parking Modern Edition 2026
#
# CHỨC NĂNG:
#   ✓ Mô phỏng bãi đỗ xe thông minh
#   ✓ Camera streaming realtime
#   ✓ Phát hiện xe bằng computer vision
#   ✓ Đếm slot còn trống
#   ✓ Hiển thị slot đã đầy
#   ✓ Dashboard hiện đại
#   ✓ Hiển thị FPS
#   ✓ Snapshot hệ thống
#   ✓ Logging hoạt động
#   ✓ Hỗ trợ Raspberry Pi
#
# CÔNG NGHỆ:
#   - OpenCV
#   - Computer Vision
#   - Motion Detection
#   - Parking Slot Detection
#
# CÀI ĐẶT:
#   pip install opencv-python numpy
#
# CHẠY:
#   python smart_parking.py
#
# PHÍM:
#   Q = Thoát
#   S = Chụp ảnh
#
# ============================================================

import cv2
import numpy as np
import os
import time
from datetime import datetime

# ============================================================
# THƯ MỤC
# ============================================================

SNAPSHOT_FOLDER = "parking_snapshots"
LOG_FILE = "parking_log.txt"

os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

# ============================================================
# CẤU HÌNH SLOT ĐỖ XE
# ============================================================

PARKING_SLOTS = [

    # x, y, width, height

    (50, 120, 120, 200),
    (200, 120, 120, 200),
    (350, 120, 120, 200),
    (500, 120, 120, 200),

    (700, 120, 120, 200),
    (850, 120, 120, 200),
    (1000, 120, 120, 200)

]

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 70)
    print("            SMART PARKING SYSTEM")
    print("             MODERN EDITION 2026")
    print("=" * 70)

    features = [

        "Realtime Camera Streaming",
        "Parking Slot Detection",
        "Vehicle Detection",
        "Available Slot Counter",
        "Modern Dashboard UI",
        "FPS Monitor",
        "Snapshot Capture",
        "System Logging",
        "Raspberry Pi Compatible",
        "Computer Vision Simulation"
    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát")
    print("S -> Chụp ảnh")

    print("\nĐang khởi động Smart Parking...\n")

# ============================================================
# GHI LOG
# ============================================================

def write_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(f"[{timestamp}] {message}\n")

# ============================================================
# VẼ TEXT
# ============================================================

def draw_text(frame, text, position,
              color=(0, 255, 0), scale=0.7):

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        2,
        cv2.LINE_AA
    )

# ============================================================
# KIỂM TRA SLOT TRỐNG
# ============================================================

def check_parking_slot(frame, slot):

    x, y, w, h = slot

    roi = frame[y:y+h, x:x+w]

    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        3
    )

    threshold = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        25,
        16
    )

    count = cv2.countNonZero(threshold)

    # ========================================================
    # GIÁ TRỊ THỰC NGHIỆM
    # ========================================================

    if count < 8000:

        return True

    return False

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    # ========================================================
    # CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():

        print("❌ Không mở được camera!")
        return

    print("✅ Camera đã kết nối thành công!")

    # ========================================================
    # FPS
    # ========================================================

    prev_time = 0

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:

            print("❌ Không đọc được camera!")
            break

        # ====================================================
        # FLIP FRAME
        # ====================================================

        frame = cv2.flip(frame, 1)

        display_frame = frame.copy()

        # ====================================================
        # ĐẾM SLOT
        # ====================================================

        free_slots = 0
        occupied_slots = 0

        # ====================================================
        # DUYỆT SLOT
        # ====================================================

        for index, slot in enumerate(PARKING_SLOTS):

            x, y, w, h = slot

            is_free = check_parking_slot(
                frame,
                slot
            )

            # ================================================
            # SLOT TRỐNG
            # ================================================

            if is_free:

                color = (0, 255, 0)

                status = "EMPTY"

                free_slots += 1

            # ================================================
            # SLOT CÓ XE
            # ================================================

            else:

                color = (0, 0, 255)

                status = "OCCUPIED"

                occupied_slots += 1

            # ================================================
            # VẼ KHUNG SLOT
            # ================================================

            cv2.rectangle(
                display_frame,
                (x, y),
                (x + w, y + h),
                color,
                3
            )

            draw_text(
                display_frame,
                f"P{index+1}",
                (x + 10, y + 30),
                color
            )

            draw_text(
                display_frame,
                status,
                (x + 10, y + 60),
                color,
                0.6
            )

        # ====================================================
        # FPS
        # ====================================================

        current_time = time.time()

        fps = 1 / (current_time - prev_time)

        prev_time = current_time

        # ====================================================
        # OVERLAY
        # ====================================================

        overlay = display_frame.copy()

        cv2.rectangle(
            overlay,
            (10, 10),
            (450, 250),
            (0, 0, 0),
            -1
        )

        alpha = 0.5

        display_frame = cv2.addWeighted(
            overlay,
            alpha,
            display_frame,
            1 - alpha,
            0
        )

        # ====================================================
        # THỜI GIAN
        # ====================================================

        current_datetime = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        total_slots = len(PARKING_SLOTS)

        # ====================================================
        # HIỂN THỊ INFO
        # ====================================================

        draw_text(
            display_frame,
            "SMART PARKING SYSTEM",
            (20, 40)
        )

        draw_text(
            display_frame,
            f"Total Slots: {total_slots}",
            (20, 80),
            (255, 255, 255)
        )

        draw_text(
            display_frame,
            f"Available: {free_slots}",
            (20, 120),
            (0, 255, 0)
        )

        draw_text(
            display_frame,
            f"Occupied: {occupied_slots}",
            (20, 160),
            (0, 0, 255)
        )

        draw_text(
            display_frame,
            f"FPS: {int(fps)}",
            (20, 200),
            (255, 255, 0)
        )

        draw_text(
            display_frame,
            current_datetime,
            (20, 240),
            (0, 255, 255),
            0.6
        )

        # ====================================================
        # CẢNH BÁO FULL
        # ====================================================

        if free_slots == 0:

            draw_text(
                display_frame,
                "⚠ PARKING FULL",
                (850, 60),
                (0, 0, 255),
                1
            )

        # ====================================================
        # GHI LOG
        # ====================================================

        write_log(
            f"Free={free_slots} | Occupied={occupied_slots}"
        )

        # ====================================================
        # CAMERA VIEW
        # ====================================================

        cv2.imshow(
            "Smart Parking Simulation System",
            display_frame
        )

        # ====================================================
        # PHÍM
        # ====================================================

        key = cv2.waitKey(1) & 0xFF

        # ====================================================
        # THOÁT
        # ====================================================

        if key == ord('q'):

            print("\nĐang thoát hệ thống...")
            break

        # ====================================================
        # CHỤP ẢNH
        # ====================================================

        elif key == ord('s'):

            filename = datetime.now().strftime(
                "%Y%m%d_%H%M%S.jpg"
            )

            filepath = os.path.join(
                SNAPSHOT_FOLDER,
                filename
            )

            cv2.imwrite(
                filepath,
                display_frame
            )

            print(f"📸 Đã lưu ảnh: {filepath}")

    # ========================================================
    # GIẢI PHÓNG
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    print("✅ Đã đóng Smart Parking System!")

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n⚠ Chương trình đã dừng")

    except Exception as e:

        print(f"\n❌ Lỗi: {e}")
