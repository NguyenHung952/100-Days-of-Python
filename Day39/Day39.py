# ============================================================
#   CAMERA STREAMING BẰNG OPENCV - PHIÊN BẢN HIỆN ĐẠI 2026
# ============================================================
#
# CHỨC NĂNG:
#   ✓ Live Camera Streaming
#   ✓ Hiển thị FPS
#   ✓ Chụp ảnh nhanh
#   ✓ Ghi video
#   ✓ Hiển thị thời gian thực
#   ✓ Full HD Support
#   ✓ Giao diện hiện đại
#   ✓ Overlay thông tin camera
#   ✓ Tự động tạo thư mục lưu
#   ✓ Hỗ trợ Webcam / USB Camera / Pi Camera
#
# CÀI ĐẶT:
#   pip install opencv-python numpy
#
# CHẠY:
#   python camera_stream.py
#
# PHÍM TẮT:
#   Q  = Thoát
#   S  = Chụp ảnh
#   R  = Bắt đầu/Dừng ghi video
#
# TÁC GIẢ:
#   Modern OpenCV Camera Streaming
#
# ============================================================

import cv2
import os
import time
import numpy as np
from datetime import datetime

# ============================================================
# KHỞI TẠO THƯ MỤC
# ============================================================

IMAGE_FOLDER = "captured_images"
VIDEO_FOLDER = "recorded_videos"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# ============================================================
# HIỂN THỊ GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 60)
    print("        CAMERA STREAMING BẰNG OPENCV")
    print("              PHIÊN BẢN 2026")
    print("=" * 60)

    print("\nCHỨC NĂNG:")
    print("✓ Live Camera Streaming")
    print("✓ Hiển thị FPS")
    print("✓ Chụp ảnh")
    print("✓ Ghi video")
    print("✓ Overlay thông tin")
    print("✓ Hỗ trợ Full HD")
    print("✓ Webcam / USB Camera / Raspberry Pi Camera")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q  -> Thoát chương trình")
    print("S  -> Chụp ảnh")
    print("R  -> Bật/Tắt ghi video")

    print("\nĐang khởi động camera...\n")

# ============================================================
# TẠO TEXT OVERLAY
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
# MAIN CAMERA STREAMING
# ============================================================

def main():

    show_intro()

    # ========================================================
    # MỞ CAMERA
    # ========================================================

    cap = cv2.VideoCapture(0)

    # ========================================================
    # THIẾT LẬP ĐỘ PHÂN GIẢI
    # ========================================================

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # ========================================================
    # KIỂM TRA CAMERA
    # ========================================================

    if not cap.isOpened():

        print("❌ Không thể mở camera!")
        return

    print("✅ Camera đã kết nối thành công!")

    # ========================================================
    # FPS
    # ========================================================

    prev_time = 0

    # ========================================================
    # VIDEO RECORDING
    # ========================================================

    recording = False
    video_writer = None

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        success, frame = cap.read()

        if not success:

            print("❌ Không đọc được frame từ camera!")
            break

        # ====================================================
        # LẬT KHUNG HÌNH
        # ====================================================

        frame = cv2.flip(frame, 1)

        # ====================================================
        # TÍNH FPS
        # ====================================================

        current_time = time.time()

        fps = 1 / (current_time - prev_time)

        prev_time = current_time

        fps_text = f"FPS: {int(fps)}"

        # ====================================================
        # THỜI GIAN HIỆN TẠI
        # ====================================================

        current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # ====================================================
        # THÔNG TIN CAMERA
        # ====================================================

        height, width, _ = frame.shape

        resolution_text = f"Resolution: {width}x{height}"

        # ====================================================
        # OVERLAY PANEL
        # ====================================================

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (10, 10),
            (380, 170),
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
        # HIỂN THỊ TEXT
        # ====================================================

        draw_text(frame, "CAMERA STREAMING SYSTEM", (20, 40))
        draw_text(frame, fps_text, (20, 70))
        draw_text(frame, resolution_text, (20, 100))
        draw_text(frame, current_datetime, (20, 130))

        # ====================================================
        # HIỂN THỊ TRẠNG THÁI RECORDING
        # ====================================================

        if recording:

            draw_text(
                frame,
                "● RECORDING",
                (20, 160),
                (0, 0, 255)
            )

        # ====================================================
        # GHI VIDEO
        # ====================================================

        if recording and video_writer is not None:

            video_writer.write(frame)

        # ====================================================
        # HIỂN THỊ CAMERA
        # ====================================================

        cv2.imshow(
            "OpenCV Camera Streaming - Modern Edition",
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
                IMAGE_FOLDER,
                filename
            )

            cv2.imwrite(filepath, frame)

            print(f"📸 Đã chụp ảnh: {filepath}")

        # ====================================================
        # RECORD VIDEO
        # ====================================================

        elif key == ord('r'):

            if not recording:

                filename = datetime.now().strftime(
                    "%Y%m%d_%H%M%S.mp4"
                )

                filepath = os.path.join(
                    VIDEO_FOLDER,
                    filename
                )

                fourcc = cv2.VideoWriter_fourcc(*'mp4v')

                video_writer = cv2.VideoWriter(
                    filepath,
                    fourcc,
                    20.0,
                    (width, height)
                )

                recording = True

                print(f"🎥 Bắt đầu ghi video: {filepath}")

            else:

                recording = False

                if video_writer is not None:

                    video_writer.release()

                print("⏹ Đã dừng ghi video")

    # ========================================================
    # GIẢI PHÓNG
    # ========================================================

    cap.release()

    if video_writer is not None:

        video_writer.release()

    cv2.destroyAllWindows()

    print("✅ Đã đóng camera thành công!")

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n⚠ Chương trình đã dừng bởi người dùng")

    except Exception as e:

        print(f"\n❌ Lỗi: {e}")
