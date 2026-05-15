# =========================================================
#            IoT DIGITAL TWIN SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Xây dựng Digital Twin cho hệ IoT
#
# Chức năng:
#   ✓ Mô phỏng cảm biến IoT
#   ✓ Digital Twin Dashboard
#   ✓ Real-time Data Simulation
#   ✓ MQTT-style Communication
#   ✓ Device Monitoring
#   ✓ Sensor Analytics
#   ✓ Predictive Alert System
#   ✓ Data Visualization
#   ✓ ASCII IoT Visualization
#   ✓ CSV Report Export
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install matplotlib pandas numpy colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python iot_digital_twin.py
#
# =========================================================

from colorama import Fore, Style, init

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import random
import json
import os
import time
import datetime

init(autoreset=True)

# =========================================================
# DATABASE FILE
# =========================================================

DATA_FILE = "iot_digital_twin.json"

# =========================================================
# DATABASE
# =========================================================

data = {

    "project_name": "Smart Factory",

    "devices": [],

    "sensor_logs": []
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

    title("GIỚI THIỆU IOT DIGITAL TWIN")

    print(Fore.WHITE + """
IoT Digital Twin giúp:

   ✓ Mô phỏng hệ IoT thời gian thực
   ✓ Theo dõi sensor thông minh
   ✓ Digital Twin Visualization
   ✓ Dự đoán và cảnh báo thiết bị

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Device Monitoring
✓ Sensor Simulation
✓ Predictive Analytics
✓ Real-time Dashboard
✓ IoT Communication

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Smart Factory
✓ Smart City
✓ Smart Agriculture
✓ Industrial IoT
✓ AIoT Systems

=========================================================
IOT CONCEPTS
=========================================================

✓ Sensors
✓ MQTT
✓ Telemetry
✓ Cloud Monitoring
✓ Digital Twin
""")

    line()


# =========================================================
# ADD DEVICE
# =========================================================

def add_device():

    clear()

    title("ADD IOT DEVICE")

    device_name = input(
        Fore.YELLOW +
        "Tên thiết bị: "
    )

    device_type = input(
        Fore.YELLOW +
        "Loại thiết bị: "
    )

    device = {

        "name": device_name,
        "type": device_type,
        "status": "ONLINE",
        "created": str(
            datetime.datetime.now()
        )
    }

    data["devices"].append(
        device
    )

    save_data()

    print(Fore.GREEN +
          "\nĐã thêm thiết bị.")

    pause()


# =========================================================
# VIEW DEVICES
# =========================================================

def view_devices():

    clear()

    title("IOT DEVICE LIST")

    if not data["devices"]:

        print(Fore.RED +
              "\nChưa có thiết bị.")

        pause()

        return

    for index, device in enumerate(
        data["devices"],
        start=1
    ):

        print(Fore.GREEN +
              f"\n[{index}] {device['name']}")

        print(Fore.CYAN +
              f"Type   : {device['type']}")

        print(Fore.YELLOW +
              f"Status : {device['status']}")

        print(Fore.MAGENTA +
              f"Created: {device['created']}")

        line()

    pause()


# =========================================================
# SENSOR SIMULATION
# =========================================================

def sensor_simulation():

    clear()

    title("SENSOR DATA SIMULATION")

    if not data["devices"]:

        print(Fore.RED +
              "\nChưa có thiết bị IoT.")

        pause()

        return

    timestamps = []

    temperatures = []

    humidities = []

    print(Fore.GREEN +
          "\nRealtime Sensor Simulation\n")

    for i in range(10):

        temp = random.uniform(
            20,
            40
        )

        hum = random.uniform(
            40,
            90
        )

        current_time = datetime.datetime.now()

        timestamps.append(
            current_time.strftime(
                "%H:%M:%S"
            )
        )

        temperatures.append(temp)

        humidities.append(hum)

        log = {

            "time":
            str(current_time),

            "temperature":
            round(temp, 2),

            "humidity":
            round(hum, 2)
        }

        data["sensor_logs"].append(
            log
        )

        print(Fore.CYAN +
              f"[{timestamps[-1]}]")

        print(Fore.YELLOW +
              f"Temp : {temp:.2f} °C")

        print(Fore.GREEN +
              f"Hum  : {hum:.2f} %")

        line()

        time.sleep(0.5)

    save_data()

    pause()


# =========================================================
# SENSOR GRAPH
# =========================================================

def sensor_graph():

    clear()

    title("SENSOR GRAPH")

    if not data["sensor_logs"]:

        print(Fore.RED +
              "\nChưa có dữ liệu sensor.")

        pause()

        return

    temps = [

        log["temperature"]

        for log in data["sensor_logs"]
    ]

    hums = [

        log["humidity"]

        for log in data["sensor_logs"]
    ]

    plt.figure(figsize=(10, 5))

    plt.plot(
        temps,
        label="Temperature"
    )

    plt.plot(
        hums,
        label="Humidity"
    )

    plt.title(
        "IoT Sensor Dashboard"
    )

    plt.xlabel("Sample")

    plt.ylabel("Value")

    plt.legend()

    plt.grid()

    plt.show()

    pause()


# =========================================================
# DIGITAL TWIN DASHBOARD
# =========================================================

def digital_twin_dashboard():

    clear()

    title("DIGITAL TWIN DASHBOARD")

    total_devices = len(
        data["devices"]
    )

    total_logs = len(
        data["sensor_logs"]
    )

    online_devices = total_devices

    print(Fore.GREEN +
          f"\nPROJECT: "
          f"{data['project_name']}")

    line()

    print(Fore.CYAN +
          f"Total Devices : "
          f"{total_devices}")

    print(Fore.YELLOW +
          f"Online Devices: "
          f"{online_devices}")

    print(Fore.MAGENTA +
          f"Sensor Logs   : "
          f"{total_logs}")

    line()

    print(Fore.GREEN +
          "\nDIGITAL TWIN STATUS")

    print(Fore.GREEN +
          "█" * 40)

    pause()


# =========================================================
# MQTT STYLE COMMUNICATION
# =========================================================

def mqtt_simulation():

    clear()

    title("MQTT COMMUNICATION")

    topics = [

        "factory/temp",
        "factory/humidity",
        "factory/motor"
    ]

    messages = [

        "32.5C",
        "65%",
        "RUNNING"
    ]

    print(Fore.GREEN +
          "\nMQTT Message Stream\n")

    for topic, msg in zip(
        topics,
        messages
    ):

        print(Fore.CYAN +
              f"TOPIC : {topic}")

        print(Fore.YELLOW +
              f"DATA  : {msg}")

        line()

        time.sleep(1)

    data["history"] = [

        "MQTT Simulation"
    ]

    save_data()

    pause()


# =========================================================
# PREDICTIVE ALERT SYSTEM
# =========================================================

def predictive_alert():

    clear()

    title("PREDICTIVE ALERT SYSTEM")

    temp = random.uniform(
        20,
        50
    )

    vibration = random.uniform(
        0,
        10
    )

    print(Fore.GREEN +
          f"\nTemperature: "
          f"{temp:.2f} °C")

    print(Fore.CYAN +
          f"Vibration : "
          f"{vibration:.2f}")

    if temp > 40 or vibration > 7:

        print(Fore.RED +
              "\n⚠ WARNING:")

        print(Fore.RED +
              "Potential machine failure!")

    else:

        print(Fore.GREEN +
              "\nSystem Normal")

    pause()


# =========================================================
# ASCII DIGITAL TWIN VIEW
# =========================================================

def ascii_view():

    clear()

    title("ASCII DIGITAL TWIN")

    print(Fore.GREEN + """
             CLOUD SERVER
                 ||
     =========================
      IoT DIGITAL TWIN SYSTEM
     =========================
        /        |        \\
       /         |         \\
 SENSOR      GATEWAY      AI
   ||            ||         ||
DEVICE 1      DEVICE 2   DEVICE 3
""")

    pause()


# =========================================================
# DEVICE ANALYTICS
# =========================================================

def analytics():

    clear()

    title("DEVICE ANALYTICS")

    if not data["sensor_logs"]:

        print(Fore.RED +
              "\nChưa có dữ liệu.")

        pause()

        return

    temps = [

        log["temperature"]

        for log in data["sensor_logs"]
    ]

    hums = [

        log["humidity"]

        for log in data["sensor_logs"]
    ]

    avg_temp = np.mean(temps)

    avg_hum = np.mean(hums)

    print(Fore.GREEN +
          f"\nAverage Temp : "
          f"{avg_temp:.2f} °C")

    print(Fore.CYAN +
          f"Average Hum  : "
          f"{avg_hum:.2f} %")

    print(Fore.YELLOW +
          f"Total Samples: "
          f"{len(temps)}")

    pause()


# =========================================================
# EXPORT CSV REPORT
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    if not data["sensor_logs"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["sensor_logs"]
        )

        filename = "iot_sensor_report.csv"

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

    title("DEMO DIGITAL TWIN")

    print(Fore.WHITE + """
Digital Twin Demo:

=========================================================
SMART FACTORY
=========================================================

✓ Machine Monitoring
✓ Predictive Maintenance
✓ Sensor Analytics

=========================================================
SMART CITY
=========================================================

✓ Traffic Sensors
✓ Air Monitoring
✓ IoT Dashboard

=========================================================
AIOT SYSTEMS
=========================================================

✓ AI + IoT
✓ Cloud Analytics
✓ Real-time Monitoring
""")

    pause()


# =========================================================
# EXPLAIN DIGITAL TWIN
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH DIGITAL TWIN")

    print(Fore.WHITE + """
=========================================================
1. DIGITAL TWIN
=========================================================

Digital Twin:
   ✓ Bản sao số của hệ thống thật

=========================================================
2. IOT
=========================================================

IoT:
   ✓ Sensors
   ✓ Devices
   ✓ Cloud

=========================================================
3. MQTT
=========================================================

MQTT:
   ✓ Lightweight Protocol

=========================================================
4. SENSOR DATA
=========================================================

Thu thập:
   ✓ Temperature
   ✓ Humidity
   ✓ Vibration

=========================================================
5. AIOT
=========================================================

AI + IoT:
   ✓ Predictive Analytics

=========================================================
6. SMART FACTORY
=========================================================

Ứng dụng:
   ✓ Industrial Automation

=========================================================
7. CLOUD DASHBOARD
=========================================================

Theo dõi:
   ✓ Real-time Monitoring

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Smart City
✓ Smart Agriculture
✓ Smart Healthcare
✓ Industry 4.0
""")

    pause()


# =========================================================
# MAIN MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("IOT DIGITAL TWIN SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu hệ thống
[2] Add IoT Device
[3] View Devices
[4] Sensor Simulation
[5] Sensor Graph
[6] Digital Twin Dashboard
[7] MQTT Communication
[8] Predictive Alert System
[9] ASCII Digital Twin View
[10] Device Analytics
[11] Export CSV Report
[12] Demo mode
[13] Giải thích Digital Twin
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

            add_device()

        elif choice == '3':

            view_devices()

        elif choice == '4':

            sensor_simulation()

        elif choice == '5':

            sensor_graph()

        elif choice == '6':

            digital_twin_dashboard()

        elif choice == '7':

            mqtt_simulation()

        elif choice == '8':

            predictive_alert()

        elif choice == '9':

            ascii_view()
