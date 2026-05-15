# =========================================================
#          ELECTRONIC DATASHEET FINDER TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Công cụ tra datasheet linh kiện
#
# Chức năng:
#   ✓ Tra cứu datasheet IC/Sensor
#   ✓ Search linh kiện điện tử
#   ✓ Mô phỏng tìm datasheet online
#   ✓ Hiển thị thông số kỹ thuật
#   ✓ Export datasheet report
#   ✓ Save search history
#   ✓ Search by category
#   ✓ Keyword search
#   ✓ Dashboard terminal hiện đại
#   ✓ Demo mode
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install requests pandas colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python datasheet_finder.py
#
# =========================================================

from colorama import Fore, Style, init

import requests
import pandas as pd

import os
import json
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "datasheet_history.json"

# =========================================================
# DATABASE
# =========================================================

data = {
    "history": []
}

# =========================================================
# SAMPLE DATASHEET DATABASE
# =========================================================

datasheets = [

    {
        "name": "ESP32",
        "category": "WiFi MCU",
        "voltage": "3.3V",
        "datasheet": "ESP32_datasheet.pdf",
        "description": "WiFi + Bluetooth MCU"
    },

    {
        "name": "DHT11",
        "category": "Temperature Sensor",
        "voltage": "5V",
        "datasheet": "DHT11_datasheet.pdf",
        "description": "Humidity + Temperature Sensor"
    },

    {
        "name": "MPU6050",
        "category": "Gyroscope Sensor",
        "voltage": "3.3V",
        "datasheet": "MPU6050_datasheet.pdf",
        "description": "Accelerometer + Gyroscope"
    },

    {
        "name": "Arduino UNO",
        "category": "Microcontroller Board",
        "voltage": "5V",
        "datasheet": "ArduinoUNO_datasheet.pdf",
        "description": "ATmega328P Development Board"
    },

    {
        "name": "HC-SR04",
        "category": "Ultrasonic Sensor",
        "voltage": "5V",
        "datasheet": "HCSR04_datasheet.pdf",
        "description": "Distance Measuring Sensor"
    }
]

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

    title("GIỚI THIỆU DATASHEET FINDER")

    print(Fore.WHITE + """
Datasheet Finder giúp:

   ✓ Tra cứu datasheet linh kiện
   ✓ Tìm thông số kỹ thuật IC/Sensor
   ✓ Hỗ trợ Embedded/IoT Development

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Datasheet Search
✓ Component Lookup
✓ Technical Specifications
✓ Export Report
✓ Search History

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Arduino Projects
✓ Embedded Systems
✓ Robotics
✓ IoT Engineering

=========================================================
LINH KIỆN HỖ TRỢ
=========================================================

✓ ESP32
✓ Arduino
✓ Sensors
✓ IC Modules
""")

    line()


# =========================================================
# SEARCH DATASHEET
# =========================================================

def search_datasheet():

    clear()

    title("SEARCH DATASHEET")

    keyword = input(
        Fore.YELLOW +
        "Nhập tên linh kiện: "
    ).lower()

    found = False

    for item in datasheets:

        if keyword in item["name"].lower():

            found = True

            print(Fore.GREEN +
                  f"\nComponent : {item['name']}")

            print(Fore.CYAN +
                  f"Category  : {item['category']}")

            print(Fore.YELLOW +
                  f"Voltage   : {item['voltage']}")

            print(Fore.MAGENTA +
                  f"Datasheet : {item['datasheet']}")

            print(Fore.WHITE +
                  f"Description: "
                  f"{item['description']}")

            line()

            data["history"].append(item)

    save_data()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy datasheet.")

    pause()


# =========================================================
# VIEW ALL COMPONENTS
# =========================================================

def view_components():

    clear()

    title("ALL COMPONENTS")

    for index, item in enumerate(
        datasheets,
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {item['name']}")

        print(Fore.CYAN +
              f"Category : {item['category']}")

        print(Fore.YELLOW +
              f"Voltage  : {item['voltage']}")

        line()

    pause()


# =========================================================
# SEARCH CATEGORY
# =========================================================

def search_category():

    clear()

    title("SEARCH BY CATEGORY")

    keyword = input(
        Fore.YELLOW +
        "Nhập category: "
    ).lower()

    found = False

    for item in datasheets:

        if keyword in item["category"].lower():

            found = True

            print(Fore.GREEN +
                  f"\n{item['name']}")

            print(Fore.CYAN +
                  f"{item['category']}")

            print(Fore.YELLOW +
                  f"{item['datasheet']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy category.")

    pause()


# =========================================================
# VIEW SEARCH HISTORY
# =========================================================

def view_history():

    clear()

    title("SEARCH HISTORY")

    if not data["history"]:

        print(Fore.RED +
              "\nChưa có lịch sử.")

        pause()

        return

    for index, item in enumerate(
        data["history"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {item['name']}")

        print(Fore.CYAN +
              f"Category : {item['category']}")

        print(Fore.YELLOW +
              f"Datasheet: {item['datasheet']}")

        line()

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    try:

        df = pd.DataFrame(datasheets)

        filename = "datasheet_report.csv"

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
# COMPONENT STATISTICS
# =========================================================

def statistics():

    clear()

    title("COMPONENT STATISTICS")

    total = len(datasheets)

    categories = {}

    for item in datasheets:

        cat = item["category"]

        categories[cat] = (
            categories.get(cat, 0)
            + 1
        )

    print(Fore.GREEN +
          f"\nTotal Components: {total}")

    line()

    print(Fore.CYAN +
          "\nCATEGORY STATISTICS\n")

    for cat, count in categories.items():

        print(Fore.YELLOW +
              f"{cat:<25} {count}")

    pause()


# =========================================================
# HTTP REQUEST DEMO
# =========================================================

def request_demo():

    clear()

    title("HTTP REQUEST DEMO")

    url = "https://example.com"

    try:

        response = requests.get(url)

        print(Fore.GREEN +
              f"\nStatus Code: {response.status_code}")

        print(Fore.CYAN +
              f"Response Length: "
              f"{len(response.text)}")

    except Exception as e:

        print(Fore.RED +
              f"\nRequest lỗi:\n{e}")

    pause()


# =========================================================
# TECHNICAL ANALYSIS
# =========================================================

def technical_analysis():

    clear()

    title("TECHNICAL ANALYSIS")

    for item in datasheets:

        voltage = item["voltage"]

        print(Fore.GREEN +
              f"\n{item['name']}")

        print(Fore.CYAN +
              f"Operating Voltage: {voltage}")

        if voltage == "3.3V":

            print(Fore.YELLOW +
                  "Suitable for low-power IoT.")

        elif voltage == "5V":

            print(Fore.MAGENTA +
                  "Compatible with Arduino.")

        line()

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO DATASHEET TOOL")

    print(Fore.WHITE + """
Demo Datasheet Search:

=========================================================
CÁCH HOẠT ĐỘNG
=========================================================

1. User nhập tên linh kiện
2. Tool tìm database
3. Hiển thị thông số
4. Save history

=========================================================
THÔNG TIN DATASHEET
=========================================================

✓ Voltage
✓ Category
✓ Description
✓ PDF Datasheet

=========================================================
ỨNG DỤNG
=========================================================

✓ Embedded Engineering
✓ Electronics Repair
✓ IoT Projects
""")

    pause()


# =========================================================
# EXPLAIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH DATASHEET SYSTEM")

    print(Fore.WHITE + """
=========================================================
1. DATASHEET
=========================================================

Datasheet chứa:
   ✓ Voltage
   ✓ Pinout
   ✓ Features

=========================================================
2. EMBEDDED SYSTEM
=========================================================

Hệ thống:
   ✓ MCU
   ✓ Sensors
   ✓ IC

=========================================================
3. IOT DEVELOPMENT
=========================================================

Thiết bị:
   ✓ ESP32
   ✓ Arduino

=========================================================
4. ELECTRONICS ENGINEERING
=========================================================

Kỹ sư dùng:
   ✓ Datasheet
   ✓ Specifications

=========================================================
5. HTTP REQUEST
=========================================================

Python gửi:
   ✓ GET Request

=========================================================
6. CSV EXPORT
=========================================================

Xuất dữ liệu:
   ✓ Excel
   ✓ CSV

=========================================================
7. JSON DATABASE
=========================================================

Lưu:
   ✓ History
   ✓ Components

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Electronics Repair
✓ Robotics
✓ Embedded Programming
✓ PCB Design
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("ELECTRONIC DATASHEET FINDER")

        print(Fore.CYAN + """
[1] Giới thiệu Tool
[2] Search datasheet
[3] View all components
[4] Search by category
[5] View search history
[6] Component statistics
[7] Technical analysis
[8] Export CSV report
[9] HTTP request demo
[10] Demo mode
[11] Giải thích hệ thống
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

            search_datasheet()

        elif choice == '3':

            view_components()

        elif choice == '4':

            search_category()

        elif choice == '5':

            view_history()

        elif choice == '6':

            statistics()

        elif choice == '7':

            technical_analysis()

        elif choice == '8':

            export_csv()

        elif choice == '9':

            request_demo()

        elif choice == '10':

            demo_mode()

        elif choice == '11':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Datasheet Finder.

Kiến thức đạt được:
   ✓ Datasheet Lookup
   ✓ Embedded Systems
   ✓ Electronics Engineering
   ✓ HTTP Requests
   ✓ CSV Export
   ✓ IoT Hardware
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
