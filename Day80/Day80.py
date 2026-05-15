# =========================================================
#           STUDENT DEADLINE MANAGER APP
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : App quản lý deadline sinh viên
#
# Chức năng:
#   ✓ Quản lý deadline học tập
#   ✓ Thêm/Xóa/Sửa công việc
#   ✓ Deadline reminder
#   ✓ Phân loại môn học
#   ✓ Priority task
#   ✓ Theo dõi tiến độ
#   ✓ Calendar task
#   ✓ Countdown deadline
#   ✓ Export report
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
# python student_deadline_manager.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import json
import time
import datetime

init(autoreset=True)

# =========================================================
# FILE DATABASE
# =========================================================

DATA_FILE = "deadline_data.json"

# =========================================================
# DATABASE
# =========================================================

data = {
    "tasks": []
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

    title("GIỚI THIỆU DEADLINE MANAGER")

    print(Fore.WHITE + """
Student Deadline Manager giúp:

   ✓ Quản lý deadline học tập
   ✓ Nhắc việc tự động
   ✓ Theo dõi tiến độ học
   ✓ Quản lý task sinh viên

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Add Task
✓ Deadline Reminder
✓ Priority Task
✓ Progress Tracking
✓ Countdown Timer

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Homework
✓ Assignment
✓ Exam Schedule
✓ Research Project
✓ Online Course

=========================================================
LỢI ÍCH
=========================================================

✓ Không quên deadline
✓ Học tập có tổ chức
✓ Tăng productivity
✓ Quản lý thời gian tốt hơn
""")

    line()


# =========================================================
# THÊM TASK
# =========================================================

def add_task():

    clear()

    title("THÊM DEADLINE TASK")

    name = input(
        Fore.YELLOW +
        "Tên công việc: "
    )

    subject = input(
        Fore.YELLOW +
        "Môn học: "
    )

    deadline = input(
        Fore.YELLOW +
        "Deadline (YYYY-MM-DD): "
    )

    print(Fore.CYAN + """
1. LOW
2. MEDIUM
3. HIGH
""")

    priority_choice = input(
        Fore.YELLOW +
        "Priority: "
    )

    priority_map = {
        "1": "LOW",
        "2": "MEDIUM",
        "3": "HIGH"
    }

    priority = priority_map.get(
        priority_choice,
        "MEDIUM"
    )

    task = {
        "name": name,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
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

    title("DANH SÁCH DEADLINE")

    if not data["tasks"]:

        print(Fore.RED +
              "\nKhông có task.")

        pause()

        return

    for index, task in enumerate(
        data["tasks"],
        start=1
    ):

        color = Fore.GREEN

        if task["priority"] == "HIGH":

            color = Fore.RED

        elif task["priority"] == "MEDIUM":

            color = Fore.YELLOW

        status = "DONE"

        if not task["done"]:

            status = "PENDING"

        print(color +
              f"\n[{index}] {task['name']}")

        print(Fore.CYAN +
              f"Môn học : {task['subject']}")

        print(Fore.YELLOW +
              f"Deadline: {task['deadline']}")

        print(color +
              f"Priority: {task['priority']}")

        print(Fore.GREEN +
              f"Status  : {status}")

        line()

    pause()


# =========================================================
# COMPLETE TASK
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
              f"[{index}] {task['name']}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn task hoàn thành: "
        ))

        data["tasks"][choice - 1]["done"] = True

        save_data()

        print(Fore.GREEN +
              "\nTask completed.")

    except:

        print(Fore.RED +
              "\nLỗi thao tác.")

    pause()


# =========================================================
# DELETE TASK
# =========================================================

def delete_task():

    clear()

    title("DELETE TASK")

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
              f"[{index}] {task['name']}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn task xóa: "
        ))

        removed = data["tasks"].pop(choice - 1)

        save_data()

        print(Fore.RED +
              f"\nĐã xóa: {removed['name']}")

    except:

        print(Fore.RED +
              "\nLỗi xóa task.")

    pause()


# =========================================================
# DEADLINE REMINDER
# =========================================================

def deadline_reminder():

    clear()

    title("DEADLINE REMINDER")

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

                if days_left <= 7:

                    found = True

                    color = Fore.GREEN

                    if days_left <= 1:

                        color = Fore.RED

                    elif days_left <= 3:

                        color = Fore.YELLOW

                    print(color +
                          f"\n⚠ {task['name']}")

                    print(Fore.CYAN +
                          f"Môn học: {task['subject']}")

                    print(color +
                          f"Còn {days_left} ngày")

                    line()

            except:
                pass

    if not found:

        print(Fore.GREEN +
              "\nKhông có deadline gần.")

    pause()


# =========================================================
# COUNTDOWN DEADLINE
# =========================================================

def countdown_deadline():

    clear()

    title("COUNTDOWN DEADLINE")

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
              f"[{index}] {task['name']}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn task: "
        ))

        task = data["tasks"][choice - 1]

        deadline = datetime.datetime.strptime(
            task["deadline"],
            "%Y-%m-%d"
        )

        now = datetime.datetime.now()

        remaining = deadline - now

        print(Fore.CYAN +
              f"\nCountdown: {remaining}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# THỐNG KÊ
# =========================================================

def statistics():

    clear()

    title("STUDENT STATISTICS")

    total = len(data["tasks"])

    completed = sum(
        1 for t in data["tasks"]
        if t["done"]
    )

    pending = total - completed

    high_priority = sum(
        1 for t in data["tasks"]
        if t["priority"] == "HIGH"
    )

    print(Fore.GREEN +
          f"\nTotal Tasks   : {total}")

    print(Fore.CYAN +
          f"Completed     : {completed}")

    print(Fore.RED +
          f"Pending       : {pending}")

    print(Fore.YELLOW +
          f"High Priority : {high_priority}")

    if total > 0:

        progress = (
            completed / total
        ) * 100

        print(Fore.GREEN +
              f"Progress      : "
              f"{progress:.2f}%")

    pause()


# =========================================================
# EXPORT REPORT
# =========================================================

def export_report():

    clear()

    title("EXPORT REPORT")

    filename = "deadline_report.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "STUDENT DEADLINE REPORT\n"
            )

            f.write("=" * 50 + "\n\n")

            for task in data["tasks"]:

                f.write(
                    f"Task     : {task['name']}\n"
                )

                f.write(
                    f"Subject  : {task['subject']}\n"
                )

                f.write(
                    f"Deadline : {task['deadline']}\n"
                )

                f.write(
                    f"Priority : {task['priority']}\n"
                )

                f.write(
                    f"Status   : "
                    f"{'DONE' if task['done'] else 'PENDING'}\n"
                )

                f.write("\n")

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO DEADLINE MANAGER")

    demo_tasks = [

        {
            "name": "Làm bài Python",
            "subject": "Python",
            "deadline": "2026-05-20",
            "priority": "HIGH",
            "done": False
        },

        {
            "name": "Ôn thi Math",
            "subject": "Math",
            "deadline": "2026-05-25",
            "priority": "MEDIUM",
            "done": False
        }
    ]

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

    title("GIẢI THÍCH DEADLINE MANAGER")

    print(Fore.WHITE + """
=========================================================
1. DEADLINE
=========================================================

Deadline:
   ✓ Hạn chót công việc

=========================================================
2. TASK MANAGEMENT
=========================================================

Quản lý:
   ✓ Assignment
   ✓ Homework
   ✓ Project

=========================================================
3. PRIORITY
=========================================================

✓ LOW
✓ MEDIUM
✓ HIGH

=========================================================
4. PRODUCTIVITY
=========================================================

Giúp:
   ✓ Học tập hiệu quả
   ✓ Quản lý thời gian

=========================================================
5. COUNTDOWN
=========================================================

Hiển thị:
   ✓ Thời gian còn lại

=========================================================
6. JSON DATABASE
=========================================================

Lưu:
   ✓ Tasks
   ✓ Deadlines
   ✓ Progress

=========================================================
7. STUDENT ORGANIZATION
=========================================================

✓ Planning
✓ Time Management
✓ Study Tracking

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ University
✓ School
✓ Bootcamp
✓ Online Learning
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("STUDENT DEADLINE MANAGER")

        print(Fore.CYAN + """
[1] Giới thiệu App
[2] Thêm deadline task
[3] Xem deadline tasks
[4] Complete task
[5] Delete task
[6] Deadline reminder
[7] Countdown deadline
[8] Statistics
[9] Export report
[10] Demo mode
[11] Giải thích chi tiết
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

            add_task()

        elif choice == '3':

            view_tasks()

        elif choice == '4':

            complete_task()

        elif choice == '5':

            delete_task()

        elif choice == '6':

            deadline_reminder()

        elif choice == '7':

            countdown_deadline()

        elif choice == '8':

            statistics()

        elif choice == '9':

            export_report()

        elif choice == '10':

            demo_mode()

        elif choice == '11':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Student Deadline Manager.

Kiến thức đạt được:
   ✓ Deadline Tracking
   ✓ Task Management
   ✓ Productivity
   ✓ Time Management
   ✓ JSON Database
   ✓ Study Planning
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
