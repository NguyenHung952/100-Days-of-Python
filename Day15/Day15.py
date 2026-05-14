# =========================================================
#           AUDIO FREQUENCY SPECTRUM ANALYZER
# =========================================================
#
# Chủ đề:
#   Hiển thị phổ tần số âm thanh
#
# Chức năng:
#   • Thu âm từ microphone
#   • Phân tích FFT thời gian thực
#   • Hiển thị phổ tần số âm thanh
#   • Hiển thị waveform tín hiệu
#   • Phát hiện tần số mạnh nhất
#   • Hiển thị mức âm lượng
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • DSP / Audio Processing
#   • IoT / Embedded
#   • Machine Learning Audio
#
# Thư viện cần:
#   pip install numpy matplotlib sounddevice
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
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
    print("            AUDIO FREQUENCY SPECTRUM ANALYZER")
    print("=" * 85)

    slow_print("\nXin chào! Đây là chương trình phân tích âm thanh.")
    slow_print("Các chức năng chính:")
    slow_print("• Thu âm microphone")
    slow_print("• Phân tích FFT thời gian thực")
    slow_print("• Hiển thị waveform")
    slow_print("• Hiển thị phổ tần số")
    slow_print("• Phát hiện tần số mạnh nhất")
    slow_print("• Đo mức âm lượng tín hiệu")

    print("\n" + "=" * 85)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. FFT:")
    print("   FFT = Fast Fourier Transform")

    print("\n2. Chức năng:")
    print("   • Chuyển tín hiệu từ miền thời gian")
    print("     sang miền tần số")

    print("\n3. Ứng dụng:")
    print("   • DSP")
    print("   • Audio Processing")
    print("   • Voice Recognition")
    print("   • RF")
    print("   • Viễn thông")

    print("\n4. Dải tần âm thanh:")
    print("   • Tai người: 20Hz → 20kHz")

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
# GHI ÂM
# =========================================================

def record_audio(duration, sample_rate):

    print("\n🎤 Đang ghi âm...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float64"
    )

    sd.wait()

    print("✅ Hoàn tất ghi âm.")

    return audio.flatten()

# =========================================================
# FFT
# =========================================================

def analyze_fft(signal, sample_rate):

    n = len(signal)

    fft_result = np.fft.fft(signal)

    fft_freq = np.fft.fftfreq(
        n,
        d=1 / sample_rate
    )

    magnitude = np.abs(fft_result) / n

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
# MỨC ÂM LƯỢNG
# =========================================================

def calculate_volume(signal):

    rms = np.sqrt(np.mean(signal**2))

    return rms

# =========================================================
# HIỂN THỊ THÔNG TIN
# =========================================================

def show_info(main_freq, volume):

    print("\n" + "=" * 85)
    print("                  KẾT QUẢ PHÂN TÍCH")
    print("=" * 85)

    print(f"\nTần số mạnh nhất:")
    print(f"→ {main_freq:.2f} Hz")

    print(f"\nMức âm lượng RMS:")
    print(f"→ {volume:.5f}")

    print("\nĐánh giá:")

    if volume < 0.01:

        print("→ Âm lượng thấp")

    elif volume < 0.1:

        print("→ Âm lượng trung bình")

    else:

        print("→ Âm lượng lớn")

# =========================================================
# VẼ ĐỒ THỊ
# =========================================================

def plot_graphs(signal, sample_rate, freqs, magnitudes):

    time_axis = np.linspace(
        0,
        len(signal) / sample_rate,
        len(signal)
    )

    # =====================================================
    # WAVEFORM
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        time_axis,
        signal,
        linewidth=1
    )

    plt.title("Waveform âm thanh")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

    # =====================================================
    # FFT SPECTRUM
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        freqs,
        magnitudes,
        linewidth=1.5
    )

    plt.title("Phổ tần số âm thanh (FFT)")

    plt.xlabel("Tần số (Hz)")
    plt.ylabel("Biên độ phổ")

    plt.xlim(0, 5000)

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =========================================================
# MENU PHÂN TÍCH
# =========================================================

def spectrum_analyzer():

    print("\n=== PHÂN TÍCH ÂM THANH ===\n")

    duration = input_positive_float(
        "Nhập thời gian ghi âm (s): "
    )

    sample_rate = int(
        input_positive_float(
            "Nhập tần số lấy mẫu (Hz): "
        )
    )

    signal = record_audio(
        duration,
        sample_rate
    )

    print("\nĐang phân tích FFT...")

    freqs, magnitudes = analyze_fft(
        signal,
        sample_rate
    )

    main_freq = detect_main_frequency(
        freqs,
        magnitudes
    )

    volume = calculate_volume(signal)

    show_info(main_freq, volume)

    plot_graphs(
        signal,
        sample_rate,
        freqs,
        magnitudes
    )

# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 85)
        print("                    MENU CHỨC NĂNG")
        print("=" * 85)

        print("1. Hiển thị phổ tần số âm thanh")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            spectrum_analyzer()

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
