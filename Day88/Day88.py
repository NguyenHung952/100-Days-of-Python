# =========================================================
#         ELECTRONIC COMPONENT INVENTORY SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Bộ quản lý kho linh kiện điện tử
#
# Chức năng:
#   ✓ Quản lý kho linh kiện
#   ✓ Thêm/Xóa/Sửa linh kiện
#   ✓ Theo dõi số lượng tồn kho
#   ✓ Low-stock alert
#   ✓ Search linh kiện
#   ✓ Category management
#   ✓ Export CSV report
#   ✓ Inventory statistics
#   ✓ Save JSON database
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
# python component_inventory.py
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

DATA_FILE = "component_inventory.json"

# =========================================================
# DATABASE
# =========================================================

data = {
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

    title("GIỚI THIỆU INVENTORY SYSTEM")

    print(Fore.WHITE + """
Electronic Component Inventory giúp:

   ✓ Quản lý kho linh kiện điện tử
   ✓ Theo dõi tồn kho
   ✓ Quản lý nhập/xuất linh kiện
   ✓ Hỗ trợ Embedded/IoT Projects

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Add Components
✓ Update Stock
✓ Low Stock Alert
✓ Search Components
✓ Export CSV

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Electronics Lab
✓ IoT Projects
✓ Robotics
✓ Embedded Systems

=========================================================
LINH KIỆN HỖ TRỢ
=========================================================

✓ ESP32
✓ Arduino
✓ Sensors
✓ IC Chips
✓ Modules
""")

    line()


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

    location = input(
        Fore.YELLOW +
        "Vị trí lưu kho: "
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

    component = {

        "name": name,
        "category": category,
        "location": location,
        "quantity": quantity,
        "price": price,
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
# VIEW COMPONENTS
# =========================================================

def view_components():

    clear()

    title("ALL COMPONENTS")

    if not data["components"]:

        print(Fore.RED +
              "\nKho linh kiện trống.")

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
              f"Location : {item['location']}")

        print(Fore.MAGENTA +
              f"Quantity : {item['quantity']}")

        print(Fore.WHITE +
              f"Price    : {item['price']}")

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
                  f"{item['category']}")

            print(Fore.YELLOW +
                  f"Qty: {item['quantity']}")

            print(Fore.WHITE +
                  f"Location: {item['location']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy linh kiện.")

    pause()


# =========================================================
# UPDATE STOCK
# =========================================================

def update_stock():

    clear()

    title("UPDATE STOCK")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

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
            "\nChọn linh kiện: "
        ))

        new_qty = int(input(
            Fore.YELLOW +
            "Số lượng mới: "
        ))

        data["components"][
            choice - 1
        ]["quantity"] = new_qty

        save_data()

        print(Fore.GREEN +
              "\nĐã cập nhật stock.")

    except:

        print(Fore.RED +
              "\nLỗi cập nhật.")

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
              "\nLỗi xóa.")

    pause()


# =========================================================
# LOW STOCK ALERT
# =========================================================

def low_stock_alert():

    clear()

    title("LOW STOCK ALERT")

    found = False

    for item in data["components"]:

        if item["quantity"] <= 5:

            found = True

            print(Fore.RED +
                  f"\n⚠ {item['name']}")

            print(Fore.YELLOW +
                  f"Stock: {item['quantity']}")

            line()

    if not found:

        print(Fore.GREEN +
              "\nTất cả stock ổn định.")

    pause()


# =========================================================
# INVENTORY VALUE
# =========================================================

def inventory_value():

    clear()

    title("INVENTORY VALUE")

    total = 0

    for item in data["components"]:

        value = (
            item["quantity"] *
            item["price"]
        )

        total += value

        print(Fore.GREEN +
              f"\n{item['name']}")

        print(Fore.CYAN +
              f"Value: {value}")

        line()

    print(Fore.YELLOW +
          f"\nTOTAL INVENTORY VALUE: {total}")

    pause()


# =========================================================
# CATEGORY STATISTICS
# =========================================================

def statistics():

    clear()

    title("CATEGORY STATISTICS")

    stats = {}

    for item in data["components"]:

        cat = item["category"]

        stats[cat] = (
            stats.get(cat, 0)
            + 1
        )

    print(Fore.GREEN +
          "\nCATEGORY OVERVIEW\n")

    for cat, count in stats.items():

        print(Fore.YELLOW +
              f"{cat:<25} {count}")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["components"]
        )

        filename = "inventory_report.csv"

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
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO INVENTORY DATA")

    demo_components = [

        {
            "name": "ESP32",
            "category": "WiFi MCU",
            "location": "Box A1",
            "quantity": 12,
            "price": 120000,
            "date_added": "2026-05-15"
        },

        {
            "name": "DHT11",
            "category": "Sensor",
            "location": "Box B2",
            "quantity": 3,
            "price": 25000,
            "date_added": "2026-05-15"
        },

        {
            "name": "Arduino Nano",
            "category": "MCU Board",
            "location": "Shelf C3",
            "quantity": 7,
            "price": 180000,
            "date_added": "2026-05-15"
        }
    ]

    data["components"] = demo_components

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# EXPLAIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH INVENTORY SYSTEM")

    print(Fore.WHITE + """
=========================================================
1. INVENTORY MANAGEMENT
=========================================================

Quản lý:
   ✓ Kho linh kiện
   ✓ Tồn kho

=========================================================
2. EMBEDDED SYSTEM
=========================================================

Linh kiện:
   ✓ ESP32
   ✓ Arduino
   ✓ Sensors

=========================================================
3. STOCK TRACKING
=========================================================

Theo dõi:
   ✓ Quantity
   ✓ Price
   ✓ Location

=========================================================
4. LOW STOCK ALERT
=========================================================

Cảnh báo:
   ✓ Thiếu linh kiện

=========================================================
5. CSV EXPORT
=========================================================

Xuất:
   ✓ Excel
   ✓ CSV

=========================================================
6. JSON DATABASE
=========================================================

Lưu:
   ✓ Components
   ✓ Inventory

=========================================================
7. ELECTRONICS LAB
=========================================================

Ứng dụng:
   ✓ IoT Lab
   ✓ Robotics Lab

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Electronics Shop
✓ Embedded Projects
✓ PCB Workshop
✓ Hardware Startup
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("COMPONENT INVENTORY SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu System
[2] Add component
[3] View components
[4] Search component
[5] Update stock
[6] Delete component
[7] Low stock alert
[8] Inventory value
[9] Category statistics
[10] Export CSV report
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

            add_component()

        elif choice == '3':

            view_components()

        elif choice == '4':

            search_component()

        elif choice == '5':

            update_stock()

        elif choice == '6':

            delete_component()

        elif choice == '7':

            low_stock_alert()

        elif choice == '8':

            inventory_value()

        elif choice == '9':

            statistics()

        elif choice == '10':

            export_csv()

        elif choice == '11':

            demo_mode()

        elif choice == '12':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Inventory System.

Kiến thức đạt được:
   ✓ Inventory Management
   ✓ Stock Tracking
   ✓ Embedded Hardware
   ✓ CSV Export
   ✓ JSON Database
   ✓ Electronics Engineering
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
