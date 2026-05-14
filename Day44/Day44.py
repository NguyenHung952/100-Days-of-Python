# ============================================================
#   AI NHẬN DIỆN KHUÔN MẶT CƠ BẢN
# ============================================================
#
# PHIÊN BẢN:
#   Modern Face Recognition Edition 2026
#
# CHỨC NĂNG:
#   ✓ Camera Streaming realtime
#   ✓ AI Face Detection
#   ✓ Nhận diện khuôn mặt
#   ✓ Vẽ khung khuôn mặt
#   ✓ Hiển thị FPS
#   ✓ Snapshot khuôn mặt
#   ✓ Overlay hiện đại
#   ✓ Logging hệ thống
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Hỗ trợ Webcam USB
#
# CÔNG NGHỆ:
#   - OpenCV
#   - Haar Cascade
#   - Computer Vision
#
# CÀI ĐẶT:
#   pip install opencv-python numpy
#
# CHẠY:
#   python face_recognition_basic.py
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

SNAPSHOT_FOLDER = "face_snapshots"
LOG_FILE = "face_recognition_log.txt"

os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 70)
    print("          AI FACE RECOGNITION SYSTEM")
    print("           MODERN EDITION 2026")
    print("=" * 70)

    features = [

        "Realtime Camera Streaming",
        "AI Face Detection",
        "Face Recognition Basic",
        "Modern Dashboard UI",
        "FPS Monitor",
        "Face Snapshot",
        "System Logging",
        "OpenCV Haar Cascade",
        "Raspberry Pi Compatible",
        "Computer Vision System"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát")
    print("S -> Chụp ảnh")

    print("\nĐang khởi động AI Face Recognition...\n")

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
# MAIN
# ============================================================

def main():

    show_intro()

    # ========================================================
    # LOAD HAAR CASCADE
    # ========================================================

    print("🔄 Đang tải AI Face Detector...")

    face_cascade = cv2.CascadeClassifier(

        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"

    )

    if face_cascade.empty():

        print("❌ Không tải được Haar Cascade!")
        return

    print("✅ AI Face Detector đã sẵn sàng!")

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
    # MAX FACE
    # ========================================================

    max_faces = 0

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:

            print("❌ Không đọc được frame!")
            break

        # ====================================================
        # FLIP FRAME
        # ====================================================

        frame = cv2.flip(frame, 1)

        display_frame = frame.copy()

        # ====================================================
        # CHUYỂN GRAY
        # ====================================================

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # ====================================================
        # DETECT FACE
        # ====================================================

        faces = face_cascade.detectMultiScale(

            gray,

            scaleFactor=1.1,

            minNeighbors=5,

            minSize=(60, 60)

        )

        # ====================================================
        # ĐẾM KHUÔN MẶT
        # ====================================================

        face_count = len(faces)

        if face_count > max_faces:

            max_faces = face_count

        # ====================================================
        # VẼ KHUNG KHUÔN MẶT
        # ====================================================

        for (x, y, w, h) in faces:

            # ================================================
            # RECTANGLE
            # ================================================

            cv2.rectangle(
                display_frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                3
            )

            # ================================================
            # LABEL
            # ================================================

            draw_text(
                display_frame,
                "FACE DETECTED",
                (x, y - 10),
                (0, 255, 0)
            )

            # ================================================
            # FACE CENTER
            # ================================================

            center_x = x + w // 2
            center_y = y + h // 2

            cv2.circle(
                display_frame,
                (center_x, center_y),
                4,
                (0, 0, 255),
                -1
            )

        # ====================================================
        # FPS
        # ====================================================

        current_time = time.time()

        fps = 1 / (current_time - prev_time)

        prev_time = current_time

        # ====================================================
        # OVERLAY DASHBOARD
        # ====================================================

        overlay = display_frame.copy()

        cv2.rectangle(
            overlay,
            (10, 10),
            (470, 250),
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

        # ====================================================
        # HIỂN THỊ THÔNG TIN
        # ====================================================

        draw_text(
            display_frame,
            "AI FACE RECOGNITION SYSTEM",
            (20, 40)
        )

        draw_text(
            display_frame,
            f"Faces Detected: {face_count}",
            (20, 80),
            (0, 255, 255)
        )

        draw_text(
            display_frame,
            f"Maximum Faces: {max_faces}",
            (20, 120),
            (255, 255, 0)
        )

        draw_text(
            display_frame,
            f"FPS: {int(fps)}",
            (20, 160),
            (0, 255, 0)
        )

        draw_text(
            display_frame,
            current_datetime,
            (20, 200),
            (255, 255, 255),
            0.6
        )

        draw_text(
            display_frame,
            "Status: ACTIVE",
            (20, 240),
            (0, 255, 0)
        )

        # ====================================================
        # CẢNH BÁO NHIỀU NGƯỜI
        # ====================================================

        if face_count >= 3:

            draw_text(
                display_frame,
                "⚠ MULTIPLE FACES DETECTED",
                (700, 50),
                (0, 0, 255),
                1
            )

        # ====================================================
        # GHI LOG
        # ====================================================

        write_log(
            f"Faces Detected: {face_count}"
        )

        # ====================================================
        # HIỂN THỊ CAMERA
        # ====================================================

        cv2.imshow(
            "AI Face Recognition System",
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

    print("✅ Đã đóng AI Face Recognition!")

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
