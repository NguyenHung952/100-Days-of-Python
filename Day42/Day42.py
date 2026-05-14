# ============================================================
#   HỆ THỐNG NHẬN DIỆN BIỂN SỐ XE CƠ BẢN
# ============================================================
#
# PHIÊN BẢN:
#   Modern OpenCV Edition 2026
#
# CHỨC NĂNG:
#   ✓ Camera Streaming realtime
#   ✓ Phát hiện biển số xe
#   ✓ OCR đọc ký tự biển số
#   ✓ Chụp ảnh biển số
#   ✓ Lưu biển số vào file
#   ✓ Hiển thị FPS
#   ✓ Overlay hiện đại
#   ✓ Hỗ trợ Webcam / Raspberry Pi
#   ✓ Tự động lưu ảnh biển số
#   ✓ Logging hệ thống
#
# CÔNG NGHỆ:
#   - OpenCV
#   - Tesseract OCR
#   - Contour Detection
#   - Image Processing
#
# CÀI ĐẶT:
#
#   pip install opencv-python numpy pytesseract
#
# WINDOWS:
#   Cài Tesseract:
#   https://github.com/UB-Mannheim/tesseract/wiki
#
# LINUX:
#   sudo apt install tesseract-ocr
#
# CHẠY:
#   python license_plate_system.py
#
# PHÍM:
#   Q = Thoát
#   S = Chụp ảnh thủ công
#
# ============================================================

import cv2
import pytesseract
import numpy as np
import os
import time
from datetime import datetime

# ============================================================
# WINDOWS TESSERACT PATH
# ============================================================

# Nếu dùng Windows:
# Bỏ comment và sửa đúng đường dẫn

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )

# ============================================================
# THƯ MỤC
# ============================================================

PLATE_FOLDER = "detected_plates"
LOG_FILE = "license_plate_log.txt"

os.makedirs(PLATE_FOLDER, exist_ok=True)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 70)
    print("       HỆ THỐNG NHẬN DIỆN BIỂN SỐ XE")
    print("          MODERN OPENCV EDITION 2026")
    print("=" * 70)

    features = [
        "Realtime Camera Streaming",
        "License Plate Detection",
        "OCR Character Recognition",
        "Automatic Snapshot",
        "FPS Monitor",
        "Overlay Modern UI",
        "Logging System",
        "Raspberry Pi Compatible",
        "OpenCV + OCR",
        "Vehicle Monitoring"
    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát")
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
# TIỀN XỬ LÝ ẢNH
# ============================================================

def preprocess_plate(plate_img):

    gray = cv2.cvtColor(
        plate_img,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    threshold = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return threshold

# ============================================================
# OCR BIỂN SỐ
# ============================================================

def read_plate_text(plate_img):

    processed = preprocess_plate(plate_img)

    config = "--psm 7"

    text = pytesseract.image_to_string(
        processed,
        config=config
    )

    # ========================================================
    # LỌC KÝ TỰ
    # ========================================================

    text = "".join(
        char for char in text
        if char.isalnum() or char == '-'
    )

    return text

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

    print("✅ Camera đã kết nối!")

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

            print("❌ Không đọc được frame!")
            break

        # ====================================================
        # LẬT FRAME
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
        # LÀM MỜ
        # ====================================================

        blur = cv2.bilateralFilter(
            gray,
            11,
            17,
            17
        )

        # ====================================================
        # CANNY EDGE
        # ====================================================

        edged = cv2.Canny(
            blur,
            30,
            200
        )

        # ====================================================
        # FIND CONTOURS
        # ====================================================

        contours, _ = cv2.findContours(
            edged.copy(),
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True
        )[:10]

        plate_text = ""

        # ====================================================
        # TÌM BIỂN SỐ
        # ====================================================

        for contour in contours:

            perimeter = cv2.arcLength(
                contour,
                True
            )

            approx = cv2.approxPolyDP(
                contour,
                0.018 * perimeter,
                True
            )

            # =================================================
            # HÌNH CHỮ NHẬT 4 CẠNH
            # =================================================

            if len(approx) == 4:

                x, y, w, h = cv2.boundingRect(
                    approx
                )

                # =============================================
                # TỶ LỆ BIỂN SỐ
                # =============================================

                ratio = w / float(h)

                if 2 < ratio < 6:

                    # =========================================
                    # CẮT BIỂN SỐ
                    # =========================================

                    plate = frame[
                        y:y+h,
                        x:x+w
                    ]

                    # =========================================
                    # OCR
                    # =========================================

                    plate_text = read_plate_text(
                        plate
                    )

                    # =========================================
                    # VẼ KHUNG
                    # =========================================

                    cv2.rectangle(
                        display_frame,
                        (x, y),
                        (x + w, y + h),
                        (0, 255, 0),
                        3
                    )

                    draw_text(
                        display_frame,
                        "LICENSE PLATE",
                        (x, y - 10),
                        (0, 255, 0)
                    )

                    # =========================================
                    # HIỂN THỊ TEXT
                    # =========================================

                    draw_text(
                        display_frame,
                        f"Plate: {plate_text}",
                        (x, y + h + 30),
                        (0, 255, 255)
                    )

                    # =========================================
                    # LƯU ẢNH
                    # =========================================

                    if len(plate_text) >= 5:

                        filename = datetime.now().strftime(
                            "%Y%m%d_%H%M%S.jpg"
                        )

                        filepath = os.path.join(
                            PLATE_FOLDER,
                            filename
                        )

                        cv2.imwrite(
                            filepath,
                            plate
                        )

                        write_log(
                            f"Detected Plate: {plate_text}"
                        )

                    break

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
            (450, 220),
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
        # HIỂN THỊ INFO
        # ====================================================

        draw_text(
            display_frame,
            "LICENSE PLATE RECOGNITION",
            (20, 40)
        )

        draw_text(
            display_frame,
            f"FPS: {int(fps)}",
            (20, 80)
        )

        draw_text(
            display_frame,
            current_datetime,
            (20, 120)
        )

        draw_text(
            display_frame,
            f"Detected Plate: {plate_text}",
            (20, 160),
            (0, 255, 255)
        )

        draw_text(
            display_frame,
            "Status: ACTIVE",
            (20, 200),
            (0, 255, 0)
        )

        # ====================================================
        # CAMERA VIEW
        # ====================================================

        cv2.imshow(
            "License Plate Recognition System",
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
                "%Y%m%d_%H%M%S_manual.jpg"
            )

            filepath = os.path.join(
                PLATE_FOLDER,
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

    print("✅ Đã đóng hệ thống!")

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
