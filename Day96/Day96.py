# =========================================================
#          BER ANALYSIS IN DIGITAL COMMUNICATION
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Phân tích BER trong truyền thông số
#
# Chức năng:
#   ✓ BER Simulation
#   ✓ BPSK Modulation
#   ✓ AWGN Noise Channel
#   ✓ SNR Analysis
#   ✓ BER vs SNR Graph
#   ✓ Bit Error Visualization
#   ✓ Digital Communication Demo
#   ✓ Random Bit Generator
#   ✓ ASCII Signal Viewer
#   ✓ Export BER Report
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install numpy matplotlib pandas colorama scipy
#
# =========================================================
# CHẠY
# =========================================================
#
# python ber_analysis.py
#
# =========================================================

from colorama import Fore, Style, init

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from scipy.special import erfc

import random
import time
import json
import os

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "ber_history.json"

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

    title("GIỚI THIỆU BER ANALYSIS")

    print(Fore.WHITE + """
BER Analysis giúp:

   ✓ Phân tích Bit Error Rate
   ✓ Mô phỏng truyền thông số
   ✓ Đánh giá chất lượng kênh truyền
   ✓ Học Digital Communication trực quan

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ BPSK Modulation
✓ AWGN Channel
✓ BER Simulation
✓ SNR Analysis
✓ BER Curve

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Wireless Communication
✓ 5G Systems
✓ Satellite Systems
✓ IoT Communication
✓ SDR Systems

=========================================================
COMMUNICATION CONCEPTS
=========================================================

✓ BER
✓ SNR
✓ Noise
✓ Modulation
✓ Channel
""")

    line()


# =========================================================
# RANDOM BIT GENERATOR
# =========================================================

def random_bits():

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
# BPSK MODULATION
# =========================================================

def bpsk_modulation():

    clear()

    title("BPSK MODULATION")

    bits = np.random.randint(
        0,
        2,
        20
    )

    bpsk_signal = 2 * bits - 1

    print(Fore.GREEN +
          "\nOriginal Bits:\n")

    print(bits)

    print(Fore.CYAN +
          "\nBPSK Signal:\n")

    print(bpsk_signal)

    plt.figure(figsize=(10, 3))

    plt.step(
        range(len(bpsk_signal)),
        bpsk_signal,
        where='mid'
    )

    plt.title("BPSK Signal")

    plt.xlabel("Bit Index")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "BPSK Modulation"
    )

    save_data()

    pause()


# =========================================================
# AWGN CHANNEL
# =========================================================

def awgn_channel():

    clear()

    title("AWGN CHANNEL SIMULATION")

    bits = np.random.randint(
        0,
        2,
        1000
    )

    signal_tx = 2 * bits - 1

    snr_db = 5

    snr_linear = 10 ** (
        snr_db / 10
    )

    noise_std = np.sqrt(
        1 / (2 * snr_linear)
    )

    noise = noise_std * np.random.randn(
        len(signal_tx)
    )

    received = signal_tx + noise

    plt.figure(figsize=(10, 4))

    plt.plot(
        received[:100]
    )

    plt.title(
        "Received Signal with AWGN"
    )

    plt.xlabel("Sample")

    plt.ylabel("Amplitude")

    plt.grid()

    plt.show()

    data["history"].append(
        "AWGN Simulation"
    )

    save_data()

    pause()


# =========================================================
# BER SIMULATION
# =========================================================

def ber_simulation():

    clear()

    title("BER SIMULATION")

    n_bits = 100000

    snr_db_range = range(0, 11)

    ber_results = []

    for snr_db in snr_db_range:

        bits = np.random.randint(
            0,
            2,
            n_bits
        )

        tx_signal = 2 * bits - 1

        snr_linear = 10 ** (
            snr_db / 10
        )

        noise_std = np.sqrt(
            1 / (2 * snr_linear)
        )

        noise = noise_std * np.random.randn(
            n_bits
        )

        rx_signal = tx_signal + noise

        detected_bits = (

            rx_signal > 0
        ).astype(int)

        errors = np.sum(
            bits != detected_bits
        )

        ber = errors / n_bits

        ber_results.append(ber)

        print(Fore.GREEN +
              f"SNR={snr_db} dB "
              f" -> BER={ber:.6f}")

    plt.figure(figsize=(8, 5))

    plt.semilogy(
        snr_db_range,
        ber_results,
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
# THEORETICAL BER
# =========================================================

def theoretical_ber():

    clear()

    title("THEORETICAL BER")

    snr_db = np.arange(0, 11)

    snr_linear = 10 ** (
        snr_db / 10
    )

    ber = 0.5 * erfc(
        np.sqrt(snr_linear)
    )

    plt.figure(figsize=(8, 5))

    plt.semilogy(
        snr_db,
        ber,
        marker='o'
    )

    plt.title(
        "Theoretical BER for BPSK"
    )

    plt.xlabel("SNR (dB)")

    plt.ylabel("BER")

    plt.grid()

    plt.show()

    data["history"].append(
        "Theoretical BER"
    )

    save_data()

    pause()


# =========================================================
# BIT ERROR VISUALIZATION
# =========================================================

def bit_error_visual():

    clear()

    title("BIT ERROR VISUALIZATION")

    tx_bits = np.random.randint(
        0,
        2,
        20
    )

    rx_bits = tx_bits.copy()

    # Tạo lỗi giả lập

    error_positions = random.sample(
        range(20),
        3
    )

    for pos in error_positions:

        rx_bits[pos] ^= 1

    print(Fore.GREEN +
          "\nTX Bits:\n")

    print(tx_bits)

    print(Fore.CYAN +
          "\nRX Bits:\n")

    print(rx_bits)

    print(Fore.RED +
          "\nError Positions:")

    print(error_positions)

    data["history"].append(
        "Bit Error Visualization"
    )

    save_data()

    pause()


# =========================================================
# ASCII SIGNAL VIEWER
# =========================================================

def ascii_signal():

    clear()

    title("ASCII SIGNAL VIEWER")

    bits = np.random.randint(
        0,
        2,
        40
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
        "ASCII Signal Viewer"
    )

    save_data()

    pause()


# =========================================================
# SNR ANALYSIS
# =========================================================

def snr_analysis():

    clear()

    title("SNR ANALYSIS")

    signal_power = 10

    noise_power = 2

    snr = signal_power / noise_power

    snr_db = 10 * np.log10(snr)

    print(Fore.GREEN +
          f"\nSignal Power: {signal_power}")

    print(Fore.CYAN +
          f"Noise Power : {noise_power}")

    print(Fore.YELLOW +
          f"SNR Linear  : {snr}")

    print(Fore.MAGENTA +
          f"SNR dB      : {snr_db:.2f} dB")

    data["history"].append(
        "SNR Analysis"
    )

    save_data()

    pause()


# =========================================================
# VIEW HISTORY
# =========================================================

def history():

    clear()

    title("BER ANALYSIS HISTORY")

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

            "BER Operations":
            data["history"]
        })

        filename = "ber_report.csv"

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

    title("DEMO BER ANALYSIS")

    print(Fore.WHITE + """
Digital Communication Demo:

=========================================================
MODULATION
=========================================================

✓ BPSK

=========================================================
CHANNEL
=========================================================

✓ AWGN Noise

=========================================================
ANALYSIS
=========================================================

✓ BER
✓ SNR

=========================================================
VISUALIZATION
=========================================================

✓ BER Curve
✓ Signal Viewer
✓ Error Visualization
""")

    pause()


# =========================================================
# EXPLAIN BER
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH BER")

    print(Fore.WHITE + """
=========================================================
1. BER
=========================================================

BER:
   Bit Error Rate

=========================================================
2. SNR
=========================================================

SNR:
   Signal-to-Noise Ratio

=========================================================
3. BPSK
=========================================================

BPSK:
   Binary Phase Shift Keying

=========================================================
4. AWGN
=========================================================

AWGN:
   Additive White Gaussian Noise

=========================================================
5. CHANNEL
=========================================================

Kênh truyền:
   ✓ Wireless
   ✓ RF
   ✓ Satellite

=========================================================
6. DIGITAL COMMUNICATION
=========================================================

Ứng dụng:
   ✓ 5G
   ✓ WiFi
   ✓ IoT

=========================================================
7. BER CURVE
=========================================================

Phân tích:
   ✓ BER vs SNR

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ SDR Systems
✓ Satellite Communication
✓ Radar Systems
✓ Embedded RF
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("BER ANALYSIS SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu BER
[2] Random Bit Generator
[3] BPSK Modulation
[4] AWGN Channel Simulation
[5] BER Simulation
[6] Theoretical BER Curve
[7] Bit Error Visualization
[8] ASCII Signal Viewer
[9] SNR Analysis
[10] View History
[11] Export CSV Report
[12] Demo mode
[13] Giải thích BER
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

            random_bits()

        elif choice == '3':

            bpsk_modulation()

        elif choice == '4':

            awgn_channel()

        elif choice == '5':

            ber_simulation()

        elif choice == '6':

            theoretical_ber()

        elif choice == '7':

            bit_error_visual()

        elif choice == '8':

            ascii_signal()

        elif choice == '9':

            snr_analysis()

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
Cảm ơn bạn đã sử dụng BER Analysis System.

Kiến thức đạt được:
   ✓ BER Simulation
   ✓ BPSK Modulation
   ✓ AWGN Channel
   ✓ SNR Analysis
   ✓ Digital Communication
   ✓ Wireless Systems
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
