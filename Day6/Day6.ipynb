# =========================================================
#  MÁY TÍNH ĐIỆN TRỞ MÀU - RESISTOR COLOR CODE CALCULATOR
# =========================================================
# Tác giả : Sinh viên Điện tử Viễn thông
# Ngôn ngữ: Python 3
# Mô tả   :
#   - Tính giá trị điện trở từ màu vòng
#   - Hỗ trợ điện trở 4 vòng và 5 vòng
#   - Hiển thị sai số
#   - Giao diện terminal hiện đại
#   - Có hướng dẫn sử dụng chi tiết
#
# =========================================================

from dataclasses import dataclass
from typing import List
import os
import time

# =========================
# CẤU HÌNH MÀU
# =========================

DIGIT_COLORS = {
    "đen": 0,
    "nâu": 1,
    "đỏ": 2,
    "cam": 3,
    "vàng": 4,
    "lục": 5,
    "xanh lá": 5,
    "lam": 6,
    "xanh dương": 6,
    "tím": 7,
    "xám": 8,
    "trắng": 9,
}

MULTIPLIER_COLORS = {
    "bạc": 0.01,
    "vàng kim": 0.1,
    "đen": 1,
    "nâu": 10,
    "đỏ": 100,
    "cam": 1_000,
    "vàng": 10_000,
    "lục": 100_000,
    "xanh lá": 100_000,
    "lam": 1_000_000,
    "xanh dương": 1_000_000,
    "tím": 10_000_000,
}

TOLERANCE_COLORS = {
    "nâu": "±1%",
    "đỏ": "±2%",
    "lục": "±0.5%",
    "xanh lá": "±0.5%",
    "lam": "±0.25%",
    "xanh dương": "±0.25%",
    "tím": "±0.1%",
    "xám": "±0.05%",
    "vàng kim": "±5%",
    "bạc": "±10%",
    "không": "±20%",
}

# =========================
# CLASS ĐIỆN TRỞ
# =========================

@dataclass
class Resistor:
    value: float
    tolerance: str
    bands: List[str]

# =========================
# HÀM HỖ TRỢ
# =========================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def format_resistance(value):
    """
    Chuyển đổi điện trở sang dạng đẹp
    """

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} MΩ"

    elif value >= 1_000:
        return f"{value / 1_000:.2f} kΩ"

    else:
        return f"{value:.2f} Ω"

# =========================
# GIỚI THIỆU
# =========================

def intro():

    clear()

    print("=" * 60)
    print("      MÁY TÍNH ĐIỆN TRỞ MÀU - PYTHON PROJECT")
    print("=" * 60)

    slow_print("\nXin chào! Đây là chương trình hỗ trợ:")
    slow_print("• Tính giá trị điện trở từ màu vòng")
    slow_print("• Hỗ trợ điện trở 4 vòng")
    slow_print("• Hỗ trợ điện trở 5 vòng")
    slow_print("• Hiển thị sai số chính xác")
    slow_print("• Dành cho sinh viên Điện tử - Viễn thông")

    print("\n" + "=" * 60)

    print("\nDANH SÁCH MÀU HỖ TRỢ:\n")

    for color, number in DIGIT_COLORS.items():
        print(f"{color:<12} → {number}")

    print("\nVí dụ:")
    print("Nâu - Đen - Đỏ - Vàng kim")
    print("=> 1kΩ ±5%")

    print("\n" + "=" * 60)

# =========================
# ĐỌC MÀU
# =========================

def get_color_input(prompt):

    while True:

        color = input(prompt).strip().lower()

        if (
            color in DIGIT_COLORS
            or color in MULTIPLIER_COLORS
            or color in TOLERANCE_COLORS
        ):
            return color

        print("❌ Màu không hợp lệ. Vui lòng nhập lại.")

# =========================
# TÍNH 4 VÒNG
# =========================

def calculate_4_band():

    print("\n--- ĐIỆN TRỞ 4 VÒNG ---\n")

    band1 = get_color_input("Vòng 1: ")
    band2 = get_color_input("Vòng 2: ")
    multiplier = get_color_input("Vòng nhân: ")
    tolerance = get_color_input("Sai số: ")

    first_digit = DIGIT_COLORS[band1]
    second_digit = DIGIT_COLORS[band2]

    multiplier_value = MULTIPLIER_COLORS[multiplier]

    resistance = ((first_digit * 10) + second_digit) * multiplier_value

    tolerance_value = TOLERANCE_COLORS.get(tolerance, "Không xác định")

    return Resistor(
        value=resistance,
        tolerance=tolerance_value,
        bands=[band1, band2, multiplier, tolerance]
    )

# =========================
# TÍNH 5 VÒNG
# =========================

def calculate_5_band():

    print("\n--- ĐIỆN TRỞ 5 VÒNG ---\n")

    band1 = get_color_input("Vòng 1: ")
    band2 = get_color_input("Vòng 2: ")
    band3 = get_color_input("Vòng 3: ")
    multiplier = get_color_input("Vòng nhân: ")
    tolerance = get_color_input("Sai số: ")

    d1 = DIGIT_COLORS[band1]
    d2 = DIGIT_COLORS[band2]
    d3 = DIGIT_COLORS[band3]

    multiplier_value = MULTIPLIER_COLORS[multiplier]

    resistance = ((d1 * 100) + (d2 * 10) + d3) * multiplier_value

    tolerance_value = TOLERANCE_COLORS.get(tolerance, "Không xác định")

    return Resistor(
        value=resistance,
        tolerance=tolerance_value,
        bands=[band1, band2, band3, multiplier, tolerance]
    )

# =========================
# HIỂN THỊ KẾT QUẢ
# =========================

def show_result(resistor: Resistor):

    print("\n" + "=" * 60)
    print("                KẾT QUẢ PHÂN TÍCH")
    print("=" * 60)

    print("\nMàu vòng:")

    for index, color in enumerate(resistor.bands, start=1):
        print(f"Vòng {index}: {color}")

    print("\nGiá trị điện trở:")
    print(f"→ {format_resistance(resistor.value)}")

    print("\nSai số:")
    print(f"→ {resistor.tolerance}")

    print("\n" + "=" * 60)

# =========================
# MENU CHÍNH
# =========================

def menu():

    while True:

        print("\nMENU:")
        print("1. Tính điện trở 4 vòng")
        print("2. Tính điện trở 5 vòng")
        print("3. Thoát")

        choice = input("\nChọn chức năng: ").strip()

        if choice == "1":

            resistor = calculate_4_band()
            show_result(resistor)

        elif choice == "2":

            resistor = calculate_5_band()
            show_result(resistor)

        elif choice == "3":

            print("\nCảm ơn đã sử dụng chương trình.")
            break

        else:
            print("\n❌ Lựa chọn không hợp lệ.")

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    intro()
    menu()
