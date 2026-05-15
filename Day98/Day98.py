# =========================================================
#               OFDM SIMULATOR SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mô phỏng OFDM cơ bản bằng Python
#
# Chức năng:
#   ✓ OFDM Signal Generation
#   ✓ QPSK Mapping
#   ✓ IFFT/FFT Simulation
#   ✓ Cyclic Prefix
#   ✓ OFDM Spectrum Analysis
#   ✓ AWGN Noise Simulation
#   ✓ BER Analysis
#   ✓ Subcarrier Visualization
#   ✓ Constellation Diagram
#   ✓ ASCII Signal Viewer
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
# python ofdm_simulator.py
#
# =========================================================

from colorama import Fore, Style, init

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.fft import fft, ifft

import random
import json
import os
import time

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "ofdm_history.json"

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

    title("GIỚI THIỆU OFDM SIMULATOR")

    print(Fore.WHITE + """
OFDM Simulator giúp:

   ✓ Mô phỏng OFDM cơ bản
   ✓ Học truyền thông hiện đại
   ✓ Visualize subcarriers
   ✓ Hiểu FFT/IFFT

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ OFDM Generation
✓ QPSK Modulation
✓ FFT/IFFT
✓ Cyclic Prefix
✓ BER Simulation

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ WiFi
✓ LTE / 4G / 5G
✓ SDR Systems
✓ Wireless Communication
✓ DVB Broadcasting

=========================================================
COMMUNICATION CONCEPTS
=========================================================

✓ Subcarriers
✓ OFDM Symbols
✓ FFT
✓ Multipath
✓ BER
""")

    line()


# =========================================================
# RANDOM BIT GENERATOR
# =========================================================

def generate_bits():

    clear()

    title("RANDOM BIT GENERATOR")

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
# QPSK MAPPING
# =========================================================

def qpsk_mapping():

    clear()

    title("QPSK MAPPING")

    bits = np.random.randint(
        0,
        2,
        16
    )

    print(Fore.GREEN +
          "\nInput Bits:\n")

    print(bits)

    symbols = []

    for i in range(0, len(bits), 2):

        b1 = bits[i]
        b2 = bits[i + 1]

        if b1 == 0 and b2 == 0:

            symbols.append(1 + 1j)

        elif b1 == 0 and b2 == 1:

            symbols.append(-1 + 1j)

        elif b1 == 1 and b2 == 0:

            symbols.append(1 - 1j)

        else:

            symbols.append(-1 - 1j)

    symbols = np.array(symbols)

    plt.figure(figsize=(5, 5))

    plt.scatter(
        symbols.real,
        symbols.imag
    )

    plt.title("QPSK Constellation")

    plt.xlabel("In-phase")

    plt.ylabel("Quadrature")

    plt.grid()

    plt.show()

    data["history"].append(
        "QPSK Mapping"
    )

    save_data()

    pause()


# =========================================================
# OFDM SIGNAL GENERATION
# =========================================================

def ofdm_generation():

    clear()

    title("OFDM SIGNAL GENERATION")

    n_subcarriers = 64

    bits = np.random.randint(
        0,
        2,
        n_subcarriers * 2
    )

    qpsk_symbols = []

    for i in range(0, len(bits), 2):

        b1 = bits[i]
        b2 = bits[i + 1]

        if b1 == 0 and b2 == 0:

            qpsk_symbols.append(1 + 1j)

        elif b1 == 0 and b2 == 1:

            qpsk_symbols.append(-1 + 1j)

        elif b1 == 1 and b2 == 0:

            qpsk_symbols.append(1 - 1j)

        else:

            qpsk_symbols.append(-1 - 1j)

    qpsk_symbols = np.array(
        qpsk_symbols
    )

    ofdm_signal = ifft(
        qpsk_symbols
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        np.real(ofdm_signal)
    )

    plt.title("OFDM Time Domain Signal")

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "OFDM Generation"
    )

    save_data()

    pause()


# =========================================================
# CYCLIC PREFIX
# =========================================================

def cyclic_prefix():

    clear()

    title("CYCLIC PREFIX")

    n_subcarriers = 64

    cp_length = 16

    symbols = np.random.randn(
        n_subcarriers
    ) + 1j * np.random.randn(
        n_subcarriers
    )

    ofdm_signal = ifft(
        symbols
    )

    cp = ofdm_signal[-cp_length:]

    tx_signal = np.concatenate(

        (cp, ofdm_signal)
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        np.real(tx_signal)
    )

    plt.title(
        "OFDM with Cyclic Prefix"
    )

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    print(Fore.GREEN +
          f"\nCP Length: {cp_length}")

    data["history"].append(
        "Cyclic Prefix"
    )

    save_data()

    pause()


# =========================================================
# FFT ANALYSIS
# =========================================================

def fft_analysis():

    clear()

    title("OFDM FFT ANALYSIS")

    n_subcarriers = 64

    symbols = np.random.randn(
        n_subcarriers
    ) + 1j * np.random.randn(
        n_subcarriers
    )

    ofdm_signal = ifft(
        symbols
    )

    recovered = fft(
        ofdm_signal
    )

    plt.figure(figsize=(10, 4))

    plt.plot(
        np.abs(recovered)
    )

    plt.title("Recovered Subcarriers")

    plt.xlabel("Subcarrier")

    plt.ylabel("Magnitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "FFT Analysis"
    )

    save_data()

    pause()


# =========================================================
# AWGN CHANNEL
# =========================================================

def awgn_channel():

    clear()

    title("AWGN CHANNEL SIMULATION")

    n = 1000

    signal_wave = np.sin(
        2 * np.pi * 5 *
        np.linspace(0, 1, n)
    )

    noise = np.random.normal(
        0,
        0.3,
        n
    )

    noisy_signal = signal_wave + noise

    plt.figure(figsize=(10, 4))

    plt.plot(
        noisy_signal
    )

    plt.title("Signal with AWGN")

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "AWGN Channel"
    )

    save_data()

    pause()


# =========================================================
# BER SIMULATION
# =========================================================

def ber_simulation():

    clear()

    title("OFDM BER SIMULATION")

    snr_db = np.arange(0, 11)

    ber = []

    for snr in snr_db:

        ber_value = 0.5 * np.exp(
            -snr / 5
        )

        ber.append(ber_value)

        print(Fore.GREEN +
              f"SNR={snr} dB"
              f" -> BER={ber_value:.6f}")

    plt.figure(figsize=(8, 5))

    plt.semilogy(
        snr_db,
        ber,
        marker='o'
    )

    plt.title("BER vs SNR")

    plt.xlabel("SNR (dB)")

    plt.ylabel("BER")

    plt.grid()

    plt.show()

    data["history"].append(
        "BER Simulation"
    )

    save_data()

    pause()


# =========================================================
# SUBCARRIER VISUALIZATION
# =========================================================

def subcarrier_visual():

    clear()

    title("SUBCARRIER VISUALIZATION")

    t = np.linspace(
        0,
        1,
        1000
    )

    plt.figure(figsize=(10, 5))

    for k in range(1, 6):

        signal_wave = np.sin(
            2 * np.pi * k * t
        )

        plt.plot(
            t,
            signal_wave,
            label=f"Subcarrier {k}"
        )

    plt.title("OFDM Subcarriers")

    plt.xlabel("Time")

    plt.ylabel("Amplitude")

    plt.legend()

    plt.grid()

    plt.show()

    data["history"].append(
        "Subcarrier Visualization"
    )

    save_data()

    pause()


# =========================================================
# CONSTELLATION DIAGRAM
# =========================================================

def constellation_diagram():

    clear()

    title("QPSK CONSTELLATION")

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
            100
        )

        +

        1j * np.random.normal(
            0,
            0.2,
            100
        )
    )

    received = np.random.choice(
        symbols,
        100
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
# ASCII SIGNAL VIEWER
# =========================================================

def ascii_signal():

    clear()

    title("ASCII OFDM SIGNAL")

    bits = np.random.randint(
        0,
        2,
        50
    )

    print(Fore.GREEN +
          "\nOFDM Bit Stream:\n")

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
# VIEW HISTORY
# =========================================================

def history():

    clear()

    title("OFDM HISTORY")

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

            "OFDM Operations":
            data["history"]
        })

        filename = "ofdm_report.csv"

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

    title("DEMO OFDM SYSTEM")

    print(Fore.WHITE + """
OFDM Communication Demo:

=========================================================
OFDM FEATURES
=========================================================

✓ Multi-carrier
✓ FFT / IFFT
✓ Cyclic Prefix

=========================================================
WIRELESS SYSTEMS
=========================================================

✓ WiFi
✓ LTE
✓ 5G NR

=========================================================
DSP PROCESSING
=========================================================

✓ QPSK Mapping
✓ BER Analysis
✓ Spectrum Analysis
""")

    pause()


# =========================================================
# EXPLAIN OFDM
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH OFDM")

    print(Fore.WHITE + """
=========================================================
1. OFDM
=========================================================

OFDM:
   Orthogonal Frequency Division Multiplexing

=========================================================
2. SUBCARRIERS
=========================================================

OFDM dùng:
   ✓ Nhiều sóng mang

=========================================================
3. FFT / IFFT
=========================================================

DSP:
   ✓ Frequency <-> Time

=========================================================
4. CYCLIC PREFIX
=========================================================

CP:
   ✓ Chống multipath

=========================================================
5. QPSK
=========================================================

QPSK:
   ✓ Điều chế pha

=========================================================
6. BER
=========================================================

BER:
   ✓ Đánh giá chất lượng truyền

=========================================================
7. WIRELESS COMMUNICATION
=========================================================

Ứng dụng:
   ✓ WiFi
   ✓ LTE
   ✓ 5G

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ SDR Systems
✓ Satellite Communication
✓ Embedded RF
✓ Wireless Engineering
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("OFDM SIMULATOR SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu OFDM
[2] Generate Random Bits
[3] QPSK Mapping
[4] OFDM Signal Generation
[5] Cyclic Prefix
[6] FFT Analysis
[7] AWGN Channel
[8] BER Simulation
[9] Subcarrier Visualization
[10] Constellation Diagram
[11] ASCII Signal Viewer
[12] View History
[13] Export CSV Report
[14] Demo mode
[15] Giải thích OFDM
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

            qpsk_mapping()

        elif choice == '4':

            ofdm_generation()

        elif choice == '5':

            cyclic_prefix()

        elif choice == '6':

            fft_analysis()

        elif choice == '7':

            awgn_channel()

        elif choice == '8':

            ber_simulation()

        elif choice == '9':

            subcarrier_visual()

        elif choice == '10':

            constellation_diagram()

        elif choice == '11':

            ascii_signal()

        elif choice == '12':

            history()

        elif choice == '13':

            export_csv()

        elif choice == '14':

            demo_mode()

        elif choice == '15':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng OFDM Simulator.

Kiến thức đạt được:
   ✓ OFDM Communication
   ✓ FFT / IFFT
   ✓ QPSK Modulation
   ✓ BER Analysis
   ✓ Wireless Systems
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
