# =========================================================
#              OHM'S LAW CALCULATOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Máy tính định luật Ohm
#
# Chức năng:
#   • Tính điện áp (V)
#   • Tính dòng điện (I)
#   • Tính điện trở (R)
#   • Tính công suất điện (P)
#   • Hiển thị công thức chi tiết
#   • Phân tích thông số mạch điện
#   • Giao diện terminal hiện đại
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded
#   • Arduino / ESP32 / STM32
#   • Học phần kỹ thuật điện
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
# FORMAT ĐƠN VỊ
# =========================================================

def format_voltage(v):

    return f"{v:.3f} V"


def format_current(i):

    if i < 1:
        return f"{i * 1000:.3f} mA"

    return f"{i:.3f} A"


def format_resistance(r):

    if r >= 1_000_000:
        return f"{r / 1_000_000:.3f} MΩ"

    elif r >= 1_000:
        return f"{r / 1_000:.3f} kΩ"

    else:
        return f"{r:.3f} Ω"


def format_power(p):

    if p < 1:
        return f"{p * 1000:.3f} mW"

    return f"{p:.3f} W"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    print("=" * 75)
    print("                OHM'S LAW CALCULATOR")
    print("=" * 75)

    slow_print("\nXin chào! Đây là chương trình tính định luật Ohm.")
    slow_print("Các chức năng chính:")
    slow_print("• Tính điện áp")
    slow_print("• Tính dòng điện")
    slow_print("• Tính điện trở")
    slow_print("• Tính công suất")
    slow_print("• Hiển thị thông tin phân tích mạch")

    print("\n" + "=" * 75)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Định luật Ohm:")
    print("   V = I × R")

    print("\n2. Công suất điện:")
    print("   P = V × I")

    print("\n3. Công thức mở rộng:")
    print("   I = V / R")
    print("   R = V / I")
    print("   P = I²R")
    print("   P = V²/R")

    print("\n4. Ứng dụng:")
    print("   • Thiết kế mạch điện")
    print("   • Arduino / ESP32")
    print("   • Nguồn điện")
    print("   • IoT")
    print("   • Mạch cảm biến")

    print("\n" + "=" * 75)

# =========================================================
# INPUT
# =========================================================

def input_positive_float(message):

    while True:

        try:

            value = float(input(message))

            if value <= 0:
                print("❌ Giá trị phải lớn hơn 0.")
                continue

            return value

        except:
            print("❌ Dữ liệu không hợp lệ.")

# =========================================================
# HIỂN THỊ KẾT QUẢ
# =========================================================

def show_result(title, formula, result):

    print("\n" + "=" * 75)
    print(f"                  {title}")
    print("=" * 75)

    print(f"\nCông thức:")
    print(f"→ {formula}")

    print(f"\nKết quả:")
    print(f"→ {result}")

# =========================================================
# TÍNH ĐIỆN ÁP
# =========================================================

def calculate_voltage():

    print("\n=== TÍNH ĐIỆN ÁP (V) ===\n")

    current = input_positive_float(
        "Nhập dòng điện I (A): "
    )

    resistance = input_positive_float(
        "Nhập điện trở R (Ω): "
    )

    voltage = current * resistance

    show_result(
        "TÍNH ĐIỆN ÁP",
        "V = I × R",
        format_voltage(voltage)
    )

# =========================================================
# TÍNH DÒNG ĐIỆN
# =========================================================

def calculate_current():

    print("\n=== TÍNH DÒNG ĐIỆN (I) ===\n")

    voltage = input_positive_float(
        "Nhập điện áp V (V): "
    )

    resistance = input_positive_float(
        "Nhập điện trở R (Ω): "
    )

    current = voltage / resistance

    show_result(
        "TÍNH DÒNG ĐIỆN",
        "I = V / R",
        format_current(current)
    )

# =========================================================
# TÍNH ĐIỆN TRỞ
# =========================================================

def calculate_resistance():

    print("\n=== TÍNH ĐIỆN TRỞ (R) ===\n")

    voltage = input_positive_float(
        "Nhập điện áp V (V): "
    )

    current = input_positive_float(
        "Nhập dòng điện I (A): "
    )

    resistance = voltage / current

    show_result(
        "TÍNH ĐIỆN TRỞ",
        "R = V / I",
        format_resistance(resistance)
    )

# =========================================================
# TÍNH CÔNG SUẤT
# =========================================================

def calculate_power():

    print("\n=== TÍNH CÔNG SUẤT (P) ===\n")

    voltage = input_positive_float(
        "Nhập điện áp V (V): "
    )

    current = input_positive_float(
        "Nhập dòng điện I (A): "
    )

    power = voltage * current

    show_result(
        "TÍNH CÔNG SUẤT",
        "P = V × I",
        format_power(power)
    )

# =========================================================
# PHÂN TÍCH MẠCH
# =========================================================

def analyze_circuit():

    print("\n=== PHÂN TÍCH MẠCH ĐIỆN ===\n")

    voltage = input_positive_float(
        "Nhập điện áp nguồn (V): "
    )

    resistance = input_positive_float(
        "Nhập điện trở tải (Ω): "
    )

    current = voltage / resistance

    power = voltage * current

    print("\n" + "=" * 75)
    print("                 KẾT QUẢ PHÂN TÍCH")
    print("=" * 75)

    print(f"\nĐiện áp:")
    print(f"→ {format_voltage(voltage)}")

    print(f"\nĐiện trở:")
    print(f"→ {format_resistance(resistance)}")

    print(f"\nDòng điện:")
    print(f"→ {format_current(current)}")

    print(f"\nCông suất:")
    print(f"→ {format_power(power)}")

    print("\nĐánh giá tải:")

    if power < 1:
        print("→ Tải công suất thấp")

    elif power < 10:
        print("→ Tải công suất trung bình")

    else:
        print("→ Tải công suất cao")

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 75)
        print("                    MENU CHỨC NĂNG")
        print("=" * 75)

        print("1. Tính điện áp (V)")
        print("2. Tính dòng điện (I)")
        print("3. Tính điện trở (R)")
        print("4. Tính công suất (P)")
        print("5. Phân tích mạch điện")
        print("6. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            calculate_voltage()

        elif choice == "2":

            calculate_current()

        elif choice == "3":

            calculate_resistance()

        elif choice == "4":

            calculate_power()

        elif choice == "5":

            analyze_circuit()

        elif choice == "6":

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
