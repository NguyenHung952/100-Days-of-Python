# =========================================================
#           MÔ PHỎNG MẠCH RC BẰNG PYTHON
# =========================================================
#
# Chức năng:
#   • Mô phỏng quá trình sạc tụ RC
#   • Mô phỏng quá trình xả tụ RC
#   • Vẽ đồ thị điện áp theo thời gian
#   • Hiển thị hằng số thời gian τ
#   • Hiển thị bảng dữ liệu mô phỏng
#   • Giao diện terminal hiện đại
#
# Phù hợp:
#   • Sinh viên Điện tử - Viễn thông
#   • Học DSP / IoT / Embedded
#   • Môn Kỹ thuật mạch điện tử
#
# Thư viện cần:
#   pip install matplotlib numpy
#
# =========================================================

import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# HÀM GIAO DIỆN
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

def format_resistance(r):

    if r >= 1_000_000:
        return f"{r / 1_000_000:.2f} MΩ"

    elif r >= 1000:
        return f"{r / 1000:.2f} kΩ"

    else:
        return f"{r:.2f} Ω"


def format_capacitance(c):

    if c < 1e-9:
        return f"{c * 1e12:.2f} pF"

    elif c < 1e-6:
        return f"{c * 1e9:.2f} nF"

    elif c < 1e-3:
        return f"{c * 1e6:.2f} µF"

    else:
        return f"{c:.6f} F"


def format_time(t):

    if t < 0.001:
        return f"{t * 1_000_000:.2f} µs"

    elif t < 1:
        return f"{t * 1000:.2f} ms"

    else:
        return f"{t:.2f} s"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    print("=" * 70)
    print("              RC CIRCUIT SIMULATOR - PYTHON")
    print("=" * 70)

    slow_print("\nXin chào! Đây là chương trình mô phỏng mạch RC.")
    slow_print("Các chức năng chính:")
    slow_print("• Mô phỏng quá trình sạc tụ điện")
    slow_print("• Mô phỏng quá trình xả tụ điện")
    slow_print("• Vẽ đồ thị điện áp theo thời gian")
    slow_print("• Hiển thị bảng dữ liệu chi tiết")
    slow_print("• Tính hằng số thời gian τ = R × C")

    print("\n" + "=" * 70)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Hằng số thời gian:")
    print("   τ = R × C")

    print("\n2. Công thức sạc tụ:")
    print("   V(t) = Vs × (1 - e^(-t/RC))")

    print("\n3. Công thức xả tụ:")
    print("   V(t) = V0 × e^(-t/RC)")

    print("\n4. Sau khoảng 5τ:")
    print("   • Tụ gần như sạc/xả hoàn toàn")

    print("\n" + "=" * 70)

# =========================================================
# NHẬP DỮ LIỆU
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
# TÍNH HẰNG SỐ THỜI GIAN
# =========================================================

def calculate_tau(r, c):

    return r * c

# =========================================================
# MÔ PHỎNG SẠC
# =========================================================

def simulate_charge():

    print("\n=== MÔ PHỎNG SẠC TỤ RC ===\n")

    r = input_positive_float("Nhập điện trở R (Ω): ")
    c = input_positive_float("Nhập điện dung C (F): ")
    vs = input_positive_float("Nhập điện áp nguồn Vs (V): ")

    tau = calculate_tau(r, c)

    print("\nĐang mô phỏng...")

    t = np.linspace(0, 5 * tau, 500)

    vc = vs * (1 - np.exp(-t / tau))

    show_simulation_info(r, c, tau)

    show_table(t, vc)

    plot_graph(
        t,
        vc,
        "Mô phỏng quá trình SẠC tụ RC",
        "Điện áp tụ (V)"
    )

# =========================================================
# MÔ PHỎNG XẢ
# =========================================================

def simulate_discharge():

    print("\n=== MÔ PHỎNG XẢ TỤ RC ===\n")

    r = input_positive_float("Nhập điện trở R (Ω): ")
    c = input_positive_float("Nhập điện dung C (F): ")
    v0 = input_positive_float("Nhập điện áp ban đầu V0 (V): ")

    tau = calculate_tau(r, c)

    print("\nĐang mô phỏng...")

    t = np.linspace(0, 5 * tau, 500)

    vc = v0 * np.exp(-t / tau)

    show_simulation_info(r, c, tau)

    show_table(t, vc)

    plot_graph(
        t,
        vc,
        "Mô phỏng quá trình XẢ tụ RC",
        "Điện áp tụ (V)"
    )

# =========================================================
# THÔNG TIN MÔ PHỎNG
# =========================================================

def show_simulation_info(r, c, tau):

    print("\n" + "=" * 70)
    print("                 THÔNG TIN MÔ PHỎNG")
    print("=" * 70)

    print(f"\nĐiện trở R : {format_resistance(r)}")
    print(f"Điện dung C: {format_capacitance(c)}")
    print(f"Hằng số τ  : {format_time(tau)}")

    print("\nÝ nghĩa:")
    print("• Sau 1τ  : đạt khoảng 63%")
    print("• Sau 5τ  : gần hoàn tất")

# =========================================================
# BẢNG DỮ LIỆU
# =========================================================

def show_table(time_values, voltage_values):

    print("\n" + "=" * 70)
    print("                 BẢNG DỮ LIỆU MÔ PHỎNG")
    print("=" * 70)

    print(f"\n{'Thời gian (s)':<20}{'Điện áp (V)':<20}")

    step = len(time_values) // 10

    for i in range(0, len(time_values), step):

        print(
            f"{time_values[i]:<20.6f}"
            f"{voltage_values[i]:<20.4f}"
        )

# =========================================================
# VẼ ĐỒ THỊ
# =========================================================

def plot_graph(t, vc, title, ylabel):

    plt.figure(figsize=(10, 5))

    plt.plot(t, vc, linewidth=2)

    plt.title(title)
    plt.xlabel("Thời gian (s)")
    plt.ylabel(ylabel)

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 70)
        print("                     MENU CHỨC NĂNG")
        print("=" * 70)

        print("1. Mô phỏng sạc tụ RC")
        print("2. Mô phỏng xả tụ RC")
        print("3. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":
            simulate_charge()

        elif choice == "2":
            simulate_discharge()

        elif choice == "3":

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
