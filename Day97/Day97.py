# =========================================================
#         DIGITAL MODULATION SIMULATOR SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mô phỏng điều chế ASK / FSK / PSK
#
# Chức năng:
#   ✓ ASK Modulation
#   ✓ FSK Modulation
#   ✓ BPSK Modulation
#   ✓ Digital Signal Generator
#   ✓ Carrier Signal Visualization
#   ✓ Modulated Waveform Viewer
#   ✓ Noise Simulation
#   ✓ FFT Spectrum Analysis
#   ✓ ASCII Signal Viewer
#   ✓ Export Report CSV
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install numpy matplotlib scipy pandas colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python digital_modulation.py
#
# =========================================================

from colorama import Fore, Style, init

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq

import random
import time
import os
import json

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "modulation_history.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "history": []
}

# =========================================================
# LOAD DATABASE
# =========================================================

def load_data():

    global data

    if os.path.exists(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except:

            pass


# =========================================================
# SAVE DATABASE
# =========================================================

def save_data():

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# UI FUNCTIONS
# =========================================================

def clear():

    os.system(
        "cls" if os.name == "nt"
        else "clear"
    )


def line():

    print(Fore.CYAN + "=" * 100)


def title(text):

    line()

    print(
        Fore.GREEN +
        Style.BRIGHT +
        text.center(100)
    )

    line()


def pause():

    input(
        Fore.YELLOW +
        "\nNhấn ENTER để tiếp tục..."
    )


# =========================================================
# INTRODUCTION
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU DIGITAL MODULATION")

    print(Fore.WHITE + """
Digital Modulation Simulator giúp:

   ✓ Mô phỏng điều chế số
   ✓ Hiểu ASK / FSK / PSK
   ✓ Visualize waveform
   ✓ Học truyền thông số trực quan

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ ASK Modulation
✓ FSK Modulation
✓ BPSK Modulation
✓ FFT Spectrum
✓ Signal Visualization

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Wireless Communication
✓ SDR Systems
✓ Satellite Systems
✓ RF Engineering
✓ IoT Communication

=========================================================
COMMUNICATION CONCEPTS
=========================================================

✓ Carrier Wave
✓ Frequency
✓ Amplitude
✓ Phase
✓ Noise
""")

    line()


# =========================================================
# GENERATE DIGITAL DATA
# =========================================================

def generate_bits():

    clear()

    title("DIGITAL BIT GENERATOR")

    try:

        n = int(input(
            Fore.YELLOW +
            "Số lượng bits: "
        ))

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    bits = np.random.randint(
        0,
        2,
        n
    )

    print(Fore.GREEN +
          "\nGenerated Bits:\n")

    print(bits)

    data["history"].append(
        f"Generated {n} bits"
    )

    save_data()

    pause()


# =========================================================
# ASK MODULATION
# =========================================================

def ask_modulation():

    clear()

    title("ASK MODULATION")

    bits = np.random.randint(
        0,
        2,
        10
    )

    bit_duration = 100

    carrier_freq = 5

    t = np.linspace(
        0,
        1,
        bit_duration
    )

    signal_wave = np.array([])

    for bit in bits:

        if bit == 1:

            carrier = np.sin(
                2 * np.pi *
                carrier_freq * t
            )

        else:

            carrier = np.zeros(
                len(t)
            )

        signal_wave = np.concatenate(

            (signal_wave, carrier)
        )

    plt.figure(figsize=(12, 4))

    plt.plot(signal_wave)

    plt.title("ASK Modulation")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    print(Fore.GREEN +
          "\nBits:")

    print(bits)

    data["history"].append(
        "ASK Modulation"
    )

    save_data()

    pause()


# =========================================================
# FSK MODULATION
# =========================================================

def fsk_modulation():

    clear()

    title("FSK MODULATION")

    bits = np.random.randint(
        0,
        2,
        10
    )

    bit_duration = 100

    t = np.linspace(
        0,
        1,
        bit_duration
    )

    signal_wave = np.array([])

    for bit in bits:

        if bit == 1:

            freq = 10

        else:

            freq = 3

        carrier = np.sin(
            2 * np.pi *
            freq * t
        )

        signal_wave = np.concatenate(

            (signal_wave, carrier)
        )

    plt.figure(figsize=(12, 4))

    plt.plot(signal_wave)

    plt.title("FSK Modulation")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    print(Fore.GREEN +
          "\nBits:")

    print(bits)

    data["history"].append(
        "FSK Modulation"
    )

    save_data()

    pause()


# =========================================================
# BPSK MODULATION
# =========================================================

def psk_modulation():

    clear()

    title("BPSK MODULATION")

    bits = np.random.randint(
        0,
        2,
        10
    )

    bit_duration = 100

    carrier_freq = 5

    t = np.linspace(
        0,
        1,
        bit_duration
    )

    signal_wave = np.array([])

    for bit in bits:

        if bit == 1:

            phase = 0

        else:

            phase = np.pi

        carrier = np.sin(
            2 * np.pi *
            carrier_freq * t
            + phase
        )

        signal_wave = np.concatenate(

            (signal_wave, carrier)
        )

    plt.figure(figsize=(12, 4))

    plt.plot(signal_wave)

    plt.title("BPSK Modulation")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    print(Fore.GREEN +
          "\nBits:")

    print(bits)

    data["history"].append(
        "BPSK Modulation"
    )

    save_data()

    pause()


# =========================================================
# NOISE SIMULATION
# =========================================================

def noise_simulation():

    clear()

    title("NOISE SIMULATION")

    t = np.linspace(
        0,
        1,
        1000
    )

    clean_signal = np.sin(
        2 * np.pi * 5 * t
    )

    noise = np.random.normal(
        0,
        0.5,
        1000
    )

    noisy_signal = clean_signal + noise

    plt.figure(figsize=(10, 4))

    plt.plot(
        noisy_signal
    )

    plt.title(
        "Signal with Noise"
    )

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "Noise Simulation"
    )

    save_data()

    pause()


# =========================================================
# FFT SPECTRUM ANALYSIS
# =========================================================

def fft_analysis():

    clear()

    title("FFT SPECTRUM ANALYSIS")

    fs = 1000

    t = np.linspace(
        0,
        1,
        fs
    )

    signal_wave = (

        np.sin(2 * np.pi * 10 * t)

        +

        0.5 * np.sin(
            2 * np.pi * 50 * t
        )
    )

    yf = fft(signal_wave)

    xf = fftfreq(fs, 1/fs)

    plt.figure(figsize=(10, 4))

    plt.plot(
        xf[:500],
        np.abs(yf[:500])
    )

    plt.title("FFT Spectrum")

    plt.xlabel("Frequency")

    plt.ylabel("Magnitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "FFT Analysis"
    )

    save_data()

    pause()


# =========================================================
# ASCII SIGNAL VIEWER
# =========================================================

def ascii_signal():

    clear()

    title("ASCII DIGITAL SIGNAL")

    bits = np.random.randint(
        0,
        2,
        50
    )

    print(Fore.GREEN +
          "\nDigital Signal:\n")

    for bit in bits:

        if bit == 1:

            print(Fore.GREEN +
                  "‾‾", end="")

        else:

            print(Fore.RED +
                  "__", end="")

        time.sleep(0.03)

    print()

    data["history"].append(
        "ASCII Signal"
    )

    save_data()

    pause()


# =========================================================
# CONSTELLATION DIAGRAM
# =========================================================

def constellation_diagram():

    clear()

    title("BPSK CONSTELLATION DIAGRAM")

    symbols = np.array([
        -1,
        1
    ])

    noise = np.random.normal(
        0,
        0.2,
        100
    )

    received = np.random.choice(
        symbols,
        100
    ) + noise

    plt.figure(figsize=(5, 5))

    plt.scatter(
        received,
        np.zeros_like(received)
    )

    plt.title(
        "BPSK Constellation"
    )

    plt.xlabel("In-phase")

    plt.grid()

    plt.show()

    data["history"].append(
        "Constellation Diagram"
    )

    save_data()

    pause()


# =========================================================
# MODULATION COMPARISON
# =========================================================

def compare_modulation():

    clear()

    title("MODULATION COMPARISON")

    print(Fore.WHITE + """
=========================================================
ASK
=========================================================

✓ Điều chế biên độ
✓ Dễ triển khai
✗ Nhạy noise

=========================================================
FSK
=========================================================

✓ Điều chế tần số
✓ Chống noise tốt
✗ Băng thông lớn

=========================================================
PSK
=========================================================

✓ Điều chế pha
✓ Hiệu quả cao
✓ Dùng nhiều trong 5G/WiFi
""")

    data["history"].append(
        "Modulation Comparison"
    )

    save_data()

    pause()


# =========================================================
# VIEW HISTORY
# =========================================================

def history():

    clear()

    title("MODULATION HISTORY")

    if not data["history"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

        pause()

        return

    for index, item in enumerate(
        data["history"],
        start=1
    ):

        print(Fore.GREEN +
              f"[{index}] {item}")

    pause()


# =========================================================
# EXPORT CSV REPORT
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    try:

        df = pd.DataFrame({

            "Operations":
            data["history"]
        })

        filename = "modulation_report.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO DIGITAL MODULATION")

    print(Fore.WHITE + """
Communication Demo:

=========================================================
DIGITAL MODULATION
=========================================================

✓ ASK
✓ FSK
✓ BPSK

=========================================================
SIGNAL PROCESSING
=========================================================

✓ FFT Spectrum
✓ Carrier Signal

=========================================================
WIRELESS SYSTEMS
=========================================================

✓ RF Communication
✓ SDR Systems
✓ IoT Wireless
""")

    pause()


# =========================================================
# EXPLAIN MODULATION
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH DIGITAL MODULATION")

    print(Fore.WHITE + """
=========================================================
1. ASK
=========================================================

ASK:
   Amplitude Shift Keying

=========================================================
2. FSK
=========================================================

FSK:
   Frequency Shift Keying

=========================================================
3. PSK
=========================================================

PSK:
   Phase Shift Keying

=========================================================
4. CARRIER SIGNAL
=========================================================

Carrier:
   ✓ RF Wave
   ✓ Wireless Signal

=========================================================
5. DIGITAL COMMUNICATION
=========================================================

Ứng dụng:
   ✓ WiFi
   ✓ Bluetooth
   ✓ 5G

=========================================================
6. FFT ANALYSIS
=========================================================

Phân tích:
   ✓ Frequency Spectrum

=========================================================
7. CONSTELLATION
=========================================================

Visualize:
   ✓ Signal Symbols

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ SDR
✓ Satellite Communication
✓ RF Engineering
✓ Embedded Wireless
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("DIGITAL MODULATION SIMULATOR")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] Generate Digital Bits
[3] ASK Modulation
[4] FSK Modulation
[5] BPSK Modulation
[6] Noise Simulation
[7] FFT Spectrum Analysis
[8] ASCII Signal Viewer
[9] Constellation Diagram
[10] Compare Modulation
[11] View History
[12] Export CSV Report
[13] Demo mode
[14] Giải thích modulation
[0] Thoát
""")

        choice = input(
            Fore.YELLOW +
            "Nhập lựa chọn: "
        )

        if choice == '1':

            intro()

            pause()

        elif choice == '2':

            generate_bits()

        elif choice == '3':

            ask_modulation()

        elif choice == '4':

            fsk_modulation()

        elif choice == '5':

            psk_modulation()

        elif choice == '6':

            noise_simulation()

        elif choice == '7':

            fft_analysis()

        elif choice == '8':

            ascii_signal()

        elif choice == '9':

            constellation_diagram()

        elif choice == '10':

            compare_modulation()

        elif choice == '11':

            history()

        elif choice == '12':

            export_csv()

        elif choice == '13':

            demo_mode()

        elif choice == '14':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Digital Modulation Simulator.

Kiến thức đạt được:
   ✓ ASK / FSK / PSK
   ✓ FFT Spectrum
   ✓ RF Communication
   ✓ Wireless Systems
   ✓ Signal Processing
   ✓ Digital Communication
""")

            break

        else:

            print(Fore.RED +
                  "\nLựa chọn không hợp lệ!")

            time.sleep(1)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    try:

        menu()

    except KeyboardInterrupt:

        print(Fore.RED +
              "\n\nĐã thoát chương trình.")
