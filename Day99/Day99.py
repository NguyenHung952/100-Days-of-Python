# =========================================================
#              WIFI SDR ANALYZER SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Phân tích tín hiệu WiFi SDR bằng Python
#
# Chức năng:
#   ✓ WiFi Spectrum Analysis
#   ✓ SDR Signal Simulation
#   ✓ FFT Spectrum Visualization
#   ✓ IQ Signal Processing
#   ✓ Waterfall Display
#   ✓ OFDM Signal Demo
#   ✓ Noise Analysis
#   ✓ Channel Power Detection
#   ✓ Constellation Diagram
#   ✓ ASCII RF Viewer
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install numpy scipy matplotlib pandas colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python wifi_sdr_analyzer.py
#
# =========================================================

from colorama import Fore, Style, init

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.fft import fft, fftfreq

import json
import os
import time
import random

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "wifi_sdr_history.json"

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

    title("GIỚI THIỆU WIFI SDR ANALYZER")

    print(Fore.WHITE + """
WiFi SDR Analyzer giúp:

   ✓ Phân tích tín hiệu RF/WiFi
   ✓ Visualize spectrum
   ✓ Học SDR và DSP trực quan
   ✓ Mô phỏng Wireless Systems

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ FFT Spectrum
✓ IQ Signal Processing
✓ Waterfall Display
✓ OFDM Analysis
✓ Constellation Diagram

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ SDR Systems
✓ RF Engineering
✓ WiFi Analysis
✓ Wireless Communication
✓ Spectrum Monitoring

=========================================================
RF CONCEPTS
=========================================================

✓ FFT
✓ IQ Samples
✓ OFDM
✓ Channel Power
✓ Noise Floor
""")

    line()


# =========================================================
# WIFI SIGNAL GENERATOR
# =========================================================

def wifi_signal():

    clear()

    title("WIFI SIGNAL GENERATOR")

    fs = 1000

    t = np.linspace(
        0,
        1,
        fs
    )

    signal_wave = (

        np.sin(2 * np.pi * 50 * t)

        +

        0.5 * np.sin(
            2 * np.pi * 120 * t
        )
    )

    plt.figure(figsize=(10, 4))

    plt.plot(signal_wave)

    plt.title("WiFi RF Signal")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "WiFi Signal"
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

        np.sin(2 * np.pi * 60 * t)

        +

        0.7 * np.sin(
            2 * np.pi * 200 * t
        )
    )

    yf = fft(signal_wave)

    xf = fftfreq(fs, 1/fs)

    plt.figure(figsize=(10, 4))

    plt.plot(
        xf[:500],
        np.abs(yf[:500])
    )

    plt.title("WiFi Spectrum")

    plt.xlabel("Frequency (Hz)")

    plt.ylabel("Magnitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "FFT Spectrum"
    )

    save_data()

    pause()


# =========================================================
# IQ SIGNAL VISUALIZATION
# =========================================================

def iq_visualization():

    clear()

    title("IQ SIGNAL VISUALIZATION")

    samples = 1000

    i_signal = np.cos(
        2 * np.pi * 5 *
        np.linspace(0, 1, samples)
    )

    q_signal = np.sin(
        2 * np.pi * 5 *
        np.linspace(0, 1, samples)
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        i_signal,
        label="I Signal"
    )

    plt.plot(
        q_signal,
        label="Q Signal"
    )

    plt.legend()

    plt.title("IQ Signals")

    plt.grid()

    plt.show()

    data["history"].append(
        "IQ Visualization"
    )

    save_data()

    pause()


# =========================================================
# WATERFALL DISPLAY
# =========================================================

def waterfall_display():

    clear()

    title("WATERFALL DISPLAY")

    spectrum = np.random.rand(
        100,
        100
    )

    plt.figure(figsize=(8, 6))

    plt.imshow(
        spectrum,
        aspect='auto',
        cmap='jet'
    )

    plt.title("RF Waterfall Display")

    plt.xlabel("Frequency")

    plt.ylabel("Time")

    plt.colorbar()

    plt.show()

    data["history"].append(
        "Waterfall Display"
    )

    save_data()

    pause()


# =========================================================
# OFDM SIGNAL DEMO
# =========================================================

def ofdm_demo():

    clear()

    title("OFDM SIGNAL DEMO")

    n_subcarriers = 64

    symbols = np.random.randn(
        n_subcarriers
    ) + 1j * np.random.randn(
        n_subcarriers
    )

    ofdm_signal = np.fft.ifft(
        symbols
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        np.real(ofdm_signal)
    )

    plt.title("OFDM Signal")

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "OFDM Demo"
    )

    save_data()

    pause()


# =========================================================
# NOISE ANALYSIS
# =========================================================

def noise_analysis():

    clear()

    title("NOISE ANALYSIS")

    samples = 1000

    noise = np.random.normal(
        0,
        1,
        samples
    )

    plt.figure(figsize=(10, 4))

    plt.hist(
        noise,
        bins=50
    )

    plt.title("Noise Distribution")

    plt.xlabel("Amplitude")

    plt.ylabel("Count")

    plt.grid()

    plt.show()

    print(Fore.GREEN +
          "\nGaussian Noise Simulation")

    data["history"].append(
        "Noise Analysis"
    )

    save_data()

    pause()


# =========================================================
# CHANNEL POWER DETECTION
# =========================================================

def channel_power():

    clear()

    title("CHANNEL POWER DETECTION")

    signal_power = random.uniform(
        5,
        20
    )

    noise_power = random.uniform(
        0.5,
        3
    )

    snr = signal_power / noise_power

    snr_db = 10 * np.log10(snr)

    print(Fore.GREEN +
          f"\nSignal Power : "
          f"{signal_power:.2f}")

    print(Fore.CYAN +
          f"Noise Power  : "
          f"{noise_power:.2f}")

    print(Fore.YELLOW +
          f"SNR dB       : "
          f"{snr_db:.2f} dB")

    data["history"].append(
        "Channel Power Detection"
    )

    save_data()

    pause()


# =========================================================
# CONSTELLATION DIAGRAM
# =========================================================

def constellation_diagram():

    clear()

    title("CONSTELLATION DIAGRAM")

    symbols = np.array([

        1 + 1j,
        -1 + 1j,
        1 - 1j,
        -1 - 1j
    ])

    noise = (

        np.random.normal(
            0,
            0.2,
            200
        )

        +

        1j * np.random.normal(
            0,
            0.2,
            200
        )
    )

    received = np.random.choice(
        symbols,
        200
    ) + noise

    plt.figure(figsize=(5, 5))

    plt.scatter(
        received.real,
        received.imag
    )

    plt.title("QPSK Constellation")

    plt.xlabel("In-phase")

    plt.ylabel("Quadrature")

    plt.grid()

    plt.show()

    data["history"].append(
        "Constellation Diagram"
    )

    save_data()

    pause()


# =========================================================
# ASCII RF VIEWER
# =========================================================

def ascii_rf_viewer():

    clear()

    title("ASCII RF VIEWER")

    samples = np.random.randint(
        0,
        2,
        60
    )

    print(Fore.GREEN +
          "\nRF Signal Stream:\n")

    for bit in samples:

        if bit == 1:

            print(Fore.GREEN +
                  "‾‾", end="")

        else:

            print(Fore.RED +
                  "__", end="")

        time.sleep(0.03)

    print()

    data["history"].append(
        "ASCII RF Viewer"
    )

    save_data()

    pause()


# =========================================================
# WIFI CHANNEL ANALYSIS
# =========================================================

def wifi_channels():

    clear()

    title("WIFI CHANNEL ANALYSIS")

    channels = {

        1: 2412,
        6: 2437,
        11: 2462
    }

    print(Fore.GREEN +
          "\n2.4GHz WiFi Channels\n")

    for ch, freq in channels.items():

        print(Fore.CYAN +
              f"Channel {ch} "
              f"-> {freq} MHz")

    data["history"].append(
        "WiFi Channel Analysis"
    )

    save_data()

    pause()


# =========================================================
# SDR OVERVIEW
# =========================================================

def sdr_overview():

    clear()

    title("SDR OVERVIEW")

    print(Fore.WHITE + """
=========================================================
SDR HARDWARE
=========================================================

✓ RTL-SDR
✓ HackRF
✓ USRP
✓ LimeSDR

=========================================================
RF ANALYSIS
=========================================================

✓ Spectrum Analysis
✓ IQ Processing
✓ Signal Detection

=========================================================
WIRELESS SYSTEMS
=========================================================

✓ WiFi
✓ Bluetooth
✓ LTE
✓ 5G
""")

    data["history"].append(
        "SDR Overview"
    )

    save_data()

    pause()


# =========================================================
# VIEW HISTORY
# =========================================================

def history():

    clear()

    title("WIFI SDR HISTORY")

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

        filename = "wifi_sdr_report.csv"

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

    title("DEMO WIFI SDR")

    print(Fore.WHITE + """
WiFi SDR Demo:

=========================================================
RF ANALYSIS
=========================================================

✓ FFT Spectrum
✓ IQ Processing
✓ Waterfall Display

=========================================================
WIRELESS SYSTEMS
=========================================================

✓ WiFi
✓ OFDM
✓ QPSK

=========================================================
SDR SYSTEMS
=========================================================

✓ RTL-SDR
✓ HackRF
✓ GNU Radio
""")

    pause()


# =========================================================
# EXPLAIN WIFI SDR
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH WIFI SDR")

    print(Fore.WHITE + """
=========================================================
1. SDR
=========================================================

SDR:
   Software Defined Radio

=========================================================
2. WIFI SIGNAL
=========================================================

WiFi dùng:
   ✓ OFDM
   ✓ QPSK/QAM

=========================================================
3. FFT
=========================================================

FFT:
   ✓ Spectrum Analysis

=========================================================
4. IQ SIGNAL
=========================================================

IQ:
   ✓ In-phase
   ✓ Quadrature

=========================================================
5. WATERFALL DISPLAY
=========================================================

Visualize:
   ✓ Frequency vs Time

=========================================================
6. RF ENGINEERING
=========================================================

Ứng dụng:
   ✓ Wireless
   ✓ SDR
   ✓ RF Design

=========================================================
7. CHANNEL POWER
=========================================================

Đo:
   ✓ SNR
   ✓ Signal Power

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ WiFi Analysis
✓ SDR Research
✓ Embedded RF
✓ Wireless Security
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("WIFI SDR ANALYZER SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] WiFi Signal Generator
[3] FFT Spectrum Analysis
[4] IQ Signal Visualization
[5] Waterfall Display
[6] OFDM Signal Demo
[7] Noise Analysis
[8] Channel Power Detection
[9] Constellation Diagram
[10] ASCII RF Viewer
[11] WiFi Channel Analysis
[12] SDR Overview
[13] View History
[14] Export CSV Report
[15] Demo mode
[16] Giải thích SDR/WiFi
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

            wifi_signal()

        elif choice == '3':

            fft_analysis()

        elif choice == '4':

            iq_visualization()

        elif choice == '5':

            waterfall_display()

        elif choice == '6':

            ofdm_demo()

        elif choice == '7':

            noise_analysis()

        elif choice == '8':

            channel_power()

        elif choice == '9':

            constellation_diagram()

        elif choice == '10':

            ascii_rf_viewer()

        elif choice == '11':

            wifi_channels()

        elif choice == '12':

            sdr_overview()

        elif choice == '13':

            history()

        elif choice == '14':

            export_csv()

        elif choice == '15':

            demo_mode()

        elif choice == '16':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng WiFi SDR Analyzer.

Kiến thức đạt được:
   ✓ SDR Systems
   ✓ WiFi RF Analysis
   ✓ FFT Spectrum
   ✓ IQ Processing
   ✓ OFDM Communication
   ✓ Wireless Engineering
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
