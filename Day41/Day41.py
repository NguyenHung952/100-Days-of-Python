# ============================================================
#   HỆ THỐNG ĐẾM NGƯỜI BẰNG COMPUTER VISION
# ============================================================
#
# PHIÊN BẢN:
#   Modern AI Edition 2026
#
# CHỨC NĂNG:
#   ✓ Đếm số người realtime
#   ✓ Nhận diện người bằng AI
#   ✓ Camera Streaming
#   ✓ Hiển thị FPS
#   ✓ Hiển thị tổng số người
#   ✓ Vẽ khung người
#   ✓ Overlay giao diện hiện đại
#   ✓ Snapshot tự động
#   ✓ Lưu log hệ thống
#   ✓ Hỗ trợ Raspberry Pi / Webcam
#
# CÔNG NGHỆ:
#   - OpenCV
#   - HOG Descriptor
#   - SVM Person Detector
#
# CÀI ĐẶT:
#   pip install opencv-python numpy
#
# CHẠY:
#   python people_counter.py
#
# PHÍM TẮT:
#   Q = Thoát
#   S = Chụp ảnh
#
# ============================================================

import cv2
import numpy as np
import time
import os
from datetime import datetime

# ============================================================
# THƯ MỤC
# ============================================================

SNAPSHOT_FOLDER = "people_snapshots"
LOG_FILE = "people_counter_log.txt"

os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 65)
    print("        HỆ THỐNG ĐẾM NGƯỜI AI")
    print("          COMPUTER VISION 2026")
    print("=" * 65)

    features = [
        "Realtime People Detection",
        "AI Human Recognition",
        "People Counter",
        "FPS Monitoring",
        "Overlay Modern UI",
        "Snapshot Capture",
        "Raspberry Pi Compatible",
        "OpenCV HOG + SVM",
        "Live Camera Streaming",
        "Automatic Logging"
    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát chương trình")
    print("S -> Chụp ảnh")

    print("\nĐang khởi động hệ thống AI...\n")

# ============================================================
# GHI LOG
# ============================================================

def write_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    # KHỞI TẠO AI DETECTOR
    # ========================================================

    print("🔄 Đang tải AI Person Detector...")

    hog = cv2.HOGDescriptor()

    hog.setSVMDetector(
        cv2.HOGDescriptor_getDefaultPeopleDetector()
    )

    print("✅ AI Detector đã sẵn sàng!")

    # ========================================================
    # CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():

        print("❌ Không thể mở camera!")
        return

    print("✅ Camera đã kết nối thành công!")

    # ========================================================
    # FPS
    # ========================================================

    prev_time = 0

    # ========================================================
    # BIẾN ĐẾM
    # ========================================================

    max_people = 0

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        ret, frame = cap.read()

        if not ret:

            print("❌ Không đọc được camera!")
            break

        # ====================================================
        # LẬT FRAME
        # ====================================================

        frame = cv2.flip(frame, 1)

        # ====================================================
        # RESIZE TĂNG TỐC
        # ====================================================

        frame = cv2.resize(frame, (960, 540))

        # ====================================================
        # DETECT NGƯỜI
        # ====================================================

        boxes, weights = hog.detectMultiScale(
            frame,
            winStride=(8, 8),
            padding=(8, 8),
            scale=1.05
        )

        # ====================================================
        # ĐẾM NGƯỜI
        # ====================================================

        people_count = len(boxes)

        # ====================================================
        # LƯU MAX
        # ====================================================

        if people_count > max_people:

            max_people = people_count

        # ====================================================
        # VẼ KHUNG
        # ====================================================

        for (x, y, w, h) in boxes:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            draw_text(
                frame,
                "PERSON",
                (x, y - 10),
                (0, 255, 0)
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

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (10, 10),
            (420, 220),
            (0, 0, 0),
            -1
        )

        alpha = 0.5

        frame = cv2.addWeighted(
            overlay,
            alpha,
            frame,
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
            frame,
            "AI PEOPLE COUNTER SYSTEM",
            (20, 40)
        )

        draw_text(
            frame,
            f"People Count: {people_count}",
            (20, 80),
            (0, 255, 255)
        )

        draw_text(
            frame,
            f"Maximum Count: {max_people}",
            (20, 120),
            (255, 255, 0)
        )

        draw_text(
            frame,
            f"FPS: {int(fps)}",
            (20, 160)
        )

        draw_text(
            frame,
            current_datetime,
            (20, 200)
        )

        # ====================================================
        # CẢNH BÁO ĐÔNG NGƯỜI
        # ====================================================

        if people_count >= 5:

            draw_text(
                frame,
                "⚠ CROWD DETECTED",
                (650, 40),
                (0, 0, 255),
                1
            )

        # ====================================================
        # GHI LOG
        # ====================================================

        write_log(f"So nguoi hien tai: {people_count}")

        # ====================================================
        # HIỂN THỊ CAMERA
        # ====================================================

        cv2.imshow(
            "AI People Counter System",
            frame
        )

        # ====================================================
        # ĐỌC PHÍM
        # ====================================================

        key = cv2.waitKey(1) & 0xFF

        # ====================================================
        # THOÁT
        # ====================================================

        if key == ord('q'):

            print("\nĐang thoát chương trình...")
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

            cv2.imwrite(filepath, frame)

            print(f"📸 Đã lưu ảnh: {filepath}")

    # ========================================================
    # GIẢI PHÓNG
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    print("✅ Đã đóng hệ thống AI!")

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
