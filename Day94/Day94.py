# =========================================================
#          NUMERICAL ALGORITHM VISUALIZER
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Visualizer thuật toán số bằng Python
#
# Chức năng:
#   ✓ Visualize Bubble Sort
#   ✓ Visualize Selection Sort
#   ✓ Visualize Insertion Sort
#   ✓ Binary Search Visualization
#   ✓ Linear Search Visualization
#   ✓ Fibonacci Visualization
#   ✓ Prime Number Visualization
#   ✓ ASCII Graph Display
#   ✓ Step-by-step Simulation
#   ✓ Dashboard terminal hiện đại
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
# python algorithm_visualizer.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import random
import time
import os
import json

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "algorithm_visualizer.json"

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
# UI FUNCTIONS
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
# ASCII BAR GRAPH
# =========================================================

def draw_array(arr, highlight1=-1, highlight2=-1):

    for index, value in enumerate(arr):

        bar = "█" * value

        if index == highlight1 or index == highlight2:

            print(
                Fore.RED +
                f"{value:>2}: {bar}"
            )

        else:

            print(
                Fore.GREEN +
                f"{value:>2}: {bar}"
            )


# =========================================================
# INTRODUCTION
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU ALGORITHM VISUALIZER")

    print(Fore.WHITE + """
Algorithm Visualizer giúp:

   ✓ Hiểu thuật toán trực quan
   ✓ Visualize sorting/searching
   ✓ Học thuật toán step-by-step
   ✓ Phân tích logic xử lý

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Bubble Sort
✓ Selection Sort
✓ Insertion Sort
✓ Binary Search
✓ Fibonacci
✓ Prime Checker

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Computer Science
✓ Data Structures
✓ Competitive Programming
✓ Algorithm Learning

=========================================================
VISUALIZATION
=========================================================

✓ ASCII Graph
✓ Step Animation
✓ Highlight Operations
✓ Timing Simulation
""")

    line()


# =========================================================
# RANDOM ARRAY GENERATOR
# =========================================================

def generate_array():

    arr = []

    for _ in range(10):

        arr.append(
            random.randint(1, 20)
        )

    return arr


# =========================================================
# BUBBLE SORT VISUALIZATION
# =========================================================

def bubble_sort_visual():

    clear()

    title("BUBBLE SORT VISUALIZATION")

    arr = generate_array()

    print(Fore.YELLOW +
          "\nMảng ban đầu:\n")

    draw_array(arr)

    time.sleep(2)

    n = len(arr)

    for i in range(n):

        for j in range(0, n - i - 1):

            clear()

            title("BUBBLE SORT VISUALIZATION")

            print(Fore.CYAN +
                  f"\nSo sánh {arr[j]} và {arr[j+1]}\n")

            draw_array(arr, j, j + 1)

            time.sleep(0.5)

            if arr[j] > arr[j + 1]:

                arr[j], arr[j + 1] = (

                    arr[j + 1],
                    arr[j]
                )

    clear()

    title("SORT COMPLETED")

    print(Fore.GREEN +
          "\nKết quả cuối:\n")

    draw_array(arr)

    data["history"].append(
        "Bubble Sort"
    )

    save_data()

    pause()


# =========================================================
# SELECTION SORT
# =========================================================

def selection_sort_visual():

    clear()

    title("SELECTION SORT VISUALIZATION")

    arr = generate_array()

    n = len(arr)

    for i in range(n):

        min_idx = i

        for j in range(i + 1, n):

            clear()

            title("SELECTION SORT")

            draw_array(arr, min_idx, j)

            time.sleep(0.5)

            if arr[j] < arr[min_idx]:

                min_idx = j

        arr[i], arr[min_idx] = (

            arr[min_idx],
            arr[i]
        )

    clear()

    title("SELECTION SORT DONE")

    draw_array(arr)

    data["history"].append(
        "Selection Sort"
    )

    save_data()

    pause()


# =========================================================
# INSERTION SORT
# =========================================================

def insertion_sort_visual():

    clear()

    title("INSERTION SORT VISUALIZATION")

    arr = generate_array()

    for i in range(1, len(arr)):

        key = arr[i]

        j = i - 1

        while j >= 0 and key < arr[j]:

            clear()

            title("INSERTION SORT")

            draw_array(arr, j, i)

            time.sleep(0.5)

            arr[j + 1] = arr[j]

            j -= 1

        arr[j + 1] = key

    clear()

    title("INSERTION SORT DONE")

    draw_array(arr)

    data["history"].append(
        "Insertion Sort"
    )

    save_data()

    pause()


# =========================================================
# LINEAR SEARCH
# =========================================================

def linear_search_visual():

    clear()

    title("LINEAR SEARCH VISUALIZATION")

    arr = generate_array()

    target = random.choice(arr)

    print(Fore.YELLOW +
          f"\nTarget: {target}")

    time.sleep(1)

    for index, value in enumerate(arr):

        clear()

        title("LINEAR SEARCH")

        draw_array(arr, index)

        print(Fore.CYAN +
              f"\nChecking: {value}")

        time.sleep(0.7)

        if value == target:

            print(Fore.GREEN +
                  f"\nFound at index {index}")

            break

    data["history"].append(
        "Linear Search"
    )

    save_data()

    pause()


# =========================================================
# BINARY SEARCH
# =========================================================

def binary_search_visual():

    clear()

    title("BINARY SEARCH VISUALIZATION")

    arr = sorted(generate_array())

    target = random.choice(arr)

    low = 0
    high = len(arr) - 1

    while low <= high:

        mid = (low + high) // 2

        clear()

        title("BINARY SEARCH")

        draw_array(arr, mid)

        print(Fore.YELLOW +
              f"\nTarget: {target}")

        print(Fore.CYAN +
              f"Middle: {arr[mid]}")

        time.sleep(1)

        if arr[mid] == target:

            print(Fore.GREEN +
                  "\nTarget Found!")

            break

        elif arr[mid] < target:

            low = mid + 1

        else:

            high = mid - 1

    data["history"].append(
        "Binary Search"
    )

    save_data()

    pause()


# =========================================================
# FIBONACCI VISUALIZATION
# =========================================================

def fibonacci_visual():

    clear()

    title("FIBONACCI VISUALIZATION")

    try:

        n = int(input(
            Fore.YELLOW +
            "Nhập số Fibonacci: "
        ))

    except:

        print(Fore.RED +
              "\nKhông hợp lệ.")

        pause()

        return

    a, b = 0, 1

    print()

    for _ in range(n):

        print(Fore.GREEN +
              f"{a}")

        time.sleep(0.5)

        a, b = b, a + b

    data["history"].append(
        "Fibonacci"
    )

    save_data()

    pause()


# =========================================================
# PRIME NUMBER VISUALIZATION
# =========================================================

def prime_visual():

    clear()

    title("PRIME NUMBER VISUALIZATION")

    try:

        number = int(input(
            Fore.YELLOW +
            "Nhập số cần kiểm tra: "
        ))

    except:

        print(Fore.RED +
              "\nKhông hợp lệ.")

        pause()

        return

    is_prime = True

    for i in range(2, int(number ** 0.5) + 1):

        print(Fore.CYAN +
              f"\nChecking division by {i}")

        time.sleep(0.7)

        if number % i == 0:

            is_prime = False

            break

    if is_prime and number > 1:

        print(Fore.GREEN +
              f"\n{number} là số nguyên tố.")

    else:

        print(Fore.RED +
              f"\n{number} không phải số nguyên tố.")

    data["history"].append(
        "Prime Check"
    )

    save_data()

    pause()


# =========================================================
# HISTORY VIEWER
# =========================================================

def history():

    clear()

    title("ALGORITHM HISTORY")

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
              f"[{index}] {item}")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    try:

        df = pd.DataFrame({

            "Algorithms": data["history"]
        })

        filename = "algorithm_history.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export CSV: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO MODE")

    print(Fore.WHITE + """
Demo Algorithms:

=========================================================
SORTING
=========================================================

✓ Bubble Sort
✓ Selection Sort
✓ Insertion Sort

=========================================================
SEARCHING
=========================================================

✓ Linear Search
✓ Binary Search

=========================================================
MATHEMATICAL
=========================================================

✓ Fibonacci
✓ Prime Number

=========================================================
VISUALIZATION
=========================================================

✓ ASCII Bars
✓ Animation
✓ Step-by-step Simulation
""")

    pause()


# =========================================================
# EXPLAIN ALGORITHMS
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH THUẬT TOÁN")

    print(Fore.WHITE + """
=========================================================
1. BUBBLE SORT
=========================================================

Đổi chỗ:
   ✓ Phần tử lớn hơn

=========================================================
2. SELECTION SORT
=========================================================

Tìm:
   ✓ Giá trị nhỏ nhất

=========================================================
3. INSERTION SORT
=========================================================

Chèn:
   ✓ Đúng vị trí

=========================================================
4. LINEAR SEARCH
=========================================================

Tìm kiếm:
   ✓ Từng phần tử

=========================================================
5. BINARY SEARCH
=========================================================

Tìm kiếm:
   ✓ Chia đôi mảng

=========================================================
6. FIBONACCI
=========================================================

Chuỗi:
   ✓ a(n)=a(n-1)+a(n-2)

=========================================================
7. PRIME NUMBER
=========================================================

Kiểm tra:
   ✓ Số nguyên tố

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ AI
✓ Data Science
✓ Competitive Programming
✓ Software Engineering
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("NUMERICAL ALGORITHM VISUALIZER")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] Bubble Sort Visualization
[3] Selection Sort Visualization
[4] Insertion Sort Visualization
[5] Linear Search Visualization
[6] Binary Search Visualization
[7] Fibonacci Visualization
[8] Prime Number Visualization
[9] View history
[10] Export CSV report
[11] Demo mode
[12] Giải thích thuật toán
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

            bubble_sort_visual()

        elif choice == '3':

            selection_sort_visual()

        elif choice == '4':

            insertion_sort_visual()

        elif choice == '5':

            linear_search_visual()

        elif choice == '6':

            binary_search_visual()

        elif choice == '7':

            fibonacci_visual()

        elif choice == '8':

            prime_visual()

        elif choice == '9':

            history()

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
Cảm ơn bạn đã sử dụng Algorithm Visualizer.

Kiến thức đạt được:
   ✓ Sorting Algorithms
   ✓ Searching Algorithms
   ✓ Data Structures
   ✓ Visualization
   ✓ Mathematical Algorithms
   ✓ Computer Science
""")

            break

        else:

            print(Fore.RED +
                  "\nLựa chọn không hợp lệ!")

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
