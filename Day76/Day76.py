# =========================================================
#              OCR IMAGE TEXT READER
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : OCR đọc văn bản từ ảnh bằng Python
#
# Chức năng:
#   ✓ OCR đọc text từ ảnh
#   ✓ Hỗ trợ tiếng Việt + English
#   ✓ Tiền xử lý ảnh
#   ✓ Chuyển ảnh grayscale
#   ✓ Threshold image
#   ✓ Resize tăng độ chính xác
#   ✓ Lưu text ra file
#   ✓ Batch OCR nhiều ảnh
#   ✓ Hiển thị thông tin ảnh
#   ✓ Demo mode
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pytesseract pillow opencv-python colorama
#
# =========================================================
# CÀI TESSERACT OCR ENGINE
# =========================================================
#
# WINDOWS:
# https://github.com/UB-Mannheim/tesseract/wiki
#
# Sau khi cài:
#
# pytesseract.pytesseract.tesseract_cmd =
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#
# LINUX:
# sudo apt install tesseract-ocr
#
# =========================================================
# CHẠY
# =========================================================
#
# python ocr_reader.py
#
# =========================================================

from colorama import Fore, Style, init

from PIL import Image
import pytesseract
import cv2
import os
import time

init(autoreset=True)

# =========================================================
# CẤU HÌNH TESSERACT
# =========================================================

# WINDOWS:
# Uncomment nếu dùng Windows

# pytesseract.pytesseract.tesseract_cmd = \
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():

    os.system(
        "cls" if os.name == "nt"
        else "clear"
    )


def line():

    print(Fore.CYAN + "=" * 100)


def title(text):

    line()

    print(
        Fore.GREEN +
        Style.BRIGHT +
        text.center(100)
    )

    line()


def pause():

    input(
        Fore.YELLOW +
        "\nNhấn ENTER để tiếp tục..."
    )


# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU OCR")

    print(Fore.WHITE + """
OCR = Optical Character Recognition

OCR giúp:
   ✓ Đọc chữ từ ảnh
   ✓ Chuyển ảnh -> text
   ✓ Tự động số hóa tài liệu

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Scan Documents
✓ CMND/CCCD OCR
✓ Invoice OCR
✓ Passport OCR
✓ AI Document Processing

=========================================================
CHỨC NĂNG CHƯƠNG TRÌNH
=========================================================

✓ OCR Image
✓ OCR Multiple Images
✓ Preprocessing
✓ Vietnamese OCR
✓ Save Text File

=========================================================
THƯ VIỆN SỬ DỤNG
=========================================================

✓ OpenCV
✓ Pillow
✓ Pytesseract
""")

    line()


# =========================================================
# KIỂM TRA FILE
# =========================================================

def check_image(path):

    if not os.path.exists(path):

        print(Fore.RED +
              "\nFile ảnh không tồn tại.")

        return False

    return True


# =========================================================
# THÔNG TIN ẢNH
# =========================================================

def image_info():

    clear()

    title("IMAGE INFORMATION")

    image_path = input(
        Fore.YELLOW +
        "Nhập file ảnh: "
    )

    if not check_image(image_path):

        pause()

        return

    try:

        img = Image.open(image_path)

        print(Fore.GREEN +
              f"\nTên file: {image_path}")

        print(Fore.CYAN +
              f"Kích thước: {img.size}")

        print(Fore.YELLOW +
              f"Mode: {img.mode}")

        print(Fore.GREEN +
              f"Format: {img.format}")

        print(Fore.CYAN +
              f"File size: "
              f"{os.path.getsize(image_path)} bytes")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# PREPROCESS IMAGE
# =========================================================

def preprocess_image(image_path):

    img = cv2.imread(image_path)

    # grayscale
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # threshold
    _, thresh = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY
    )

    # resize
    resized = cv2.resize(
        thresh,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    processed_path = "processed_image.png"

    cv2.imwrite(
        processed_path,
        resized
    )

    return processed_path


# =========================================================
# OCR ĐỌC TEXT
# =========================================================

def ocr_image():

    clear()

    title("OCR IMAGE")

    image_path = input(
        Fore.YELLOW +
        "Nhập file ảnh: "
    )

    if not check_image(image_path):

        pause()

        return

    try:

        print(Fore.CYAN +
              "\nTiền xử lý ảnh...")

        processed = preprocess_image(
            image_path
        )

        print(Fore.CYAN +
              "Đang OCR...")

        time.sleep(1)

        text = pytesseract.image_to_string(
            Image.open(processed),
            lang='eng'
        )

        line()

        print(Fore.GREEN +
              "\nTEXT OCR\n")

        print(Fore.WHITE + text)

        line()

        save = input(
            Fore.YELLOW +
            "\nLưu text ra file? (y/n): "
        )

        if save.lower() == 'y':

            with open(
                "ocr_output.txt",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(text)

            print(Fore.GREEN +
                  "\nĐã lưu: ocr_output.txt")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi OCR:\n{e}")

    pause()


# =========================================================
# OCR TIẾNG VIỆT
# =========================================================

def ocr_vietnamese():

    clear()

    title("OCR TIẾNG VIỆT")

    image_path = input(
        Fore.YELLOW +
        "Nhập file ảnh: "
    )

    if not check_image(image_path):

        pause()

        return

    try:

        processed = preprocess_image(
            image_path
        )

        print(Fore.CYAN +
              "\nĐang OCR tiếng Việt...")

        text = pytesseract.image_to_string(
            Image.open(processed),
            lang='vie'
        )

        line()

        print(Fore.GREEN +
              "\nTEXT OCR VIETNAMESE\n")

        print(Fore.WHITE + text)

        line()

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi OCR:\n{e}")

        print(Fore.YELLOW +
              "\nCần cài language pack 'vie'.")

    pause()


# =========================================================
# OCR NHIỀU ẢNH
# =========================================================

def batch_ocr():

    clear()

    title("BATCH OCR")

    folder = input(
        Fore.YELLOW +
        "Nhập folder chứa ảnh: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    output_file = "batch_ocr_output.txt"

    image_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp"
    ]

    count = 0

    try:

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as out:

            for file in os.listdir(folder):

                ext = os.path.splitext(file)[1].lower()

                if ext in image_extensions:

                    path = os.path.join(
                        folder,
                        file
                    )

                    print(Fore.CYAN +
                          f"OCR: {file}")

                    processed = preprocess_image(path)

                    text = pytesseract.image_to_string(
                        Image.open(processed),
                        lang='eng'
                    )

                    out.write(
                        f"\n===== {file} =====\n"
                    )

                    out.write(text + "\n")

                    count += 1

        print(Fore.GREEN +
              f"\nĐã OCR {count} ảnh.")

        print(Fore.CYAN +
              f"Output: {output_file}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# EXTRACT TEXT TO FILE
# =========================================================

def extract_text_file():

    clear()

    title("OCR -> TEXT FILE")

    image_path = input(
        Fore.YELLOW +
        "Nhập file ảnh: "
    )

    if not check_image(image_path):

        pause()

        return

    try:

        processed = preprocess_image(
            image_path
        )

        text = pytesseract.image_to_string(
            Image.open(processed),
            lang='eng'
        )

        output = "extracted_text.txt"

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        print(Fore.GREEN +
              f"\nĐã lưu text: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO OCR SYSTEM")

    print(Fore.WHITE + """
Demo OCR:

=========================================================
BƯỚC TEST
=========================================================

1. Chuẩn bị ảnh chứa text
2. Chạy OCR Image
3. Kiểm tra kết quả
4. Test OCR tiếng Việt

=========================================================
LƯU Ý
=========================================================

✓ Ảnh càng rõ OCR càng chính xác
✓ Text nên có độ phân giải cao
✓ Tránh ảnh bị mờ
✓ Dùng preprocessing để tăng accuracy
""")

    pause()


# =========================================================
# GIẢI THÍCH OCR
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH OCR")

    print(Fore.WHITE + """
=========================================================
1. OCR LÀ GÌ?
=========================================================

OCR:
   Optical Character Recognition

=========================================================
2. OCR HOẠT ĐỘNG
=========================================================

Ảnh -> AI nhận diện chữ -> Text

=========================================================
3. PREPROCESSING
=========================================================

Xử lý ảnh trước OCR:
   ✓ Grayscale
   ✓ Threshold
   ✓ Resize

=========================================================
4. TESSERACT
=========================================================

OCR Engine nổi tiếng của Google.

=========================================================
5. THRESHOLD
=========================================================

Làm rõ chữ trong ảnh.

=========================================================
6. OCR ACCURACY
=========================================================

Phụ thuộc:
   ✓ Chất lượng ảnh
   ✓ Font chữ
   ✓ Độ phân giải

=========================================================
7. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Scan Documents
✓ Invoice OCR
✓ Passport OCR
✓ AI Document Processing
✓ License Plate OCR

=========================================================
8. COMPUTER VISION
=========================================================

OCR là lĩnh vực:
   ✓ AI
   ✓ Computer Vision
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("OCR IMAGE TEXT READER")

        print(Fore.CYAN + """
[1] Giới thiệu OCR
[2] OCR đọc text từ ảnh
[3] OCR tiếng Việt
[4] OCR nhiều ảnh
[5] Xem thông tin ảnh
[6] Extract text ra file
[7] Demo mode
[8] Giải thích OCR
[0] Thoát
""")

        choice = input(
            Fore.YELLOW +
            "Nhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            ocr_image()

        elif choice == '3':

            ocr_vietnamese()

        elif choice == '4':

            batch_ocr()

        elif choice == '5':

            image_info()

        elif choice == '6':

            extract_text_file()

        elif choice == '7':

            demo_mode()

        elif choice == '8':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng OCR Tool.

Kiến thức đạt được:
   ✓ OCR
   ✓ Computer Vision
   ✓ Tesseract OCR
   ✓ Image Processing
   ✓ AI Text Recognition
   ✓ OpenCV
""")

            break

        else:

            print(Fore.RED +
                  "Lựa chọn không hợp lệ!")

            time.sleep(1)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        menu()

    except KeyboardInterrupt:

        print(Fore.RED +
              "\n\nĐã thoát chương trình.")
