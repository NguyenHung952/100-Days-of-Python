# =========================================================
#         SIGNAL VISUALIZER - VẼ ĐỒ THỊ SIN/COS
# =========================================================
#
# Chức năng:
#   • Vẽ tín hiệu sin
#   • Vẽ tín hiệu cos
#   • Vẽ đồng thời sin + cos
#   • Tùy chỉnh:
#       - Biên độ
#       - Tần số
#       - Pha ban đầu
#       - Thời gian mô phỏng
#   • Hiển thị thông tin tín hiệu
#   • Giao diện hiện đại bằng Python
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / Tín hiệu và hệ thống
#   • IoT / Embedded
#
# Thư viện cần:
#   pip install matplotlib numpy
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import math
import time
import os

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

    print("=" * 75)
    print("            SIGNAL VISUALIZER - PYTHON")
    print("=" * 75)

    slow_print("\nXin chào! Đây là chương trình mô phỏng tín hiệu.")
    slow_print("Các chức năng chính:")
    slow_print("• Vẽ đồ thị tín hiệu sin")
    slow_print("• Vẽ đồ thị tín hiệu cos")
    slow_print("• Phân tích biên độ và tần số")
    slow_print("• Tùy chỉnh pha ban đầu")
    slow_print("• Mô phỏng tín hiệu thời gian thực")

    print("\n" + "=" * 75)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Tín hiệu sin:")
    print("   x(t) = A × sin(2πft + φ)")

    print("\n2. Tín hiệu cos:")
    print("   x(t) = A × cos(2πft + φ)")

    print("\n3. Ý nghĩa:")
    print("   • A  : Biên độ")
    print("   • f  : Tần số")
    print("   • φ  : Pha ban đầu")

    print("\n4. Ứng dụng:")
    print("   • DSP")
    print("   • Truyền thông số")
    print("   • RF")
    print("   • IoT")
    print("   • Vi xử lý tín hiệu")

    print("\n" + "=" * 75)

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
# THÔNG TIN TÍN HIỆU
# =========================================================

def signal_info(amplitude, frequency, phase):

    print("\n" + "=" * 75)
    print("                 THÔNG TIN TÍN HIỆU")
    print("=" * 75)

    print(f"\nBiên độ (A): {amplitude}")
    print(f"Tần số (f): {frequency} Hz")
    print(f"Pha (φ)   : {phase} rad")

    print(f"\nChu kỳ tín hiệu:")
    print(f"T = 1/f = {1/frequency:.6f} s")

# =========================================================
# VẼ TÍN HIỆU SIN
# =========================================================

def plot_sin():

    print("\n=== VẼ TÍN HIỆU SIN ===\n")

    amplitude = input_positive_float("Nhập biên độ A: ")
    frequency = input_positive_float("Nhập tần số f (Hz): ")
    phase = float(input("Nhập pha φ (rad): "))
    duration = input_positive_float("Nhập thời gian mô phỏng (s): ")

    signal_info(amplitude, frequency, phase)

    print("\nĐang tạo đồ thị...")

    t = np.linspace(0, duration, 2000)

    signal = amplitude * np.sin(
        2 * np.pi * frequency * t + phase
    )

    plt.figure(figsize=(12, 5))

    plt.plot(t, signal, linewidth=2)

    plt.title("Đồ thị tín hiệu SIN")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# VẼ TÍN HIỆU COS
# =========================================================

def plot_cos():

    print("\n=== VẼ TÍN HIỆU COS ===\n")

    amplitude = input_positive_float("Nhập biên độ A: ")
    frequency = input_positive_float("Nhập tần số f (Hz): ")
    phase = float(input("Nhập pha φ (rad): "))
    duration = input_positive_float("Nhập thời gian mô phỏng (s): ")

    signal_info(amplitude, frequency, phase)

    print("\nĐang tạo đồ thị...")

    t = np.linspace(0, duration, 2000)

    signal = amplitude * np.cos(
        2 * np.pi * frequency * t + phase
    )

    plt.figure(figsize=(12, 5))

    plt.plot(t, signal, linewidth=2)

    plt.title("Đồ thị tín hiệu COS")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# VẼ SIN + COS
# =========================================================

def plot_both():

    print("\n=== VẼ ĐỒNG THỜI SIN + COS ===\n")

    amplitude = input_positive_float("Nhập biên độ A: ")
    frequency = input_positive_float("Nhập tần số f (Hz): ")
    phase = float(input("Nhập pha φ (rad): "))
    duration = input_positive_float("Nhập thời gian mô phỏng (s): ")

    signal_info(amplitude, frequency, phase)

    print("\nĐang tạo đồ thị...")

    t = np.linspace(0, duration, 2000)

    sin_signal = amplitude * np.sin(
        2 * np.pi * frequency * t + phase
    )

    cos_signal = amplitude * np.cos(
        2 * np.pi * frequency * t + phase
    )

    plt.figure(figsize=(12, 5))

    plt.plot(
        t,
        sin_signal,
        linewidth=2,
        label="SIN"
    )

    plt.plot(
        t,
        cos_signal,
        linewidth=2,
        label="COS"
    )

    plt.title("So sánh tín hiệu SIN và COS")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.legend()

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 75)
        print("                    MENU CHỨC NĂNG")
        print("=" * 75)

        print("1. Vẽ tín hiệu SIN")
        print("2. Vẽ tín hiệu COS")
        print("3. Vẽ SIN + COS")
        print("4. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            plot_sin()

        elif choice == "2":

            plot_cos()

        elif choice == "3":

            plot_both()

        elif choice == "4":

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
