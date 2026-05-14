# =========================================================
#              ADC SAMPLING SIMULATOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Mô phỏng lấy mẫu ADC
#
# Chức năng:
#   • Tạo tín hiệu analog
#   • Mô phỏng ADC sampling
#   • Điều chỉnh:
#       - Sampling Rate
#       - Độ phân giải ADC
#       - Điện áp tham chiếu
#   • Hiển thị:
#       - Tín hiệu analog
#       - Điểm lấy mẫu ADC
#       - Giá trị số hóa
#   • Phân tích Nyquist
#   • Mô phỏng lượng tử hóa tín hiệu
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
    print("                 ADC SAMPLING SIMULATOR")
    print("=" * 90)

    slow_print("\nXin chào! Đây là chương trình mô phỏng ADC.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu analog")
    slow_print("• Mô phỏng quá trình lấy mẫu ADC")
    slow_print("• Hiển thị tín hiệu số hóa")
    slow_print("• Phân tích Nyquist")
    slow_print("• Mô phỏng lượng tử hóa")
    slow_print("• Hiển thị mã ADC")

    print("\n" + "=" * 90)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. ADC là gì?")
    print("   ADC = Analog to Digital Converter")

    print("\n2. Chức năng:")
    print("   • Chuyển tín hiệu analog")
    print("     thành dữ liệu số")

    print("\n3. Công thức độ phân giải:")
    print("   Resolution = Vref / (2^n)")

    print("\n4. Nyquist:")
    print("   Fs >= 2 × Fsignal")

    print("\n5. Ứng dụng:")
    print("   • ESP32")
    print("   • STM32")
    print("   • Arduino")
    print("   • IoT")
    print("   • DSP")

    print("\n" + "=" * 90)

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
# TẠO TÍN HIỆU ANALOG
# =========================================================

def create_analog_signal():

    print("\n=== TẠO TÍN HIỆU ANALOG ===\n")

    amplitude = input_positive_float(
        "Nhập biên độ tín hiệu (V): "
    )

    frequency = input_positive_float(
        "Nhập tần số tín hiệu (Hz): "
    )

    duration = input_positive_float(
        "Nhập thời gian mô phỏng (s): "
    )

    analog_fs = 100000

    t = np.linspace(
        0,
        duration,
        int(analog_fs * duration)
    )

    signal = amplitude * np.sin(
        2 * np.pi * frequency * t
    )

    return (
        t,
        signal,
        frequency,
        duration
    )

# =========================================================
# ADC SAMPLING
# =========================================================

def adc_sampling(signal_freq, duration):

    print("\n=== CẤU HÌNH ADC ===\n")

    sampling_rate = input_positive_float(
        "Nhập Sampling Rate Fs (Hz): "
    )

    adc_bits = int(
        input_positive_float(
            "Nhập độ phân giải ADC (bit): "
        )
    )

    vref = input_positive_float(
        "Nhập điện áp tham chiếu Vref (V): "
    )

    # =====================================================
    # KIỂM TRA NYQUIST
    # =====================================================

    print("\n" + "=" * 90)
    print("                  PHÂN TÍCH NYQUIST")
    print("=" * 90)

    nyquist = 2 * signal_freq

    print(f"\nTần số tín hiệu:")
    print(f"→ {signal_freq:.2f} Hz")

    print(f"\nTần số Nyquist yêu cầu:")
    print(f"→ {nyquist:.2f} Hz")

    print(f"\nSampling Rate:")
    print(f"→ {sampling_rate:.2f} Hz")

    if sampling_rate >= nyquist:

        print("\n✅ Đạt điều kiện Nyquist")

    else:

        print("\n⚠️ Không đạt Nyquist")
        print("→ Có thể xảy ra aliasing")

    # =====================================================
    # TẠO MẪU ADC
    # =====================================================

    adc_time = np.linspace(
        0,
        duration,
        int(sampling_rate * duration)
    )

    return (
        adc_time,
        sampling_rate,
        adc_bits,
        vref
    )

# =========================================================
# LƯỢNG TỬ HÓA
# =========================================================

def quantize_signal(signal, adc_bits, vref):

    levels = 2 ** adc_bits

    resolution = vref / levels

    shifted = signal + (vref / 2)

    quantized = np.round(
        shifted / resolution
    )

    quantized = np.clip(
        quantized,
        0,
        levels - 1
    )

    return quantized.astype(int), resolution

# =========================================================
# HIỂN THỊ THÔNG TIN ADC
# =========================================================

def show_adc_info(bits, resolution):

    print("\n" + "=" * 90)
    print("                   THÔNG TIN ADC")
    print("=" * 90)

    print(f"\nĐộ phân giải ADC:")
    print(f"→ {bits} bit")

    print(f"\nSố mức lượng tử:")
    print(f"→ {2**bits} levels")

    print(f"\nADC Resolution:")
    print(f"→ {resolution:.6f} V/LSB")

# =========================================================
# HIỂN THỊ MÃ ADC
# =========================================================

def show_adc_codes(adc_values, bits):

    print("\n" + "=" * 90)
    print("                    MÃ ADC")
    print("=" * 90)

    print(
        f"\n{'Sample':<10}"
        f"{'ADC Value':<15}"
        f"{'Binary':<20}"
    )

    limit = min(20, len(adc_values))

    for i in range(limit):

        binary = format(
            adc_values[i],
            f'0{bits}b'
        )

        print(
            f"{i:<10}"
            f"{adc_values[i]:<15}"
            f"{binary:<20}"
        )

# =========================================================
# VẼ ĐỒ THỊ
# =========================================================

def plot_graphs(
    analog_time,
    analog_signal,
    adc_time,
    sampled_signal
):

    # =====================================================
    # ANALOG SIGNAL
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        analog_time,
        analog_signal,
        linewidth=2,
        label="Analog Signal"
    )

    plt.title("Tín hiệu Analog")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ (V)")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()

    # =====================================================
    # ADC SAMPLING
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        analog_time,
        analog_signal,
        linewidth=1.5,
        label="Analog"
    )

    plt.stem(
        adc_time,
        sampled_signal,
        linefmt='r-',
        markerfmt='ro',
        basefmt='k-'
    )

    plt.title("Mô phỏng lấy mẫu ADC")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Biên độ")

    plt.grid(True)

    plt.legend()

    plt.tight_layout()

    plt.show()

# =========================================================
# ADC MENU
# =========================================================

def adc_menu():

    (
        analog_time,
        analog_signal,
        signal_freq,
        duration
    ) = create_analog_signal()

    (
        adc_time,
        sampling_rate,
        adc_bits,
        vref
    ) = adc_sampling(
        signal_freq,
        duration
    )

    print("\nĐang mô phỏng ADC...")

    sampled_signal = np.sin(
        2 * np.pi * signal_freq * adc_time
    )

    adc_values, resolution = quantize_signal(
        sampled_signal,
        adc_bits,
        vref
    )

    show_adc_info(
        adc_bits,
        resolution
    )

    show_adc_codes(
        adc_values,
        adc_bits
    )

    plot_graphs(
        analog_time,
        analog_signal,
        adc_time,
        sampled_signal
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

        print("1. Mô phỏng ADC Sampling")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            adc_menu()

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
