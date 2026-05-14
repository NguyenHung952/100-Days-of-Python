# =========================================================
#            PWM SIGNAL GENERATOR SIMULATOR
# =========================================================
#
# Chủ đề:
#   Bộ tạo sóng PWM giả lập bằng Python
#
# Chức năng:
#   • Tạo tín hiệu PWM
#   • Điều chỉnh:
#       - Tần số
#       - Duty cycle
#       - Điện áp mức HIGH
#       - Thời gian mô phỏng
#   • Vẽ đồ thị PWM
#   • Hiển thị thông tin tín hiệu
#   • Giả lập điều khiển LED / Motor
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded / Arduino
#   • Vi điều khiển STM32 / ESP32
#
# Thư viện cần:
#   pip install matplotlib numpy
#
# =========================================================

import numpy as np
import matplotlib.pyplot as plt
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
    print("              PWM SIGNAL GENERATOR SIMULATOR")
    print("=" * 75)

    slow_print("\nXin chào! Đây là chương trình mô phỏng PWM.")
    slow_print("Các chức năng chính:")
    slow_print("• Tạo tín hiệu PWM")
    slow_print("• Điều chỉnh Duty Cycle")
    slow_print("• Điều chỉnh tần số")
    slow_print("• Vẽ đồ thị dạng sóng")
    slow_print("• Phân tích tín hiệu PWM")
    slow_print("• Mô phỏng điều khiển LED / Motor")

    print("\n" + "=" * 75)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. PWM là gì?")
    print("   PWM = Pulse Width Modulation")
    print("   Điều chế độ rộng xung")

    print("\n2. Duty Cycle:")
    print("   Duty = Ton / T × 100%")

    print("\n3. Ứng dụng:")
    print("   • Điều khiển độ sáng LED")
    print("   • Điều khiển tốc độ motor")
    print("   • Điều khiển servo")
    print("   • Nguồn switching")
    print("   • STM32 / Arduino / ESP32")

    print("\n4. Ý nghĩa:")
    print("   Duty càng lớn → công suất càng cao")

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
# THÔNG TIN PWM
# =========================================================

def pwm_info(freq, duty, voltage):

    period = 1 / freq

    ton = period * (duty / 100)

    toff = period - ton

    print("\n" + "=" * 75)
    print("                   THÔNG TIN PWM")
    print("=" * 75)

    print(f"\nTần số PWM      : {freq:.2f} Hz")
    print(f"Chu kỳ T        : {period:.6f} s")
    print(f"Duty Cycle      : {duty:.2f} %")

    print(f"\nThời gian ON    : {ton:.6f} s")
    print(f"Thời gian OFF   : {toff:.6f} s")

    print(f"\nĐiện áp HIGH    : {voltage:.2f} V")

    avg_voltage = voltage * (duty / 100)

    print(f"Điện áp trung bình:")
    print(f"→ {avg_voltage:.2f} V")

# =========================================================
# TẠO PWM
# =========================================================

def generate_pwm():

    print("\n=== TẠO TÍN HIỆU PWM ===\n")

    frequency = input_positive_float(
        "Nhập tần số PWM (Hz): "
    )

    while True:

        duty_cycle = float(
            input("Nhập Duty Cycle (%): ")
        )

        if 0 <= duty_cycle <= 100:
            break

        print("❌ Duty phải từ 0 → 100.")

    high_voltage = input_positive_float(
        "Nhập điện áp HIGH (V): "
    )

    duration = input_positive_float(
        "Nhập thời gian mô phỏng (s): "
    )

    pwm_info(frequency, duty_cycle, high_voltage)

    print("\nĐang tạo tín hiệu PWM...")

    # =====================================================
    # TẠO DỮ LIỆU
    # =====================================================

    sampling_rate = 100000

    t = np.linspace(
        0,
        duration,
        int(sampling_rate * duration)
    )

    period = 1 / frequency

    pwm_signal = np.where(
        (t % period) < (duty_cycle / 100) * period,
        high_voltage,
        0
    )

    # =====================================================
    # PHÂN TÍCH LED
    # =====================================================

    print("\n" + "=" * 75)
    print("                MÔ PHỎNG ĐỘ SÁNG LED")
    print("=" * 75)

    if duty_cycle == 0:
        brightness = "LED TẮT"

    elif duty_cycle < 25:
        brightness = "LED SÁNG YẾU"

    elif duty_cycle < 50:
        brightness = "LED SÁNG TRUNG BÌNH"

    elif duty_cycle < 75:
        brightness = "LED SÁNG MẠNH"

    else:
        brightness = "LED SÁNG TỐI ĐA"

    print(f"\nDuty Cycle: {duty_cycle:.2f}%")
    print(f"Trạng thái: {brightness}")

    # =====================================================
    # BẢNG DỮ LIỆU
    # =====================================================

    print("\n" + "=" * 75)
    print("                  BẢNG DỮ LIỆU PWM")
    print("=" * 75)

    print(f"\n{'Thời gian (s)':<20}{'Điện áp (V)':<20}")

    step = len(t) // 20

    for i in range(0, len(t), step):

        print(
            f"{t[i]:<20.6f}"
            f"{pwm_signal[i]:<20.2f}"
        )

    # =====================================================
    # VẼ ĐỒ THỊ
    # =====================================================

    plt.figure(figsize=(12, 5))

    plt.plot(
        t,
        pwm_signal,
        linewidth=2
    )

    plt.title("Mô phỏng tín hiệu PWM")

    plt.xlabel("Thời gian (s)")
    plt.ylabel("Điện áp (V)")

    plt.ylim(-0.5, high_voltage + 1)

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

        print("1. Tạo tín hiệu PWM")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            generate_pwm()

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
