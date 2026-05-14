# =========================================================
#              DAC SIMULATOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Mô phỏng DAC bằng đồ thị
#
# Chức năng:
#   • Mô phỏng DAC chuyển đổi số → analog
#   • Tạo dữ liệu digital mẫu
#   • Hiển thị:
#       - Tín hiệu digital
#       - Tín hiệu analog sau DAC
#   • Điều chỉnh:
#       - Độ phân giải DAC
#       - Điện áp tham chiếu
#       - Tần số lấy mẫu
#   • Hiển thị mã nhị phân DAC
#   • Phân tích staircase waveform
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • Embedded Systems
#   • STM32 / ESP32 / Arduino
#   • DSP / IoT
#
# Thư viện cần:
#   pip install numpy matplotlib
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
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

    print("=" * 90)
    print("                    DAC SIMULATOR")
    print("=" * 90)

    slow_print("\nXin chào! Đây là chương trình mô phỏng DAC.")
    slow_print("Các chức năng chính:")
    slow_print("• Mô phỏng DAC chuyển đổi số sang analog")
    slow_print("• Hiển thị staircase waveform")
    slow_print("• Mô phỏng dữ liệu digital")
    slow_print("• Hiển thị điện áp analog đầu ra")
    slow_print("• Phân tích độ phân giải DAC")
    slow_print("• Hiển thị mã nhị phân")

    print("\n" + "=" * 90)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. DAC là gì?")
    print("   DAC = Digital to Analog Converter")
    print("   Bộ chuyển đổi tín hiệu số sang analog")

    print("\n2. Chức năng:")
    print("   • Chuyển dữ liệu binary")
    print("     thành điện áp analog")

    print("\n3. Công thức DAC:")
    print("   Vout = Digital_Value × Resolution")

    print("\n4. DAC Resolution:")
    print("   Resolution = Vref / (2^n - 1)")

    print("\n5. Ứng dụng:")
    print("   • Audio")
    print("   • DSP")
    print("   • RF")
    print("   • STM32 / ESP32")
    print("   • IoT")
    print("   • Phát waveform")

    print("\n" + "=" * 90)

# DAC dùng để chuyển đổi tín hiệu số sang analog :contentReference[oaicite:0]{index=0}

# =========================================================
# INPUT
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
# TẠO DIGITAL DATA
# =========================================================

def create_digital_signal(bits):

    print("\n=== TẠO DỮ LIỆU DIGITAL ===\n")

    sample_count = int(
        input_positive_float(
            "Nhập số lượng sample: "
        )
    )

    max_value = (2 ** bits) - 1

    digital_values = np.random.randint(
        0,
        max_value + 1,
        sample_count
    )

    return digital_values

# =========================================================
# DAC CONVERSION
# =========================================================

def dac_conversion(
    digital_values,
    bits,
    vref
):

    resolution = vref / ((2 ** bits) - 1)

    analog_values = digital_values * resolution

    return analog_values, resolution

# =========================================================
# HIỂN THỊ THÔNG TIN DAC
# =========================================================

def show_dac_info(bits, vref, resolution):

    print("\n" + "=" * 90)
    print("                    THÔNG TIN DAC")
    print("=" * 90)

    print(f"\nĐộ phân giải DAC:")
    print(f"→ {bits} bit")

    print(f"\nSố mức DAC:")
    print(f"→ {2**bits} levels")

    print(f"\nĐiện áp tham chiếu:")
    print(f"→ {vref:.3f} V")

    print(f"\nDAC Resolution:")
    print(f"→ {resolution:.6f} V/LSB")

# =========================================================
# HIỂN THỊ BẢNG DỮ LIỆU
# =========================================================

def show_dac_table(
    digital_values,
    analog_values,
    bits
):

    print("\n" + "=" * 90)
    print("                    BẢNG DỮ LIỆU DAC")
    print("=" * 90)

    print(
        f"\n{'Sample':<10}"
        f"{'Digital':<15}"
        f"{'Binary':<20}"
        f"{'Analog(V)':<15}"
    )

    limit = min(20, len(digital_values))

    for i in range(limit):

        binary = format(
            digital_values[i],
            f'0{bits}b'
        )

        print(
            f"{i:<10}"
            f"{digital_values[i]:<15}"
            f"{binary:<20}"
            f"{analog_values[i]:<15.4f}"
        )

# =========================================================
# VẼ ĐỒ THỊ
# =========================================================

def plot_graphs(
    digital_values,
    analog_values
):

    samples = np.arange(len(digital_values))

    # =====================================================
    # DIGITAL SIGNAL
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.step(
        samples,
        digital_values,
        where='mid',
        linewidth=2
    )

    plt.title("Tín hiệu Digital")

    plt.xlabel("Sample")
    plt.ylabel("Digital Value")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # DAC OUTPUT
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.step(
        samples,
        analog_values,
        where='mid',
        linewidth=2
    )

    plt.title("Tín hiệu Analog sau DAC")

    plt.xlabel("Sample")
    plt.ylabel("Điện áp (V)")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# DAC MENU
# =========================================================

def dac_menu():

    print("\n=== CẤU HÌNH DAC ===\n")

    bits = int(
        input_positive_float(
            "Nhập độ phân giải DAC (bit): "
        )
    )

    vref = input_positive_float(
        "Nhập điện áp tham chiếu Vref (V): "
    )

    digital_values = create_digital_signal(bits)

    print("\nĐang mô phỏng DAC...")

    analog_values, resolution = dac_conversion(
        digital_values,
        bits,
        vref
    )

    show_dac_info(
        bits,
        vref,
        resolution
    )

    show_dac_table(
        digital_values,
        analog_values,
        bits
    )

    plot_graphs(
        digital_values,
        analog_values
    )

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 90)
        print("                    MENU CHỨC NĂNG")
        print("=" * 90)

        print("1. Mô phỏng DAC")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            dac_menu()

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
