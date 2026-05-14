# =========================================================
#         REALTIME TEMPERATURE DASHBOARD - PYTHON
# =========================================================
#
# Chủ đề:
#   Dashboard nhiệt độ thời gian thực
#
# Chức năng:
#   • Dashboard realtime bằng Python
#   • Hiển thị:
#       - Nhiệt độ
#       - Độ ẩm
#       - Biểu đồ thời gian thực
#   • Cảnh báo nhiệt độ cao
#   • Ghi log CSV
#   • Hiển thị thống kê cảm biến
#   • Hỗ trợ ESP32 / Arduino
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded
#   • ESP32 / Arduino
#   • Sensor Monitoring
#
# Thư viện cần:
#   pip install pyserial matplotlib
#
# =========================================================

import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import time
import os

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

    print("=" * 95)
    print("           REALTIME TEMPERATURE DASHBOARD")
    print("=" * 95)

    slow_print("\nXin chào! Đây là dashboard nhiệt độ realtime.")
    slow_print("Các chức năng chính:")
    slow_print("• Đọc dữ liệu ESP32 / Arduino")
    slow_print("• Hiển thị nhiệt độ realtime")
    slow_print("• Hiển thị độ ẩm realtime")
    slow_print("• Dashboard biểu đồ động")
    slow_print("• Ghi log dữ liệu CSV")
    slow_print("• Cảnh báo nhiệt độ cao")
    slow_print("• Theo dõi dữ liệu cảm biến")

    print("\n" + "=" * 95)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Realtime Dashboard:")
    print("   • Hiển thị dữ liệu thời gian thực")

    print("\n2. Sensor Monitoring:")
    print("   • Theo dõi cảm biến liên tục")

    print("\n3. Matplotlib Animation:")
    print("   • Cập nhật biểu đồ realtime")

    print("\n4. Ứng dụng:")
    print("   • Smart Home")
    print("   • IoT")
    print("   • Weather Station")
    print("   • Industrial Monitoring")
    print("   • Sensor Dashboard")

    print("\n" + "=" * 95)

# matplotlib.animation.FuncAnimation thường dùng để cập nhật đồ thị realtime trong Python dashboard. :contentReference[oaicite:0]{index=0}

# =========================================================
# DANH SÁCH COM PORT
# =========================================================

def list_com_ports():

    print("\n" + "=" * 95)
    print("                  DANH SÁCH COM PORT")
    print("=" * 95)

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

        print("\n✅ Kết nối thành công.")

        return ser

    except Exception as e:

        print("\n❌ Không thể kết nối.")
        print("Lỗi:", e)

        return None

# pySerial được dùng phổ biến để giao tiếp UART giữa Python và ESP32/Arduino. :contentReference[oaicite:1]{index=1}

# =========================================================
# DỮ LIỆU TOÀN CỤC
# =========================================================

time_data = []

temperature_data = []

humidity_data = []

# =========================================================
# LƯU CSV
# =========================================================

def save_csv(timestamp, temp, hum):

    file_exists = os.path.isfile(
        "temperature_log.csv"
    )

    with open(
        "temperature_log.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "Temperature",
                "Humidity"
            ])

        writer.writerow([
            timestamp,
            temp,
            hum
        ])

# =========================================================
# ĐỌC SERIAL
# =========================================================

def read_sensor_data(ser):

    print("\n📡 Đang đọc dữ liệu realtime...")
    print("Nhấn Ctrl + C để dừng.\n")

    try:

        while True:

            if ser.in_waiting > 0:

                raw_data = ser.readline().decode(
                    errors="ignore"
                ).strip()

                # FORMAT:
                # TEMP:30.5,HUM:65

                try:

                    parts = raw_data.split(",")

                    temp = float(
                        parts[0].split(":")[1]
                    )

                    hum = float(
                        parts[1].split(":")[1]
                    )

                    current_time = time.strftime(
                        "%H:%M:%S"
                    )

                    time_data.append(current_time)

                    temperature_data.append(temp)

                    humidity_data.append(hum)

                    print(
                        f"[{current_time}] "
                        f"🌡 {temp:.2f}°C | "
                        f"💧 {hum:.2f}%"
                    )

                    # =============================
                    # CẢNH BÁO NHIỆT ĐỘ
                    # =============================

                    if temp >= 35:

                        print(
                            "⚠️ CẢNH BÁO:"
                            " Nhiệt độ cao!"
                        )

                    save_csv(
                        current_time,
                        temp,
                        hum
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

    if len(temperature_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    print("\n" + "=" * 95)
    print("                  THỐNG KÊ DỮ LIỆU")
    print("=" * 95)

    avg_temp = (
        sum(temperature_data)
        / len(temperature_data)
    )

    avg_hum = (
        sum(humidity_data)
        / len(humidity_data)
    )

    print(f"\nSố mẫu dữ liệu:")
    print(f"→ {len(temperature_data)}")

    print(f"\nNhiệt độ trung bình:")
    print(f"→ {avg_temp:.2f} °C")

    print(f"\nĐộ ẩm trung bình:")
    print(f"→ {avg_hum:.2f} %")

    print(f"\nNhiệt độ cao nhất:")
    print(f"→ {max(temperature_data):.2f} °C")

    print(f"\nNhiệt độ thấp nhất:")
    print(f"→ {min(temperature_data):.2f} °C")

# =========================================================
# DASHBOARD REALTIME
# =========================================================

def realtime_dashboard():

    if len(temperature_data) == 0:

        print("\n❌ Chưa có dữ liệu để hiển thị.")

        return

    print("\n📊 Đang mở Dashboard realtime...")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    def update(frame):

        ax.clear()

        ax.plot(
            temperature_data,
            linewidth=2,
            label="Temperature"
        )

        ax.plot(
            humidity_data,
            linewidth=2,
            label="Humidity"
        )

        ax.set_title(
            "Realtime Temperature Dashboard"
        )

        ax.set_xlabel("Sample")

        ax.set_ylabel("Value")

        ax.grid(True)

        ax.legend()

    animation = FuncAnimation(
        fig,
        update,
        interval=1000
    )

    plt.tight_layout()

    plt.show()

# FuncAnimation hỗ trợ cập nhật biểu đồ realtime trong dashboard Python. :contentReference[oaicite:2]{index=2}

# =========================================================
# ESP32 SAMPLE CODE
# =========================================================

def show_esp32_code():

    print("\n" + "=" * 95)
    print("                 ESP32 SAMPLE CODE")
    print("=" * 95)

    code = r'''
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup()
{
    Serial.begin(115200);

    dht.begin();
}

void loop()
{
    float temp = dht.readTemperature();

    float hum = dht.readHumidity();

    Serial.print("TEMP:");

    Serial.print(temp);

    Serial.print(",");

    Serial.print("HUM:");

    Serial.println(hum);

    delay(1000);
}
'''

    print(code)

# =========================================================
# MENU DASHBOARD
# =========================================================

def dashboard_menu():

    ser = connect_serial()

    if ser is None:

        return

    while True:

        print("\n")
        print("=" * 95)
        print("                    DASHBOARD MENU")
        print("=" * 95)

        print("1. Đọc dữ liệu realtime")
        print("2. Mở dashboard realtime")
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
        print("=" * 95)
        print("                    MENU CHỨC NĂNG")
        print("=" * 95)

        print("1. Khởi động Dashboard")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            dashboard_menu()

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
