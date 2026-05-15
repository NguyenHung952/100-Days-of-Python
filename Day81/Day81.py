# =========================================================
#          STUDENT EXPENSE TRACKER SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Theo dõi chi tiêu sinh viên
#
# Chức năng:
#   ✓ Quản lý thu nhập/chi tiêu
#   ✓ Phân loại chi tiêu
#   ✓ Theo dõi ngân sách
#   ✓ Monthly Report
#   ✓ Expense Statistics
#   ✓ Budget Warning
#   ✓ Export báo cáo
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
# python student_expense_tracker.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import json
import datetime
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "expense_data.json"

# =========================================================
# DATABASE
# =========================================================

data = {
    "income": [],
    "expenses": [],
    "budget": 0
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

    title("GIỚI THIỆU EXPENSE TRACKER")

    print(Fore.WHITE + """
Student Expense Tracker giúp:

   ✓ Theo dõi chi tiêu sinh viên
   ✓ Quản lý tài chính cá nhân
   ✓ Theo dõi ngân sách
   ✓ Phân tích thu chi

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Income Tracking
✓ Expense Tracking
✓ Budget Management
✓ Monthly Statistics
✓ Expense Categories

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Quản lý tiền ăn
✓ Quản lý tiền học
✓ Theo dõi chi tiêu cá nhân
✓ Quản lý sinh hoạt phí

=========================================================
LỢI ÍCH
=========================================================

✓ Tiết kiệm tiền
✓ Kiểm soát chi tiêu
✓ Tránh vượt ngân sách
✓ Học quản lý tài chính
""")

    line()


# =========================================================
# SET BUDGET
# =========================================================

def set_budget():

    clear()

    title("SET MONTHLY BUDGET")

    try:

        budget = float(input(
            Fore.YELLOW +
            "Nhập ngân sách tháng: "
        ))

        data["budget"] = budget

        save_data()

        print(Fore.GREEN +
              "\nĐã cập nhật budget.")

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

    pause()


# =========================================================
# THÊM THU NHẬP
# =========================================================

def add_income():

    clear()

    title("THÊM THU NHẬP")

    source = input(
        Fore.YELLOW +
        "Nguồn thu nhập: "
    )

    try:

        amount = float(input(
            Fore.YELLOW +
            "Số tiền: "
        ))

    except:

        print(Fore.RED +
              "\nSố tiền không hợp lệ.")

        pause()

        return

    date = datetime.date.today().strftime(
        "%Y-%m-%d"
    )

    income = {
        "source": source,
        "amount": amount,
        "date": date
    }

    data["income"].append(income)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm thu nhập.")

    pause()


# =========================================================
# THÊM CHI TIÊU
# =========================================================

def add_expense():

    clear()

    title("THÊM CHI TIÊU")

    category = input(
        Fore.YELLOW +
        "Danh mục: "
    )

    description = input(
        Fore.YELLOW +
        "Mô tả: "
    )

    try:

        amount = float(input(
            Fore.YELLOW +
            "Số tiền: "
        ))

    except:

        print(Fore.RED +
              "\nSố tiền không hợp lệ.")

        pause()

        return

    date = datetime.date.today().strftime(
        "%Y-%m-%d"
    )

    expense = {
        "category": category,
        "description": description,
        "amount": amount,
        "date": date
    }

    data["expenses"].append(expense)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm chi tiêu.")

    pause()


# =========================================================
# XEM THU NHẬP
# =========================================================

def view_income():

    clear()

    title("DANH SÁCH THU NHẬP")

    if not data["income"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

    else:

        total = 0

        for item in data["income"]:

            print(Fore.GREEN +
                  f"\nNguồn : {item['source']}")

            print(Fore.CYAN +
                  f"Số tiền: {item['amount']}")

            print(Fore.YELLOW +
                  f"Ngày   : {item['date']}")

            total += item["amount"]

            line()

        print(Fore.GREEN +
              f"\nTổng thu nhập: {total}")

    pause()


# =========================================================
# XEM CHI TIÊU
# =========================================================

def view_expenses():

    clear()

    title("DANH SÁCH CHI TIÊU")

    if not data["expenses"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

    else:

        total = 0

        for item in data["expenses"]:

            print(Fore.RED +
                  f"\nDanh mục: {item['category']}")

            print(Fore.CYAN +
                  f"Mô tả   : {item['description']}")

            print(Fore.YELLOW +
                  f"Số tiền : {item['amount']}")

            print(Fore.GREEN +
                  f"Ngày    : {item['date']}")

            total += item["amount"]

            line()

        print(Fore.RED +
              f"\nTổng chi tiêu: {total}")

    pause()


# =========================================================
# TÍNH SỐ DƯ
# =========================================================

def calculate_balance():

    clear()

    title("TÍNH SỐ DƯ")

    total_income = sum(
        item["amount"]
        for item in data["income"]
    )

    total_expense = sum(
        item["amount"]
        for item in data["expenses"]
    )

    balance = total_income - total_expense

    print(Fore.GREEN +
          f"\nTổng thu nhập : {total_income}")

    print(Fore.RED +
          f"Tổng chi tiêu : {total_expense}")

    print(Fore.CYAN +
          f"Số dư hiện tại: {balance}")

    if data["budget"] > 0:

        print(Fore.YELLOW +
              f"Monthly Budget: {data['budget']}")

        if total_expense > data["budget"]:

            print(Fore.RED +
                  "\n⚠ ĐÃ VƯỢT NGÂN SÁCH!")

        else:

            remain = (
                data["budget"] -
                total_expense
            )

            print(Fore.GREEN +
                  f"Còn lại budget: {remain}")

    pause()


# =========================================================
# THỐNG KÊ CHI TIÊU
# =========================================================

def expense_statistics():

    clear()

    title("EXPENSE STATISTICS")

    if not data["expenses"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    categories = {}

    total = 0

    for item in data["expenses"]:

        category = item["category"]

        amount = item["amount"]

        total += amount

        categories[category] = (
            categories.get(category, 0)
            + amount
        )

    print(Fore.GREEN +
          f"\nTổng chi tiêu: {total}")

    line()

    print(Fore.CYAN +
          "\nTHEO DANH MỤC\n")

    for category, amount in categories.items():

        percent = (
            amount / total
        ) * 100

        print(Fore.YELLOW +
              f"{category:<15} "
              f"{amount:<10} "
              f"{percent:.2f}%")

    pause()


# =========================================================
# MONTHLY REPORT
# =========================================================

def monthly_report():

    clear()

    title("MONTHLY REPORT")

    income_total = sum(
        item["amount"]
        for item in data["income"]
    )

    expense_total = sum(
        item["amount"]
        for item in data["expenses"]
    )

    balance = income_total - expense_total

    print(Fore.GREEN +
          "\nMONTHLY FINANCIAL REPORT")

    line()

    print(Fore.CYAN +
          f"\nIncome  : {income_total}")

    print(Fore.RED +
          f"Expense : {expense_total}")

    print(Fore.YELLOW +
          f"Balance : {balance}")

    if balance >= 0:

        print(Fore.GREEN +
              "\nTài chính ổn định.")

    else:

        print(Fore.RED +
              "\n⚠ Chi tiêu vượt thu nhập!")

    pause()


# =========================================================
# EXPORT REPORT
# =========================================================

def export_report():

    clear()

    title("EXPORT REPORT")

    filename = "expense_report.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "STUDENT EXPENSE REPORT\n"
            )

            f.write("=" * 50 + "\n\n")

            f.write("INCOME\n\n")

            for item in data["income"]:

                f.write(
                    f"{item['source']} - "
                    f"{item['amount']}\n"
                )

            f.write("\nEXPENSES\n\n")

            for item in data["expenses"]:

                f.write(
                    f"{item['category']} - "
                    f"{item['amount']}\n"
                )

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

    title("DEMO EXPENSE TRACKER")

    data["income"] = [

        {
            "source": "Ba mẹ gửi",
            "amount": 5000000,
            "date": "2026-05-01"
        }
    ]

    data["expenses"] = [

        {
            "category": "Ăn uống",
            "description": "Cơm trưa",
            "amount": 50000,
            "date": "2026-05-10"
        },

        {
            "category": "Học tập",
            "description": "Mua sách",
            "amount": 200000,
            "date": "2026-05-12"
        }
    ]

    data["budget"] = 3000000

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# GIẢI THÍCH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH EXPENSE TRACKER")

    print(Fore.WHITE + """
=========================================================
1. PERSONAL FINANCE
=========================================================

Quản lý:
   ✓ Thu nhập
   ✓ Chi tiêu
   ✓ Tiết kiệm

=========================================================
2. BUDGET
=========================================================

Ngân sách:
   ✓ Giới hạn chi tiêu

=========================================================
3. EXPENSE CATEGORY
=========================================================

Danh mục:
   ✓ Ăn uống
   ✓ Học tập
   ✓ Giải trí

=========================================================
4. FINANCIAL TRACKING
=========================================================

Theo dõi:
   ✓ Income
   ✓ Expenses
   ✓ Balance

=========================================================
5. STUDENT FINANCE
=========================================================

Giúp sinh viên:
   ✓ Tiết kiệm
   ✓ Tránh lãng phí

=========================================================
6. MONTHLY REPORT
=========================================================

Báo cáo:
   ✓ Thu
   ✓ Chi
   ✓ Số dư

=========================================================
7. JSON DATABASE
=========================================================

Lưu:
   ✓ Income
   ✓ Expense
   ✓ Budget

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Student Finance
✓ Family Budget
✓ Expense Tracking
✓ Financial Planning
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("STUDENT EXPENSE TRACKER")

        print(Fore.CYAN + """
[1] Giới thiệu App
[2] Set monthly budget
[3] Thêm thu nhập
[4] Thêm chi tiêu
[5] Xem thu nhập
[6] Xem chi tiêu
[7] Tính số dư
[8] Expense statistics
[9] Monthly report
[10] Export report
[11] Demo mode
[12] Giải thích chi tiết
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

            set_budget()

        elif choice == '3':

            add_income()

        elif choice == '4':

            add_expense()

        elif choice == '5':

            view_income()

        elif choice == '6':

            view_expenses()

        elif choice == '7':

            calculate_balance()

        elif choice == '8':

            expense_statistics()

        elif choice == '9':

            monthly_report()

        elif choice == '10':

            export_report()

        elif choice == '11':

            demo_mode()

        elif choice == '12':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Student Expense Tracker.

Kiến thức đạt được:
   ✓ Personal Finance
   ✓ Expense Tracking
   ✓ Budget Management
   ✓ Financial Statistics
   ✓ JSON Database
   ✓ Financial Planning
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
