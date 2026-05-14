# =========================================================
#              FFT SIGNAL ANALYZER - PYTHON
# =========================================================
#
# Chủ đề:
#   Bộ phân tích tín hiệu bằng FFT
#
# Chức năng:
#   • Tạo tín hiệu sin/cos mẫu
#   • Phân tích phổ tần số bằng FFT
#   • Hiển thị:
#       - Miền thời gian
#       - Miền tần số
#   • Phát hiện tần số chính
#   • Mô phỏng nhiễu tín hiệu
#   • Hỗ trợ học DSP cơ bản
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / Xử lý tín hiệu số
#   • IoT / RF / Truyền thông
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

    print("=" * 80)
    print("                FFT SIGNAL ANALYZER")
    print("=" * 80)

    slow_print("\nXin chào! Đây là chương trình phân tích tín hiệu FFT.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu mẫu")
    slow_print("• Phân tích phổ tần số FFT")
    slow_print("• Vẽ đồ thị miền thời gian")
    slow_print("• Vẽ đồ thị miền tần số")
    slow_print("• Phát hiện tần số tín hiệu")
    slow_print("• Mô phỏng nhiễu tín hiệu")

    print("\n" + "=" * 80)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. FFT là gì?")
    print("   FFT = Fast Fourier Transform")

    print("\n2. Công dụng:")
    print("   • Chuyển tín hiệu từ miền thời gian")
    print("     sang miền tần số")

    print("\n3. Ứng dụng:")
    print("   • DSP")
    print("   • RF")
    print("   • Audio Processing")
    print("   • IoT")
    print("   • Radar")
    print("   • Viễn thông")

    print("\n4. FFT giúp xác định:")
    print("   • Tần số chính")
    print("   • Thành phần nhiễu")
    print("   • Biên độ phổ")

    print("\n" + "=" * 80)

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

    amplitude = input_positive_float(
        "Nhập biên độ tín hiệu: "
    )

    frequency = input_positive_float(
        "Nhập tần số tín hiệu (Hz): "
    )

    sampling_rate = input_positive_float(
        "Nhập tần số lấy mẫu Fs (Hz): "
    )

    duration = input_positive_float(
        "Nhập thời gian mô phỏng (s): "
    )

    noise_level = float(
        input(
            "Nhập mức nhiễu (0 -> 1): "
        )
    )

    # =====================================================
    # TẠO TÍN HIỆU
    # =====================================================

    t = np.linspace(
        0,
        duration,
        int(sampling_rate * duration),
        endpoint=False
    )

    signal = amplitude * np.sin(
        2 * np.pi * frequency * t
    )

    # =====================================================
    # THÊM NHIỄU
    # =====================================================

    noise = noise_level * np.random.randn(len(t))

    noisy_signal = signal + noise

    return (
        t,
        noisy_signal,
        sampling_rate,
        frequency
    )

# =========================================================
# PHÂN TÍCH FFT
# =========================================================

def analyze_fft(signal, sampling_rate):

    n = len(signal)

    fft_result = np.fft.fft(signal)

    fft_freq = np.fft.fftfreq(
        n,
        d=1 / sampling_rate
    )

    magnitude = np.abs(fft_result) / n

    # Chỉ lấy nửa phổ dương
    positive = fft_freq >= 0

    return (
        fft_freq[positive],
        magnitude[positive]
    )

# =========================================================
# PHÁT HIỆN TẦN SỐ CHÍNH
# =========================================================

def detect_main_frequency(freqs, magnitudes):

    index = np.argmax(magnitudes)

    return freqs[index]

# =========================================================
# HIỂN THỊ THÔNG TIN
# =========================================================

def show_info(main_freq):

    print("\n" + "=" * 80)
    print("                 KẾT QUẢ PHÂN TÍCH FFT")
    print("=" * 80)

    print(f"\nTần số phát hiện:")
    print(f"→ {main_freq:.2f} Hz")

    print("\nĐánh giá:")

    if main_freq < 100:
        print("→ Tín hiệu tần số thấp")

    elif main_freq < 10_000:
        print("→ Tín hiệu audio / DSP")

    else:
        print("→ Tín hiệu tần số cao")

# =========================================================
# VẼ ĐỒ THỊ
# =========================================================

def plot_graphs(
    t,
    signal,
    freqs,
    magnitudes
):

    # =====================================================
    # ĐỒ THỊ MIỀN THỜI GIAN
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        t,
        signal,
        linewidth=1.5
    )

    plt.title("Tín hiệu trong miền thời gian")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # ĐỒ THỊ FFT
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        freqs,
        magnitudes,
        linewidth=1.5
    )

    plt.title("Phổ tần số FFT")

    plt.xlabel("Tần số (Hz)")
    plt.ylabel("Biên độ phổ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# PHÂN TÍCH FFT
# =========================================================

def fft_menu():

    (
        t,
        signal,
        sampling_rate,
        original_freq
    ) = create_signal()

    print("\nĐang xử lý FFT...")

    freqs, magnitudes = analyze_fft(
        signal,
        sampling_rate
    )

    detected_freq = detect_main_frequency(
        freqs,
        magnitudes
    )

    show_info(detected_freq)

    print("\nTần số gốc:")
    print(f"→ {original_freq:.2f} Hz")

    print("\nSai số:")
    print(
        f"→ {abs(original_freq - detected_freq):.4f} Hz"
    )

    plot_graphs(
        t,
        signal,
        freqs,
        magnitudes
    )

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 80)
        print("                    MENU CHỨC NĂNG")
        print("=" * 80)

        print("1. Phân tích FFT")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            fft_menu()

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
