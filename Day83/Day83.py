# =========================================================
#               AUTO CV BUILDER SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Tool tạo CV tự động bằng Python
#
# Chức năng:
#   ✓ Tạo CV tự động
#   ✓ Sinh CV PDF
#   ✓ Quản lý thông tin cá nhân
#   ✓ Skills Manager
#   ✓ Education Section
#   ✓ Work Experience
#   ✓ AI Summary Generator
#   ✓ Export TXT + PDF
#   ✓ CV Preview
#   ✓ Dashboard terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install reportlab colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python auto_cv_builder.py
#
# =========================================================

from colorama import Fore, Style, init

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
import json
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "cv_data.json"

# =========================================================
# DATABASE
# =========================================================

cv_data = {

    "name": "",
    "email": "",
    "phone": "",
    "address": "",
    "summary": "",
    "skills": [],
    "education": [],
    "experience": []
}

# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    global cv_data

    if os.path.exists(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                cv_data = json.load(f)

        except:

            pass


# =========================================================
# SAVE DATA
# =========================================================

def save_data():

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cv_data,
            f,
            indent=4,
            ensure_ascii=False
        )


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

    title("GIỚI THIỆU AUTO CV BUILDER")

    print(Fore.WHITE + """
Auto CV Builder giúp:

   ✓ Tạo CV chuyên nghiệp
   ✓ Export PDF tự động
   ✓ Quản lý kỹ năng cá nhân
   ✓ Tạo Resume hiện đại

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Personal Information
✓ Skills Section
✓ Education Section
✓ Experience Section
✓ PDF Export

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Xin việc
✓ Internship
✓ Freelancer
✓ Portfolio
✓ LinkedIn Resume

=========================================================
LỢI ÍCH
=========================================================

✓ Nhanh
✓ Chuyên nghiệp
✓ Dễ chỉnh sửa
✓ Tự động hóa
""")

    line()


# =========================================================
# NHẬP THÔNG TIN CÁ NHÂN
# =========================================================

def personal_info():

    clear()

    title("PERSONAL INFORMATION")

    cv_data["name"] = input(
        Fore.YELLOW +
        "Họ tên: "
    )

    cv_data["email"] = input(
        Fore.YELLOW +
        "Email: "
    )

    cv_data["phone"] = input(
        Fore.YELLOW +
        "Số điện thoại: "
    )

    cv_data["address"] = input(
        Fore.YELLOW +
        "Địa chỉ: "
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã lưu thông tin.")

    pause()


# =========================================================
# AI SUMMARY GENERATOR
# =========================================================

def generate_summary():

    clear()

    title("AI SUMMARY GENERATOR")

    role = input(
        Fore.YELLOW +
        "Vị trí ứng tuyển: "
    )

    years = input(
        Fore.YELLOW +
        "Số năm kinh nghiệm: "
    )

    summary = f"""
Tôi là ứng viên năng động với {years} năm kinh nghiệm
trong lĩnh vực {role}. Có khả năng làm việc nhóm,
giải quyết vấn đề và học hỏi công nghệ mới nhanh chóng.
Mục tiêu là phát triển kỹ năng chuyên môn và đóng góp
giá trị cho doanh nghiệp.
"""

    cv_data["summary"] = summary

    save_data()

    print(Fore.GREEN +
          "\nAI SUMMARY\n")

    print(Fore.WHITE + summary)

    pause()


# =========================================================
# ADD SKILL
# =========================================================

def add_skill():

    clear()

    title("ADD SKILL")

    skill = input(
        Fore.YELLOW +
        "Nhập skill: "
    )

    cv_data["skills"].append(skill)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm skill.")

    pause()


# =========================================================
# VIEW SKILLS
# =========================================================

def view_skills():

    clear()

    title("SKILLS")

    if not cv_data["skills"]:

        print(Fore.RED +
              "\nChưa có skills.")

    else:

        for skill in cv_data["skills"]:

            print(Fore.GREEN +
                  f"✓ {skill}")

    pause()


# =========================================================
# ADD EDUCATION
# =========================================================

def add_education():

    clear()

    title("ADD EDUCATION")

    school = input(
        Fore.YELLOW +
        "Trường học: "
    )

    major = input(
        Fore.YELLOW +
        "Chuyên ngành: "
    )

    year = input(
        Fore.YELLOW +
        "Năm học: "
    )

    edu = {

        "school": school,
        "major": major,
        "year": year
    }

    cv_data["education"].append(edu)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm education.")

    pause()


# =========================================================
# ADD EXPERIENCE
# =========================================================

def add_experience():

    clear()

    title("ADD EXPERIENCE")

    company = input(
        Fore.YELLOW +
        "Công ty: "
    )

    role = input(
        Fore.YELLOW +
        "Vị trí: "
    )

    years = input(
        Fore.YELLOW +
        "Thời gian làm việc: "
    )

    exp = {

        "company": company,
        "role": role,
        "years": years
    }

    cv_data["experience"].append(exp)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm experience.")

    pause()


# =========================================================
# CV PREVIEW
# =========================================================

def preview_cv():

    clear()

    title("CV PREVIEW")

    print(Fore.GREEN +
          f"\n{cv_data['name']}")

    print(Fore.CYAN +
          f"Email : {cv_data['email']}")

    print(Fore.YELLOW +
          f"Phone : {cv_data['phone']}")

    print(Fore.WHITE +
          f"Address: {cv_data['address']}")

    line()

    print(Fore.GREEN +
          "\nSUMMARY\n")

    print(Fore.WHITE +
          cv_data["summary"])

    line()

    print(Fore.CYAN +
          "\nSKILLS\n")

    for skill in cv_data["skills"]:

        print(Fore.GREEN +
              f"✓ {skill}")

    line()

    print(Fore.YELLOW +
          "\nEDUCATION\n")

    for edu in cv_data["education"]:

        print(Fore.GREEN +
              f"{edu['school']}")

        print(Fore.CYAN +
              f"{edu['major']}")

        print(Fore.YELLOW +
              f"{edu['year']}\n")

    line()

    print(Fore.MAGENTA +
          "\nEXPERIENCE\n")

    for exp in cv_data["experience"]:

        print(Fore.GREEN +
              f"{exp['company']}")

        print(Fore.CYAN +
              f"{exp['role']}")

        print(Fore.YELLOW +
              f"{exp['years']}\n")

    pause()


# =========================================================
# EXPORT TXT
# =========================================================

def export_txt():

    clear()

    title("EXPORT TXT CV")

    filename = "cv_output.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"{cv_data['name']}\n"
            )

            f.write(
                f"{cv_data['email']}\n"
            )

            f.write(
                f"{cv_data['phone']}\n"
            )

            f.write(
                f"{cv_data['address']}\n\n"
            )

            f.write("SUMMARY\n")
            f.write(cv_data["summary"] + "\n\n")

            f.write("SKILLS\n")

            for skill in cv_data["skills"]:

                f.write(f"- {skill}\n")

            f.write("\nEDUCATION\n")

            for edu in cv_data["education"]:

                f.write(
                    f"{edu['school']} - "
                    f"{edu['major']} - "
                    f"{edu['year']}\n"
                )

            f.write("\nEXPERIENCE\n")

            for exp in cv_data["experience"]:

                f.write(
                    f"{exp['company']} - "
                    f"{exp['role']} - "
                    f"{exp['years']}\n"
                )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# EXPORT PDF
# =========================================================

def export_pdf():

    clear()

    title("EXPORT PDF CV")

    filename = "cv_output.pdf"

    try:

        c = canvas.Canvas(
            filename,
            pagesize=letter
        )

        y = 750

        c.setFont("Helvetica-Bold", 18)

        c.drawString(
            50,
            y,
            cv_data["name"]
        )

        y -= 30

        c.setFont("Helvetica", 12)

        c.drawString(
            50,
            y,
            f"Email: {cv_data['email']}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Phone: {cv_data['phone']}"
        )

        y -= 20

        c.drawString(
            50,
            y,
            f"Address: {cv_data['address']}"
        )

        y -= 40

        c.setFont("Helvetica-Bold", 14)

        c.drawString(
            50,
            y,
            "SUMMARY"
        )

        y -= 20

        c.setFont("Helvetica", 11)

        for line_text in cv_data["summary"].split("\n"):

            c.drawString(
                50,
                y,
                line_text
            )

            y -= 15

        y -= 20

        c.setFont("Helvetica-Bold", 14)

        c.drawString(
            50,
            y,
            "SKILLS"
        )

        y -= 20

        c.setFont("Helvetica", 11)

        for skill in cv_data["skills"]:

            c.drawString(
                60,
                y,
                f"- {skill}"
            )

            y -= 15

        y -= 20

        c.setFont("Helvetica-Bold", 14)

        c.drawString(
            50,
            y,
            "EDUCATION"
        )

        y -= 20

        c.setFont("Helvetica", 11)

        for edu in cv_data["education"]:

            c.drawString(
                60,
                y,
                f"{edu['school']} - "
                f"{edu['major']} "
                f"({edu['year']})"
            )

            y -= 15

        y -= 20

        c.setFont("Helvetica-Bold", 14)

        c.drawString(
            50,
            y,
            "EXPERIENCE"
        )

        y -= 20

        c.setFont("Helvetica", 11)

        for exp in cv_data["experience"]:

            c.drawString(
                60,
                y,
                f"{exp['company']} - "
                f"{exp['role']} "
                f"({exp['years']})"
            )

            y -= 15

        c.save()

        print(Fore.GREEN +
              f"\nĐã export PDF: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi PDF:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO CV DATA")

    cv_data["name"] = "Nguyen Van A"

    cv_data["email"] = "nguyenvana@gmail.com"

    cv_data["phone"] = "0123456789"

    cv_data["address"] = "Ho Chi Minh City"

    cv_data["summary"] = """
Sinh viên IT năng động với kỹ năng Python,
AI và phát triển phần mềm.
"""

    cv_data["skills"] = [
        "Python",
        "Machine Learning",
        "SQL",
        "Git"
    ]

    cv_data["education"] = [

        {
            "school": "ABC University",
            "major": "Computer Science",
            "year": "2022-2026"
        }
    ]

    cv_data["experience"] = [

        {
            "company": "Tech Company",
            "role": "Intern Developer",
            "years": "2025"
        }
    ]

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# EXPLAIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH CV BUILDER")

    print(Fore.WHITE + """
=========================================================
1. CV / RESUME
=========================================================

CV:
   Curriculum Vitae

=========================================================
2. PERSONAL BRANDING
=========================================================

CV giúp:
   ✓ Giới thiệu bản thân
   ✓ Thể hiện kỹ năng

=========================================================
3. ATS SYSTEM
=========================================================

AI tuyển dụng quét:
   ✓ Skills
   ✓ Keywords

=========================================================
4. PDF RESUME
=========================================================

PDF là chuẩn:
   ✓ Professional
   ✓ Portable

=========================================================
5. AI SUMMARY
=========================================================

AI tự sinh:
   ✓ Career Summary

=========================================================
6. SKILLS SECTION
=========================================================

Ví dụ:
   ✓ Python
   ✓ AI
   ✓ SQL

=========================================================
7. EXPERIENCE
=========================================================

Kinh nghiệm:
   ✓ Internship
   ✓ Freelance
   ✓ Projects

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Job Application
✓ Internship
✓ Freelancer
✓ LinkedIn
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("AUTO CV BUILDER SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu CV Builder
[2] Nhập thông tin cá nhân
[3] AI generate summary
[4] Add skill
[5] View skills
[6] Add education
[7] Add experience
[8] Preview CV
[9] Export TXT CV
[10] Export PDF CV
[11] Demo mode
[12] Giải thích CV System
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

            personal_info()

        elif choice == '3':

            generate_summary()

        elif choice == '4':

            add_skill()

        elif choice == '5':

            view_skills()

        elif choice == '6':

            add_education()

        elif choice == '7':

            add_experience()

        elif choice == '8':

            preview_cv()

        elif choice == '9':

            export_txt()

        elif choice == '10':

            export_pdf()

        elif choice == '11':

            demo_mode()

        elif choice == '12':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Auto CV Builder.

Kiến thức đạt được:
   ✓ Resume Building
   ✓ PDF Generation
   ✓ Career Branding
   ✓ ATS Resume
   ✓ Personal Portfolio
   ✓ Professional CV Design
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
