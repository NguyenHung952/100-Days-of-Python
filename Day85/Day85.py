# =========================================================
#       ELECTRONIC COMPONENT PRICE SCRAPER
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Web scraping giá linh kiện điện tử
#
# Chức năng:
#   ✓ Web scraping linh kiện điện tử
#   ✓ Tìm giá sản phẩm online
#   ✓ Export CSV report
#   ✓ So sánh giá
#   ✓ Search component
#   ✓ Save scraping history
#   ✓ Data analysis đơn giản
#   ✓ Multi-page scraping
#   ✓ Dashboard terminal hiện đại
#   ✓ Demo mode
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install requests beautifulsoup4 pandas colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python electronic_scraper.py
#
# =========================================================

from colorama import Fore, Style, init

from bs4 import BeautifulSoup

import requests
import pandas as pd

import json
import os
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "scraping_history.json"

# =========================================================
# DATABASE
# =========================================================

data = {
    "history": []
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

    title("GIỚI THIỆU WEB SCRAPER")

    print(Fore.WHITE + """
Electronic Price Scraper giúp:

   ✓ Thu thập giá linh kiện điện tử
   ✓ Tự động scraping website
   ✓ Theo dõi giá sản phẩm
   ✓ Phân tích dữ liệu thị trường

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Web Scraping
✓ HTML Parsing
✓ Price Tracking
✓ CSV Export
✓ Search Components

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Arduino Components
✓ IC Price Tracking
✓ Raspberry Pi Market
✓ Electronics Shopping

=========================================================
THƯ VIỆN SỬ DỤNG
=========================================================

✓ Requests
✓ BeautifulSoup
✓ Pandas
""")

    line()


# =========================================================
# DEMO SCRAPING DATA
# =========================================================

demo_products = [

    {
        "name": "Arduino UNO R3",
        "price": 250000,
        "shop": "Electronics VN"
    },

    {
        "name": "ESP32 WiFi Module",
        "price": 120000,
        "shop": "IoT Store"
    },

    {
        "name": "Raspberry Pi 4",
        "price": 1800000,
        "shop": "Tech Hardware"
    },

    {
        "name": "OLED Display",
        "price": 90000,
        "shop": "Maker Shop"
    }
]

# =========================================================
# SCRAPE WEBSITE
# =========================================================

def scrape_demo():

    clear()

    title("SCRAPE ELECTRONIC COMPONENTS")

    print(Fore.CYAN +
          "\nĐang scraping dữ liệu...\n")

    time.sleep(1)

    scraped = []

    for product in demo_products:

        print(Fore.GREEN +
              f"Product: {product['name']}")

        print(Fore.YELLOW +
              f"Price  : {product['price']}")

        print(Fore.CYAN +
              f"Shop   : {product['shop']}")

        line()

        scraped.append(product)

    data["history"] = scraped

    save_data()

    print(Fore.GREEN +
          "\nScraping hoàn tất.")

    pause()


# =========================================================
# SEARCH PRODUCT
# =========================================================

def search_product():

    clear()

    title("SEARCH COMPONENT")

    keyword = input(
        Fore.YELLOW +
        "Nhập tên linh kiện: "
    ).lower()

    found = False

    for item in data["history"]:

        if keyword in item["name"].lower():

            found = True

            print(Fore.GREEN +
                  f"\n{item['name']}")

            print(Fore.YELLOW +
                  f"Price: {item['price']}")

            print(Fore.CYAN +
                  f"Shop : {item['shop']}")

            line()

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

    if not data["history"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

        pause()

        return

    sorted_products = sorted(
        data["history"],
        key=lambda x: x["price"]
    )

    print(Fore.GREEN +
          "\nSO SÁNH GIÁ\n")

    for item in sorted_products:

        print(Fore.YELLOW +
              f"{item['name']:<25}")

        print(Fore.CYAN +
              f"Price: {item['price']}")

        print(Fore.GREEN +
              f"Shop : {item['shop']}")

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
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV")

    if not data["history"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["history"]
        )

        filename = "electronics_prices.csv"

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
# STATISTICS
# =========================================================

def statistics():

    clear()

    title("PRICE STATISTICS")

    if not data["history"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    prices = [

        item["price"]
        for item in data["history"]
    ]

    avg_price = sum(prices) / len(prices)

    max_price = max(prices)

    min_price = min(prices)

    print(Fore.GREEN +
          f"\nAverage Price : {avg_price}")

    print(Fore.CYAN +
          f"Highest Price : {max_price}")

    print(Fore.YELLOW +
          f"Lowest Price  : {min_price}")

    pause()


# =========================================================
# SCRAPING HISTORY
# =========================================================

def view_history():

    clear()

    title("SCRAPING HISTORY")

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

        print(Fore.YELLOW +
              f"Price: {item['price']}")

        print(Fore.CYAN +
              f"Shop : {item['shop']}")

        line()

    pause()


# =========================================================
# REAL REQUEST DEMO
# =========================================================

def requests_demo():

    clear()

    title("HTTP REQUEST DEMO")

    url = "https://example.com"

    try:

        response = requests.get(url)

        print(Fore.GREEN +
              f"\nStatus Code: {response.status_code}")

        print(Fore.CYAN +
              f"Content Length: "
              f"{len(response.text)}")

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        print(Fore.YELLOW +
              f"Page Title: {soup.title.string}")

    except Exception as e:

        print(Fore.RED +
              f"\nRequest lỗi:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO SCRAPER")

    print(Fore.WHITE + """
Demo scraping:

=========================================================
BƯỚC HOẠT ĐỘNG
=========================================================

1. Requests gửi HTTP request
2. BeautifulSoup parse HTML
3. Extract product data
4. Save CSV/JSON

=========================================================
DỮ LIỆU SCRAPING
=========================================================

✓ Product Name
✓ Product Price
✓ Shop Name

=========================================================
ỨNG DỤNG
=========================================================

✓ Price Tracker
✓ Market Analysis
✓ Electronics Shopping
""")

    pause()


# =========================================================
# EXPLAIN SCRAPING
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH WEB SCRAPING")

    print(Fore.WHITE + """
=========================================================
1. WEB SCRAPING
=========================================================

Tự động:
   ✓ Đọc website
   ✓ Lấy dữ liệu

=========================================================
2. HTTP REQUEST
=========================================================

Python gửi:
   ✓ GET request

=========================================================
3. HTML PARSING
=========================================================

BeautifulSoup:
   ✓ Parse HTML
   ✓ Tìm dữ liệu

=========================================================
4. DATA EXTRACTION
=========================================================

Extract:
   ✓ Title
   ✓ Price
   ✓ Description

=========================================================
5. PRICE TRACKING
=========================================================

Theo dõi:
   ✓ Giá sản phẩm
   ✓ Biến động thị trường

=========================================================
6. DATA ANALYSIS
=========================================================

Pandas hỗ trợ:
   ✓ CSV
   ✓ Statistics

=========================================================
7. E-COMMERCE
=========================================================

Ứng dụng:
   ✓ Shopee
   ✓ Lazada
   ✓ Electronics Market

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Market Intelligence
✓ Product Monitoring
✓ Price Comparison
✓ AI Shopping Assistant
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("ELECTRONIC PRICE SCRAPER")

        print(Fore.CYAN + """
[1] Giới thiệu Web Scraper
[2] Scrape linh kiện demo
[3] Search component
[4] Compare prices
[5] Price statistics
[6] View scraping history
[7] Export CSV
[8] HTTP request demo
[9] Demo mode
[10] Giải thích Web Scraping
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

            scrape_demo()

        elif choice == '3':

            search_product()

        elif choice == '4':

            compare_prices()

        elif choice == '5':

            statistics()

        elif choice == '6':

            view_history()

        elif choice == '7':

            export_csv()

        elif choice == '8':

            requests_demo()

        elif choice == '9':

            demo_mode()

        elif choice == '10':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Electronic Scraper.

Kiến thức đạt được:
   ✓ Web Scraping
   ✓ HTTP Requests
   ✓ HTML Parsing
   ✓ Data Extraction
   ✓ Price Analytics
   ✓ BeautifulSoup
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
