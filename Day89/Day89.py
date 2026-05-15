# =========================================================
#           ELECTRONIC BOM GENERATOR SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : BOM Generator cho project điện tử
#
# Chức năng:
#   ✓ Tạo BOM tự động
#   ✓ Quản lý linh kiện project
#   ✓ Tính tổng chi phí
#   ✓ Export CSV BOM
#   ✓ Inventory summary
#   ✓ Search component
#   ✓ BOM statistics
#   ✓ Cost analysis
#   ✓ Save project JSON
#   ✓ Dashboard terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pandas colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python bom_generator.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import json
import os
import time
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "bom_project.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "",
    "components": []
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

    title("GIỚI THIỆU BOM GENERATOR")

    print(Fore.WHITE + """
BOM Generator giúp:

   ✓ Tạo Bill Of Materials tự động
   ✓ Quản lý linh kiện project điện tử
   ✓ Tính tổng chi phí project
   ✓ Export BOM chuyên nghiệp

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ BOM Creation
✓ Cost Analysis
✓ CSV Export
✓ Component Tracking
✓ Inventory Summary

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Arduino Projects
✓ IoT Devices
✓ PCB Design
✓ Robotics
✓ Embedded Systems

=========================================================
THÔNG TIN BOM
=========================================================

✓ Component Name
✓ Quantity
✓ Unit Price
✓ Total Cost
✓ Supplier
""")

    line()


# =========================================================
# SET PROJECT NAME
# =========================================================

def set_project():

    clear()

    title("SET PROJECT")

    project_name = input(
        Fore.YELLOW +
        "Tên project: "
    )

    data["project_name"] = project_name

    save_data()

    print(Fore.GREEN +
          "\nĐã lưu project.")

    pause()


# =========================================================
# ADD COMPONENT
# =========================================================

def add_component():

    clear()

    title("ADD COMPONENT")

    name = input(
        Fore.YELLOW +
        "Tên linh kiện: "
    )

    category = input(
        Fore.YELLOW +
        "Category: "
    )

    supplier = input(
        Fore.YELLOW +
        "Supplier: "
    )

    try:

        quantity = int(input(
            Fore.YELLOW +
            "Số lượng: "
        ))

        price = float(input(
            Fore.YELLOW +
            "Giá mỗi linh kiện: "
        ))

    except:

        print(Fore.RED +
              "\nDữ liệu không hợp lệ.")

        pause()

        return

    total_cost = quantity * price

    component = {

        "name": name,
        "category": category,
        "supplier": supplier,
        "quantity": quantity,
        "price": price,
        "total_cost": total_cost,
        "date_added": str(
            datetime.date.today()
        )
    }

    data["components"].append(
        component
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm linh kiện.")

    pause()


# =========================================================
# VIEW BOM
# =========================================================

def view_bom():

    clear()

    title("BILL OF MATERIALS")

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    line()

    if not data["components"]:

        print(Fore.RED +
              "\nChưa có linh kiện.")

        pause()

        return

    for index, item in enumerate(
        data["components"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {item['name']}")

        print(Fore.CYAN +
              f"Category : {item['category']}")

        print(Fore.YELLOW +
              f"Supplier : {item['supplier']}")

        print(Fore.MAGENTA +
              f"Quantity : {item['quantity']}")

        print(Fore.WHITE +
              f"Unit Price: {item['price']}")

        print(Fore.GREEN +
              f"Total Cost: {item['total_cost']}")

        line()

    pause()


# =========================================================
# SEARCH COMPONENT
# =========================================================

def search_component():

    clear()

    title("SEARCH COMPONENT")

    keyword = input(
        Fore.YELLOW +
        "Nhập tên linh kiện: "
    ).lower()

    found = False

    for item in data["components"]:

        if keyword in item["name"].lower():

            found = True

            print(Fore.GREEN +
                  f"\n{item['name']}")

            print(Fore.CYAN +
                  f"Supplier: {item['supplier']}")

            print(Fore.YELLOW +
                  f"Quantity: {item['quantity']}")

            print(Fore.MAGENTA +
                  f"Cost: {item['total_cost']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy linh kiện.")

    pause()


# =========================================================
# TOTAL COST
# =========================================================

def total_cost():

    clear()

    title("TOTAL PROJECT COST")

    total = 0

    for item in data["components"]:

        total += item["total_cost"]

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    print(Fore.YELLOW +
          f"\nTOTAL COST: {total}")

    pause()


# =========================================================
# CATEGORY STATISTICS
# =========================================================

def statistics():

    clear()

    title("BOM STATISTICS")

    stats = {}

    total_items = 0

    for item in data["components"]:

        cat = item["category"]

        stats[cat] = (
            stats.get(cat, 0)
            + 1
        )

        total_items += item["quantity"]

    print(Fore.GREEN +
          f"\nTotal Components: "
          f"{len(data['components'])}")

    print(Fore.CYAN +
          f"Total Items: {total_items}")

    line()

    print(Fore.YELLOW +
          "\nCATEGORY OVERVIEW\n")

    for cat, count in stats.items():

        print(Fore.GREEN +
              f"{cat:<25} {count}")

    pause()


# =========================================================
# COST ANALYSIS
# =========================================================

def cost_analysis():

    clear()

    title("COST ANALYSIS")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    sorted_items = sorted(
        data["components"],
        key=lambda x: x["total_cost"],
        reverse=True
    )

    print(Fore.GREEN +
          "\nTOP EXPENSIVE COMPONENTS\n")

    for item in sorted_items:

        print(Fore.YELLOW +
              f"{item['name']}")

        print(Fore.CYAN +
              f"Cost: {item['total_cost']}")

        line()

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT BOM CSV")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có BOM.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["components"]
        )

        filename = "bom_report.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# DELETE COMPONENT
# =========================================================

def delete_component():

    clear()

    title("DELETE COMPONENT")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có linh kiện.")

        pause()

        return

    for index, item in enumerate(
        data["components"],
        start=1
    ):

        print(Fore.GREEN +
              f"[{index}] {item['name']}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn linh kiện xóa: "
        ))

        removed = data["components"].pop(
            choice - 1
        )

        save_data()

        print(Fore.RED +
              f"\nĐã xóa: {removed['name']}")

    except:

        print(Fore.RED +
              "\nLỗi xóa linh kiện.")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO BOM PROJECT")

    data["project_name"] = "Smart IoT Weather Station"

    data["components"] = [

        {
            "name": "ESP32",
            "category": "WiFi MCU",
            "supplier": "IoT Store",
            "quantity": 1,
            "price": 120000,
            "total_cost": 120000,
            "date_added": "2026-05-15"
        },

        {
            "name": "DHT11",
            "category": "Sensor",
            "supplier": "Electronics VN",
            "quantity": 1,
            "price": 25000,
            "total_cost": 25000,
            "date_added": "2026-05-15"
        },

        {
            "name": "OLED Display",
            "category": "Display",
            "supplier": "Maker Shop",
            "quantity": 1,
            "price": 90000,
            "total_cost": 90000,
            "date_added": "2026-05-15"
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

    title("GIẢI THÍCH BOM SYSTEM")

    print(Fore.WHITE + """
=========================================================
1. BOM
=========================================================

BOM:
   Bill Of Materials

=========================================================
2. ELECTRONIC PROJECT
=========================================================

Project:
   ✓ Arduino
   ✓ ESP32
   ✓ IoT Devices

=========================================================
3. COMPONENT TRACKING
=========================================================

Theo dõi:
   ✓ Quantity
   ✓ Cost
   ✓ Supplier

=========================================================
4. COST ANALYSIS
=========================================================

Phân tích:
   ✓ Tổng chi phí
   ✓ Linh kiện đắt nhất

=========================================================
5. CSV EXPORT
=========================================================

Xuất:
   ✓ Excel
   ✓ CSV

=========================================================
6. INVENTORY MANAGEMENT
=========================================================

Quản lý:
   ✓ Kho linh kiện
   ✓ Dự án điện tử

=========================================================
7. EMBEDDED ENGINEERING
=========================================================

Ứng dụng:
   ✓ PCB Design
   ✓ Robotics

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Hardware Startup
✓ Electronics Workshop
✓ IoT Development
✓ Embedded Systems
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("ELECTRONIC BOM GENERATOR")

        print(Fore.CYAN + """
[1] Giới thiệu BOM Generator
[2] Set project name
[3] Add component
[4] View BOM
[5] Search component
[6] Total project cost
[7] BOM statistics
[8] Cost analysis
[9] Export CSV BOM
[10] Delete component
[11] Demo mode
[12] Giải thích hệ thống
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

            set_project()

        elif choice == '3':

            add_component()

        elif choice == '4':

            view_bom()

        elif choice == '5':

            search_component()

        elif choice == '6':

            total_cost()

        elif choice == '7':

            statistics()

        elif choice == '8':

            cost_analysis()

        elif choice == '9':

            export_csv()

        elif choice == '10':

            delete_component()

        elif choice == '11':

            demo_mode()

        elif choice == '12':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng BOM Generator.

Kiến thức đạt được:
   ✓ BOM Management
   ✓ Electronics Projects
   ✓ Cost Analysis
   ✓ CSV Export
   ✓ Inventory Tracking
   ✓ Embedded Engineering
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
