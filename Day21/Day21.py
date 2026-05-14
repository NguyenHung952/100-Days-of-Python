# =========================================================
#              MINI OSCILLOSCOPE - PYTHON
# =========================================================
#
# Chủ đề:
#   Tạo oscilloscope mini bằng Python
#
# Chức năng:
#   • Mô phỏng oscilloscope thời gian thực
#   • Hiển thị waveform tín hiệu
#   • Điều chỉnh:
#       - Tần số
#       - Biên độ
#       - Sampling Rate
#   • Hỗ trợ:
#       - Sóng SIN
#       - Sóng COS
#       - Sóng PWM
#   • Hiển thị Grid Oscilloscope
#   • Phân tích tín hiệu realtime
#   • Đo Peak / RMS
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / IoT / Embedded
#   • STM32 / ESP32
#   • Xử lý tín hiệu
#
# Thư viện cần:
#   pip install numpy matplotlib
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
    print("                  MINI OSCILLOSCOPE")
    print("=" * 90)

    slow_print("\nXin chào! Đây là chương trình oscilloscope mini.")
    slow_print("Các chức năng chính:")
    slow_print("• Hiển thị waveform thời gian thực")
    slow_print("• Mô phỏng tín hiệu điện tử")
    slow_print("• Oscilloscope grid")
    slow_print("• Đo Peak Voltage")
    slow_print("• Đo RMS Voltage")
    slow_print("• Hỗ trợ nhiều loại sóng")

    print("\n" + "=" * 90)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Oscilloscope là gì?")
    print("   • Thiết bị hiển thị tín hiệu điện")

    print("\n2. Chức năng:")
    print("   • Quan sát waveform")
    print("   • Đo biên độ")
    print("   • Đo tần số")
    print("   • Phân tích tín hiệu")

    print("\n3. Ứng dụng:")
    print("   • Embedded Systems")
    print("   • RF")
    print("   • DSP")
    print("   • IoT")
    print("   • Audio")
    print("   • Debug mạch điện")

    print("\n4. Hỗ trợ tín hiệu:")
    print("   • SIN")
    print("   • COS")
    print("   • PWM")

    print("\n" + "=" * 90)

# Oscilloscope realtime bằng Python thường dùng matplotlib.animation.FuncAnimation. :contentReference[oaicite:0]{index=0}

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
# CHỌN LOẠI TÍN HIỆU
# =========================================================

def choose_signal():

    print("\n=== CHỌN TÍN HIỆU ===\n")

    print("1. Sóng SIN")
    print("2. Sóng COS")
    print("3. Sóng PWM")

    while True:

        choice = input("\nChọn tín hiệu: ")

        if choice in ["1", "2", "3"]:

            return choice

        print("❌ Lựa chọn không hợp lệ.")

# =========================================================
# TÍNH RMS
# =========================================================

def calculate_rms(signal):

    return np.sqrt(np.mean(signal**2))

# =========================================================
# TẠO OSCILLOSCOPE
# =========================================================

def oscilloscope():

    signal_type = choose_signal()

    print("\n=== CẤU HÌNH TÍN HIỆU ===\n")

    amplitude = input_positive_float(
        "Nhập biên độ tín hiệu: "
    )

    frequency = input_positive_float(
        "Nhập tần số tín hiệu (Hz): "
    )

    sample_rate = input_positive_float(
        "Nhập Sampling Rate (Hz): "
    )

    duration = input_positive_float(
        "Nhập thời gian hiển thị (s): "
    )

    # =====================================================
    # TIME AXIS
    # =====================================================

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration)
    )

    # =====================================================
    # TẠO TÍN HIỆU
    # =====================================================

    if signal_type == "1":

        signal = amplitude * np.sin(
            2 * np.pi * frequency * t
        )

        signal_name = "SIN"

    elif signal_type == "2":

        signal = amplitude * np.cos(
            2 * np.pi * frequency * t
        )

        signal_name = "COS"

    else:

        signal = amplitude * (
            np.sin(
                2 * np.pi * frequency * t
            ) > 0
        )

        signal_name = "PWM"

    # =====================================================
    # THÔNG TIN TÍN HIỆU
    # =====================================================

    peak_voltage = np.max(signal)

    rms_voltage = calculate_rms(signal)

    print("\n" + "=" * 90)
    print("                 THÔNG TIN TÍN HIỆU")
    print("=" * 90)

    print(f"\nLoại tín hiệu:")
    print(f"→ {signal_name}")

    print(f"\nBiên độ:")
    print(f"→ {amplitude:.3f} V")

    print(f"\nTần số:")
    print(f"→ {frequency:.3f} Hz")

    print(f"\nPeak Voltage:")
    print(f"→ {peak_voltage:.3f} V")

    print(f"\nRMS Voltage:")
    print(f"→ {rms_voltage:.3f} V")

    # =====================================================
    # OSCILLOSCOPE DISPLAY
    # =====================================================

    print("\nĐang khởi tạo oscilloscope realtime...")

    fig, ax = plt.subplots(figsize=(12, 5))

    line, = ax.plot([], [], linewidth=2)

    ax.set_xlim(0, duration)

    ax.set_ylim(
        -amplitude * 1.5,
        amplitude * 1.5
    )

    ax.set_title(
        f"Mini Oscilloscope - {signal_name} Wave"
    )

    ax.set_xlabel("Thời gian (s)")

    ax.set_ylabel("Biên độ (V)")

    ax.grid(True)

    # =====================================================
    # ANIMATION UPDATE
    # =====================================================

    def update(frame):

        current_t = t[:frame]

        current_signal = signal[:frame]

        line.set_data(
            current_t,
            current_signal
        )

        return line,

    # =====================================================
    # ANIMATION
    # =====================================================

    animation = FuncAnimation(
        fig,
        update,
        frames=len(t),
        interval=10,
        blit=True,
        repeat=True
    )

    plt.tight_layout()

    plt.show()

# FuncAnimation thường được dùng để tạo oscilloscope realtime với matplotlib. :contentReference[oaicite:1]{index=1}

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 90)
        print("                    MENU CHỨC NĂNG")
        print("=" * 90)

        print("1. Khởi động Mini Oscilloscope")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            oscilloscope()

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
