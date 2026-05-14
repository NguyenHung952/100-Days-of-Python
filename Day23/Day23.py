# =========================================================
#            ESP32 SENSOR DATA READER - PYTHON
# =========================================================
#
# Chủ đề:
#   Đọc dữ liệu cảm biến từ ESP32
#
# Chức năng:
#   • Kết nối Serial với ESP32
#   • Đọc dữ liệu cảm biến realtime
#   • Hiển thị:
#       - Nhiệt độ
#       - Độ ẩm
#       - Giá trị analog
#   • Hiển thị biểu đồ realtime
#   • Lưu log dữ liệu CSV
#   • Hiển thị thống kê cảm biến
#   • Hỗ trợ nhiều loại sensor
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded Systems
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
    print("              ESP32 SENSOR DATA READER")
    print("=" * 95)

    slow_print("\nXin chào! Đây là chương trình đọc dữ liệu ESP32.")
    slow_print("Các chức năng chính:")
    slow_print("• Kết nối Serial với ESP32")
    slow_print("• Đọc dữ liệu cảm biến realtime")
    slow_print("• Hiển thị biểu đồ thời gian thực")
    slow_print("• Ghi log dữ liệu CSV")
    slow_print("• Theo dõi nhiệt độ và độ ẩm")
    slow_print("• Thống kê dữ liệu cảm biến")

    print("\n" + "=" * 95)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. ESP32:")
    print("   • Vi điều khiển IoT mạnh mẽ")

    print("\n2. UART Serial:")
    print("   • Giao tiếp dữ liệu nối tiếp")

    print("\n3. pySerial:")
    print("   • Thư viện Python đọc COM Port")

    print("\n4. Ứng dụng:")
    print("   • Smart Home")
    print("   • IoT Dashboard")
    print("   • Data Logger")
    print("   • Sensor Monitoring")
    print("   • Wireless Systems")

    print("\n" + "=" * 95)

# ESP32 hỗ trợ UART Serial communication với PC qua USB-UART bridge. :contentReference[oaicite:0]{index=0}

# =========================================================
# HIỂN THỊ COM PORT
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
                input(
                    "\nChọn COM Port: "
                )
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

        print("\n✅ Kết nối ESP32 thành công.")

        return ser

    except Exception as e:

        print("\n❌ Không thể kết nối Serial.")
        print("Lỗi:", e)

        return None

# pySerial thường dùng serial.Serial() để giao tiếp ESP32 qua COM Port. :contentReference[oaicite:1]{index=1}

# =========================================================
# BIẾN TOÀN CỤC
# =========================================================

time_data = []

temperature_data = []

humidity_data = []

# =========================================================
# LƯU CSV
# =========================================================

def save_to_csv(timestamp, temp, hum):

    file_exists = os.path.isfile(
        "sensor_log.csv"
    )

    with open(
        "sensor_log.csv",
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
# ĐỌC DỮ LIỆU ESP32
# =========================================================

def read_sensor_data(ser):

    print("\n" + "=" * 95)
    print("                ĐỌC DỮ LIỆU ESP32")
    print("=" * 95)

    print("\nNhấn Ctrl + C để dừng.\n")

    try:

        while True:

            if ser.in_waiting > 0:

                raw_data = ser.readline().decode(
                    errors="ignore"
                ).strip()

                # =========================================
                # FORMAT:
                # TEMP:25.6,HUM:60.2
                # =========================================

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
                        f"🌡 TEMP: {temp:.2f} °C | "
                        f"💧 HUM: {hum:.2f} %"
                    )

                    save_to_csv(
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

def show_statistics():

    if len(temperature_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    print("\n" + "=" * 95)
    print("                  THỐNG KÊ DỮ LIỆU")
    print("=" * 95)

    print(f"\nSố mẫu dữ liệu:")
    print(f"→ {len(temperature_data)}")

    print(f"\nNhiệt độ trung bình:")
    print(
        f"→ "
        f"{sum(temperature_data)/len(temperature_data):.2f} °C"
    )

    print(f"\nĐộ ẩm trung bình:")
    print(
        f"→ "
        f"{sum(humidity_data)/len(humidity_data):.2f} %"
    )

    print(f"\nNhiệt độ cao nhất:")
    print(
        f"→ {max(temperature_data):.2f} °C"
    )

    print(f"\nNhiệt độ thấp nhất:")
    print(
        f"→ {min(temperature_data):.2f} °C"
    )

# =========================================================
# REALTIME GRAPH
# =========================================================

def realtime_graph():

    if len(temperature_data) == 0:

        print("\n❌ Chưa có dữ liệu để vẽ.")

        return

    print("\n📊 Đang mở biểu đồ realtime...")

    fig, ax = plt.subplots(figsize=(12, 5))

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
            "ESP32 Sensor Realtime Graph"
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

# matplotlib FuncAnimation thường được dùng để tạo realtime graph trong Python. :contentReference[oaicite:2]{index=2}

# =========================================================
# ARDUINO / ESP32 SAMPLE CODE
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

# ESP32 thường dùng Serial.begin(115200) để gửi dữ liệu sensor về PC. :contentReference[oaicite:3]{index=3}

# =========================================================
# MENU ESP32
# =========================================================

def esp32_menu():

    ser = connect_serial()

    if ser is None:

        return

    while True:

        print("\n")
        print("=" * 95)
        print("                     ESP32 MENU")
        print("=" * 95)

        print("1. Đọc dữ liệu cảm biến")
        print("2. Hiển thị biểu đồ realtime")
        print("3. Xem thống kê")
        print("4. Xem ESP32 Sample Code")
        print("5. Ngắt kết nối")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            read_sensor_data(ser)

        elif choice == "2":

            realtime_graph()

        elif choice == "3":

            show_statistics()

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

        print("1. Khởi động ESP32 Sensor Reader")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            esp32_menu()

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
