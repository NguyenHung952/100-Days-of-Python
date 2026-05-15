# =========================================================
#              AI PDF SUMMARIZER TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Tóm tắt PDF bằng AI với Python
#
# Chức năng:
#   ✓ Đọc file PDF
#   ✓ Trích xuất text PDF
#   ✓ AI tóm tắt nội dung
#   ✓ Tóm tắt theo số câu
#   ✓ Keyword Extraction
#   ✓ Hiển thị thống kê PDF
#   ✓ Lưu summary ra file
#   ✓ Batch PDF Summary
#   ✓ Demo mode
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pypdf transformers torch colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python ai_pdf_summarizer.py
#
# =========================================================

from colorama import Fore, Style, init

from pypdf import PdfReader

from transformers import pipeline

import os
import time
import re

init(autoreset=True)

# =========================================================
# LOAD AI MODEL
# =========================================================

print(Fore.CYAN +
      "\nĐang load AI model...")

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

print(Fore.GREEN +
      "AI model loaded thành công.\n")

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

    title("GIỚI THIỆU AI PDF SUMMARIZER")

    print(Fore.WHITE + """
AI PDF Summarizer giúp:

   ✓ Đọc file PDF
   ✓ AI tóm tắt nội dung
   ✓ Tiết kiệm thời gian đọc
   ✓ Phân tích tài liệu thông minh

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Research Papers
✓ E-books
✓ Reports
✓ Contracts
✓ Study Notes

=========================================================
AI MODEL SỬ DỤNG
=========================================================

✓ Facebook BART
✓ NLP Summarization
✓ Transformer AI

=========================================================
CHỨC NĂNG
=========================================================

✓ Extract PDF Text
✓ AI Summary
✓ Keyword Extraction
✓ Save Summary
✓ Batch Processing
""")

    line()


# =========================================================
# ĐỌC PDF
# =========================================================

def extract_pdf_text(pdf_path):

    text = ""

    reader = PdfReader(pdf_path)

    for page in reader.pages:

        content = page.extract_text()

        if content:

            text += content + "\n"

    return text


# =========================================================
# THỐNG KÊ PDF
# =========================================================

def pdf_statistics(text):

    words = len(text.split())

    chars = len(text)

    sentences = len(
        re.split(r'[.!?]', text)
    )

    return words, chars, sentences


# =========================================================
# KEYWORD EXTRACTION
# =========================================================

def extract_keywords(text, top_n=10):

    words = re.findall(
        r'\b[a-zA-Z]{4,}\b',
        text.lower()
    )

    stopwords = {
        "this", "that", "with",
        "from", "have", "there",
        "their", "about", "which",
        "would", "could", "should"
    }

    freq = {}

    for word in words:

        if word not in stopwords:

            freq[word] = freq.get(word, 0) + 1

    sorted_words = sorted(
        freq.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_words[:top_n]


# =========================================================
# AI SUMMARY
# =========================================================

def summarize_text(text):

    # giới hạn model
    text = text[:3000]

    result = summarizer(
        text,
        max_length=150,
        min_length=50,
        do_sample=False
    )

    return result[0]['summary_text']


# =========================================================
# PDF INFO
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

        print(Fore.GREEN +
              f"\nPDF File: {pdf_file}")

        print(Fore.CYAN +
              f"Số trang: {pages}")

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

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# AI SUMMARY PDF
# =========================================================

def summarize_pdf():

    clear()

    title("AI PDF SUMMARY")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nFile PDF không tồn tại.")

        pause()

        return

    try:

        print(Fore.CYAN +
              "\nĐang đọc PDF...")

        text = extract_pdf_text(pdf_file)

        if len(text.strip()) == 0:

            print(Fore.RED +
                  "\nKhông đọc được text.")

            pause()

            return

        words, chars, sentences = pdf_statistics(text)

        print(Fore.GREEN +
              "\nPDF STATISTICS")

        line()

        print(Fore.CYAN +
              f"Words     : {words}")

        print(Fore.YELLOW +
              f"Characters: {chars}")

        print(Fore.GREEN +
              f"Sentences : {sentences}")

        line()

        print(Fore.CYAN +
              "\nAI đang tóm tắt nội dung...")

        time.sleep(1)

        summary = summarize_text(text)

        line()

        print(Fore.GREEN +
              "\nAI SUMMARY\n")

        print(Fore.WHITE + summary)

        line()

        # KEYWORDS
        print(Fore.YELLOW +
              "\nTOP KEYWORDS\n")

        keywords = extract_keywords(text)

        for word, freq in keywords:

            print(Fore.CYAN +
                  f"{word:<15} {freq}")

        line()

        save = input(
            Fore.YELLOW +
            "\nLưu summary? (y/n): "
        )

        if save.lower() == 'y':

            with open(
                "summary_output.txt",
                "w",
                encoding="utf-8"
            ) as f:

                f.write(summary)

            print(Fore.GREEN +
                  "\nĐã lưu summary_output.txt")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi AI Summary:\n{e}")

    pause()


# =========================================================
# BATCH SUMMARY
# =========================================================

def batch_summary():

    clear()

    title("BATCH PDF SUMMARY")

    folder = input(
        Fore.YELLOW +
        "Nhập folder PDF: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    output_file = "batch_summary.txt"

    count = 0

    try:

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as out:

            for file in os.listdir(folder):

                if file.lower().endswith(".pdf"):

                    path = os.path.join(
                        folder,
                        file
                    )

                    print(Fore.CYAN +
                          f"\nSummarizing: {file}")

                    text = extract_pdf_text(path)

                    if len(text.strip()) > 50:

                        summary = summarize_text(text)

                        out.write(
                            f"\n===== {file} =====\n"
                        )

                        out.write(summary + "\n")

                        count += 1

        print(Fore.GREEN +
              f"\nĐã xử lý {count} PDF.")

        print(Fore.CYAN +
              f"Output: {output_file}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# EXTRACT TEXT
# =========================================================

def extract_text_file():

    clear()

    title("EXTRACT PDF TEXT")

    pdf_file = input(
        Fore.YELLOW +
        "Nhập file PDF: "
    )

    if not os.path.exists(pdf_file):

        print(Fore.RED +
              "\nPDF không tồn tại.")

        pause()

        return

    try:

        text = extract_pdf_text(pdf_file)

        output = "pdf_text_output.txt"

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        print(Fore.GREEN +
              f"\nĐã extract text: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO AI PDF SUMMARY")

    print(Fore.WHITE + """
Demo AI PDF Summary:

=========================================================
CÁCH TEST
=========================================================

1. Chuẩn bị file PDF
2. Chạy AI Summary
3. AI đọc PDF
4. AI tạo summary

=========================================================
AI MODEL
=========================================================

✓ Facebook BART
✓ NLP Transformer
✓ Text Summarization

=========================================================
ỨNG DỤNG
=========================================================

✓ Research Paper Summary
✓ Book Summary
✓ Report Analysis
""")

    pause()


# =========================================================
# GIẢI THÍCH AI SUMMARY
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH AI PDF SUMMARY")

    print(Fore.WHITE + """
=========================================================
1. NLP
=========================================================

NLP:
   Natural Language Processing

=========================================================
2. TEXT SUMMARIZATION
=========================================================

AI tự động:
   ✓ Đọc text
   ✓ Hiểu nội dung
   ✓ Tạo summary

=========================================================
3. TRANSFORMER
=========================================================

Kiến trúc AI hiện đại:
   ✓ BERT
   ✓ GPT
   ✓ BART

=========================================================
4. BART MODEL
=========================================================

Facebook AI model:
   ✓ Tóm tắt text mạnh

=========================================================
5. PDF EXTRACTION
=========================================================

PDF -> Extract Text -> AI Summary

=========================================================
6. KEYWORD EXTRACTION
=========================================================

Tìm từ khóa quan trọng.

=========================================================
7. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Research
✓ Legal Documents
✓ Reports
✓ E-books
✓ AI Assistant

=========================================================
8. GENERATIVE AI
=========================================================

AI tạo nội dung tự động.
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("AI PDF SUMMARIZER TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu AI PDF Summary
[2] Xem thông tin PDF
[3] AI tóm tắt PDF
[4] Batch PDF Summary
[5] Extract PDF Text
[6] Demo mode
[7] Giải thích AI Summary
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

            summarize_pdf()

        elif choice == '4':

            batch_summary()

        elif choice == '5':

            extract_text_file()

        elif choice == '6':

            demo_mode()

        elif choice == '7':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng AI PDF Summarizer.

Kiến thức đạt được:
   ✓ NLP
   ✓ AI Summarization
   ✓ Transformer Model
   ✓ PDF Processing
   ✓ Keyword Extraction
   ✓ Generative AI
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
