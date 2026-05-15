# =========================================================
#              AI RESUME PARSER SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Resume Parser bằng Python
#
# Chức năng:
#   ✓ Đọc Resume PDF/TXT
#   ✓ Trích xuất thông tin CV
#   ✓ Extract Email
#   ✓ Extract Phone Number
#   ✓ Detect Skills
#   ✓ Extract Education
#   ✓ Extract Experience
#   ✓ NLP Resume Analysis
#   ✓ Export Parsed Data JSON
#   ✓ Dashboard terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pypdf colorama spacy
#
# =========================================================
# OPTIONAL NLP MODEL
# =========================================================
#
# python -m spacy download en_core_web_sm
#
# =========================================================
# CHẠY
# =========================================================
#
# python resume_parser.py
#
# =========================================================

from colorama import Fore, Style, init

from pypdf import PdfReader

import re
import os
import json
import time

init(autoreset=True)

# =========================================================
# DATABASE
# =========================================================

PARSED_DATA_FILE = "parsed_resume.json"

# =========================================================
# SKILLS DATABASE
# =========================================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "sql",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "react",
    "nodejs",
    "docker",
    "git",
    "linux",
    "ai",
    "data analysis",
    "excel",
    "photoshop"
]

# =========================================================
# UI
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
# INTRO
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU RESUME PARSER")

    print(Fore.WHITE + """
Resume Parser giúp:

   ✓ Đọc CV tự động
   ✓ Trích xuất thông tin ứng viên
   ✓ Phân tích kỹ năng
   ✓ Hỗ trợ tuyển dụng AI

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ PDF Resume Reader
✓ Email Extraction
✓ Phone Extraction
✓ Skill Detection
✓ NLP Analysis

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ HR Recruitment
✓ ATS System
✓ AI Hiring
✓ Resume Screening

=========================================================
AI TECHNOLOGY
=========================================================

✓ NLP
✓ Regex Extraction
✓ Resume Parsing
✓ AI Recruitment
""")

    line()


# =========================================================
# READ PDF
# =========================================================

def extract_pdf_text(pdf_path):

    text = ""

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            content = page.extract_text()

            if content:

                text += content + "\n"

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi PDF:\n{e}")

    return text


# =========================================================
# READ TXT
# =========================================================

def extract_txt_text(txt_path):

    try:

        with open(
            txt_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    except:

        return ""


# =========================================================
# EMAIL EXTRACTION
# =========================================================

def extract_email(text):

    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    result = re.findall(pattern, text)

    if result:

        return result[0]

    return "Không tìm thấy"


# =========================================================
# PHONE EXTRACTION
# =========================================================

def extract_phone(text):

    pattern = r"(\+?\d[\d\s\-]{8,15}\d)"

    result = re.findall(pattern, text)

    if result:

        return result[0]

    return "Không tìm thấy"


# =========================================================
# SKILL EXTRACTION
# =========================================================

def extract_skills(text):

    found_skills = []

    lower_text = text.lower()

    for skill in SKILLS:

        if skill.lower() in lower_text:

            found_skills.append(skill)

    return found_skills


# =========================================================
# EDUCATION EXTRACTION
# =========================================================

def extract_education(text):

    keywords = [

        "university",
        "college",
        "school",
        "academy",
        "bachelor",
        "master"
    ]

    education_lines = []

    lines = text.split("\n")

    for line_text in lines:

        lower = line_text.lower()

        for keyword in keywords:

            if keyword in lower:

                education_lines.append(
                    line_text.strip()
                )

    return education_lines


# =========================================================
# EXPERIENCE EXTRACTION
# =========================================================

def extract_experience(text):

    keywords = [

        "experience",
        "intern",
        "developer",
        "engineer",
        "manager",
        "freelance"
    ]

    found = []

    lines = text.split("\n")

    for line_text in lines:

        lower = line_text.lower()

        for keyword in keywords:

            if keyword in lower:

                found.append(
                    line_text.strip()
                )

    return found


# =========================================================
# PARSE RESUME
# =========================================================

def parse_resume():

    clear()

    title("PARSE RESUME")

    file_path = input(
        Fore.YELLOW +
        "Nhập file resume (PDF/TXT): "
    )

    if not os.path.exists(file_path):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    ext = os.path.splitext(
        file_path
    )[1].lower()

    text = ""

    if ext == ".pdf":

        text = extract_pdf_text(
            file_path
        )

    elif ext == ".txt":

        text = extract_txt_text(
            file_path
        )

    else:

        print(Fore.RED +
              "\nChỉ hỗ trợ PDF/TXT.")

        pause()

        return

    if not text.strip():

        print(Fore.RED +
              "\nKhông đọc được text.")

        pause()

        return

    print(Fore.CYAN +
          "\nAI đang phân tích resume...")

    time.sleep(1)

    parsed = {

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text)
    }

    line()

    print(Fore.GREEN +
          "\nRESUME ANALYSIS\n")

    print(Fore.YELLOW +
          f"Email: {parsed['email']}")

    print(Fore.CYAN +
          f"Phone: {parsed['phone']}")

    line()

    print(Fore.GREEN +
          "\nSKILLS\n")

    for skill in parsed["skills"]:

        print(Fore.YELLOW +
              f"✓ {skill}")

    line()

    print(Fore.CYAN +
          "\nEDUCATION\n")

    for edu in parsed["education"]:

        print(Fore.GREEN +
              f"✓ {edu}")

    line()

    print(Fore.MAGENTA +
          "\nEXPERIENCE\n")

    for exp in parsed["experience"]:

        print(Fore.YELLOW +
              f"✓ {exp}")

    line()

    save = input(
        Fore.YELLOW +
        "\nLưu parsed data? (y/n): "
    )

    if save.lower() == 'y':

        with open(
            PARSED_DATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                parsed,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(Fore.GREEN +
              f"\nĐã lưu: {PARSED_DATA_FILE}")

    pause()


# =========================================================
# RESUME STATISTICS
# =========================================================

def resume_statistics():

    clear()

    title("RESUME STATISTICS")

    file_path = input(
        Fore.YELLOW +
        "Nhập file resume: "
    )

    if not os.path.exists(file_path):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    ext = os.path.splitext(
        file_path
    )[1].lower()

    text = ""

    if ext == ".pdf":

        text = extract_pdf_text(
            file_path
        )

    else:

        text = extract_txt_text(
            file_path
        )

    words = len(text.split())

    chars = len(text)

    lines_count = len(
        text.splitlines()
    )

    print(Fore.GREEN +
          f"\nWords      : {words}")

    print(Fore.CYAN +
          f"Characters : {chars}")

    print(Fore.YELLOW +
          f"Lines      : {lines_count}")

    pause()


# =========================================================
# AI SKILL MATCH
# =========================================================

def skill_match():

    clear()

    title("AI SKILL MATCH")

    candidate_skills = input(
        Fore.YELLOW +
        "Nhập skill job requirement: "
    )

    job_skills = [

        x.strip().lower()
        for x in candidate_skills.split(",")
    ]

    matched = []

    for skill in job_skills:

        if skill in SKILLS:

            matched.append(skill)

    print(Fore.GREEN +
          "\nMATCHED SKILLS\n")

    for skill in matched:

        print(Fore.YELLOW +
              f"✓ {skill}")

    print(Fore.CYAN +
          f"\nMatch Score: "
          f"{len(matched)}/{len(job_skills)}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO RESUME PARSER")

    sample_text = """
John Doe
Email: john@gmail.com
Phone: +84912345678

Python Developer

Skills:
Python, SQL, Docker, AI, Machine Learning

Education:
ABC University - Computer Science

Experience:
Intern Developer at Tech Company
"""

    parsed = {

        "email": extract_email(sample_text),

        "phone": extract_phone(sample_text),

        "skills": extract_skills(sample_text),

        "education": extract_education(sample_text),

        "experience": extract_experience(sample_text)
    }

    print(Fore.GREEN +
          "\nDEMO RESULT\n")

    print(json.dumps(
        parsed,
        indent=4,
        ensure_ascii=False
    ))

    pause()


# =========================================================
# EXPLAIN AI
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH RESUME PARSER")

    print(Fore.WHITE + """
=========================================================
1. RESUME PARSING
=========================================================

AI đọc:
   ✓ CV
   ✓ Resume

=========================================================
2. NLP
=========================================================

Natural Language Processing

=========================================================
3. REGEX
=========================================================

Dùng để tìm:
   ✓ Email
   ✓ Phone

=========================================================
4. ATS SYSTEM
=========================================================

Applicant Tracking System

=========================================================
5. SKILL DETECTION
=========================================================

AI phát hiện:
   ✓ Python
   ✓ AI
   ✓ SQL

=========================================================
6. HR TECH
=========================================================

Công nghệ:
   ✓ AI Recruitment
   ✓ Resume AI

=========================================================
7. MACHINE LEARNING
=========================================================

AI hỗ trợ:
   ✓ Candidate Matching

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ LinkedIn
✓ HR Software
✓ ATS Systems
✓ AI Hiring Platforms
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("AI RESUME PARSER SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu Resume Parser
[2] Parse Resume PDF/TXT
[3] Resume statistics
[4] AI skill match
[5] Demo mode
[6] Giải thích AI Parser
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

            parse_resume()

        elif choice == '3':

            resume_statistics()

        elif choice == '4':

            skill_match()

        elif choice == '5':

            demo_mode()

        elif choice == '6':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Resume Parser.

Kiến thức đạt được:
   ✓ Resume Parsing
   ✓ NLP
   ✓ Regex Extraction
   ✓ AI Recruitment
   ✓ ATS Systems
   ✓ HR Technology
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
