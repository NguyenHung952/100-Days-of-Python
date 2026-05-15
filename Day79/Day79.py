# =========================================================
#           STUDY MANAGEMENT DASHBOARD
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Dashboard quản lý học tập bằng Python
#
# Chức năng:
#   ✓ Quản lý môn học
#   ✓ Thêm/Xóa task học tập
#   ✓ Theo dõi tiến độ học
#   ✓ Pomodoro Timer
#   ✓ Quản lý deadline
#   ✓ GPA Calculator
#   ✓ Thống kê học tập
#   ✓ Lưu dữ liệu JSON
#   ✓ Dashboard terminal hiện đại
#   ✓ Demo mode
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python study_dashboard.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import json
import time
import datetime

init(autoreset=True)

# =========================================================
# FILE DATA
# =========================================================

DATA_FILE = "study_data.json"

# =========================================================
# DATA
# =========================================================

data = {
    "subjects": [],
    "tasks": [],
    "grades": []
}

# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    global data

    if os.path.exists(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

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
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


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

    title("GIỚI THIỆU STUDY DASHBOARD")

    print(Fore.WHITE + """
Study Dashboard giúp:

   ✓ Quản lý học tập
   ✓ Theo dõi deadline
   ✓ Quản lý task
   ✓ Theo dõi GPA

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Subject Manager
✓ Study Tasks
✓ GPA Calculator
✓ Pomodoro Timer
✓ Progress Tracking

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Sinh viên
✓ Học sinh
✓ Self-learning
✓ Online Courses

=========================================================
LỢI ÍCH
=========================================================

✓ Học tập có tổ chức
✓ Tăng hiệu suất
✓ Theo dõi tiến độ
✓ Giảm quên deadline
""")

    line()


# =========================================================
# THÊM MÔN HỌC
# =========================================================

def add_subject():

    clear()

    title("THÊM MÔN HỌC")

    name = input(
        Fore.YELLOW +
        "Tên môn học: "
    )

    teacher = input(
        Fore.YELLOW +
        "Giảng viên: "
    )

    subject = {
        "name": name,
        "teacher": teacher
    }

    data["subjects"].append(subject)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm môn học.")

    pause()


# =========================================================
# XEM MÔN HỌC
# =========================================================

def view_subjects():

    clear()

    title("DANH SÁCH MÔN HỌC")

    if not data["subjects"]:

        print(Fore.RED +
              "\nChưa có môn học.")

    else:

        for index, subject in enumerate(
            data["subjects"],
            start=1
        ):

            print(Fore.GREEN +
                  f"\n[{index}] {subject['name']}")

            print(Fore.CYAN +
                  f"Giảng viên: "
                  f"{subject['teacher']}")

            line()

    pause()


# =========================================================
# THÊM TASK
# =========================================================

def add_task():

    clear()

    title("THÊM TASK HỌC TẬP")

    task_name = input(
        Fore.YELLOW +
        "Tên task: "
    )

    subject = input(
        Fore.YELLOW +
        "Môn học: "
    )

    deadline = input(
        Fore.YELLOW +
        "Deadline (YYYY-MM-DD): "
    )

    task = {
        "task": task_name,
        "subject": subject,
        "deadline": deadline,
        "done": False
    }

    data["tasks"].append(task)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm task.")

    pause()


# =========================================================
# XEM TASK
# =========================================================

def view_tasks():

    clear()

    title("STUDY TASKS")

    if not data["tasks"]:

        print(Fore.RED +
              "\nChưa có task.")

    else:

        for index, task in enumerate(
            data["tasks"],
            start=1
        ):

            color = Fore.GREEN

            status = "DONE"

            if not task["done"]:

                color = Fore.RED

                status = "PENDING"

            print(color +
                  f"\n[{index}] {task['task']}")

            print(Fore.CYAN +
                  f"Môn học : {task['subject']}")

            print(Fore.YELLOW +
                  f"Deadline: {task['deadline']}")

            print(color +
                  f"Status  : {status}")

            line()

    pause()


# =========================================================
# HOÀN THÀNH TASK
# =========================================================

def complete_task():

    clear()

    title("COMPLETE TASK")

    if not data["tasks"]:

        print(Fore.RED +
              "\nKhông có task.")

        pause()

        return

    for index, task in enumerate(
        data["tasks"],
        start=1
    ):

        print(Fore.GREEN +
              f"[{index}] {task['task']}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn task: "
        ))

        data["tasks"][choice - 1]["done"] = True

        save_data()

        print(Fore.GREEN +
              "\nTask completed.")

    except:

        print(Fore.RED +
              "\nLỗi.")

    pause()


# =========================================================
# GPA CALCULATOR
# =========================================================

def add_grade():

    clear()

    title("THÊM ĐIỂM")

    subject = input(
        Fore.YELLOW +
        "Môn học: "
    )

    try:

        grade = float(input(
            Fore.YELLOW +
            "Điểm: "
        ))

    except:

        print(Fore.RED +
              "\nĐiểm không hợp lệ.")

        pause()

        return

    data["grades"].append({
        "subject": subject,
        "grade": grade
    })

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm điểm.")

    pause()


def calculate_gpa():

    clear()

    title("GPA CALCULATOR")

    if not data["grades"]:

        print(Fore.RED +
              "\nChưa có điểm.")

        pause()

        return

    total = 0

    for g in data["grades"]:

        total += g["grade"]

    gpa = total / len(data["grades"])

    print(Fore.GREEN +
          f"\nGPA: {round(gpa, 2)}")

    print(Fore.CYAN +
          "\nCHI TIẾT\n")

    for item in data["grades"]:

        print(Fore.YELLOW +
              f"{item['subject']:<20} "
              f"{item['grade']}")

    pause()


# =========================================================
# POMODORO TIMER
# =========================================================

def pomodoro_timer():

    clear()

    title("POMODORO TIMER")

    try:

        minutes = int(input(
            Fore.YELLOW +
            "Thời gian học (phút): "
        ))

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    seconds = minutes * 60

    print(Fore.GREEN +
          "\nPomodoro bắt đầu...\n")

    try:

        while seconds > 0:

            mins = seconds // 60

            secs = seconds % 60

            timer = f"{mins:02d}:{secs:02d}"

            print(Fore.CYAN +
                  f"\rTime: {timer}",
                  end="")

            time.sleep(1)

            seconds -= 1

        print(Fore.GREEN +
              "\n\nHoàn thành Pomodoro!")

    except KeyboardInterrupt:

        print(Fore.RED +
              "\n\nĐã dừng timer.")

    pause()


# =========================================================
# THỐNG KÊ
# =========================================================

def statistics():

    clear()

    title("STUDY STATISTICS")

    total_subjects = len(data["subjects"])

    total_tasks = len(data["tasks"])

    completed = sum(
        1 for t in data["tasks"]
        if t["done"]
    )

    pending = total_tasks - completed

    print(Fore.GREEN +
          f"\nMôn học      : {total_subjects}")

    print(Fore.CYAN +
          f"Total Tasks  : {total_tasks}")

    print(Fore.GREEN +
          f"Completed    : {completed}")

    print(Fore.RED +
          f"Pending      : {pending}")

    if total_tasks > 0:

        progress = (
            completed / total_tasks
        ) * 100

        print(Fore.YELLOW +
              f"Progress     : "
              f"{progress:.2f}%")

    pause()


# =========================================================
# DEADLINE CHECKER
# =========================================================

def deadline_checker():

    clear()

    title("DEADLINE CHECKER")

    today = datetime.date.today()

    found = False

    for task in data["tasks"]:

        if not task["done"]:

            try:

                deadline = datetime.datetime.strptime(
                    task["deadline"],
                    "%Y-%m-%d"
                ).date()

                days_left = (
                    deadline - today
                ).days

                if days_left <= 3:

                    found = True

                    print(Fore.RED +
                          f"\n⚠ {task['task']}")

                    print(Fore.YELLOW +
                          f"Còn {days_left} ngày")

                    line()

            except:
                pass

    if not found:

        print(Fore.GREEN +
              "\nKhông có deadline gấp.")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO STUDY DASHBOARD")

    demo_subjects = [
        {
            "name": "Python",
            "teacher": "Mr. AI"
        },

        {
            "name": "Math",
            "teacher": "Dr. Logic"
        }
    ]

    demo_tasks = [
        {
            "task": "Làm bài tập Python",
            "subject": "Python",
            "deadline": "2026-05-20",
            "done": False
        }
    ]

    data["subjects"] = demo_subjects

    data["tasks"] = demo_tasks

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# GIẢI THÍCH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH STUDY DASHBOARD")

    print(Fore.WHITE + """
=========================================================
1. STUDY MANAGEMENT
=========================================================

Quản lý:
   ✓ Môn học
   ✓ Task
   ✓ Deadline

=========================================================
2. GPA
=========================================================

Grade Point Average

=========================================================
3. POMODORO
=========================================================

Kỹ thuật học:
   ✓ 25 phút tập trung
   ✓ 5 phút nghỉ

=========================================================
4. PRODUCTIVITY
=========================================================

Tăng:
   ✓ Hiệu suất học
   ✓ Quản lý thời gian

=========================================================
5. TASK MANAGEMENT
=========================================================

✓ Add Task
✓ Complete Task
✓ Track Progress

=========================================================
6. DEADLINE TRACKING
=========================================================

Nhắc deadline gần tới.

=========================================================
7. JSON DATABASE
=========================================================

Lưu dữ liệu:
   ✓ Subjects
   ✓ Tasks
   ✓ Grades

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ University
✓ Online Learning
✓ Self-learning
✓ Bootcamp
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("STUDY MANAGEMENT DASHBOARD")

        print(Fore.CYAN + """
[1] Giới thiệu Dashboard
[2] Thêm môn học
[3] Xem môn học
[4] Thêm task học tập
[5] Xem task
[6] Complete task
[7] Thêm điểm
[8] GPA calculator
[9] Pomodoro timer
[10] Study statistics
[11] Deadline checker
[12] Demo mode
[13] Giải thích Dashboard
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

            add_subject()

        elif choice == '3':

            view_subjects()

        elif choice == '4':

            add_task()

        elif choice == '5':

            view_tasks()

        elif choice == '6':

            complete_task()

        elif choice == '7':

            add_grade()

        elif choice == '8':

            calculate_gpa()

        elif choice == '9':

            pomodoro_timer()

        elif choice == '10':

            statistics()

        elif choice == '11':

            deadline_checker()

        elif choice == '12':

            demo_mode()

        elif choice == '13':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Study Dashboard.

Kiến thức đạt được:
   ✓ Study Management
   ✓ Productivity
   ✓ GPA Calculation
   ✓ Pomodoro Technique
   ✓ Task Tracking
   ✓ JSON Database
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
