# =========================================================
#              MINI SCHEMATIC VIEWER
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Schematic Viewer Mini bằng Python
#
# Chức năng:
#   ✓ Hiển thị schematic điện tử
#   ✓ ASCII schematic viewer
#   ✓ Quản lý project schematic
#   ✓ Search linh kiện
#   ✓ Export schematic TXT
#   ✓ Schematic statistics
#   ✓ Component connections
#   ✓ Save project JSON
#   ✓ Dashboard terminal hiện đại
#   ✓ Demo circuit viewer
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install colorama pandas
#
# =========================================================
# CHẠY
# =========================================================
#
# python schematic_viewer.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import os
import json
import time
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "schematic_project.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "",
    "components": [],
    "connections": []
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

    title("GIỚI THIỆU SCHEMATIC VIEWER")

    print(Fore.WHITE + """
Mini Schematic Viewer giúp:

   ✓ Hiển thị sơ đồ mạch điện tử
   ✓ Quản lý project embedded
   ✓ Theo dõi kết nối linh kiện
   ✓ Mô phỏng schematic đơn giản

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Schematic Viewer
✓ Component Management
✓ Connection Mapping
✓ ASCII Circuit Display
✓ Export TXT

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Arduino Projects
✓ IoT Devices
✓ PCB Design
✓ Robotics
✓ Embedded Systems

=========================================================
LINH KIỆN HỖ TRỢ
=========================================================

✓ ESP32
✓ Arduino
✓ Sensors
✓ OLED Display
✓ LEDs
""")

    line()


# =========================================================
# SET PROJECT
# =========================================================

def set_project():

    clear()

    title("SET PROJECT")

    project_name = input(
        Fore.YELLOW +
        "Tên project schematic: "
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

    symbol = input(
        Fore.YELLOW +
        "Ký hiệu schematic: "
    )

    category = input(
        Fore.YELLOW +
        "Category: "
    )

    component = {

        "name": name,
        "symbol": symbol,
        "category": category,
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
# ADD CONNECTION
# =========================================================

def add_connection():

    clear()

    title("ADD CONNECTION")

    source = input(
        Fore.YELLOW +
        "Từ linh kiện: "
    )

    target = input(
        Fore.YELLOW +
        "Đến linh kiện: "
    )

    signal = input(
        Fore.YELLOW +
        "Tên tín hiệu: "
    )

    connection = {

        "source": source,
        "target": target,
        "signal": signal
    }

    data["connections"].append(
        connection
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm kết nối.")

    pause()


# =========================================================
# VIEW COMPONENTS
# =========================================================

def view_components():

    clear()

    title("SCHEMATIC COMPONENTS")

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
              f"Symbol   : {item['symbol']}")

        print(Fore.YELLOW +
              f"Category : {item['category']}")

        line()

    pause()


# =========================================================
# VIEW CONNECTIONS
# =========================================================

def view_connections():

    clear()

    title("SCHEMATIC CONNECTIONS")

    if not data["connections"]:

        print(Fore.RED +
              "\nChưa có kết nối.")

        pause()

        return

    for index, conn in enumerate(
        data["connections"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}]")

        print(Fore.CYAN +
              f"{conn['source']}")

        print(Fore.YELLOW +
              f" --> {conn['signal']} --> ")

        print(Fore.GREEN +
              f"{conn['target']}")

        line()

    pause()


# =========================================================
# ASCII SCHEMATIC VIEWER
# =========================================================

def schematic_viewer():

    clear()

    title("ASCII SCHEMATIC VIEWER")

    if not data["connections"]:

        print(Fore.RED +
              "\nKhông có schematic.")

        pause()

        return

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    line()

    print(Fore.CYAN +
          "\nSCHEMATIC VIEW\n")

    for conn in data["connections"]:

        print(Fore.YELLOW +
              f"[{conn['source']}]")

        print(Fore.CYAN +
              f"   |")

        print(Fore.GREEN +
              f"   |--- {conn['signal']} ---")

        print(Fore.CYAN +
              f"   |")

        print(Fore.YELLOW +
              f"[{conn['target']}]\n")

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
                  f"{item['symbol']}")

            print(Fore.YELLOW +
                  f"{item['category']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy linh kiện.")

    pause()


# =========================================================
# CIRCUIT STATISTICS
# =========================================================

def statistics():

    clear()

    title("SCHEMATIC STATISTICS")

    total_components = len(
        data["components"]
    )

    total_connections = len(
        data["connections"]
    )

    categories = {}

    for item in data["components"]:

        cat = item["category"]

        categories[cat] = (
            categories.get(cat, 0)
            + 1
        )

    print(Fore.GREEN +
          f"\nTotal Components : "
          f"{total_components}")

    print(Fore.CYAN +
          f"Total Connections: "
          f"{total_connections}")

    line()

    print(Fore.YELLOW +
          "\nCATEGORY OVERVIEW\n")

    for cat, count in categories.items():

        print(Fore.GREEN +
              f"{cat:<25} {count}")

    pause()


# =========================================================
# EXPORT TXT
# =========================================================

def export_txt():

    clear()

    title("EXPORT SCHEMATIC TXT")

    filename = "schematic_report.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"PROJECT: "
                f"{data['project_name']}\n"
            )

            f.write("=" * 50 + "\n\n")

            f.write("COMPONENTS\n\n")

            for item in data["components"]:

                f.write(
                    f"{item['name']} | "
                    f"{item['symbol']} | "
                    f"{item['category']}\n"
                )

            f.write("\nCONNECTIONS\n\n")

            for conn in data["connections"]:

                f.write(
                    f"{conn['source']} "
                    f"--> {conn['signal']} --> "
                    f"{conn['target']}\n"
                )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT COMPONENT CSV")

    if not data["components"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["components"]
        )

        filename = "schematic_components.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi CSV:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO SCHEMATIC")

    data["project_name"] = (
        "Smart IoT Weather Station"
    )

    data["components"] = [

        {
            "name": "ESP32",
            "symbol": "U1",
            "category": "MCU"
        },

        {
            "name": "DHT11",
            "symbol": "S1",
            "category": "Sensor"
        },

        {
            "name": "OLED Display",
            "symbol": "D1",
            "category": "Display"
        }
    ]

    data["connections"] = [

        {
            "source": "ESP32",
            "target": "DHT11",
            "signal": "GPIO4"
        },

        {
            "source": "ESP32",
            "target": "OLED Display",
            "signal": "I2C SDA/SCL"
        }
    ]

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo schematic demo.")

    pause()


# =========================================================
# EXPLAIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH SCHEMATIC VIEWER")

    print(Fore.WHITE + """
=========================================================
1. SCHEMATIC
=========================================================

Schematic:
   ✓ Sơ đồ mạch điện tử

=========================================================
2. COMPONENTS
=========================================================

Linh kiện:
   ✓ MCU
   ✓ Sensor
   ✓ Display

=========================================================
3. CONNECTIONS
=========================================================

Kết nối:
   ✓ GPIO
   ✓ I2C
   ✓ SPI
   ✓ UART

=========================================================
4. EMBEDDED SYSTEM
=========================================================

Ứng dụng:
   ✓ Arduino
   ✓ ESP32
   ✓ IoT

=========================================================
5. ASCII VIEWER
=========================================================

Terminal hiển thị:
   ✓ Circuit Connections

=========================================================
6. EXPORT SYSTEM
=========================================================

Xuất:
   ✓ TXT
   ✓ CSV

=========================================================
7. PCB DESIGN
=========================================================

Hỗ trợ:
   ✓ Prototype
   ✓ Hardware Design

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Electronics Lab
✓ Robotics
✓ Embedded Engineering
✓ IoT Development
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("MINI SCHEMATIC VIEWER")

        print(Fore.CYAN + """
[1] Giới thiệu Viewer
[2] Set project name
[3] Add component
[4] Add connection
[5] View components
[6] View connections
[7] ASCII schematic viewer
[8] Search component
[9] Schematic statistics
[10] Export TXT schematic
[11] Export CSV components
[12] Demo mode
[13] Giải thích hệ thống
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

            add_connection()

        elif choice == '5':

            view_components()

        elif choice == '6':

            view_connections()

        elif choice == '7':

            schematic_viewer()

        elif choice == '8':

            search_component()

        elif choice == '9':

            statistics()

        elif choice == '10':

            export_txt()

        elif choice == '11':

            export_csv()

        elif choice == '12':

            demo_mode()

        elif choice == '13':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Mini Schematic Viewer.

Kiến thức đạt được:
   ✓ Schematic Design
   ✓ Circuit Connections
   ✓ Embedded Systems
   ✓ ASCII Visualization
   ✓ CSV/TXT Export
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
