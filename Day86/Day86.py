# =========================================================
#            IC & SENSOR PRICE TRACKER
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Theo dõi giá IC/Sensor online
#
# Chức năng:
#   ✓ Theo dõi giá IC/Sensor
#   ✓ Price monitoring
#   ✓ Price alert
#   ✓ Search linh kiện
#   ✓ Export CSV report
#   ✓ Save history JSON
#   ✓ So sánh giá
#   ✓ Price statistics
#   ✓ Simulate online tracking
#   ✓ Dashboard terminal hiện đại
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
# python ic_sensor_tracker.py
#
# =========================================================

from colorama import Fore, Style, init

import requests
import pandas as pd

import json
import os
import time
import random
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "ic_sensor_prices.json"

# =========================================================
# DATABASE
# =========================================================

data = {
    "products": []
}

# =========================================================
# SAMPLE PRODUCTS
# =========================================================

sample_products = [

    {
        "name": "ESP32",
        "category": "WiFi MCU",
        "price": 120000
    },

    {
        "name": "DHT11",
        "category": "Temperature Sensor",
        "price": 25000
    },

    {
        "name": "MPU6050",
        "category": "Gyroscope Sensor",
        "price": 65000
    },

    {
        "name": "Arduino Nano",
        "category": "Microcontroller",
        "price": 180000
    },

    {
        "name": "HC-SR04",
        "category": "Ultrasonic Sensor",
        "price": 45000
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

    title("GIỚI THIỆU IC/SENSOR TRACKER")

    print(Fore.WHITE + """
IC & Sensor Price Tracker giúp:

   ✓ Theo dõi giá linh kiện điện tử
   ✓ Monitor IC/Sensor online
   ✓ So sánh giá sản phẩm
   ✓ Theo dõi biến động thị trường

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Price Tracking
✓ Price Alert
✓ Statistics
✓ CSV Export
✓ Search Product

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Arduino Projects
✓ IoT Development
✓ Robotics
✓ Embedded Systems

=========================================================
THƯ VIỆN SỬ DỤNG
=========================================================

✓ Requests
✓ Pandas
✓ JSON Database
""")

    line()


# =========================================================
# INIT DEMO DATA
# =========================================================

def initialize_products():

    data["products"] = sample_products

    save_data()


# =========================================================
# SIMULATE ONLINE PRICE UPDATE
# =========================================================

def update_prices():

    clear()

    title("UPDATE ONLINE PRICES")

    if not data["products"]:

        initialize_products()

    print(Fore.CYAN +
          "\nĐang cập nhật giá online...\n")

    time.sleep(1)

    for item in data["products"]:

        change = random.randint(
            -10000,
            10000
        )

        item["price"] += change

        if item["price"] < 1000:

            item["price"] = 1000

        print(Fore.GREEN +
              f"{item['name']}")

        print(Fore.YELLOW +
              f"New Price: {item['price']}")

        line()

    save_data()

    print(Fore.GREEN +
          "\nCập nhật hoàn tất.")

    pause()


# =========================================================
# VIEW PRODUCTS
# =========================================================

def view_products():

    clear()

    title("IC/SENSOR PRODUCTS")

    if not data["products"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

        pause()

        return

    for index, item in enumerate(
        data["products"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {item['name']}")

        print(Fore.CYAN +
              f"Category: {item['category']}")

        print(Fore.YELLOW +
              f"Price   : {item['price']}")

        line()

    pause()


# =========================================================
# SEARCH PRODUCT
# =========================================================

def search_product():

    clear()

    title("SEARCH IC/SENSOR")

    keyword = input(
        Fore.YELLOW +
        "Nhập tên linh kiện: "
    ).lower()

    found = False

    for item in data["products"]:

        if keyword in item["name"].lower():

            found = True

            print(Fore.GREEN +
                  f"\n{item['name']}")

            print(Fore.CYAN +
                  f"Category: {item['category']}")

            print(Fore.YELLOW +
                  f"Price   : {item['price']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy.")

    pause()


# =========================================================
# PRICE ALERT
# =========================================================

def price_alert():

    clear()

    title("PRICE ALERT")

    keyword = input(
        Fore.YELLOW +
        "Tên sản phẩm: "
    ).lower()

    try:

        target_price = int(input(
            Fore.YELLOW +
            "Giá mục tiêu: "
        ))

    except:

        print(Fore.RED +
              "\nGiá không hợp lệ.")

        pause()

        return

    found = False

    for item in data["products"]:

        if keyword in item["name"].lower():

            found = True

            current = item["price"]

            print(Fore.GREEN +
                  f"\nCurrent Price: {current}")

            if current <= target_price:

                print(Fore.GREEN +
                      "\n✓ GIÁ ĐÃ GIẢM!")

            else:

                print(Fore.RED +
                      "\n⚠ Giá vẫn cao.")

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy sản phẩm.")

    pause()


# =========================================================
# PRICE COMPARISON
# =========================================================

def compare_prices():

    clear()

    title("PRICE COMPARISON")

    if not data["products"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    sorted_products = sorted(
        data["products"],
        key=lambda x: x["price"]
    )

    print(Fore.GREEN +
          "\nSO SÁNH GIÁ\n")

    for item in sorted_products:

        print(Fore.YELLOW +
              f"{item['name']:<20}")

        print(Fore.CYAN +
              f"{item['price']}")

        line()

    cheapest = sorted_products[0]

    print(Fore.GREEN +
          "\nRẺ NHẤT\n")

    print(Fore.YELLOW +
          f"{cheapest['name']}")

    print(Fore.CYAN +
          f"{cheapest['price']}")

    pause()


# =========================================================
# STATISTICS
# =========================================================

def statistics():

    clear()

    title("PRICE STATISTICS")

    if not data["products"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    prices = [

        item["price"]
        for item in data["products"]
    ]

    avg_price = sum(prices) / len(prices)

    highest = max(prices)

    lowest = min(prices)

    print(Fore.GREEN +
          f"\nAverage Price: {avg_price}")

    print(Fore.CYAN +
          f"Highest Price: {highest}")

    print(Fore.YELLOW +
          f"Lowest Price : {lowest}")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    if not data["products"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["products"]
        )

        filename = "ic_sensor_prices.csv"

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
# HTTP REQUEST TEST
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
# MARKET ANALYSIS
# =========================================================

def market_analysis():

    clear()

    title("MARKET ANALYSIS")

    if not data["products"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    expensive = []

    cheap = []

    for item in data["products"]:

        if item["price"] > 100000:

            expensive.append(item)

        else:

            cheap.append(item)

    print(Fore.RED +
          "\nHIGH PRICE PRODUCTS\n")

    for item in expensive:

        print(Fore.YELLOW +
              f"{item['name']} - {item['price']}")

    line()

    print(Fore.GREEN +
          "\nLOW PRICE PRODUCTS\n")

    for item in cheap:

        print(Fore.CYAN +
              f"{item['name']} - {item['price']}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO TRACKER")

    initialize_products()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# EXPLAIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH PRICE TRACKER")

    print(Fore.WHITE + """
=========================================================
1. PRICE TRACKING
=========================================================

Theo dõi:
   ✓ Giá IC
   ✓ Giá Sensor

=========================================================
2. MARKET ANALYSIS
=========================================================

Phân tích:
   ✓ Giá cao
   ✓ Giá thấp

=========================================================
3. EMBEDDED SYSTEM
=========================================================

Linh kiện:
   ✓ ESP32
   ✓ Arduino
   ✓ MPU6050

=========================================================
4. IOT HARDWARE
=========================================================

Thiết bị:
   ✓ Sensor
   ✓ MCU
   ✓ Module

=========================================================
5. CSV EXPORT
=========================================================

Xuất dữ liệu:
   ✓ Excel
   ✓ CSV

=========================================================
6. JSON DATABASE
=========================================================

Lưu:
   ✓ Products
   ✓ Prices

=========================================================
7. HTTP REQUEST
=========================================================

Python gửi:
   ✓ GET Request

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Electronics Shop
✓ IoT Market
✓ Robotics
✓ Embedded Engineering
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("IC & SENSOR PRICE TRACKER")

        print(Fore.CYAN + """
[1] Giới thiệu Tracker
[2] Khởi tạo dữ liệu demo
[3] Update online prices
[4] Xem sản phẩm
[5] Search product
[6] Price alert
[7] Compare prices
[8] Statistics
[9] Market analysis
[10] Export CSV
[11] HTTP request demo
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

            demo_mode()

        elif choice == '3':

            update_prices()

        elif choice == '4':

            view_products()

        elif choice == '5':

            search_product()

        elif choice == '6':

            price_alert()

        elif choice == '7':

            compare_prices()

        elif choice == '8':

            statistics()

        elif choice == '9':

            market_analysis()

        elif choice == '10':

            export_csv()

        elif choice == '11':

            request_demo()

        elif choice == '12':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng IC/Sensor Tracker.

Kiến thức đạt được:
   ✓ Price Tracking
   ✓ Electronics Market
   ✓ HTTP Requests
   ✓ CSV Export
   ✓ JSON Database
   ✓ Embedded Hardware
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
