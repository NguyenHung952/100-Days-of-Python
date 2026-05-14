# =========================================================
#         ARDUINO SERIAL COMMUNICATION - PYTHON
# =========================================================
#
# Chủ đề:
#   Giao tiếp Serial với Arduino
#
# Chức năng:
#   • Kết nối Serial COM với Arduino
#   • Gửi dữ liệu từ Python → Arduino
#   • Nhận dữ liệu từ Arduino → Python
#   • Hiển thị dữ liệu realtime
#   • Điều khiển LED bằng Python
#   • Log dữ liệu Serial
#   • Hiển thị danh sách COM Port
#
# Phù hợp:
#   • Sinh viên Điện tử Viễn thông
#   • IoT / Embedded Systems
#   • STM32 / ESP32 / Arduino
#   • Python Automation
#
# Thư viện cần:
#   pip install pyserial
#
# =========================================================

import serial
import serial.tools.list_ports
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

    print("=" * 90)
    print("          ARDUINO SERIAL COMMUNICATION")
    print("=" * 90)

    slow_print("\nXin chào! Đây là chương trình giao tiếp Serial.")
    slow_print("Các chức năng chính:")
    slow_print("• Kết nối COM Port với Arduino")
    slow_print("• Gửi dữ liệu Serial")
    slow_print("• Nhận dữ liệu realtime")
    slow_print("• Điều khiển LED Arduino")
    slow_print("• Theo dõi dữ liệu cảm biến")
    slow_print("• Debug Serial Monitor")

    print("\n" + "=" * 90)

    print("\nKIẾN THỨC LIÊN QUAN:\n")

    print("1. Serial Communication:")
    print("   • Giao tiếp dữ liệu UART")

    print("\n2. Thông số phổ biến:")
    print("   • Baudrate: 9600")
    print("   • Data bits: 8")
    print("   • Stop bits: 1")

    print("\n3. Ứng dụng:")
    print("   • Giao tiếp Arduino")
    print("   • ESP32")
    print("   • STM32")
    print("   • IoT")
    print("   • Sensor Monitoring")

    print("\n4. Python sử dụng:")
    print("   • pySerial Library")

    print("\n" + "=" * 90)

# PySerial hỗ trợ giao tiếp serial cross-platform với Arduino và thiết bị UART. :contentReference[oaicite:0]{index=0}

# =========================================================
# HIỂN THỊ COM PORT
# =========================================================

def list_com_ports():

    print("\n" + "=" * 90)
    print("                   DANH SÁCH COM PORT")
    print("=" * 90)

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
            "\nNhập Baudrate (VD: 9600): "
        )
    )

    try:

        ser = serial.Serial(
            ports[index],
            baudrate,
            timeout=1
        )

        time.sleep(2)

        print("\n✅ Kết nối Serial thành công.")

        print(f"COM Port : {ports[index]}")
        print(f"Baudrate : {baudrate}")

        return ser

    except Exception as e:

        print("\n❌ Không thể kết nối Serial.")
        print("Lỗi:", e)

        return None

# PySerial dùng serial.Serial() để mở cổng UART/COM. :contentReference[oaicite:1]{index=1}

# =========================================================
# GỬI DỮ LIỆU
# =========================================================

def send_data(ser):

    print("\n=== GỬI DỮ LIỆU SERIAL ===")

    while True:

        data = input(
            "\nNhập dữ liệu gửi "
            "(exit để thoát): "
        )

        if data.lower() == "exit":

            break

        try:

            ser.write(
                (data + "\n").encode()
            )

            print("✅ Đã gửi:", data)

        except Exception as e:

            print("❌ Lỗi gửi dữ liệu:", e)

# =========================================================
# NHẬN DỮ LIỆU
# =========================================================

def receive_data(ser):

    print("\n=== NHẬN DỮ LIỆU SERIAL ===")
    print("Nhấn Ctrl + C để dừng.\n")

    try:

        while True:

            if ser.in_waiting > 0:

                data = ser.readline().decode(
                    errors="ignore"
                ).strip()

                print("📥 Arduino:", data)

    except KeyboardInterrupt:

        print("\n⛔ Dừng nhận dữ liệu.")

# =========================================================
# ĐIỀU KHIỂN LED
# =========================================================

def led_control(ser):

    print("\n=== ĐIỀU KHIỂN LED ===\n")

    print("1. Bật LED")
    print("2. Tắt LED")

    choice = input("\nChọn chức năng: ")

    try:

        if choice == "1":

            ser.write(b'1')

            print("\n💡 Đã gửi lệnh bật LED.")

        elif choice == "2":

            ser.write(b'0')

            print("\n🌑 Đã gửi lệnh tắt LED.")

        else:

            print("\n❌ Lựa chọn không hợp lệ.")

    except Exception as e:

        print("\n❌ Lỗi Serial:", e)

# =========================================================
# ARDUINO SAMPLE CODE
# =========================================================

def show_arduino_code():

    print("\n" + "=" * 90)
    print("                ARDUINO SAMPLE CODE")
    print("=" * 90)

    arduino_code = r'''
void setup()
{
    pinMode(13, OUTPUT);

    Serial.begin(9600);
}

void loop()
{
    if (Serial.available())
    {
        char data = Serial.read();

        if (data == '1')
        {
            digitalWrite(13, HIGH);

            Serial.println("LED ON");
        }

        else if (data == '0')
        {
            digitalWrite(13, LOW);

            Serial.println("LED OFF");
        }
    }
}
'''

    print(arduino_code)

# Arduino Serial.begin() thường dùng cùng baudrate khớp với Python pySerial. :contentReference[oaicite:2]{index=2}

# =========================================================
# MENU SERIAL
# =========================================================

def serial_menu():

    ser = connect_serial()

    if ser is None:

        return

    while True:

        print("\n")
        print("=" * 90)
        print("                    SERIAL MENU")
        print("=" * 90)

        print("1. Gửi dữ liệu")
        print("2. Nhận dữ liệu")
        print("3. Điều khiển LED")
        print("4. Xem Arduino Sample Code")
        print("5. Ngắt kết nối")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            send_data(ser)

        elif choice == "2":

            receive_data(ser)

        elif choice == "3":

            led_control(ser)

        elif choice == "4":

            show_arduino_code()

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
        print("=" * 90)
        print("                    MENU CHỨC NĂNG")
        print("=" * 90)

        print("1. Khởi động Serial Communication")
        print("2. Thoát")

        choice = input("\nChọn chức năng: ")

        if choice == "1":

            serial_menu()

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
