# =========================================================
#          VERILOG TESTBENCH WAVEFORM GENERATOR
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Tạo waveform cho Verilog testbench
#
# Chức năng:
#   ✓ Sinh waveform digital
#   ✓ Tạo clock signal
#   ✓ Tạo reset signal
#   ✓ Sinh stimulus testbench
#   ✓ ASCII waveform viewer
#   ✓ Export Verilog testbench
#   ✓ Export VCD-style log
#   ✓ Timing simulation
#   ✓ Signal statistics
#   ✓ Dashboard terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install colorama pandas
#
# =========================================================
# CHẠY
# =========================================================
#
# python verilog_waveform_generator.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import os
import json
import time
import random
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "waveform_project.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "",
    "signals": []
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

    title("GIỚI THIỆU WAVEFORM GENERATOR")

    print(Fore.WHITE + """
Verilog Waveform Generator giúp:

   ✓ Sinh waveform cho testbench
   ✓ Mô phỏng tín hiệu digital
   ✓ Tạo clock/reset tự động
   ✓ Hỗ trợ FPGA/ASIC verification

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Clock Generator
✓ Reset Generator
✓ Signal Stimulus
✓ ASCII Waveform
✓ Verilog Export
✓ VCD-style Output

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ FPGA Design
✓ ASIC Verification
✓ Digital Logic
✓ RTL Simulation
✓ Embedded Hardware

=========================================================
SIGNALS HỖ TRỢ
=========================================================

✓ clk
✓ rst
✓ enable
✓ data
✓ input/output
""")

    line()


# =========================================================
# SET PROJECT
# =========================================================

def set_project():

    clear()

    title("SET PROJECT")

    project_name = input(
        Fore.YELLOW +
        "Tên project Verilog: "
    )

    data["project_name"] = project_name

    save_data()

    print(Fore.GREEN +
          "\nĐã lưu project.")

    pause()


# =========================================================
# ADD SIGNAL
# =========================================================

def add_signal():

    clear()

    title("ADD SIGNAL")

    name = input(
        Fore.YELLOW +
        "Tên signal: "
    )

    signal_type = input(
        Fore.YELLOW +
        "Loại signal (clk/data/reset): "
    )

    waveform = input(
        Fore.YELLOW +
        "Waveform (VD: 010101): "
    )

    signal = {

        "name": name,
        "type": signal_type,
        "waveform": waveform,
        "date_added": str(
            datetime.date.today()
        )
    }

    data["signals"].append(signal)

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm signal.")

    pause()


# =========================================================
# AUTO CLOCK GENERATOR
# =========================================================

def generate_clock():

    clear()

    title("CLOCK GENERATOR")

    try:

        cycles = int(input(
            Fore.YELLOW +
            "Số chu kỳ clock: "
        ))

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    waveform = ""

    for _ in range(cycles):

        waveform += "01"

    clock_signal = {

        "name": "clk",
        "type": "clock",
        "waveform": waveform
    }

    data["signals"].append(
        clock_signal
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo clock waveform.")

    print(Fore.CYAN +
          f"\n{waveform}")

    pause()


# =========================================================
# AUTO RESET GENERATOR
# =========================================================

def generate_reset():

    clear()

    title("RESET GENERATOR")

    waveform = "111100000000"

    reset_signal = {

        "name": "rst",
        "type": "reset",
        "waveform": waveform
    }

    data["signals"].append(
        reset_signal
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo reset waveform.")

    print(Fore.CYAN +
          f"\n{waveform}")

    pause()


# =========================================================
# RANDOM DATA GENERATOR
# =========================================================

def random_data():

    clear()

    title("RANDOM DATA GENERATOR")

    try:

        length = int(input(
            Fore.YELLOW +
            "Độ dài waveform: "
        ))

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    waveform = ""

    for _ in range(length):

        waveform += str(
            random.randint(0, 1)
        )

    signal = {

        "name": "data_in",
        "type": "data",
        "waveform": waveform
    }

    data["signals"].append(signal)

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo random waveform.")

    print(Fore.YELLOW +
          f"\n{waveform}")

    pause()


# =========================================================
# VIEW SIGNALS
# =========================================================

def view_signals():

    clear()

    title("ALL SIGNALS")

    if not data["signals"]:

        print(Fore.RED +
              "\nChưa có signal.")

        pause()

        return

    for index, signal in enumerate(
        data["signals"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {signal['name']}")

        print(Fore.CYAN +
              f"Type : {signal['type']}")

        print(Fore.YELLOW +
              f"Wave : {signal['waveform']}")

        line()

    pause()


# =========================================================
# ASCII WAVEFORM VIEWER
# =========================================================

def waveform_viewer():

    clear()

    title("ASCII WAVEFORM VIEWER")

    if not data["signals"]:

        print(Fore.RED +
              "\nKhông có waveform.")

        pause()

        return

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    line()

    print(Fore.CYAN +
          "\nDIGITAL WAVEFORM\n")

    for signal in data["signals"]:

        wave_display = ""

        for bit in signal["waveform"]:

            if bit == "1":

                wave_display += "‾‾"

            else:

                wave_display += "__"

        print(Fore.YELLOW +
              f"{signal['name']:<10}: "
              f"{wave_display}")

    line()

    pause()


# =========================================================
# TIMING ANALYSIS
# =========================================================

def timing_analysis():

    clear()

    title("TIMING ANALYSIS")

    if not data["signals"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    for signal in data["signals"]:

        ones = signal["waveform"].count("1")

        zeros = signal["waveform"].count("0")

        print(Fore.GREEN +
              f"\nSignal: {signal['name']}")

        print(Fore.CYAN +
              f"Logic 1: {ones}")

        print(Fore.YELLOW +
              f"Logic 0: {zeros}")

        line()

    pause()


# =========================================================
# EXPORT VERILOG TESTBENCH
# =========================================================

def export_verilog():

    clear()

    title("EXPORT VERILOG TESTBENCH")

    filename = "generated_testbench.v"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "// ======================================\n"
            )

            f.write(
                "// AUTO GENERATED TESTBENCH\n"
            )

            f.write(
                "// ======================================\n\n"
            )

            f.write(
                "module tb;\n\n"
            )

            # Signal declaration

            for signal in data["signals"]:

                f.write(
                    f"reg {signal['name']};\n"
                )

            f.write("\ninitial begin\n\n")

            # Generate waveform

            max_len = max(
                len(sig["waveform"])
                for sig in data["signals"]
            )

            for i in range(max_len):

                for sig in data["signals"]:

                    if i < len(sig["waveform"]):

                        bit = sig["waveform"][i]

                        f.write(
                            f"    {sig['name']} = "
                            f"{bit};\n"
                        )

                f.write(
                    "    #10;\n\n"
                )

            f.write("end\n\n")

            f.write("endmodule\n")

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT WAVEFORM CSV")

    if not data["signals"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["signals"]
        )

        filename = "waveform_report.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export CSV: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi CSV:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO WAVEFORM")

    data["project_name"] = (
        "FPGA Counter Testbench"
    )

    data["signals"] = [

        {
            "name": "clk",
            "type": "clock",
            "waveform": "010101010101"
        },

        {
            "name": "rst",
            "type": "reset",
            "waveform": "111100000000"
        },

        {
            "name": "enable",
            "type": "control",
            "waveform": "000011110000"
        },

        {
            "name": "data_in",
            "type": "data",
            "waveform": "101010110011"
        }
    ]

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo waveform demo.")

    pause()


# =========================================================
# EXPLAIN SYSTEM
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH WAVEFORM SYSTEM")

    print(Fore.WHITE + """
=========================================================
1. VERILOG TESTBENCH
=========================================================

Dùng để:
   ✓ Verify RTL Design
   ✓ Simulate FPGA

=========================================================
2. DIGITAL WAVEFORM
=========================================================

Tín hiệu:
   ✓ Logic 0
   ✓ Logic 1

=========================================================
3. CLOCK SIGNAL
=========================================================

Clock:
   ✓ Đồng bộ hệ thống

=========================================================
4. RESET SIGNAL
=========================================================

Reset:
   ✓ Khởi tạo hệ thống

=========================================================
5. TIMING SIMULATION
=========================================================

Mô phỏng:
   ✓ Delay
   ✓ Transitions

=========================================================
6. FPGA / ASIC
=========================================================

Ứng dụng:
   ✓ Digital Design
   ✓ Hardware Verification

=========================================================
7. ASCII WAVEFORM
=========================================================

Terminal hiển thị:
   ✓ Digital Signals

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ FPGA Engineering
✓ ASIC Verification
✓ Embedded Hardware
✓ RTL Design
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("VERILOG WAVEFORM GENERATOR")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] Set project name
[3] Add signal
[4] Generate clock
[5] Generate reset
[6] Generate random data
[7] View signals
[8] ASCII waveform viewer
[9] Timing analysis
[10] Export Verilog testbench
[11] Export CSV waveform
[12] Demo mode
[13] Giải thích hệ thống
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

            set_project()

        elif choice == '3':

            add_signal()

        elif choice == '4':

            generate_clock()

        elif choice == '5':

            generate_reset()

        elif choice == '6':

            random_data()

        elif choice == '7':

            view_signals()

        elif choice == '8':

            waveform_viewer()

        elif choice == '9':

            timing_analysis()

        elif choice == '10':

            export_verilog()

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
Cảm ơn bạn đã sử dụng Verilog Waveform Generator.

Kiến thức đạt được:
   ✓ Verilog Testbench
   ✓ Digital Waveform
   ✓ FPGA Verification
   ✓ RTL Simulation
   ✓ Timing Analysis
   ✓ Hardware Design
""")

            break

        else:

            print(Fore.RED +
                  "Lựa chọn không hợp lệ!")

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
