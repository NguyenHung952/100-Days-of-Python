# =========================================================
#        SMART SOIL MOISTURE MONITOR - PYTHON
# =========================================================
#
# Chủ đề:
#   Giám sát độ ẩm đất thông minh
#
# Chức năng:
#   • Đọc dữ liệu cảm biến độ ẩm đất realtime
#   • Kết nối ESP32 / Arduino qua Serial
#   • Hiển thị dashboard realtime
#   • Cảnh báo đất khô
#   • Phân tích trạng thái cây trồng
#   • Ghi log CSV
#   • Hiển thị biểu đồ thời gian thực
#   • Mô phỏng hệ thống tưới tự động
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded Systems
#   • Smart Agriculture
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
# WINDOWS ALERT
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
    print("          SMART SOIL MOISTURE MONITOR")
    print("=" * 100)

    slow_print("\nXin chào! Đây là hệ thống giám sát độ ẩm đất thông minh.")
    slow_print("Các chức năng chính:")
    slow_print("• Đọc cảm biến độ ẩm đất realtime")
    slow_print("• Dashboard biểu đồ thời gian thực")
    slow_print("• Cảnh báo đất khô")
    slow_print("• Theo dõi trạng thái cây trồng")
    slow_print("• Ghi log dữ liệu CSV")
    slow_print("• Mô phỏng tưới nước tự động")
    slow_print("• Hỗ trợ ESP32 / Arduino")

    print("\n" + "=" * 100)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Soil Moisture Sensor:")
    print("   • Cảm biến đo độ ẩm đất")

    print("\n2. Nguyên lý:")
    print("   • Đất càng ẩm → giá trị ADC càng thấp")
    print("   • Đất càng khô → giá trị ADC càng cao")

    print("\n3. Ứng dụng:")
    print("   • Smart Agriculture")
    print("   • IoT Farming")
    print("   • Greenhouse")
    print("   • Hệ thống tưới tự động")

    print("\n4. Hệ thống hỗ trợ:")
    print("   • ESP32")
    print("   • Arduino")
    print("   • UART Serial")
    print("   • Dashboard Python")

    print("\n5. Tính năng thông minh:")
    print("   • Cảnh báo đất khô")
    print("   • Gợi ý tưới cây")
    print("   • Theo dõi độ ẩm realtime")

    print("\n" + "=" * 100)

# Cảm biến độ ẩm đất thường dùng với ESP32 cho hệ thống Smart Agriculture và IoT. :contentReference[oaicite:0]{index=0}

# =========================================================
# DANH SÁCH COM PORT
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

# ESP32 hỗ trợ ADC 12-bit và thường dùng để đọc cảm biến độ ẩm đất realtime. :contentReference[oaicite:1]{index=1}

# =========================================================
# BIẾN TOÀN CỤC
# =========================================================

time_data = []

moisture_data = []

# =========================================================
# LƯU CSV
# =========================================================

def save_csv(timestamp, moisture):

    file_exists = os.path.isfile(
        "soil_moisture_log.csv"
    )

    with open(
        "soil_moisture_log.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "Moisture"
            ])

        writer.writerow([
            timestamp,
            moisture
        ])

# =========================================================
# PHÂN TÍCH ĐỘ ẨM
# =========================================================

def moisture_status(value):

    if value < 30:

        return "🌊 Đất rất ẩm"

    elif value < 60:

        return "🌱 Độ ẩm tốt"

    elif value < 80:

        return "⚠️ Đất hơi khô"

    else:

        return "🚨 Đất rất khô"

# =========================================================
# CẢNH BÁO
# =========================================================

def moisture_alert(value):

    if value >= 80:

        print("\n🚨 CẢNH BÁO: ĐẤT RẤT KHÔ!")

        print("💧 Khuyến nghị: Tưới nước ngay.")

        if WINDOWS_SOUND:

            winsound.Beep(2000, 700)

    elif value >= 60:

        print("\n⚠️ ĐẤT ĐANG KHÔ.")

        print("💧 Nên tưới cây sớm.")

        if WINDOWS_SOUND:

            winsound.Beep(1200, 300)

# =========================================================
# ĐỌC DỮ LIỆU SENSOR
# =========================================================

def read_sensor_data(ser):

    print("\n📡 Đang đọc dữ liệu độ ẩm đất...")
    print("Nhấn Ctrl + C để dừng.\n")

    try:

        while True:

            if ser.in_waiting > 0:

                raw_data = ser.readline().decode(
                    errors="ignore"
                ).strip()

                # FORMAT:
                # MOISTURE:65

                try:

                    moisture = int(
                        raw_data.split(":")[1]
                    )

                    current_time = time.strftime(
                        "%H:%M:%S"
                    )

                    time_data.append(current_time)

                    moisture_data.append(moisture)

                    print(
                        f"[{current_time}] "
                        f"🌱 Moisture: {moisture}%"
                    )

                    print(
                        f"Trạng thái: "
                        f"{moisture_status(moisture)}"
                    )

                    moisture_alert(moisture)

                    save_csv(
                        current_time,
                        moisture
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

    if len(moisture_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    avg_moisture = (
        sum(moisture_data)
        / len(moisture_data)
    )

    print("\n" + "=" * 100)
    print("                 THỐNG KÊ ĐỘ ẨM ĐẤT")
    print("=" * 100)

    print(f"\nSố mẫu dữ liệu:")
    print(f"→ {len(moisture_data)}")

    print(f"\nĐộ ẩm trung bình:")
    print(f"→ {avg_moisture:.2f}%")

    print(f"\nĐộ ẩm cao nhất:")
    print(f"→ {max(moisture_data)}%")

    print(f"\nĐộ ẩm thấp nhất:")
    print(f"→ {min(moisture_data)}%")

    print("\nĐánh giá:")

    print(
        f"→ {moisture_status(avg_moisture)}"
    )

# =========================================================
# DASHBOARD REALTIME
# =========================================================

def realtime_dashboard():

    if len(moisture_data) == 0:

        print("\n❌ Chưa có dữ liệu.")

        return

    print("\n📊 Đang mở dashboard realtime...")

    fig, ax = plt.subplots(
        figsize=(12, 5)
    )

    def update(frame):

        ax.clear()

        ax.plot(
            moisture_data,
            linewidth=2,
            label="Soil Moisture"
        )

        ax.axhline(
            y=60,
            linestyle="--",
            label="Dry Warning"
        )

        ax.axhline(
            y=80,
            linestyle="--",
            label="Danger Level"
        )

        ax.set_title(
            "Smart Soil Moisture Dashboard"
        )

        ax.set_xlabel("Sample")

        ax.set_ylabel("Moisture (%)")

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
#define SOIL_SENSOR 34

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    int rawValue = analogRead(SOIL_SENSOR);

    int moisture = map(
        rawValue,
        4095,
        1200,
        0,
        100
    );

    moisture = constrain(
        moisture,
        0,
        100
    );

    Serial.print("MOISTURE:");

    Serial.println(moisture);

    delay(1000);
}
'''

    print(code)

# ESP32 thường dùng analogRead() để đọc cảm biến độ ẩm đất và gửi dữ liệu qua Serial. :contentReference[oaicite:3]{index=3}

# =========================================================
# MÔ PHỎNG TƯỚI TỰ ĐỘNG
# =========================================================

def auto_irrigation_demo():

    print("\n" + "=" * 100)
    print("               MÔ PHỎNG TƯỚI TỰ ĐỘNG")
    print("=" * 100)

    moisture = int(
        input(
            "\nNhập độ ẩm đất hiện tại (%): "
        )
    )

    print("\nĐang phân tích...")

    time.sleep(1)

    if moisture < 40:

        print("\n🚿 BẬT HỆ THỐNG TƯỚI.")

        print("→ Đất đang quá khô.")

    elif moisture < 70:

        print("\n🌱 Độ ẩm ổn định.")

        print("→ Chưa cần tưới.")

    else:

        print("\n🌊 Đất đang rất ẩm.")

        print("→ Không cần tưới.")

# =========================================================
# MENU HỆ THỐNG
# =========================================================

def soil_monitor_menu():

    ser = connect_serial()

    if ser is None:

        return

    while True:

        print("\n")
        print("=" * 100)
        print("                  SOIL MONITOR MENU")
        print("=" * 100)

        print("1. Đọc dữ liệu độ ẩm đất")
        print("2. Dashboard realtime")
        print("3. Xem thống kê")
        print("4. Mô phỏng tưới tự động")
        print("5. Xem ESP32 Sample Code")
        print("6. Ngắt kết nối")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            read_sensor_data(ser)

        elif choice == "2":

            realtime_dashboard()

        elif choice == "3":

            statistics()

        elif choice == "4":

            auto_irrigation_demo()

        elif choice == "5":

            show_esp32_code()

        elif choice == "6":

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

        print("1. Khởi động hệ thống giám sát")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            soil_monitor_menu()

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
