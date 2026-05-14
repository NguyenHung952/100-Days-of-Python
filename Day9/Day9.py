# =========================================================
#            MÔ PHỎNG MẠCH RLC CƠ BẢN BẰNG PYTHON
# =========================================================
#
# Chức năng:
#   • Mô phỏng đáp ứng mạch RLC nối tiếp
#   • Vẽ đồ thị dao động điện áp
#   • Phân tích:
#       - Underdamped
#       - Critically damped
#       - Overdamped
#   • Tính:
#       - Tần số cộng hưởng
#       - Hệ số tắt dần
#       - Hằng số damping
#   • Hiển thị thông tin kỹ thuật chi tiết
#
# Phù hợp:
#   • Sinh viên Điện tử - Viễn thông
#   • Học phần Mạch điện tử
#   • DSP / Điều khiển / IoT
#
# Cài thư viện:
#   pip install numpy matplotlib
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import math
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

def format_resistance(r):

    if r >= 1_000_000:
        return f"{r / 1_000_000:.2f} MΩ"

    elif r >= 1_000:
        return f"{r / 1_000:.2f} kΩ"

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


def format_inductance(l):

    if l < 1e-3:
        return f"{l * 1000:.2f} mH"

    else:
        return f"{l:.3f} H"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    print("=" * 75)
    print("             RLC CIRCUIT SIMULATOR - PYTHON")
    print("=" * 75)

    slow_print("\nXin chào! Đây là chương trình mô phỏng mạch RLC.")
    slow_print("Chương trình hỗ trợ:")
    slow_print("• Mô phỏng dao động điện áp mạch RLC")
    slow_print("• Phân tích trạng thái damping")
    slow_print("• Vẽ đồ thị tín hiệu theo thời gian")
    slow_print("• Tính tần số cộng hưởng")
    slow_print("• Hiển thị thông số kỹ thuật chi tiết")

    print("\n" + "=" * 75)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Tần số cộng hưởng:")
    print("   f0 = 1 / (2π√LC)")

    print("\n2. Hệ số damping:")
    print("   α = R / (2L)")

    print("\n3. Dao động:")
    print("   • Underdamped  : Dao động giảm dần")
    print("   • Critically   : Tắt nhanh nhất")
    print("   • Overdamped   : Không dao động")

    print("\n" + "=" * 75)

# =========================================================
# NHẬP DỮ LIỆU
# =========================================================

def input_positive_float(message):

    while True:

        try:

            value = float(input(message))

            if value <= 0:
                print("❌ Giá trị phải > 0")
                continue

            return value

        except:
            print("❌ Dữ liệu không hợp lệ.")

# =========================================================
# TÍNH TOÁN THÔNG SỐ
# =========================================================

def resonance_frequency(l, c):

    return 1 / (2 * math.pi * math.sqrt(l * c))


def damping_factor(r, l):

    return r / (2 * l)


def natural_frequency(l, c):

    return 1 / math.sqrt(l * c)

# =========================================================
# PHÂN LOẠI MẠCH
# =========================================================

def classify_circuit(alpha, w0):

    if alpha < w0:
        return "UNDERDAMPED (Dao động giảm dần)"

    elif alpha == w0:
        return "CRITICALLY DAMPED"

    else:
        return "OVERDAMPED"

# =========================================================
# MÔ PHỎNG ĐÁP ỨNG
# =========================================================

def simulate_rlc():

    print("\n=== NHẬP THÔNG SỐ MẠCH ===\n")

    r = input_positive_float("Nhập điện trở R (Ω): ")
    l = input_positive_float("Nhập cuộn cảm L (H): ")
    c = input_positive_float("Nhập tụ điện C (F): ")
    v0 = input_positive_float("Nhập điện áp ban đầu (V): ")

    alpha = damping_factor(r, l)
    w0 = natural_frequency(l, c)

    f0 = resonance_frequency(l, c)

    circuit_type = classify_circuit(alpha, w0)

    # =====================================================
    # HIỂN THỊ THÔNG TIN
    # =====================================================

    print("\n" + "=" * 75)
    print("                  THÔNG TIN PHÂN TÍCH")
    print("=" * 75)

    print(f"\nR = {format_resistance(r)}")
    print(f"L = {format_inductance(l)}")
    print(f"C = {format_capacitance(c)}")

    print(f"\nTần số cộng hưởng:")
    print(f"→ {f0:.2f} Hz")

    print(f"\nHệ số damping:")
    print(f"→ {alpha:.4f}")

    print(f"\nLoại đáp ứng:")
    print(f"→ {circuit_type}")

    # =====================================================
    # MÔ PHỎNG ĐỒ THỊ
    # =====================================================

    print("\nĐang mô phỏng đồ thị...")

    t = np.linspace(0, 0.1, 2000)

    # UNDERDAMPED
    if alpha < w0:

        wd = math.sqrt(w0**2 - alpha**2)

        v = v0 * np.exp(-alpha * t) * np.cos(wd * t)

    # CRITICAL
    elif alpha == w0:

        v = v0 * np.exp(-alpha * t)

    # OVERDAMPED
    else:

        s1 = -alpha + math.sqrt(alpha**2 - w0**2)
        s2 = -alpha - math.sqrt(alpha**2 - w0**2)

        v = (
            v0 * np.exp(s1 * t)
            + v0 * np.exp(s2 * t)
        ) / 2

    # =====================================================
    # BẢNG DỮ LIỆU
    # =====================================================

    print("\n" + "=" * 75)
    print("                     BẢNG DỮ LIỆU")
    print("=" * 75)

    print(f"\n{'Thời gian (s)':<20}{'Điện áp (V)':<20}")

    step = len(t) // 10

    for i in range(0, len(t), step):

        print(
            f"{t[i]:<20.6f}"
            f"{v[i]:<20.4f}"
        )

    # =====================================================
    # VẼ ĐỒ THỊ
    # =====================================================

    plt.figure(figsize=(11, 5))

    plt.plot(t, v, linewidth=2)

    plt.title("Mô phỏng đáp ứng mạch RLC")
    plt.xlabel("Thời gian (s)")
    plt.ylabel("Điện áp (V)")

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
        print("                     MENU CHỨC NĂNG")
        print("=" * 75)

        print("1. Mô phỏng mạch RLC")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            simulate_rlc()

        elif choice == "2":

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
