# =========================================================
#        RC CIRCUIT CALCULATOR - MẠCH RC PYTHON
# =========================================================
#
# Chức năng:
#   • Tính hằng số thời gian RC
#   • Tính điện áp sạc tụ theo thời gian
#   • Tính điện áp xả tụ theo thời gian
#   • Tính tần số cắt mạch RC
#   • Hiển thị bảng phân tích chi tiết
#   • Giao diện terminal hiện đại
#
# Phù hợp:
#   • Sinh viên Điện tử - Viễn thông
#   • Học phần Mạch điện tử
#   • IoT / Embedded
#
# Python Version: 3.x
#
# =========================================================

from dataclasses import dataclass
import math
import time
import os

# =========================================================
# CLASS DỮ LIỆU
# =========================================================

@dataclass
class RCCircuit:
    resistance: float
    capacitance: float

# =========================================================
# HÀM HỖ TRỢ
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def slow_print(text, delay=0.01):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def format_time(seconds):

    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f} µs"

    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"

    else:
        return f"{seconds:.2f} s"


def format_capacitance(cap):

    if cap < 1e-9:
        return f"{cap * 1e12:.2f} pF"

    elif cap < 1e-6:
        return f"{cap * 1e9:.2f} nF"

    elif cap < 1e-3:
        return f"{cap * 1e6:.2f} µF"

    else:
        return f"{cap:.6f} F"


def format_resistance(res):

    if res >= 1_000_000:
        return f"{res / 1_000_000:.2f} MΩ"

    elif res >= 1_000:
        return f"{res / 1000:.2f} kΩ"

    else:
        return f"{res:.2f} Ω"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    print("=" * 65)
    print("          RC CIRCUIT CALCULATOR - PYTHON")
    print("=" * 65)

    slow_print("\nXin chào! Chương trình hỗ trợ:")
    slow_print("• Tính toán mạch RC cơ bản")
    slow_print("• Phân tích quá trình sạc tụ")
    slow_print("• Phân tích quá trình xả tụ")
    slow_print("• Tính tần số cắt bộ lọc RC")
    slow_print("• Hiển thị dữ liệu chi tiết")
    slow_print("• Phù hợp học tập ngành Điện tử Viễn thông")

    print("\n" + "=" * 65)

    print("\nCÔNG THỨC QUAN TRỌNG:\n")

    print("1. Hằng số thời gian:")
    print("   τ = R × C")

    print("\n2. Điện áp sạc tụ:")
    print("   V(t) = Vsource × (1 - e^(-t/RC))")

    print("\n3. Điện áp xả tụ:")
    print("   V(t) = Vinitial × e^(-t/RC)")

    print("\n4. Tần số cắt RC:")
    print("   fc = 1 / (2πRC)")

    print("\n" + "=" * 65)

# =========================================================
# NHẬP DỮ LIỆU
# =========================================================

def input_float(message):

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
# TÍNH HẰNG SỐ THỜI GIAN
# =========================================================

def calculate_tau(rc: RCCircuit):

    return rc.resistance * rc.capacitance

# =========================================================
# ĐIỆN ÁP SẠC TỤ
# =========================================================

def charging_voltage(v_source, time_value, tau):

    return v_source * (1 - math.exp(-time_value / tau))

# =========================================================
# ĐIỆN ÁP XẢ TỤ
# =========================================================

def discharging_voltage(v_initial, time_value, tau):

    return v_initial * math.exp(-time_value / tau)

# =========================================================
# TẦN SỐ CẮT RC
# =========================================================

def cutoff_frequency(rc: RCCircuit):

    return 1 / (2 * math.pi * rc.resistance * rc.capacitance)

# =========================================================
# MENU 1 - TÍNH HẰNG SỐ THỜI GIAN
# =========================================================

def menu_tau():

    print("\n=== TÍNH HẰNG SỐ THỜI GIAN RC ===\n")

    r = input_float("Nhập điện trở R (Ω): ")
    c = input_float("Nhập điện dung C (F): ")

    rc = RCCircuit(r, c)

    tau = calculate_tau(rc)

    print("\nKẾT QUẢ:")
    print(f"R = {format_resistance(r)}")
    print(f"C = {format_capacitance(c)}")
    print(f"τ = {format_time(tau)}")

# =========================================================
# MENU 2 - SẠC TỤ
# =========================================================

def menu_charge():

    print("\n=== PHÂN TÍCH SẠC TỤ ===\n")

    r = input_float("Nhập điện trở R (Ω): ")
    c = input_float("Nhập điện dung C (F): ")
    vs = input_float("Nhập điện áp nguồn (V): ")
    t = input_float("Nhập thời gian t (s): ")

    rc = RCCircuit(r, c)

    tau = calculate_tau(rc)

    voltage = charging_voltage(vs, t, tau)

    print("\nKẾT QUẢ:")
    print(f"Hằng số thời gian: {format_time(tau)}")
    print(f"Điện áp tụ tại t={t}s:")
    print(f"→ {voltage:.3f} V")

# =========================================================
# MENU 3 - XẢ TỤ
# =========================================================

def menu_discharge():

    print("\n=== PHÂN TÍCH XẢ TỤ ===\n")

    r = input_float("Nhập điện trở R (Ω): ")
    c = input_float("Nhập điện dung C (F): ")
    vi = input_float("Nhập điện áp ban đầu (V): ")
    t = input_float("Nhập thời gian t (s): ")

    rc = RCCircuit(r, c)

    tau = calculate_tau(rc)

    voltage = discharging_voltage(vi, t, tau)

    print("\nKẾT QUẢ:")
    print(f"Hằng số thời gian: {format_time(tau)}")
    print(f"Điện áp còn lại tại t={t}s:")
    print(f"→ {voltage:.3f} V")

# =========================================================
# MENU 4 - TẦN SỐ CẮT
# =========================================================

def menu_cutoff():

    print("\n=== TÍNH TẦN SỐ CẮT RC ===\n")

    r = input_float("Nhập điện trở R (Ω): ")
    c = input_float("Nhập điện dung C (F): ")

    rc = RCCircuit(r, c)

    fc = cutoff_frequency(rc)

    print("\nKẾT QUẢ:")
    print(f"R = {format_resistance(r)}")
    print(f"C = {format_capacitance(c)}")
    print(f"Tần số cắt fc = {fc:.2f} Hz")

# =========================================================
# MENU CHÍNH
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 65)
        print("                    MENU CHỨC NĂNG")
        print("=" * 65)

        print("1. Tính hằng số thời gian RC")
        print("2. Phân tích sạc tụ")
        print("3. Phân tích xả tụ")
        print("4. Tính tần số cắt RC")
        print("5. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":
            menu_tau()

        elif choice == "2":
            menu_charge()

        elif choice == "3":
            menu_discharge()

        elif choice == "4":
            menu_cutoff()

        elif choice == "5":
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
