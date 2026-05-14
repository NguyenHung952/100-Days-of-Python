# ============================================================
#   PHÁT HIỆN CHUYỂN ĐỘNG CAMERA - MODERN EDITION 2026
# ============================================================
#
# CHỨC NĂNG:
#   ✓ Phát hiện chuyển động realtime
#   ✓ Camera streaming
#   ✓ Vẽ khung vùng chuyển động
#   ✓ Chụp ảnh khi phát hiện
#   ✓ Ghi video tự động
#   ✓ Hiển thị FPS
#   ✓ Hiển thị thời gian
#   ✓ Overlay hiện đại
#   ✓ Cảnh báo chuyển động
#   ✓ Lưu log sự kiện
#   ✓ Hỗ trợ Raspberry Pi / Webcam
#
# CÀI ĐẶT:
#   pip install opencv-python numpy
#
# CHẠY:
#   python motion_detection.py
#
# PHÍM TẮT:
#   Q = Thoát
#   S = Chụp ảnh thủ công
#
# ============================================================

import cv2
import numpy as np
import os
import time
from datetime import datetime

# ============================================================
# KHỞI TẠO THƯ MỤC
# ============================================================

IMAGE_FOLDER = "motion_images"
VIDEO_FOLDER = "motion_videos"
LOG_FILE = "motion_log.txt"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 65)
    print("        HỆ THỐNG PHÁT HIỆN CHUYỂN ĐỘNG")
    print("               MODERN EDITION 2026")
    print("=" * 65)

    print("\nCHỨC NĂNG:")

    features = [
        "Live Camera Streaming",
        "Motion Detection",
        "Tự động chụp ảnh",
        "Tự động ghi video",
        "Hiển thị FPS",
        "Hiển thị thời gian",
        "Vẽ vùng chuyển động",
        "Lưu log sự kiện",
        "Overlay hiện đại",
        "Raspberry Pi Compatible"
    ]

    for feature in features:
        print(f"✓ {feature}")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát")
    print("S -> Chụp ảnh thủ công")

    print("\nĐang khởi động hệ thống camera...\n")

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

def draw_text(frame, text, position, color=(0, 255, 0), scale=0.7):

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
    # FRAME ĐẦU TIÊN
    # ========================================================

    ret, frame1 = cap.read()

    if not ret:

        print("❌ Không đọc được frame đầu tiên!")
        return

    frame1 = cv2.flip(frame1, 1)

    # ========================================================
    # VIDEO RECORDING
    # ========================================================

    recording = False
    video_writer = None
    last_motion_time = time.time()

    # ========================================================
    # FPS
    # ========================================================

    prev_time = 0

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        ret, frame2 = cap.read()

        if not ret:

            print("❌ Không đọc được camera!")
            break

        frame2 = cv2.flip(frame2, 1)

        # ====================================================
        # COPY FRAME
        # ====================================================

        display_frame = frame2.copy()

        # ====================================================
        # TÍNH SAI KHÁC
        # ====================================================

        diff = cv2.absdiff(frame1, frame2)

        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        _, threshold = cv2.threshold(
            blur,
            20,
            255,
            cv2.THRESH_BINARY
        )

        dilated = cv2.dilate(threshold, None, iterations=3)

        contours, _ = cv2.findContours(
            dilated,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # ====================================================
        # MOTION FLAG
        # ====================================================

        motion_detected = False

        # ====================================================
        # XỬ LÝ CONTOUR
        # ====================================================

        for contour in contours:

            area = cv2.contourArea(contour)

            # BỎ NHIỄU NHỎ
            if area < 1500:
                continue

            motion_detected = True

            x, y, w, h = cv2.boundingRect(contour)

            # =================================================
            # VẼ KHUNG
            # =================================================

            cv2.rectangle(
                display_frame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            draw_text(
                display_frame,
                "MOTION DETECTED",
                (x, y - 10),
                (0, 0, 255)
            )

        # ====================================================
        # FPS
        # ====================================================

        current_time = time.time()

        fps = 1 / (current_time - prev_time)

        prev_time = current_time

        # ====================================================
        # THÔNG TIN
        # ====================================================

        current_datetime = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        # ====================================================
        # OVERLAY
        # ====================================================

        overlay = display_frame.copy()

        cv2.rectangle(
            overlay,
            (10, 10),
            (420, 180),
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
        # HIỂN THỊ TEXT
        # ====================================================

        draw_text(
            display_frame,
            "MOTION DETECTION SYSTEM",
            (20, 40)
        )

        draw_text(
            display_frame,
            f"FPS: {int(fps)}",
            (20, 75)
        )

        draw_text(
            display_frame,
            current_datetime,
            (20, 110)
        )

        # ====================================================
        # TRẠNG THÁI
        # ====================================================

        if motion_detected:

            draw_text(
                display_frame,
                "STATUS: MOVEMENT DETECTED",
                (20, 145),
                (0, 0, 255)
            )

        else:

            draw_text(
                display_frame,
                "STATUS: SAFE",
                (20, 145),
                (0, 255, 0)
            )

        # ====================================================
        # XỬ LÝ KHI PHÁT HIỆN
        # ====================================================

        if motion_detected:

            last_motion_time = time.time()

            # ================================================
            # GHI LOG
            # ================================================

            write_log("Đã phát hiện chuyển động")

            # ================================================
            # CHỤP ẢNH
            # ================================================

            image_name = datetime.now().strftime(
                "%Y%m%d_%H%M%S.jpg"
            )

            image_path = os.path.join(
                IMAGE_FOLDER,
                image_name
            )

            cv2.imwrite(image_path, display_frame)

            # ================================================
            # GHI VIDEO
            # ================================================

            if not recording:

                video_name = datetime.now().strftime(
                    "%Y%m%d_%H%M%S.mp4"
                )

                video_path = os.path.join(
                    VIDEO_FOLDER,
                    video_name
                )

                height, width, _ = display_frame.shape

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

                video_writer = cv2.VideoWriter(
                    video_path,
                    fourcc,
                    20.0,
                    (width, height)
                )

                recording = True

                print(f"🎥 Đang ghi video: {video_name}")

        # ====================================================
        # GHI VIDEO KHI RECORDING
        # ====================================================

        if recording and video_writer is not None:

            video_writer.write(display_frame)

            # ================================================
            # TỰ DỪNG SAU 5 GIÂY KHÔNG CÓ CHUYỂN ĐỘNG
            # ================================================

            if time.time() - last_motion_time > 5:

                recording = False

                video_writer.release()

                video_writer = None

                print("⏹ Đã dừng ghi video")

        # ====================================================
        # HIỂN THỊ RECORDING
        # ====================================================

        if recording:

            draw_text(
                display_frame,
                "● RECORDING",
                (20, 175),
                (0, 0, 255)
            )

        # ====================================================
        # HIỂN THỊ CAMERA
        # ====================================================

        cv2.imshow(
            "Modern Motion Detection System",
            display_frame
        )

        # ====================================================
        # CẬP NHẬT FRAME
        # ====================================================

        frame1 = frame2.copy()

        # ====================================================
        # BÀN PHÍM
        # ====================================================

        key = cv2.waitKey(1) & 0xFF

        # ====================================================
        # THOÁT
        # ====================================================

        if key == ord('q'):

            print("\nĐang thoát chương trình...")
            break

        # ====================================================
        # CHỤP ẢNH THỦ CÔNG
        # ====================================================

        elif key == ord('s'):

            image_name = datetime.now().strftime(
                "%Y%m%d_%H%M%S_manual.jpg"
            )

            image_path = os.path.join(
                IMAGE_FOLDER,
                image_name
            )

            cv2.imwrite(image_path, display_frame)

            print(f"📸 Đã chụp ảnh: {image_path}")

    # ========================================================
    # GIẢI PHÓNG
    # ========================================================

    cap.release()

    if video_writer is not None:

        video_writer.release()

    cv2.destroyAllWindows()

    print("✅ Đã đóng hệ thống camera!")

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
