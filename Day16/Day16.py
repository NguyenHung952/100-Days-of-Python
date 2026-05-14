# =========================================================
#              FIR FILTER SIMULATOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Bộ lọc số FIR đơn giản
#
# Chức năng:
#   • Tạo tín hiệu mẫu
#   • Thêm nhiễu tín hiệu
#   • Thiết kế bộ lọc FIR Low-pass
#   • Lọc tín hiệu bằng FIR
#   • Hiển thị:
#       - Tín hiệu gốc
#       - Tín hiệu nhiễu
#       - Tín hiệu sau lọc
#   • Hiển thị đáp ứng tần số FIR
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / Xử lý tín hiệu số
#   • IoT / Audio Processing
#
# Thư viện cần:
#   pip install numpy matplotlib scipy
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz
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

    print("=" * 85)
    print("                FIR FILTER SIMULATOR")
    print("=" * 85)

    slow_print("\nXin chào! Đây là chương trình mô phỏng bộ lọc FIR.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu mẫu")
    slow_print("• Mô phỏng nhiễu tín hiệu")
    slow_print("• Thiết kế FIR Low-pass")
    slow_print("• Lọc tín hiệu bằng FIR")
    slow_print("• Hiển thị đáp ứng tần số")
    slow_print("• Phân tích tín hiệu trước và sau lọc")

    print("\n" + "=" * 85)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. FIR là gì?")
    print("   FIR = Finite Impulse Response")

    print("\n2. Đặc điểm FIR:")
    print("   • Ổn định")
    print("   • Pha tuyến tính")
    print("   • Dễ thiết kế")

    print("\n3. Ứng dụng:")
    print("   • DSP")
    print("   • Audio Processing")
    print("   • RF")
    print("   • Viễn thông")
    print("   • IoT")

    print("\n4. Bộ lọc Low-pass:")
    print("   • Cho tần số thấp đi qua")
    print("   • Loại bỏ nhiễu cao tần")

    print("\n" + "=" * 85)

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
# TẠO TÍN HIỆU
# =========================================================

def create_signal():

    print("\n=== TẠO TÍN HIỆU ===\n")

    signal_freq = input_positive_float(
        "Nhập tần số tín hiệu chính (Hz): "
    )

    noise_freq = input_positive_float(
        "Nhập tần số nhiễu (Hz): "
    )

    sample_rate = input_positive_float(
        "Nhập tần số lấy mẫu Fs (Hz): "
    )

    duration = input_positive_float(
        "Nhập thời gian mô phỏng (s): "
    )

    t = np.linspace(
        0,
        duration,
        int(sample_rate * duration),
        endpoint=False
    )

    # =====================================================
    # TÍN HIỆU GỐC
    # =====================================================

    signal = np.sin(
        2 * np.pi * signal_freq * t
    )

    # =====================================================
    # NHIỄU
    # =====================================================

    noise = 0.5 * np.sin(
        2 * np.pi * noise_freq * t
    )

    noisy_signal = signal + noise

    return (
        t,
        signal,
        noisy_signal,
        sample_rate
    )

# =========================================================
# THIẾT KẾ FIR
# =========================================================

def design_fir_filter(sample_rate):

    print("\n=== THIẾT KẾ FIR FILTER ===\n")

    cutoff = input_positive_float(
        "Nhập tần số cắt (Hz): "
    )

    num_taps = int(
        input_positive_float(
            "Nhập số taps FIR: "
        )
    )

    fir_coeff = firwin(
        num_taps,
        cutoff,
        fs=sample_rate
    )

    return fir_coeff, cutoff, num_taps

# =========================================================
# LỌC TÍN HIỆU
# =========================================================

def apply_filter(signal, fir_coeff):

    filtered = lfilter(
        fir_coeff,
        1.0,
        signal
    )

    return filtered

# =========================================================
# HIỂN THỊ THÔNG TIN
# =========================================================

def show_info(cutoff, taps):

    print("\n" + "=" * 85)
    print("                 THÔNG TIN FIR FILTER")
    print("=" * 85)

    print(f"\nTần số cắt:")
    print(f"→ {cutoff:.2f} Hz")

    print(f"\nSố taps FIR:")
    print(f"→ {taps}")

    print("\nĐánh giá:")

    if taps < 20:

        print("→ Bộ lọc đơn giản")

    elif taps < 80:

        print("→ Bộ lọc trung bình")

    else:

        print("→ Bộ lọc chất lượng cao")

# =========================================================
# VẼ TÍN HIỆU
# =========================================================

def plot_signals(
    t,
    original,
    noisy,
    filtered
):

    # =====================================================
    # TÍN HIỆU GỐC
    # =====================================================

    plt.figure(figsize=(12, 4))

    plt.plot(
        t,
        original,
        linewidth=1.5
    )

    plt.title("Tín hiệu gốc")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # TÍN HIỆU NHIỄU
    # =====================================================

    plt.figure(figsize=(12, 4))

    plt.plot(
        t,
        noisy,
        linewidth=1.2
    )

    plt.title("Tín hiệu có nhiễu")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # TÍN HIỆU SAU LỌC
    # =====================================================

    plt.figure(figsize=(12, 4))

    plt.plot(
        t,
        filtered,
        linewidth=1.5
    )

    plt.title("Tín hiệu sau FIR Filter")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# ĐÁP ỨNG TẦN SỐ FIR
# =========================================================

def plot_frequency_response(fir_coeff):

    w, h = freqz(fir_coeff)

    plt.figure(figsize=(12, 5))

    plt.plot(
        w / np.pi,
        np.abs(h),
        linewidth=2
    )

    plt.title("Đáp ứng tần số FIR Filter")

    plt.xlabel("Tần số chuẩn hóa")

    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# FIR MENU
# =========================================================

def fir_menu():

    (
        t,
        original_signal,
        noisy_signal,
        sample_rate
    ) = create_signal()

    fir_coeff, cutoff, taps = design_fir_filter(
        sample_rate
    )

    print("\nĐang lọc tín hiệu...")

    filtered_signal = apply_filter(
        noisy_signal,
        fir_coeff
    )

    show_info(cutoff, taps)

    plot_signals(
        t,
        original_signal,
        noisy_signal,
        filtered_signal
    )

    plot_frequency_response(fir_coeff)

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 85)
        print("                    MENU CHỨC NĂNG")
        print("=" * 85)

        print("1. Mô phỏng FIR Filter")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            fir_menu()

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
