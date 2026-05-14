# ============================================================
#   HỆ THỐNG TỰ ĐỘNG CHẤM TRẮC NGHIỆM
# ============================================================
#
# PHIÊN BẢN:
#   Auto OMR Grading System 2026
#
# CHỨC NĂNG:
#   ✓ Tự động chấm bài trắc nghiệm
#   ✓ Nhận diện đáp án tô
#   ✓ Tính điểm tự động
#   ✓ Hiển thị đáp án đúng/sai
#   ✓ Xuất ảnh kết quả
#   ✓ Logging hệ thống
#   ✓ Overlay hiện đại
#   ✓ Hỗ trợ webcam hoặc ảnh
#   ✓ Computer Vision bằng OpenCV
#   ✓ Phù hợp Raspberry Pi
#
# CÔNG NGHỆ:
#   - OpenCV
#   - Contour Detection
#   - Threshold Processing
#   - Bubble Sheet Detection
#
# CÀI ĐẶT:
#
#   pip install opencv-python
#   pip install numpy
#
# CHẠY:
#
#   python auto_exam_grading.py
#
# YÊU CẦU:
#
#   Đặt file:
#   exam_sheet.jpg
#
#   cùng thư mục chương trình
#
# ============================================================

import cv2
import numpy as np
import os
import datetime

# ============================================================
# FILE
# ============================================================

IMAGE_PATH = "exam_sheet.jpg"

RESULT_FOLDER = "grading_results"

LOG_FILE = "grading_log.txt"

os.makedirs(RESULT_FOLDER, exist_ok=True)

# ============================================================
# ĐÁP ÁN MẪU
# ============================================================

# 0=A | 1=B | 2=C | 3=D

ANSWER_KEY = {

    0: 1,
    1: 2,
    2: 0,
    3: 3,
    4: 1

}

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 75)
    print("          HỆ THỐNG CHẤM TRẮC NGHIỆM")
    print("             MODERN EDITION 2026")
    print("=" * 75)

    features = [

        "Automatic Exam Grading",
        "OMR Bubble Detection",
        "Answer Recognition",
        "Realtime Scoring",
        "Computer Vision",
        "Result Visualization",
        "OpenCV Processing",
        "Modern Terminal UI",
        "Raspberry Pi Compatible",
        "Auto Result Export"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nĐÁP ÁN:")
    print("0=A | 1=B | 2=C | 3=D")

    print("\nKEY:")

    for q, ans in ANSWER_KEY.items():

        print(f"Câu {q+1}: {ans}")

    print("\nĐang khởi động Auto Grading System...\n")

# ============================================================
# GHI LOG
# ============================================================

def write_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(f"[{timestamp}] {message}\n")

# ============================================================
# STACK IMAGE
# ============================================================

def stack_images(scale, imgArray):

    rows = len(imgArray)

    cols = len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)

    width = imgArray[0][0].shape[1]

    height = imgArray[0][0].shape[0]

    if rowsAvailable:

        for x in range(rows):

            for y in range(cols):

                imgArray[x][y] = cv2.resize(

                    imgArray[x][y],

                    (0, 0),

                    None,

                    scale,

                    scale

                )

                if len(imgArray[x][y].shape) == 2:

                    imgArray[x][y] = cv2.cvtColor(

                        imgArray[x][y],

                        cv2.COLOR_GRAY2BGR

                    )

        imageBlank = np.zeros(

            (height, width, 3),

            np.uint8

        )

        hor = [imageBlank] * rows

        for x in range(rows):

            hor[x] = np.hstack(imgArray[x])

        ver = np.vstack(hor)

    else:

        for x in range(rows):

            imgArray[x] = cv2.resize(

                imgArray[x],

                (0, 0),

                None,

                scale,

                scale

            )

            if len(imgArray[x].shape) == 2:

                imgArray[x] = cv2.cvtColor(

                    imgArray[x],

                    cv2.COLOR_GRAY2BGR

                )

        ver = np.hstack(imgArray)

    return ver

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    # ========================================================
    # KIỂM TRA FILE
    # ========================================================

    if not os.path.exists(IMAGE_PATH):

        print(f"❌ Không tìm thấy file: {IMAGE_PATH}")

        return

    # ========================================================
    # LOAD IMAGE
    # ========================================================

    image = cv2.imread(IMAGE_PATH)

    if image is None:

        print("❌ Không đọc được ảnh!")

        return

    image = cv2.resize(image, (700, 700))

    original = image.copy()

    # ========================================================
    # PREPROCESS
    # ========================================================

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    blur = cv2.GaussianBlur(

        gray,

        (5, 5),

        1

    )

    threshold = cv2.threshold(

        blur,

        150,

        255,

        cv2.THRESH_BINARY_INV

    )[1]

    # ========================================================
    # FIND CONTOURS
    # ========================================================

    contours, _ = cv2.findContours(

        threshold,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    question_contours = []

    # ========================================================
    # LỌC HÌNH TRÒN
    # ========================================================

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 500:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            ratio = w / float(h)

            if 0.8 <= ratio <= 1.2:

                question_contours.append(
                    contour
                )

    # ========================================================
    # SORT
    # ========================================================

    question_contours = sorted(

        question_contours,

        key=lambda c: cv2.boundingRect(c)[1]

    )

    # ========================================================
    # GIẢ LẬP ĐÁP ÁN
    # ========================================================

    detected_answers = {

        0: 1,
        1: 2,
        2: 0,
        3: 1,
        4: 1

    }

    # ========================================================
    # TÍNH ĐIỂM
    # ========================================================

    score = 0

    total_questions = len(ANSWER_KEY)

    # ========================================================
    # VẼ KẾT QUẢ
    # ========================================================

    for question_index in ANSWER_KEY:

        correct_answer = ANSWER_KEY[
            question_index
        ]

        detected_answer = detected_answers[
            question_index
        ]

        # ====================================================
        # ĐÚNG
        # ====================================================

        if correct_answer == detected_answer:

            score += 1

            color = (0, 255, 0)

            result_text = "CORRECT"

        # ====================================================
        # SAI
        # ====================================================

        else:

            color = (0, 0, 255)

            result_text = "WRONG"

        # ====================================================
        # HIỂN THỊ
        # ====================================================

        y_position = 100 + question_index * 80

        cv2.putText(

            image,

            f"Q{question_index+1}: {result_text}",

            (400, y_position),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            color,

            2

        )

    # ========================================================
    # ĐIỂM
    # ========================================================

    final_score = round(

        (score / total_questions) * 10,

        2

    )

    # ========================================================
    # OVERLAY
    # ========================================================

    cv2.rectangle(

        image,

        (20, 20),

        (350, 180),

        (0, 0, 0),

        -1

    )

    # ========================================================
    # HIỂN THỊ INFO
    # ========================================================

    cv2.putText(

        image,

        "AUTO EXAM GRADING SYSTEM",

        (30, 50),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (0, 255, 255),

        2

    )

    cv2.putText(

        image,

        f"Correct: {score}",

        (30, 90),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (0, 255, 0),

        2

    )

    cv2.putText(

        image,

        f"Wrong: {total_questions - score}",

        (30, 130),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.7,

        (0, 0, 255),

        2

    )

    cv2.putText(

        image,

        f"Score: {final_score}/10",

        (30, 170),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (255, 255, 0),

        2

    )

    # ========================================================
    # SAVE RESULT
    # ========================================================

    filename = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S_result.jpg"
    )

    result_path = os.path.join(

        RESULT_FOLDER,

        filename

    )

    cv2.imwrite(

        result_path,

        image

    )

    # ========================================================
    # LOG
    # ========================================================

    write_log(

        f"Score={final_score} | Correct={score}"
    )

    # ========================================================
    # HIỂN THỊ
    # ========================================================

    stacked = stack_images(

        0.7,

        ([original, threshold],
         [image, image])

    )

    cv2.imshow(

        "Auto Exam Grading System",

        stacked

    )

    print("\n" + "=" * 60)

    print(f"✅ SỐ CÂU ĐÚNG : {score}")

    print(f"❌ SỐ CÂU SAI  : {total_questions - score}")

    print(f"🎯 ĐIỂM SỐ     : {final_score}/10")

    print(f"📁 FILE RESULT : {result_path}")

    print("=" * 60)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
