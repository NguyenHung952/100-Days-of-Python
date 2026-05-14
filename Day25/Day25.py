# =========================================================
#              IOT GAS ALERT SYSTEM - PYTHON
# =========================================================
#
# Chủ đề:
#   Hệ thống cảnh báo gas IoT
#
# Chức năng:
#   • Đọc dữ liệu cảm biến gas MQ2/MQ135
#   • Kết nối ESP32 / Arduino qua Serial
#   • Hiển thị nồng độ gas realtime
#   • Dashboard biểu đồ thời gian thực
#   • Cảnh báo khí gas nguy hiểm
#   • Còi cảnh báo bằng Python
#   • Lưu log CSV
#   • Thống kê dữ liệu cảm biến
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded Systems
#   • Smart Home
#   • ESP32 / Arduino
#
# Thư viện cần:
#   pip install pyserial matplotlib numpy
#
# =========================================================

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import csv
import time
import os

# =========================================================
# WINDOWS BEEP
# =========================================================

try:

    import winsound

    WINDOWS_SOUND = True

except:

    WINDOWS_SOUND = False

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

    print("=" * 100)
    print("                IOT GAS ALERT SYSTEM")
    print("=" * 100)

    slow_print("\nXin chào! Đây là hệ thống cảnh báo gas IoT.")
    slow_print("Các chức năng chính:")
    slow_print("• Đọc dữ liệu cảm biến gas MQ2 / MQ135")
    slow_print("• Hiển thị nồng độ gas realtime")
    slow_print("• Dashboard biểu đồ thời gian thực")
    slow_print("• Cảnh báo gas nguy hiểm")
    slow_print("• Ghi log dữ liệu CSV")
    slow_print("• Hệ thống còi cảnh báo")
    slow_print("• Theo dõi an toàn môi trường")

    print("\n" + "=" * 100)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. MQ2 / MQ135:")
    print("   • Cảm biến phát hiện khí gas")

    print("\n2. Khí có thể phát hiện:")
    print("   • LPG")
    print("   • Methane")
    print("   • Smoke")
    print("   • CO2")
    print("   • Alcohol")

    print("\n3. Ứng dụng:")
    print("   • Smart Home")
    print("   • Industrial Safety")
    print("   • IoT Monitoring")
    print("   • Hệ thống cảnh báo cháy")

    print("\n4. Hệ thống hỗ trợ:")
    print("   • ESP32")
    print("   • Arduino")
    print("   • UART Serial")
    print("   • Dashboard Python")

    print("\n" + "=" * 100)

# MQ-2 và MQ-135 thường dùng trong hệ thống IoT phát hiện khí gas và chất lượng không khí. :contentReference[oaicite:0]{index=0}

# =========================================================
# HIỂN THỊ COM PORT
# =========================================================

def list_com_ports():

    print("\n" + "=" * 100)
    print("                    DANH SÁCH COM PORT")
    print("=" * 100)

    ports = serial.tools.list_ports.comports()

    port_list = []

    for index, port in enumerate(ports):

        print(f"\n[{index}] {port.device}")
        print(f"    Mô tả: {port.description}")

        port_list.append(port.device)

    if len(port_list) == 0:

        print("\n❌ Không tìm thấy COM Port.")

    return port_list

# =========================================================
# KẾT NỐI SERIAL
# =========================================================

def connect_serial():

    ports = list_com_ports()

    if len(ports) == 0:

        return None

    while True:

        try:

            index = int(
                input("\nChọn COM Port: ")
            )

            if index < 0 or index >= len(ports):

                print("❌ COM Port không hợp lệ.")

                continue

            break

        except:

            print("❌ Dữ liệu không hợp lệ.")

    baudrate = int(
        input(
            "\nNhập Baudrate "
            "(VD: 115200): "
        )
    )

    try:

        ser = serial.Serial(
            ports[index],
            baudrate,
            timeout=1
        )

        time.sleep(2)

        print("\n✅ Kết nối ESP32/Arduino thành công.")

        return ser

    except Exception as e:

        print("\n❌ Không thể kết nối Serial.")
        print("Lỗi:", e)

        return None

# pySerial thường dùng để giao tiếp UART giữa Python và ESP32/Arduino. :contentReference[oaicite:1]{index=1}

# =========================================================
# DỮ LIỆU TOÀN CỤC
# =========================================================

time_data = []

gas_data = []

# =========================================================
# LƯU CSV
# =========================================================

def save_csv(timestamp, gas_value):

    file_exists = os.path.isfile(
        "gas_log.csv"
    )

    with open(
        "gas_log.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "GasValue"
            ])

        writer.writerow([
            timestamp,
            gas_value
        ])

# =========================================================
# CẢNH BÁO
# =========================================================

def gas_alert(gas_value):

    if gas_value >= 700:

        print("\n🚨 NGUY HIỂM: GAS RẤT CAO!")

        if WINDOWS_SOUND:

            winsound.Beep(2000, 700)

    elif gas_value >= 400:

        print("\n⚠️ CẢNH BÁO: PHÁT HIỆN GAS!")

        if WINDOWS_SOUND:

            winsound.Beep(1200, 400)

# =========================================================
# ĐỌC DỮ LIỆU SENSOR
# =========================================================

def read_sensor_data(ser):

    print("\n📡 Đang đọc dữ liệu gas realtime...")
    print("Nhấn Ctrl + C để dừng.\n")

    try:

        while True:

            if ser.in_waiting > 0:

                raw_data = ser.readline().decode(
                    errors="ignore"
                ).strip()

                # FORMAT:
                # GAS:350

                try:

                    gas_value = int(
                        raw_data.split(":")[1]
                    )

                    current_time = time.strftime(
                        "%H:%M:%S"
                    )

                    time_data.append(current_time)

                    gas_data.append(gas_value)

                    print(
                        f"[{current_time}] "
                        f"⛽ GAS: {gas_value}"
                    )

                    gas_alert(gas_value)

                    save_csv(
                        current_time,
                        gas_value
                    )

                except:

                    print(
                        "⚠️ Dữ liệu lỗi:",
                        raw_data
                    )

    except KeyboardInterrupt:

        print("\n⛔ Dừng đọc dữ liệu.")

# =========================================================
# THỐNG KÊ
# =========================================================

def statistics():

    if len(gas_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    print("\n" + "=" * 100)
    print("                    THỐNG KÊ GAS")
    print("=" * 100)

    avg_gas = sum(gas_data) / len(gas_data)

    print(f"\nSố mẫu dữ liệu:")
    print(f"→ {len(gas_data)}")

    print(f"\nGas trung bình:")
    print(f"→ {avg_gas:.2f}")

    print(f"\nGas cao nhất:")
    print(f"→ {max(gas_data)}")

    print(f"\nGas thấp nhất:")
    print(f"→ {min(gas_data)}")

    print("\nĐánh giá:")

    if avg_gas < 300:

        print("→ Không khí an toàn")

    elif avg_gas < 600:

        print("→ Có dấu hiệu khí gas")

    else:

        print("→ Môi trường nguy hiểm")

# =========================================================
# DASHBOARD REALTIME
# =========================================================

def realtime_dashboard():

    if len(gas_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    print("\n📊 Đang mở dashboard realtime...")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    def update(frame):

        ax.clear()

        ax.plot(
            gas_data,
            linewidth=2,
            label="Gas Level"
        )

        ax.axhline(
            y=400,
            linestyle="--",
            label="Warning Level"
        )

        ax.axhline(
            y=700,
            linestyle="--",
            label="Danger Level"
        )

        ax.set_title(
            "IoT Gas Monitoring Dashboard"
        )

        ax.set_xlabel("Sample")

        ax.set_ylabel("Gas Value")

        ax.grid(True)

        ax.legend()

    animation = FuncAnimation(
        fig,
        update,
        interval=1000
    )

    plt.tight_layout()

    plt.show()

# FuncAnimation thường được dùng để tạo dashboard realtime bằng matplotlib. :contentReference[oaicite:2]{index=2}

# =========================================================
# ESP32 SAMPLE CODE
# =========================================================

def show_esp32_code():

    print("\n" + "=" * 100)
    print("                    ESP32 SAMPLE CODE")
    print("=" * 100)

    code = r'''
#define MQ2_PIN 34

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    int gasValue = analogRead(MQ2_PIN);

    Serial.print("GAS:");

    Serial.println(gasValue);

    delay(1000);
}
'''

    print(code)

# MQ-2 thường dùng analogRead() để đọc nồng độ khí gas trên ESP32/Arduino. :contentReference[oaicite:3]{index=3}

# =========================================================
# MENU HỆ THỐNG
# =========================================================

def gas_system_menu():

    ser = connect_serial()

    if ser is None:

        return

    while True:

        print("\n")
        print("=" * 100)
        print("                     GAS SYSTEM MENU")
        print("=" * 100)

        print("1. Đọc dữ liệu gas realtime")
        print("2. Dashboard realtime")
        print("3. Xem thống kê")
        print("4. Xem ESP32 Sample Code")
        print("5. Ngắt kết nối")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            read_sensor_data(ser)

        elif choice == "2":

            realtime_dashboard()

        elif choice == "3":

            statistics()

        elif choice == "4":

            show_esp32_code()

        elif choice == "5":

            ser.close()

            print("\n🔌 Đã đóng Serial Port.")

            break

        else:

            print("\n❌ Lựa chọn không hợp lệ.")

# =========================================================
# MENU CHÍNH
# =========================================================

def menu():

    while True:

        print("\n")
        print("=" * 100)
        print("                    MENU CHỨC NĂNG")
        print("=" * 100)

        print("1. Khởi động hệ thống cảnh báo gas")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            gas_system_menu()

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
