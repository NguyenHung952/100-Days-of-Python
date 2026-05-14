# =========================================================
#              IIR FILTER SIMULATOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Bộ lọc số IIR đơn giản
#
# Chức năng:
#   • Tạo tín hiệu mẫu
#   • Mô phỏng nhiễu tín hiệu
#   • Thiết kế bộ lọc IIR:
#       - Low-pass
#       - High-pass
#   • Lọc tín hiệu bằng IIR
#   • Hiển thị:
#       - Tín hiệu gốc
#       - Tín hiệu nhiễu
#       - Tín hiệu sau lọc
#   • Hiển thị đáp ứng tần số
#   • Phân tích hệ số lọc
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / Xử lý tín hiệu số
#   • Audio Processing
#   • RF / IoT
#
# Thư viện cần:
#   pip install numpy matplotlib scipy
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz
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
    print("                IIR FILTER SIMULATOR")
    print("=" * 85)

    slow_print("\nXin chào! Đây là chương trình mô phỏng bộ lọc IIR.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu mẫu")
    slow_print("• Mô phỏng nhiễu tín hiệu")
    slow_print("• Thiết kế bộ lọc IIR")
    slow_print("• Lọc tín hiệu bằng IIR")
    slow_print("• Hiển thị đáp ứng tần số")
    slow_print("• Phân tích tín hiệu trước và sau lọc")

    print("\n" + "=" * 85)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. IIR là gì?")
    print("   IIR = Infinite Impulse Response")

    print("\n2. Đặc điểm IIR:")
    print("   • Đáp ứng nhanh")
    print("   • Hiệu quả tính toán cao")
    print("   • Số hệ số ít hơn FIR")

    print("\n3. Nhược điểm:")
    print("   • Có thể mất ổn định")
    print("   • Pha không tuyến tính")

    print("\n4. Ứng dụng:")
    print("   • Audio Processing")
    print("   • DSP")
    print("   • RF")
    print("   • Viễn thông")
    print("   • Embedded Systems")

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
# THIẾT KẾ IIR FILTER
# =========================================================

def design_iir_filter(sample_rate):

    print("\n=== THIẾT KẾ IIR FILTER ===\n")

    print("1. Low-pass Filter")
    print("2. High-pass Filter")

    filter_choice = input("\nChọn loại filter: ")

    cutoff = input_positive_float(
        "Nhập tần số cắt (Hz): "
    )

    order = int(
        input_positive_float(
            "Nhập bậc filter: "
        )
    )

    nyquist = 0.5 * sample_rate

    normalized_cutoff = cutoff / nyquist

    # =====================================================
    # LOW PASS
    # =====================================================

    if filter_choice == "1":

        b, a = butter(
            order,
            normalized_cutoff,
            btype="low"
        )

        filter_name = "LOW-PASS"

    # =====================================================
    # HIGH PASS
    # =====================================================

    elif filter_choice == "2":

        b, a = butter(
            order,
            normalized_cutoff,
            btype="high"
        )

        filter_name = "HIGH-PASS"

    else:

        print("\n❌ Lựa chọn không hợp lệ.")
        return None

    return (
        b,
        a,
        filter_name,
        cutoff,
        order
    )

# =========================================================
# LỌC TÍN HIỆU
# =========================================================

def apply_iir_filter(signal, b, a):

    filtered = lfilter(
        b,
        a,
        signal
    )

    return filtered

# =========================================================
# HIỂN THỊ THÔNG TIN
# =========================================================

def show_info(filter_name, cutoff, order):

    print("\n" + "=" * 85)
    print("                 THÔNG TIN IIR FILTER")
    print("=" * 85)

    print(f"\nLoại filter:")
    print(f"→ {filter_name}")

    print(f"\nTần số cắt:")
    print(f"→ {cutoff:.2f} Hz")

    print(f"\nBậc filter:")
    print(f"→ {order}")

    print("\nĐánh giá:")

    if order <= 2:

        print("→ Filter đơn giản")

    elif order <= 6:

        print("→ Filter trung bình")

    else:

        print("→ Filter sắc nét")

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

    plt.title("Tín hiệu nhiễu")

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

    plt.title("Tín hiệu sau IIR Filter")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# ĐÁP ỨNG TẦN SỐ
# =========================================================

def plot_frequency_response(b, a):

    w, h = freqz(b, a)

    plt.figure(figsize=(12, 5))

    plt.plot(
        w / np.pi,
        np.abs(h),
        linewidth=2
    )

    plt.title("Đáp ứng tần số IIR Filter")

    plt.xlabel("Tần số chuẩn hóa")

    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# MENU IIR
# =========================================================

def iir_menu():

    (
        t,
        original_signal,
        noisy_signal,
        sample_rate
    ) = create_signal()

    filter_result = design_iir_filter(
        sample_rate
    )

    if filter_result is None:

        return

    (
        b,
        a,
        filter_name,
        cutoff,
        order
    ) = filter_result

    print("\nĐang lọc tín hiệu bằng IIR...")

    filtered_signal = apply_iir_filter(
        noisy_signal,
        b,
        a
    )

    show_info(
        filter_name,
        cutoff,
        order
    )

    plot_signals(
        t,
        original_signal,
        noisy_signal,
        filtered_signal
    )

    plot_frequency_response(b, a)

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 85)
        print("                    MENU CHỨC NĂNG")
        print("=" * 85)

        print("1. Mô phỏng IIR Filter")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            iir_menu()

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
