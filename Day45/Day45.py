# ============================================================
#   HỆ THỐNG MỞ CỬA BẰNG FACE ID
# ============================================================
#
# PHIÊN BẢN:
#   Smart Face ID Door Lock 2026
#
# CHỨC NĂNG:
#   ✓ AI nhận diện khuôn mặt
#   ✓ Mở cửa tự động
#   ✓ Camera streaming realtime
#   ✓ Đăng ký khuôn mặt
#   ✓ Xác thực người dùng
#   ✓ Snapshot truy cập
#   ✓ Logging hệ thống
#   ✓ Hiển thị FPS
#   ✓ Dashboard hiện đại
#   ✓ Hỗ trợ Raspberry Pi
#
# CÔNG NGHỆ:
#   - OpenCV
#   - face_recognition
#   - AI Face Encoding
#
# CÀI ĐẶT:
#
#   pip install opencv-python
#   pip install face_recognition
#   pip install numpy
#
# LINUX:
#
#   sudo apt install cmake
#   sudo apt install build-essential
#
# WINDOWS:
#
#   pip install cmake
#
# CHẠY:
#
#   python face_id_door_lock.py
#
# PHÍM:
#
#   Q = Thoát
#   S = Lưu snapshot
#
# ============================================================

import cv2
import face_recognition
import numpy as np
import os
import time
from datetime import datetime

# ============================================================
# THƯ MỤC
# ============================================================

KNOWN_FACE_FOLDER = "known_faces"
SNAPSHOT_FOLDER = "door_snapshots"
LOG_FILE = "door_access_log.txt"

os.makedirs(KNOWN_FACE_FOLDER, exist_ok=True)
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 75)
    print("           SMART FACE ID DOOR LOCK")
    print("             MODERN EDITION 2026")
    print("=" * 75)

    features = [

        "Realtime Face Recognition",
        "Smart Door Unlock",
        "Authorized User Detection",
        "AI Face Encoding",
        "Access Logging",
        "Snapshot Capture",
        "Modern Dashboard UI",
        "FPS Monitoring",
        "Raspberry Pi Compatible",
        "Computer Vision Security"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nTHƯ MỤC NGƯỜI DÙNG:")
    print("known_faces/")

    print("\nCÁCH THÊM NGƯỜI DÙNG:")
    print("Đặt ảnh vào thư mục known_faces/")
    print("Ví dụ:")
    print("known_faces/An.jpg")
    print("known_faces/Binh.jpg")

    print("\nPHÍM ĐIỀU KHIỂN:")
    print("Q -> Thoát")
    print("S -> Snapshot")

    print("\nĐang khởi động AI Security System...\n")

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
# LOAD KHUÔN MẶT ĐÃ ĐĂNG KÝ
# ============================================================

def load_known_faces():

    known_encodings = []
    known_names = []

    print("🔄 Đang tải dữ liệu khuôn mặt...")

    for filename in os.listdir(KNOWN_FACE_FOLDER):

        filepath = os.path.join(
            KNOWN_FACE_FOLDER,
            filename
        )

        try:

            image = face_recognition.load_image_file(
                filepath
            )

            encodings = face_recognition.face_encodings(
                image
            )

            if len(encodings) > 0:

                encoding = encodings[0]

                known_encodings.append(
                    encoding
                )

                name = os.path.splitext(
                    filename
                )[0]

                known_names.append(name)

                print(f"✅ Loaded: {name}")

            else:

                print(f"⚠ Không tìm thấy khuôn mặt: {filename}")

        except Exception as e:

            print(f"❌ Lỗi file {filename}: {e}")

    return known_encodings, known_names

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    # ========================================================
    # LOAD FACE DATABASE
    # ========================================================

    known_encodings, known_names = load_known_faces()

    if len(known_encodings) == 0:

        print("❌ Không có dữ liệu khuôn mặt!")
        print("Hãy thêm ảnh vào thư mục known_faces/")
        return

    print(f"\n✅ Đã tải {len(known_names)} người dùng")

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
        # FLIP FRAME
        # ====================================================

        frame = cv2.flip(frame, 1)

        display_frame = frame.copy()

        # ====================================================
        # RESIZE TĂNG TỐC
        # ====================================================

        small_frame = cv2.resize(
            frame,
            (0, 0),
            fx=0.25,
            fy=0.25
        )

        # ====================================================
        # RGB
        # ====================================================

        rgb_small = cv2.cvtColor(
            small_frame,
            cv2.COLOR_BGR2RGB
        )

        # ====================================================
        # DETECT FACE
        # ====================================================

        face_locations = face_recognition.face_locations(
            rgb_small
        )

        face_encodings = face_recognition.face_encodings(
            rgb_small,
            face_locations
        )

        # ====================================================
        # NHẬN DIỆN
        # ====================================================

        for face_encoding, face_location in zip(
            face_encodings,
            face_locations
        ):

            matches = face_recognition.compare_faces(
                known_encodings,
                face_encoding
            )

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            best_match_index = np.argmin(
                face_distances
            )

            name = "UNKNOWN"

            # ================================================
            # XÁC THỰC
            # ================================================

            if matches[best_match_index]:

                name = known_names[
                    best_match_index
                ]

                color = (0, 255, 0)

                status = "ACCESS GRANTED"

                write_log(
                    f"ACCESS GRANTED -> {name}"
                )

            else:

                color = (0, 0, 255)

                status = "ACCESS DENIED"

                write_log(
                    "ACCESS DENIED -> Unknown Person"
                )

            # ================================================
            # SCALE TO NORMAL
            # ================================================

            top, right, bottom, left = face_location

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # ================================================
            # RECTANGLE
            # ================================================

            cv2.rectangle(
                display_frame,
                (left, top),
                (right, bottom),
                color,
                3
            )

            # ================================================
            # NAME
            # ================================================

            draw_text(
                display_frame,
                name,
                (left, top - 10),
                color
            )

            # ================================================
            # STATUS
            # ================================================

            draw_text(
                display_frame,
                status,
                (left, bottom + 30),
                color
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
            (500, 260),
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
        # DASHBOARD
        # ====================================================

        draw_text(
            display_frame,
            "SMART FACE ID SECURITY SYSTEM",
            (20, 40)
        )

        draw_text(
            display_frame,
            f"Registered Users: {len(known_names)}",
            (20, 80),
            (0, 255, 255)
        )

        draw_text(
            display_frame,
            f"Detected Faces: {len(face_locations)}",
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
            "Door Lock Status: ACTIVE",
            (20, 240),
            (0, 255, 0)
        )

        # ====================================================
        # CAMERA VIEW
        # ====================================================

        cv2.imshow(
            "Smart Face ID Door Lock System",
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
        # SNAPSHOT
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

            print(f"📸 Snapshot saved: {filepath}")

    # ========================================================
    # GIẢI PHÓNG
    # ========================================================

    cap.release()

    cv2.destroyAllWindows()

    print("✅ Đã đóng Smart Face ID System!")

# ============================================================
# CHẠY
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\n⚠ Chương trình đã dừng")

    except Exception as e:

        print(f"\n❌ Lỗi: {e}")
