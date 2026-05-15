# =========================================================
#               PDF MERGER / SPLITTER TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Gộp và tách file PDF bằng Python
#
# Chức năng:
#   ✓ Gộp nhiều file PDF
#   ✓ Tách PDF theo trang
#   ✓ Trích xuất từng trang PDF
#   ✓ Xem thông tin PDF
#   ✓ Đếm số trang PDF
#   ✓ Rotate PDF pages
#   ✓ Watermark PDF
#   ✓ Demo mode
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pypdf colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python pdf_tools.py
#
# =========================================================

from colorama import Fore, Style, init
from pypdf import (
    PdfReader,
    PdfWriter,
    PdfMerger
)

import os
import time

init(autoreset=True)

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

    title("GIỚI THIỆU PDF TOOL")

    print(Fore.WHITE + """
PDF Tool giúp:

   ✓ Gộp nhiều file PDF
   ✓ Tách file PDF
   ✓ Quản lý tài liệu PDF
   ✓ Tự động xử lý PDF

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ PDF Merge
✓ PDF Split
✓ Extract Pages
✓ Rotate Pages
✓ Watermark PDF
✓ PDF Information

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Office Documents
✓ E-books
✓ Scan Documents
✓ Reports
✓ Contracts

=========================================================
LỢI ÍCH
=========================================================

✓ Tiết kiệm thời gian
✓ Tự động hóa
✓ Quản lý tài liệu dễ dàng
""")

    line()


# =========================================================
# THÔNG TIN PDF
# =========================================================

def pdf_info():

    clear()

    title("PDF INFORMATION")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    try:

        reader = PdfReader(pdf_file)

        pages = len(reader.pages)

        metadata = reader.metadata

        line()

        print(Fore.GREEN +
              f"\nFile PDF : {pdf_file}")

        print(Fore.CYAN +
              f"Số trang : {pages}")

        print(Fore.YELLOW +
              f"Kích thước: "
              f"{os.path.getsize(pdf_file)} bytes")

        print(Fore.GREEN +
              "\nMETADATA\n")

        if metadata:

            for key, value in metadata.items():

                print(
                    Fore.CYAN +
                    f"{key}: {value}"
                )

        else:

            print(Fore.YELLOW +
                  "Không có metadata.")

        line()

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# MERGE PDF
# =========================================================

def merge_pdfs():

    clear()

    title("MERGE PDF FILES")

    print(Fore.CYAN +
          "\nNhập danh sách PDF.")

    print(Fore.YELLOW +
          "Nhập 'done' để kết thúc.\n")

    pdfs = []

    while True:

        pdf = input(
            Fore.YELLOW +
            "PDF file: "
        )

        if pdf.lower() == 'done':

            break

        if os.path.exists(pdf):

            pdfs.append(pdf)

        else:

            print(Fore.RED +
                  "File không tồn tại.")

    if len(pdfs) < 2:

        print(Fore.RED +
              "\nCần ít nhất 2 file PDF.")

        pause()

        return

    output = input(
        Fore.YELLOW +
        "\nTên file output: "
    )

    if not output.endswith(".pdf"):

        output += ".pdf"

    try:

        merger = PdfMerger()

        print(Fore.CYAN +
              "\nĐang merge PDF...\n")

        for pdf in pdfs:

            merger.append(pdf)

            print(Fore.GREEN +
                  f"Added: {pdf}")

        merger.write(output)

        merger.close()

        print(Fore.GREEN +
              f"\nMerge thành công: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi merge:\n{e}")

    pause()


# =========================================================
# SPLIT PDF
# =========================================================

def split_pdf():

    clear()

    title("SPLIT PDF")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    try:

        reader = PdfReader(pdf_file)

        total_pages = len(reader.pages)

        print(Fore.GREEN +
              f"\nTổng số trang: {total_pages}")

        output_folder = "split_pages"

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        print(Fore.CYAN +
              "\nĐang split PDF...\n")

        for i in range(total_pages):

            writer = PdfWriter()

            writer.add_page(
                reader.pages[i]
            )

            output_path = os.path.join(
                output_folder,
                f"page_{i+1}.pdf"
            )

            with open(output_path, "wb") as f:

                writer.write(f)

            print(Fore.GREEN +
                  f"Created: {output_path}")

        print(Fore.CYAN +
              "\nSplit hoàn tất.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi split:\n{e}")

    pause()


# =========================================================
# EXTRACT PAGES
# =========================================================

def extract_pages():

    clear()

    title("EXTRACT PDF PAGES")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    try:

        start = int(input(
            Fore.YELLOW +
            "Trang bắt đầu: "
        ))

        end = int(input(
            Fore.YELLOW +
            "Trang kết thúc: "
        ))

        output = input(
            Fore.YELLOW +
            "Tên output PDF: "
        )

        if not output.endswith(".pdf"):

            output += ".pdf"

        reader = PdfReader(pdf_file)

        writer = PdfWriter()

        for i in range(start - 1, end):

            writer.add_page(
                reader.pages[i]
            )

        with open(output, "wb") as f:

            writer.write(f)

        print(Fore.GREEN +
              f"\nĐã extract: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi extract:\n{e}")

    pause()


# =========================================================
# ROTATE PDF
# =========================================================

def rotate_pdf():

    clear()

    title("ROTATE PDF")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    try:

        angle = int(input(
            Fore.YELLOW +
            "Góc xoay (90/180/270): "
        ))

        output = input(
            Fore.YELLOW +
            "Tên output PDF: "
        )

        if not output.endswith(".pdf"):

            output += ".pdf"

        reader = PdfReader(pdf_file)

        writer = PdfWriter()

        for page in reader.pages:

            page.rotate(angle)

            writer.add_page(page)

        with open(output, "wb") as f:

            writer.write(f)

        print(Fore.GREEN +
              f"\nĐã rotate PDF: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi rotate:\n{e}")

    pause()


# =========================================================
# WATERMARK PDF
# =========================================================

def watermark_pdf():

    clear()

    title("WATERMARK PDF")

    pdf_file = input(
        Fore.YELLOW +
        "PDF chính: "
    )

    watermark = input(
        Fore.YELLOW +
        "PDF watermark: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nPDF chính không tồn tại.")

        pause()

        return

    if not os.path.exists(watermark):

        print(Fore.RED +
              "\nWatermark PDF không tồn tại.")

        pause()

        return

    try:

        reader = PdfReader(pdf_file)

        watermark_reader = PdfReader(watermark)

        watermark_page = watermark_reader.pages[0]

        writer = PdfWriter()

        for page in reader.pages:

            page.merge_page(
                watermark_page
            )

            writer.add_page(page)

        output = "watermarked.pdf"

        with open(output, "wb") as f:

            writer.write(f)

        print(Fore.GREEN +
              f"\nĐã thêm watermark: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi watermark:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO PDF TOOL")

    print(Fore.WHITE + """
Demo mode mô phỏng:

✓ Merge PDF
✓ Split PDF
✓ Extract Pages
✓ Rotate PDF
✓ Watermark PDF

=========================================================
Để test thực tế:
=========================================================

1. Tạo vài file PDF
2. Chạy chức năng Merge
3. Chạy Split PDF
4. Kiểm tra output
""")

    pause()


# =========================================================
# GIẢI THÍCH PDF
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH PDF TOOL")

    print(Fore.WHITE + """
=========================================================
1. PDF
=========================================================

PDF:
   Portable Document Format

=========================================================
2. PDF MERGE
=========================================================

Gộp nhiều PDF thành 1 file.

=========================================================
3. PDF SPLIT
=========================================================

Tách PDF thành nhiều trang.

=========================================================
4. EXTRACT PAGE
=========================================================

Lấy riêng từng trang PDF.

=========================================================
5. ROTATE PDF
=========================================================

Xoay trang PDF:
   ✓ 90 độ
   ✓ 180 độ
   ✓ 270 độ

=========================================================
6. WATERMARK
=========================================================

Thêm logo/text vào PDF.

=========================================================
7. METADATA
=========================================================

Thông tin PDF:
   ✓ Author
   ✓ Title
   ✓ Producer

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Office
✓ Scan Documents
✓ Contracts
✓ Reports
✓ E-books
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("PDF MERGER / SPLITTER TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu PDF Tool
[2] Xem thông tin PDF
[3] Merge PDF
[4] Split PDF
[5] Extract Pages
[6] Rotate PDF
[7] Watermark PDF
[8] Demo mode
[9] Giải thích PDF
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

            pdf_info()

        elif choice == '3':

            merge_pdfs()

        elif choice == '4':

            split_pdf()

        elif choice == '5':

            extract_pages()

        elif choice == '6':

            rotate_pdf()

        elif choice == '7':

            watermark_pdf()

        elif choice == '8':

            demo_mode()

        elif choice == '9':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng PDF Tool.

Kiến thức đạt được:
   ✓ PDF Merge
   ✓ PDF Split
   ✓ Page Extraction
   ✓ PDF Rotation
   ✓ Watermark
   ✓ Document Automation
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
