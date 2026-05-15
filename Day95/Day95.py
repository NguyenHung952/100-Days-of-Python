# =========================================================
#            DSP SOLVER SYSTEM WITH PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Giải bài toán DSP bằng Python
#
# Chức năng:
#   ✓ Generate sine wave
#   ✓ Generate cosine wave
#   ✓ FFT Spectrum Analysis
#   ✓ Signal Filtering
#   ✓ Noise Simulation
#   ✓ Convolution
#   ✓ Moving Average Filter
#   ✓ Sampling Visualization
#   ✓ DSP Theory Learning
#   ✓ ASCII Signal Viewer
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
# python dsp_solver.py
#
# =========================================================

from colorama import Fore, Style, init

import numpy as np
import pandas as pd

from scipy import signal

import matplotlib.pyplot as plt

import json
import os
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "dsp_history.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "history": []
}

# =========================================================
# LOAD DATA
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
# SAVE DATA
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

    title("GIỚI THIỆU DSP SOLVER")

    print(Fore.WHITE + """
DSP Solver giúp:

   ✓ Xử lý tín hiệu số
   ✓ Phân tích FFT
   ✓ Mô phỏng filter
   ✓ Học DSP trực quan

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Sine Wave Generator
✓ FFT Spectrum
✓ Noise Filtering
✓ Signal Processing
✓ Convolution

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Audio Processing
✓ Communication Systems
✓ Radar Systems
✓ Embedded DSP
✓ AI Signal Analysis

=========================================================
THƯ VIỆN SỬ DỤNG
=========================================================

✓ NumPy
✓ SciPy
✓ Matplotlib
""")

    line()


# =========================================================
# SINE WAVE GENERATOR
# =========================================================

def sine_wave():

    clear()

    title("SINE WAVE GENERATOR")

    try:

        freq = float(input(
            Fore.YELLOW +
            "Frequency (Hz): "
        ))

        sample_rate = 1000

        duration = 1

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    t = np.linspace(
        0,
        duration,
        sample_rate
    )

    signal_wave = np.sin(
        2 * np.pi * freq * t
    )

    plt.figure(figsize=(10, 4))

    plt.plot(t, signal_wave)

    plt.title("Sine Wave")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        f"Sine Wave {freq}Hz"
    )

    save_data()

    pause()


# =========================================================
# COSINE WAVE
# =========================================================

def cosine_wave():

    clear()

    title("COSINE WAVE GENERATOR")

    try:

        freq = float(input(
            Fore.YELLOW +
            "Frequency (Hz): "
        ))

        sample_rate = 1000

        duration = 1

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    t = np.linspace(
        0,
        duration,
        sample_rate
    )

    signal_wave = np.cos(
        2 * np.pi * freq * t
    )

    plt.figure(figsize=(10, 4))

    plt.plot(t, signal_wave)

    plt.title("Cosine Wave")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        f"Cosine Wave {freq}Hz"
    )

    save_data()

    pause()


# =========================================================
# FFT ANALYSIS
# =========================================================

def fft_analysis():

    clear()

    title("FFT SPECTRUM ANALYSIS")

    sample_rate = 1000

    t = np.linspace(
        0,
        1,
        sample_rate
    )

    signal_wave = (

        np.sin(2 * np.pi * 50 * t)

        +

        0.5 * np.sin(
            2 * np.pi * 120 * t
        )
    )

    fft_result = np.fft.fft(
        signal_wave
    )

    frequencies = np.fft.fftfreq(
        len(signal_wave),
        1 / sample_rate
    )

    magnitude = np.abs(
        fft_result
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        frequencies[:500],
        magnitude[:500]
    )

    plt.title("FFT Spectrum")

    plt.xlabel("Frequency (Hz)")

    plt.ylabel("Magnitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "FFT Analysis"
    )

    save_data()

    pause()


# =========================================================
# NOISE SIMULATION
# =========================================================

def noise_simulation():

    clear()

    title("NOISE SIMULATION")

    sample_rate = 1000

    t = np.linspace(
        0,
        1,
        sample_rate
    )

    clean_signal = np.sin(
        2 * np.pi * 10 * t
    )

    noise = np.random.normal(
        0,
        0.5,
        sample_rate
    )

    noisy_signal = clean_signal + noise

    plt.figure(figsize=(10, 4))

    plt.plot(
        t,
        noisy_signal
    )

    plt.title("Noisy Signal")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "Noise Simulation"
    )

    save_data()

    pause()


# =========================================================
# MOVING AVERAGE FILTER
# =========================================================

def moving_average_filter():

    clear()

    title("MOVING AVERAGE FILTER")

    sample_rate = 1000

    t = np.linspace(
        0,
        1,
        sample_rate
    )

    signal_wave = np.sin(
        2 * np.pi * 10 * t
    )

    noise = np.random.normal(
        0,
        0.5,
        sample_rate
    )

    noisy = signal_wave + noise

    kernel_size = 10

    kernel = np.ones(
        kernel_size
    ) / kernel_size

    filtered = np.convolve(
        noisy,
        kernel,
        mode='same'
    )

    plt.figure(figsize=(10, 4))

    plt.plot(t, noisy,
             label="Noisy")

    plt.plot(t, filtered,
             label="Filtered")

    plt.legend()

    plt.title(
        "Moving Average Filter"
    )

    plt.grid()

    plt.show()

    data["history"].append(
        "Moving Average Filter"
    )

    save_data()

    pause()


# =========================================================
# CONVOLUTION
# =========================================================

def convolution_demo():

    clear()

    title("CONVOLUTION DEMO")

    x = np.array([1, 2, 3])

    h = np.array([0, 1, 0.5])

    y = np.convolve(x, h)

    print(Fore.GREEN +
          f"\nInput x[n]: {x}")

    print(Fore.CYAN +
          f"Impulse h[n]: {h}")

    print(Fore.YELLOW +
          f"Output y[n]: {y}")

    data["history"].append(
        "Convolution"
    )

    save_data()

    pause()


# =========================================================
# LOWPASS FILTER
# =========================================================

def lowpass_filter():

    clear()

    title("LOWPASS FILTER")

    fs = 1000

    t = np.linspace(
        0,
        1,
        fs
    )

    signal_wave = (

        np.sin(2 * np.pi * 10 * t)

        +

        np.sin(2 * np.pi * 100 * t)
    )

    b, a = signal.butter(
        4,
        20 / (fs / 2),
        btype='low'
    )

    filtered = signal.filtfilt(
        b,
        a,
        signal_wave
    )

    plt.figure(figsize=(10, 4))

    plt.plot(t, signal_wave,
             label="Original")

    plt.plot(t, filtered,
             label="Filtered")

    plt.legend()

    plt.title("Lowpass Filter")

    plt.grid()

    plt.show()

    data["history"].append(
        "Lowpass Filter"
    )

    save_data()

    pause()


# =========================================================
# ASCII SIGNAL VISUALIZER
# =========================================================

def ascii_visualizer():

    clear()

    title("ASCII SIGNAL VISUALIZER")

    signal_data = np.sin(
        np.linspace(0, 10, 60)
    )

    for value in signal_data:

        position = int(
            (value + 1) * 20
        )

        print(
            " " * position +
            Fore.GREEN + "*"
        )

        time.sleep(0.03)

    data["history"].append(
        "ASCII Signal"
    )

    save_data()

    pause()


# =========================================================
# VIEW HISTORY
# =========================================================

def history():

    clear()

    title("DSP HISTORY")

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
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    try:

        df = pd.DataFrame({

            "DSP Operations":
            data["history"]
        })

        filename = "dsp_history.csv"

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

    title("DEMO DSP SYSTEM")

    print(Fore.WHITE + """
DSP Algorithms Demo:

=========================================================
SIGNAL GENERATION
=========================================================

✓ Sine Wave
✓ Cosine Wave

=========================================================
FREQUENCY ANALYSIS
=========================================================

✓ FFT Spectrum

=========================================================
FILTERING
=========================================================

✓ Lowpass Filter
✓ Moving Average

=========================================================
SIGNAL PROCESSING
=========================================================

✓ Noise Simulation
✓ Convolution
""")

    pause()


# =========================================================
# EXPLAIN DSP
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH DSP")

    print(Fore.WHITE + """
=========================================================
1. DSP
=========================================================

DSP:
   Digital Signal Processing

=========================================================
2. FFT
=========================================================

FFT:
   Fast Fourier Transform

=========================================================
3. FILTER
=========================================================

Lọc tín hiệu:
   ✓ Lowpass
   ✓ Highpass

=========================================================
4. SIGNAL
=========================================================

Tín hiệu:
   ✓ Audio
   ✓ RF
   ✓ Radar

=========================================================
5. CONVOLUTION
=========================================================

DSP Operation:
   ✓ Signal Filtering

=========================================================
6. NOISE
=========================================================

Nhiễu:
   ✓ Gaussian Noise

=========================================================
7. EMBEDDED DSP
=========================================================

Ứng dụng:
   ✓ STM32
   ✓ FPGA DSP

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ AI Audio
✓ Communication
✓ Radar Systems
✓ Biomedical DSP
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("DSP SOLVER SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu DSP
[2] Generate Sine Wave
[3] Generate Cosine Wave
[4] FFT Spectrum Analysis
[5] Noise Simulation
[6] Moving Average Filter
[7] Convolution Demo
[8] Lowpass Filter
[9] ASCII Signal Viewer
[10] View DSP History
[11] Export CSV Report
[12] Demo mode
[13] Giải thích DSP
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

            sine_wave()

        elif choice == '3':

            cosine_wave()

        elif choice == '4':

            fft_analysis()

        elif choice == '5':

            noise_simulation()

        elif choice == '6':

            moving_average_filter()

        elif choice == '7':

            convolution_demo()

        elif choice == '8':

            lowpass_filter()

        elif choice == '9':

            ascii_visualizer()

        elif choice == '10':

            history()

        elif choice == '11':

            export_csv()

        elif choice == '12':

            demo_mode()

        elif choice == '13':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng DSP Solver.

Kiến thức đạt được:
   ✓ FFT Analysis
   ✓ Signal Filtering
   ✓ DSP Algorithms
   ✓ Signal Processing
   ✓ Frequency Spectrum
   ✓ Embedded DSP
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
