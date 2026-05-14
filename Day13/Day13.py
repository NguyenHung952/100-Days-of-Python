# =========================================================
#            ELECTRONIC UNIT CONVERTER - PYTHON
# =========================================================
#
# Chủ đề:
#   Công cụ đổi đơn vị điện tử
#
# Chức năng:
#   • Đổi điện áp
#   • Đổi dòng điện
#   • Đổi điện trở
#   • Đổi điện dung
#   • Đổi tần số
#   • Đổi công suất
#   • Hiển thị bảng quy đổi chi tiết
#   • Giao diện terminal hiện đại
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded
#   • Arduino / ESP32 / STM32
#   • DSP / Vi điều khiển
#
# Python Version:
#   Python 3.x
#
# =========================================================

import os
import time

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.01):

    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)

    print()

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    print("=" * 80)
    print("              ELECTRONIC UNIT CONVERTER")
    print("=" * 80)

    slow_print("\nXin chào! Đây là công cụ đổi đơn vị điện tử.")
    slow_print("Các chức năng chính:")
    slow_print("• Đổi điện áp")
    slow_print("• Đổi dòng điện")
    slow_print("• Đổi điện trở")
    slow_print("• Đổi điện dung")
    slow_print("• Đổi tần số")
    slow_print("• Đổi công suất")
    slow_print("• Hiển thị bảng chuyển đổi chi tiết")

    print("\n" + "=" * 80)

    print("\nĐƠN VỊ HỖ TRỢ:\n")

    print("1. Điện áp:")
    print("   V, mV, µV, kV")

    print("\n2. Dòng điện:")
    print("   A, mA, µA")

    print("\n3. Điện trở:")
    print("   Ω, kΩ, MΩ")

    print("\n4. Điện dung:")
    print("   F, mF, µF, nF, pF")

    print("\n5. Tần số:")
    print("   Hz, kHz, MHz, GHz")

    print("\n6. Công suất:")
    print("   W, mW, kW")

    print("\n" + "=" * 80)

# =========================================================
# INPUT
# =========================================================

def input_positive_float(message):

    while True:

        try:

            value = float(input(message))

            if value < 0:
                print("❌ Giá trị không hợp lệ.")
                continue

            return value

        except:
            print("❌ Dữ liệu không hợp lệ.")

# =========================================================
# HÀM CHUYỂN ĐỔI
# =========================================================

def convert_unit(value, from_factor, to_factor):

    base_value = value * from_factor

    converted = base_value / to_factor

    return converted

# =========================================================
# MENU ĐIỆN ÁP
# =========================================================

def voltage_converter():

    units = {
        "1": ("µV", 1e-6),
        "2": ("mV", 1e-3),
        "3": ("V", 1),
        "4": ("kV", 1e3)
    }

    convert_menu("ĐIỆN ÁP", units)

# =========================================================
# MENU DÒNG ĐIỆN
# =========================================================

def current_converter():

    units = {
        "1": ("µA", 1e-6),
        "2": ("mA", 1e-3),
        "3": ("A", 1)
    }

    convert_menu("DÒNG ĐIỆN", units)

# =========================================================
# MENU ĐIỆN TRỞ
# =========================================================

def resistance_converter():

    units = {
        "1": ("Ω", 1),
        "2": ("kΩ", 1e3),
        "3": ("MΩ", 1e6)
    }

    convert_menu("ĐIỆN TRỞ", units)

# =========================================================
# MENU ĐIỆN DUNG
# =========================================================

def capacitance_converter():

    units = {
        "1": ("pF", 1e-12),
        "2": ("nF", 1e-9),
        "3": ("µF", 1e-6),
        "4": ("mF", 1e-3),
        "5": ("F", 1)
    }

    convert_menu("ĐIỆN DUNG", units)

# =========================================================
# MENU TẦN SỐ
# =========================================================

def frequency_converter():

    units = {
        "1": ("Hz", 1),
        "2": ("kHz", 1e3),
        "3": ("MHz", 1e6),
        "4": ("GHz", 1e9)
    }

    convert_menu("TẦN SỐ", units)

# =========================================================
# MENU CÔNG SUẤT
# =========================================================

def power_converter():

    units = {
        "1": ("mW", 1e-3),
        "2": ("W", 1),
        "3": ("kW", 1e3)
    }

    convert_menu("CÔNG SUẤT", units)

# =========================================================
# MENU CHUYỂN ĐỔI CHUNG
# =========================================================

def convert_menu(title, units):

    print("\n" + "=" * 80)
    print(f"                 CHUYỂN ĐỔI {title}")
    print("=" * 80)

    print("\nDanh sách đơn vị:\n")

    for key, unit in units.items():

        print(f"{key}. {unit[0]}")

    value = input_positive_float("\nNhập giá trị: ")

    from_unit = input("\nĐổi từ đơn vị: ")
    to_unit = input("Sang đơn vị: ")

    if from_unit not in units or to_unit not in units:

        print("\n❌ Đơn vị không hợp lệ.")
        return

    from_name, from_factor = units[from_unit]
    to_name, to_factor = units[to_unit]

    result = convert_unit(
        value,
        from_factor,
        to_factor
    )

    print("\n" + "=" * 80)
    print("                     KẾT QUẢ")
    print("=" * 80)

    print(
        f"\n{value} {from_name}"
        f" = "
        f"{result:.6f} {to_name}"
    )

# =========================================================
# MENU CHÍNH
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 80)
        print("                    MENU CHỨC NĂNG")
        print("=" * 80)

        print("1. Đổi điện áp")
        print("2. Đổi dòng điện")
        print("3. Đổi điện trở")
        print("4. Đổi điện dung")
        print("5. Đổi tần số")
        print("6. Đổi công suất")
        print("7. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            voltage_converter()

        elif choice == "2":

            current_converter()

        elif choice == "3":

            resistance_converter()

        elif choice == "4":

            capacitance_converter()

        elif choice == "5":

            frequency_converter()

        elif choice == "6":

            power_converter()

        elif choice == "7":

            print("\nCảm ơn đã sử dụng chương trình.")
            break

        else:
            print("\n❌ Lựa chọn không hợp lệ.")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    intro()
    menu()
