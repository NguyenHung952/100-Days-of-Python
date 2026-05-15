# =========================================================
#           HDL TEST VECTOR GENERATOR SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Sinh test vector tự động HDL
#
# Chức năng:
#   ✓ Sinh test vector tự động
#   ✓ Tạo stimulus cho Verilog/VHDL
#   ✓ Generate random vectors
#   ✓ Generate binary patterns
#   ✓ Export testbench vectors
#   ✓ ASCII waveform display
#   ✓ Timing simulation
#   ✓ HDL verification support
#   ✓ CSV/TXT export
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
# python hdl_test_vector_generator.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import random
import json
import os
import time
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "hdl_test_vectors.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "",
    "vectors": []
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

    title("GIỚI THIỆU HDL TEST VECTOR GENERATOR")

    print(Fore.WHITE + """
HDL Test Vector Generator giúp:

   ✓ Sinh test vector tự động
   ✓ Verify mạch số HDL
   ✓ Tạo stimulus cho testbench
   ✓ Hỗ trợ FPGA/ASIC verification

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Random Vector Generation
✓ Binary Pattern Generation
✓ HDL Testbench Export
✓ ASCII Waveform Viewer
✓ Timing Simulation

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ FPGA Design
✓ ASIC Verification
✓ RTL Simulation
✓ Digital Logic Design

=========================================================
HDL HỖ TRỢ
=========================================================

✓ Verilog
✓ SystemVerilog
✓ VHDL
""")

    line()


# =========================================================
# SET PROJECT
# =========================================================

def set_project():

    clear()

    title("SET HDL PROJECT")

    project_name = input(
        Fore.YELLOW +
        "Tên HDL Project: "
    )

    data["project_name"] = project_name

    save_data()

    print(Fore.GREEN +
          "\nĐã lưu project.")

    pause()


# =========================================================
# RANDOM VECTOR GENERATOR
# =========================================================

def generate_random_vectors():

    clear()

    title("RANDOM TEST VECTOR GENERATOR")

    signal_name = input(
        Fore.YELLOW +
        "Tên signal: "
    )

    try:

        width = int(input(
            Fore.YELLOW +
            "Bit width: "
        ))

        count = int(input(
            Fore.YELLOW +
            "Số lượng vector: "
        ))

    except:

        print(Fore.RED +
              "\nGiá trị không hợp lệ.")

        pause()

        return

    print(Fore.GREEN +
          "\nGENERATED VECTORS\n")

    for i in range(count):

        vector = ""

        for _ in range(width):

            vector += str(
                random.randint(0, 1)
            )

        vector_data = {

            "signal": signal_name,
            "vector": vector,
            "type": "random"
        }

        data["vectors"].append(
            vector_data
        )

        print(Fore.CYAN +
              f"[{i+1}] {vector}")

    save_data()

    pause()


# =========================================================
# COUNTER PATTERN GENERATOR
# =========================================================

def generate_counter_vectors():

    clear()

    title("COUNTER VECTOR GENERATOR")

    signal_name = input(
        Fore.YELLOW +
        "Tên signal: "
    )

    try:

        width = int(input(
            Fore.YELLOW +
            "Bit width: "
        ))

        count = int(input(
            Fore.YELLOW +
            "Số lượng vector: "
        ))

    except:

        print(Fore.RED +
              "\nDữ liệu không hợp lệ.")

        pause()

        return

    print(Fore.GREEN +
          "\nCOUNTER PATTERNS\n")

    for i in range(count):

        vector = format(
            i,
            f"0{width}b"
        )

        vector_data = {

            "signal": signal_name,
            "vector": vector,
            "type": "counter"
        }

        data["vectors"].append(
            vector_data
        )

        print(Fore.YELLOW +
              f"[{i}] {vector}")

    save_data()

    pause()


# =========================================================
# ADD MANUAL VECTOR
# =========================================================

def add_manual_vector():

    clear()

    title("ADD MANUAL VECTOR")

    signal = input(
        Fore.YELLOW +
        "Tên signal: "
    )

    vector = input(
        Fore.YELLOW +
        "Binary vector: "
    )

    vector_data = {

        "signal": signal,
        "vector": vector,
        "type": "manual"
    }

    data["vectors"].append(
        vector_data
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm vector.")

    pause()


# =========================================================
# VIEW VECTORS
# =========================================================

def view_vectors():

    clear()

    title("ALL TEST VECTORS")

    if not data["vectors"]:

        print(Fore.RED +
              "\nChưa có vectors.")

        pause()

        return

    for index, item in enumerate(
        data["vectors"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}]")

        print(Fore.CYAN +
              f"Signal : {item['signal']}")

        print(Fore.YELLOW +
              f"Vector : {item['vector']}")

        print(Fore.MAGENTA +
              f"Type   : {item['type']}")

        line()

    pause()


# =========================================================
# ASCII WAVEFORM VIEWER
# =========================================================

def waveform_viewer():

    clear()

    title("ASCII WAVEFORM VIEWER")

    if not data["vectors"]:

        print(Fore.RED +
              "\nKhông có vectors.")

        pause()

        return

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    line()

    for item in data["vectors"]:

        waveform = ""

        for bit in item["vector"]:

            if bit == "1":

                waveform += "‾‾"

            else:

                waveform += "__"

        print(Fore.YELLOW +
              f"{item['signal']:<10}: "
              f"{waveform}")

    line()

    pause()


# =========================================================
# TIMING ANALYSIS
# =========================================================

def timing_analysis():

    clear()

    title("TIMING ANALYSIS")

    if not data["vectors"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    for item in data["vectors"]:

        ones = item["vector"].count("1")

        zeros = item["vector"].count("0")

        transitions = 0

        vector = item["vector"]

        for i in range(1, len(vector)):

            if vector[i] != vector[i - 1]:

                transitions += 1

        print(Fore.GREEN +
              f"\nSignal: {item['signal']}")

        print(Fore.CYAN +
              f"Logic 1     : {ones}")

        print(Fore.YELLOW +
              f"Logic 0     : {zeros}")

        print(Fore.MAGENTA +
              f"Transitions : {transitions}")

        line()

    pause()


# =========================================================
# EXPORT VERILOG TESTBENCH
# =========================================================

def export_verilog():

    clear()

    title("EXPORT VERILOG TESTBENCH")

    filename = "auto_test_vectors.v"

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
                "// AUTO GENERATED HDL TEST VECTORS\n"
            )

            f.write(
                "// ======================================\n\n"
            )

            f.write("module tb;\n\n")

            unique_signals = []

            for item in data["vectors"]:

                if item["signal"] not in unique_signals:

                    unique_signals.append(
                        item["signal"]
                    )

            for signal in unique_signals:

                f.write(
                    f"reg {signal};\n"
                )

            f.write("\ninitial begin\n\n")

            for item in data["vectors"]:

                f.write(
                    f"    // "
                    f"{item['type']} vector\n"
                )

                for bit in item["vector"]:

                    f.write(
                        f"    {item['signal']} "
                        f"= {bit};\n"
                    )

                    f.write(
                        "    #10;\n"
                    )

                f.write("\n")

            f.write("end\n\n")

            f.write("endmodule\n")

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# EXPORT TXT
# =========================================================

def export_txt():

    clear()

    title("EXPORT TXT REPORT")

    filename = "hdl_vectors.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"PROJECT: "
                f"{data['project_name']}\n"
            )

            f.write("=" * 50 + "\n\n")

            for item in data["vectors"]:

                f.write(
                    f"Signal : {item['signal']}\n"
                )

                f.write(
                    f"Vector : {item['vector']}\n"
                )

                f.write(
                    f"Type   : {item['type']}\n"
                )

                f.write("\n")

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

    title("EXPORT CSV")

    if not data["vectors"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["vectors"]
        )

        filename = "hdl_vectors.csv"

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

    title("DEMO HDL TEST VECTORS")

    data["project_name"] = (
        "FPGA ALU Verification"
    )

    data["vectors"] = [

        {
            "signal": "clk",
            "vector": "010101010101",
            "type": "clock"
        },

        {
            "signal": "rst",
            "vector": "111100000000",
            "type": "reset"
        },

        {
            "signal": "data_in",
            "vector": "101001110010",
            "type": "random"
        },

        {
            "signal": "enable",
            "vector": "000011110000",
            "type": "control"
        }
    ]

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# EXPLAIN HDL SYSTEM
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH HDL TEST VECTOR")

    print(Fore.WHITE + """
=========================================================
1. HDL
=========================================================

HDL:
   ✓ Verilog
   ✓ VHDL
   ✓ SystemVerilog

=========================================================
2. TEST VECTOR
=========================================================

Vector dùng để:
   ✓ Verify logic
   ✓ Simulation

=========================================================
3. FPGA / ASIC
=========================================================

Ứng dụng:
   ✓ Hardware Design
   ✓ RTL Verification

=========================================================
4. DIGITAL SIGNAL
=========================================================

Logic:
   ✓ 0
   ✓ 1

=========================================================
5. TIMING ANALYSIS
=========================================================

Phân tích:
   ✓ Transitions
   ✓ Clock cycles

=========================================================
6. TESTBENCH
=========================================================

Verify:
   ✓ Inputs
   ✓ Outputs

=========================================================
7. ASCII WAVEFORM
=========================================================

Hiển thị:
   ✓ Digital waveform

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ FPGA Engineering
✓ ASIC Verification
✓ Embedded Hardware
✓ Digital IC Design
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("HDL TEST VECTOR GENERATOR")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] Set project name
[3] Generate random vectors
[4] Generate counter vectors
[5] Add manual vector
[6] View vectors
[7] ASCII waveform viewer
[8] Timing analysis
[9] Export Verilog testbench
[10] Export TXT report
[11] Export CSV report
[12] Demo mode
[13] Giải thích HDL system
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

            generate_random_vectors()

        elif choice == '4':

            generate_counter_vectors()

        elif choice == '5':

            add_manual_vector()

        elif choice == '6':

            view_vectors()

        elif choice == '7':

            waveform_viewer()

        elif choice == '8':

            timing_analysis()

        elif choice == '9':

            export_verilog()

        elif choice == '10':

            export_txt()

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
Cảm ơn bạn đã sử dụng HDL Test Vector Generator.

Kiến thức đạt được:
   ✓ HDL Verification
   ✓ FPGA Simulation
   ✓ Testbench Design
   ✓ Timing Analysis
   ✓ Digital Waveform
   ✓ RTL Verification
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
