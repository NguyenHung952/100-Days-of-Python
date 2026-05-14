# =========================================================
#            SIGNAL NOISE ANALYZER - PYTHON
# =========================================================
#
# Chủ đề:
#   Phân tích nhiễu tín hiệu
#
# Chức năng:
#   • Tạo tín hiệu sạch (Clean Signal)
#   • Mô phỏng nhiễu:
#       - Gaussian Noise
#       - White Noise
#   • Phân tích:
#       - SNR
#       - Công suất tín hiệu
#       - Công suất nhiễu
#   • Hiển thị:
#       - Tín hiệu gốc
#       - Tín hiệu nhiễu
#       - FFT Spectrum
#   • Đánh giá chất lượng tín hiệu
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / RF
#   • Audio Processing
#   • Wireless Communication
#   • IoT
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
    print("                SIGNAL NOISE ANALYZER")
    print("=" * 90)

    slow_print("\nXin chào! Đây là chương trình phân tích nhiễu tín hiệu.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu sạch")
    slow_print("• Mô phỏng nhiễu Gaussian")
    slow_print("• Phân tích SNR")
    slow_print("• Hiển thị FFT Spectrum")
    slow_print("• So sánh tín hiệu trước và sau nhiễu")
    slow_print("• Đánh giá chất lượng tín hiệu")

    print("\n" + "=" * 90)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Noise là gì?")
    print("   • Nhiễu làm méo tín hiệu")

    print("\n2. SNR:")
    print("   SNR = Signal-to-Noise Ratio")

    print("\n3. Công thức:")
    print("   SNR(dB) = 10log10(Psignal / Pnoise)")

    print("\n4. Ý nghĩa:")
    print("   • SNR cao → tín hiệu sạch")
    print("   • SNR thấp → tín hiệu nhiễu mạnh")

    print("\n5. Ứng dụng:")
    print("   • RF")
    print("   • DSP")
    print("   • Audio")
    print("   • Radar")
    print("   • Wireless")
    print("   • IoT")

    print("\n" + "=" * 90)

# FFT và SNR là các kỹ thuật phổ biến trong DSP và phân tích tín hiệu. 

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

    sample_rate = input_positive_float(
        "Nhập tần số lấy mẫu Fs (Hz): "
    )

    duration = input_positive_float(
        "Nhập thời gian mô phỏng (s): "
    )

    noise_level = input_positive_float(
        "Nhập mức nhiễu (0.01 → 1): "
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

    clean_signal = amplitude * np.sin(
        2 * np.pi * frequency * t
    )

    # =====================================================
    # NHIỄU GAUSSIAN
    # =====================================================

    noise = noise_level * np.random.randn(
        len(t)
    )

    noisy_signal = clean_signal + noise

    return (
        t,
        clean_signal,
        noise,
        noisy_signal,
        sample_rate
    )

# =========================================================
# TÍNH CÔNG SUẤT
# =========================================================

def signal_power(signal):

    return np.mean(signal ** 2)

# =========================================================
# TÍNH SNR
# =========================================================

def calculate_snr(clean_signal, noise):

    psignal = signal_power(clean_signal)

    pnoise = signal_power(noise)

    snr = 10 * np.log10(
        psignal / pnoise
    )

    return snr, psignal, pnoise

# =========================================================
# FFT
# =========================================================

def compute_fft(signal, sample_rate):

    n = len(signal)

    fft_result = np.fft.fft(signal)

    freqs = np.fft.fftfreq(
        n,
        d=1/sample_rate
    )

    magnitude = np.abs(fft_result) / n

    positive = freqs >= 0

    return (
        freqs[positive],
        magnitude[positive]
    )

# =========================================================
# ĐÁNH GIÁ SNR
# =========================================================

def evaluate_snr(snr):

    if snr >= 40:

        return "Tín hiệu rất sạch"

    elif snr >= 20:

        return "Tín hiệu tốt"

    elif snr >= 10:

        return "Tín hiệu trung bình"

    else:

        return "Tín hiệu nhiễu mạnh"

# =========================================================
# HIỂN THỊ THÔNG TIN
# =========================================================

def show_info(
    snr,
    psignal,
    pnoise
):

    print("\n" + "=" * 90)
    print("                 KẾT QUẢ PHÂN TÍCH")
    print("=" * 90)

    print(f"\nCông suất tín hiệu:")
    print(f"→ {psignal:.6f}")

    print(f"\nCông suất nhiễu:")
    print(f"→ {pnoise:.6f}")

    print(f"\nSNR:")
    print(f"→ {snr:.2f} dB")

    print(f"\nĐánh giá:")
    print(f"→ {evaluate_snr(snr)}")

# =========================================================
# VẼ TÍN HIỆU
# =========================================================

def plot_signals(
    t,
    clean_signal,
    noisy_signal
):

    # =====================================================
    # CLEAN SIGNAL
    # =====================================================

    plt.figure(figsize=(12, 4))

    plt.plot(
        t,
        clean_signal,
        linewidth=1.5
    )

    plt.title("Tín hiệu sạch")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # NOISY SIGNAL
    # =====================================================

    plt.figure(figsize=(12, 4))

    plt.plot(
        t,
        noisy_signal,
        linewidth=1
    )

    plt.title("Tín hiệu có nhiễu")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# FFT PLOT
# =========================================================

def plot_fft(
    freqs,
    magnitude
):

    plt.figure(figsize=(12, 5))

    plt.plot(
        freqs,
        magnitude,
        linewidth=1.5
    )

    plt.title("FFT Spectrum")

    plt.xlabel("Tần số (Hz)")
    plt.ylabel("Biên độ phổ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# MENU PHÂN TÍCH
# =========================================================

def analyze_noise():

    (
        t,
        clean_signal,
        noise,
        noisy_signal,
        sample_rate
    ) = create_signal()

    print("\nĐang phân tích tín hiệu...")

    snr, psignal, pnoise = calculate_snr(
        clean_signal,
        noise
    )

    show_info(
        snr,
        psignal,
        pnoise
    )

    plot_signals(
        t,
        clean_signal,
        noisy_signal
    )

    freqs, magnitude = compute_fft(
        noisy_signal,
        sample_rate
    )

    plot_fft(
        freqs,
        magnitude
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

        print("1. Phân tích nhiễu tín hiệu")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            analyze_noise()

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
