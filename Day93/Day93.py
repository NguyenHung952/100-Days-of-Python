# =========================================================
#               FSM SIMULATOR SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Mô phỏng FSM bằng Python
#
# Chức năng:
#   ✓ Mô phỏng Finite State Machine
#   ✓ Hỗ trợ Moore FSM
#   ✓ Hỗ trợ Mealy FSM
#   ✓ State transition simulation
#   ✓ ASCII FSM visualization
#   ✓ FSM timing simulation
#   ✓ Export FSM report
#   ✓ Digital design learning
#   ✓ HDL/FPGA education
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
# python fsm_simulator.py
#
# =========================================================

from colorama import Fore, Style, init

import pandas as pd

import json
import os
import time
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "fsm_project.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "",
    "fsm_type": "",
    "states": [],
    "transitions": [],
    "current_state": ""
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

    title("GIỚI THIỆU FSM SIMULATOR")

    print(Fore.WHITE + """
FSM Simulator giúp:

   ✓ Mô phỏng Finite State Machine
   ✓ Hiểu state transition
   ✓ Verify logic design
   ✓ Hỗ trợ FPGA/ASIC learning

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Moore FSM
✓ Mealy FSM
✓ State Transition
✓ Input Simulation
✓ ASCII FSM Viewer

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ FPGA Design
✓ ASIC Verification
✓ Embedded Systems
✓ Robotics
✓ Digital Logic

=========================================================
FSM CONCEPTS
=========================================================

✓ States
✓ Inputs
✓ Outputs
✓ Transitions
✓ Clocked Logic
""")

    line()


# =========================================================
# SET PROJECT
# =========================================================

def set_project():

    clear()

    title("SET FSM PROJECT")

    project_name = input(
        Fore.YELLOW +
        "Tên FSM project: "
    )

    fsm_type = input(
        Fore.YELLOW +
        "FSM Type (Moore/Mealy): "
    )

    data["project_name"] = project_name

    data["fsm_type"] = fsm_type

    save_data()

    print(Fore.GREEN +
          "\nĐã lưu FSM project.")

    pause()


# =========================================================
# ADD STATE
# =========================================================

def add_state():

    clear()

    title("ADD FSM STATE")

    state_name = input(
        Fore.YELLOW +
        "Tên state: "
    )

    output = input(
        Fore.YELLOW +
        "Output của state: "
    )

    state = {

        "name": state_name,
        "output": output,
        "date_added": str(
            datetime.date.today()
        )
    }

    data["states"].append(state)

    if data["current_state"] == "":

        data["current_state"] = state_name

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm state.")

    pause()


# =========================================================
# ADD TRANSITION
# =========================================================

def add_transition():

    clear()

    title("ADD STATE TRANSITION")

    from_state = input(
        Fore.YELLOW +
        "From state: "
    )

    input_signal = input(
        Fore.YELLOW +
        "Input signal: "
    )

    to_state = input(
        Fore.YELLOW +
        "To state: "
    )

    transition = {

        "from": from_state,
        "input": input_signal,
        "to": to_state
    }

    data["transitions"].append(
        transition
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm transition.")

    pause()


# =========================================================
# VIEW STATES
# =========================================================

def view_states():

    clear()

    title("FSM STATES")

    if not data["states"]:

        print(Fore.RED +
              "\nChưa có state.")

        pause()

        return

    for index, state in enumerate(
        data["states"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {state['name']}")

        print(Fore.CYAN +
              f"Output: {state['output']}")

        if state["name"] == data["current_state"]:

            print(Fore.YELLOW +
                  "ACTIVE STATE")

        line()

    pause()


# =========================================================
# VIEW TRANSITIONS
# =========================================================

def view_transitions():

    clear()

    title("FSM TRANSITIONS")

    if not data["transitions"]:

        print(Fore.RED +
              "\nChưa có transition.")

        pause()

        return

    for index, trans in enumerate(
        data["transitions"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}]")

        print(Fore.CYAN +
              f"{trans['from']}")

        print(Fore.YELLOW +
              f" --[{trans['input']}]--> ")

        print(Fore.GREEN +
              f"{trans['to']}")

        line()

    pause()


# =========================================================
# FSM SIMULATION
# =========================================================

def simulate_fsm():

    clear()

    title("FSM SIMULATION")

    if not data["states"]:

        print(Fore.RED +
              "\nFSM chưa có states.")

        pause()

        return

    print(Fore.GREEN +
          f"\nCurrent State: "
          f"{data['current_state']}")

    input_signal = input(
        Fore.YELLOW +
        "\nNhập input signal: "
    )

    found = False

    for trans in data["transitions"]:

        if (
            trans["from"] == data["current_state"]
            and
            trans["input"] == input_signal
        ):

            found = True

            old_state = data["current_state"]

            data["current_state"] = trans["to"]

            save_data()

            print(Fore.CYAN +
                  f"\nTransition:")

            print(Fore.YELLOW +
                  f"{old_state}")

            print(Fore.GREEN +
                  f" --> {trans['to']}")

            break

    if not found:

        print(Fore.RED +
              "\nKhông có transition phù hợp.")

    pause()


# =========================================================
# ASCII FSM VIEWER
# =========================================================

def ascii_viewer():

    clear()

    title("ASCII FSM VIEWER")

    if not data["transitions"]:

        print(Fore.RED +
              "\nKhông có FSM.")

        pause()

        return

    print(Fore.GREEN +
          f"\nPROJECT: {data['project_name']}")

    print(Fore.CYAN +
          f"FSM TYPE: {data['fsm_type']}")

    line()

    print(Fore.YELLOW +
          "\nFSM DIAGRAM\n")

    for trans in data["transitions"]:

        print(Fore.GREEN +
              f"[{trans['from']}]")

        print(Fore.CYAN +
              f"    |")

        print(Fore.YELLOW +
              f"    |--- "
              f"{trans['input']} --->")

        print(Fore.CYAN +
              f"    |")

        print(Fore.GREEN +
              f"[{trans['to']}]\n")

    line()

    pause()


# =========================================================
# TIMING SIMULATION
# =========================================================

def timing_simulation():

    clear()

    title("FSM TIMING SIMULATION")

    if not data["transitions"]:

        print(Fore.RED +
              "\nKhông có FSM.")

        pause()

        return

    print(Fore.GREEN +
          "\nCLOCK CYCLE SIMULATION\n")

    cycle = 0

    for trans in data["transitions"]:

        cycle += 1

        print(Fore.CYAN +
              f"Cycle {cycle}")

        print(Fore.YELLOW +
              f"State : {trans['from']}")

        print(Fore.GREEN +
              f"Input : {trans['input']}")

        print(Fore.MAGENTA +
              f"Next  : {trans['to']}")

        line()

        time.sleep(0.5)

    pause()


# =========================================================
# EXPORT FSM REPORT
# =========================================================

def export_report():

    clear()

    title("EXPORT FSM REPORT")

    filename = "fsm_report.txt"

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"FSM PROJECT: "
                f"{data['project_name']}\n"
            )

            f.write(
                f"FSM TYPE: "
                f"{data['fsm_type']}\n"
            )

            f.write("=" * 50 + "\n\n")

            f.write("STATES\n\n")

            for state in data["states"]:

                f.write(
                    f"{state['name']} | "
                    f"Output: "
                    f"{state['output']}\n"
                )

            f.write("\nTRANSITIONS\n\n")

            for trans in data["transitions"]:

                f.write(
                    f"{trans['from']} "
                    f"--[{trans['input']}]--> "
                    f"{trans['to']}\n"
                )

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

    if not data["transitions"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["transitions"]
        )

        filename = "fsm_transitions.csv"

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
# FSM STATISTICS
# =========================================================

def statistics():

    clear()

    title("FSM STATISTICS")

    total_states = len(
        data["states"]
    )

    total_transitions = len(
        data["transitions"]
    )

    print(Fore.GREEN +
          f"\nFSM Type: {data['fsm_type']}")

    print(Fore.CYAN +
          f"Total States: {total_states}")

    print(Fore.YELLOW +
          f"Total Transitions: "
          f"{total_transitions}")

    print(Fore.MAGENTA +
          f"Current State: "
          f"{data['current_state']}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO FSM")

    data["project_name"] = (
        "Traffic Light Controller"
    )

    data["fsm_type"] = "Moore"

    data["states"] = [

        {
            "name": "RED",
            "output": "100"
        },

        {
            "name": "GREEN",
            "output": "001"
        },

        {
            "name": "YELLOW",
            "output": "010"
        }
    ]

    data["transitions"] = [

        {
            "from": "RED",
            "input": "timer",
            "to": "GREEN"
        },

        {
            "from": "GREEN",
            "input": "timer",
            "to": "YELLOW"
        },

        {
            "from": "YELLOW",
            "input": "timer",
            "to": "RED"
        }
    ]

    data["current_state"] = "RED"

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo FSM demo.")

    pause()


# =========================================================
# EXPLAIN FSM
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH FSM")

    print(Fore.WHITE + """
=========================================================
1. FSM
=========================================================

FSM:
   Finite State Machine

=========================================================
2. MOORE MACHINE
=========================================================

Output phụ thuộc:
   ✓ Current State

=========================================================
3. MEALY MACHINE
=========================================================

Output phụ thuộc:
   ✓ State
   ✓ Input

=========================================================
4. STATE TRANSITION
=========================================================

FSM chuyển:
   ✓ State hiện tại
   ✓ State kế tiếp

=========================================================
5. DIGITAL DESIGN
=========================================================

Ứng dụng:
   ✓ FPGA
   ✓ ASIC
   ✓ Embedded Logic

=========================================================
6. CLOCKED SYSTEM
=========================================================

FSM hoạt động:
   ✓ Theo clock

=========================================================
7. HDL DESIGN
=========================================================

Viết bằng:
   ✓ Verilog
   ✓ VHDL

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Traffic Light
✓ UART Controller
✓ CPU Control Unit
✓ Robotics FSM
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("FSM SIMULATOR SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu FSM
[2] Set FSM project
[3] Add state
[4] Add transition
[5] View states
[6] View transitions
[7] Simulate FSM
[8] ASCII FSM viewer
[9] Timing simulation
[10] FSM statistics
[11] Export FSM report
[12] Export CSV
[13] Demo mode
[14] Giải thích FSM
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

            add_state()

        elif choice == '4':

            add_transition()

        elif choice == '5':

            view_states()

        elif choice == '6':

            view_transitions()

        elif choice == '7':

            simulate_fsm()

        elif choice == '8':

            ascii_viewer()

        elif choice == '9':

            timing_simulation()

        elif choice == '10':

            statistics()

        elif choice == '11':

            export_report()

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
Cảm ơn bạn đã sử dụng FSM Simulator.

Kiến thức đạt được:
   ✓ Finite State Machine
   ✓ Moore FSM
   ✓ Mealy FSM
   ✓ Digital Logic
   ✓ FPGA Verification
   ✓ HDL Design
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
