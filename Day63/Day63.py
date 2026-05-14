# =========================================================
#              NETWORK SPEED TEST TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Kiểm tra tốc độ mạng Internet
#
# Chức năng:
#   ✓ Kiểm tra Download Speed
#   ✓ Kiểm tra Upload Speed
#   ✓ Kiểm tra Ping
#   ✓ Hiển thị ISP
#   ✓ Hiển thị Server Speedtest
#   ✓ Hiển thị đánh giá mạng
#   ✓ Giao diện terminal hiện đại
#   ✓ Lưu kết quả vào file log
#   ✓ Demo mode an toàn
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install speedtest-cli colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python speed_test.py
#
# =========================================================

from colorama import Fore, Style, init
import speedtest
import datetime
import time
import random
import os

init(autoreset=True)

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print(Fore.CYAN + "=" * 100)


def title(text):
    line()
    print(Fore.GREEN + Style.BRIGHT + text.center(100))
    line()


def pause():
    input(Fore.YELLOW + "\nNhấn ENTER để tiếp tục...")


# =========================================================
# FILE LOG
# =========================================================

LOG_FILE = "speedtest_log.txt"

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU NETWORK SPEED TEST")

    print(Fore.WHITE + """
Speed Test Tool là công cụ dùng để:

   ✓ Đo tốc độ Internet
   ✓ Kiểm tra độ ổn định mạng
   ✓ Đo Ping
   ✓ Đánh giá chất lượng mạng
   ✓ Kiểm tra ISP

=========================================================
THÔNG SỐ KIỂM TRA
=========================================================

✓ Download Speed
✓ Upload Speed
✓ Ping / Latency
✓ ISP
✓ Server Speed Test

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Kiểm tra WiFi
✓ Gaming
✓ Streaming
✓ Server Monitoring
✓ Network Troubleshooting

=========================================================
Ý NGHĨA
=========================================================

Download:
   ✓ Tốc độ tải dữ liệu

Upload:
   ✓ Tốc độ gửi dữ liệu

Ping:
   ✓ Độ trễ mạng

Ping càng thấp:
   ✓ Mạng càng tốt
""")

    line()


# =========================================================
# GHI LOG
# =========================================================

def save_log(text):

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write(text + "\n")


# =========================================================
# ĐÁNH GIÁ TỐC ĐỘ
# =========================================================

def evaluate_speed(download, upload, ping):

    print(Fore.CYAN + "\nĐÁNH GIÁ MẠNG")

    line()

    # Download
    if download >= 100:

        print(Fore.GREEN +
              "✓ Download: RẤT NHANH")

    elif download >= 50:

        print(Fore.GREEN +
              "✓ Download: TỐT")

    elif download >= 10:

        print(Fore.YELLOW +
              "✓ Download: TRUNG BÌNH")

    else:

        print(Fore.RED +
              "✓ Download: CHẬM")

    # Upload
    if upload >= 50:

        print(Fore.GREEN +
              "✓ Upload: RẤT TỐT")

    elif upload >= 10:

        print(Fore.YELLOW +
              "✓ Upload: ỔN")

    else:

        print(Fore.RED +
              "✓ Upload: THẤP")

    # Ping
    if ping <= 20:

        print(Fore.GREEN +
              "✓ Ping: TUYỆT VỜI")

    elif ping <= 50:

        print(Fore.YELLOW +
              "✓ Ping: ỔN")

    else:

        print(Fore.RED +
              "✓ Ping: CAO")

    line()


# =========================================================
# VẼ THANH BIỂU ĐỒ
# =========================================================

def draw_bar(label, value, scale=2):

    bars = int(value / scale)

    print(Fore.GREEN +
          f"{label:<12}: " +
          "█" * bars +
          f" {value}")


# =========================================================
# SPEED TEST THẬT
# =========================================================

def real_speed_test():

    clear()

    title("REAL INTERNET SPEED TEST")

    print(Fore.YELLOW +
          "\nĐang khởi tạo speedtest...\n")

    try:

        st = speedtest.Speedtest()

        print(Fore.CYAN +
              "Đang tìm server gần nhất...")

        st.get_best_server()

        server = st.results.server

        print(Fore.GREEN +
              f"\nServer: {server['host']}")

        print(Fore.GREEN +
              f"ISP   : {st.results.client['isp']}")

        print(Fore.YELLOW +
              "\nĐang đo Ping...")

        ping = round(st.results.ping, 2)

        print(Fore.YELLOW +
              "\nĐang đo Download Speed...")

        download = round(
            st.download() / 1_000_000,
            2
        )

        print(Fore.YELLOW +
              "\nĐang đo Upload Speed...")

        upload = round(
            st.upload() / 1_000_000,
            2
        )

        # HIỂN THỊ
        line()

        print(Fore.GREEN + Style.BRIGHT +
              "\nKẾT QUẢ SPEED TEST")

        line()

        print(Fore.CYAN +
              f"Ping           : {ping} ms")

        print(Fore.GREEN +
              f"Download Speed : {download} Mbps")

        print(Fore.YELLOW +
              f"Upload Speed   : {upload} Mbps")

        # BAR CHART
        print(Fore.MAGENTA +
              "\nBIỂU ĐỒ TỐC ĐỘ\n")

        draw_bar("DOWNLOAD", download)

        draw_bar("UPLOAD", upload)

        line()

        evaluate_speed(download, upload, ping)

        # GHI LOG
        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log = (
            f"[{timestamp}] "
            f"Ping={ping}ms | "
            f"Download={download}Mbps | "
            f"Upload={upload}Mbps"
        )

        save_log(log)

        print(Fore.GREEN +
              f"\nĐã lưu log vào: {LOG_FILE}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi speed test:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO SPEED TEST")

    print(Fore.CYAN +
          "\nĐang mô phỏng kiểm tra mạng...\n")

    time.sleep(1)

    ping = round(random.uniform(5, 80), 2)

    download = round(random.uniform(20, 300), 2)

    upload = round(random.uniform(10, 150), 2)

    print(Fore.GREEN +
          f"Ping           : {ping} ms")

    time.sleep(1)

    print(Fore.GREEN +
          f"Download Speed : {download} Mbps")

    time.sleep(1)

    print(Fore.GREEN +
          f"Upload Speed   : {upload} Mbps")

    print(Fore.MAGENTA +
          "\nBIỂU ĐỒ TỐC ĐỘ\n")

    draw_bar("DOWNLOAD", download)

    draw_bar("UPLOAD", upload)

    evaluate_speed(download, upload, ping)

    pause()


# =========================================================
# XEM LOG
# =========================================================

def view_logs():

    clear()

    title("LỊCH SỬ SPEED TEST")

    if not os.path.exists(LOG_FILE):

        print(Fore.RED +
              "\nChưa có log.")

    else:

        with open(LOG_FILE,
                  "r",
                  encoding="utf-8") as f:

            content = f.read()

            if content.strip():

                print(Fore.GREEN +
                      "\n" + content)

            else:

                print(Fore.RED +
                      "\nLog trống.")

    pause()


# =========================================================
# GIẢI THÍCH CHI TIẾT
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH SPEED TEST")

    print(Fore.WHITE + """
=========================================================
1. DOWNLOAD SPEED
=========================================================

Là tốc độ tải dữ liệu từ Internet.

Ứng dụng:
   ✓ Xem video
   ✓ Download file
   ✓ Streaming

=========================================================
2. UPLOAD SPEED
=========================================================

Là tốc độ gửi dữ liệu lên Internet.

Ứng dụng:
   ✓ Upload file
   ✓ Livestream
   ✓ Cloud Backup

=========================================================
3. PING / LATENCY
=========================================================

Là độ trễ mạng.

Đơn vị:
   milliseconds (ms)

Ping thấp:
   ✓ Gaming tốt
   ✓ Call ổn định

=========================================================
4. ISP
=========================================================

ISP = Nhà cung cấp Internet.

Ví dụ:
   ✓ Viettel
   ✓ FPT
   ✓ VNPT

=========================================================
5. SPEEDTEST SERVER
=========================================================

Server dùng để đo tốc độ.

Thường chọn:
   ✓ Server gần nhất

=========================================================
6. Mbps
=========================================================

Mbps:
   Megabit per second

1 Byte = 8 bit

=========================================================
7. ỨNG DỤNG
=========================================================

✓ Kiểm tra WiFi
✓ Gaming
✓ Streaming
✓ Monitoring
✓ Network Troubleshooting
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("NETWORK SPEED TEST TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu Speed Test
[2] Kiểm tra tốc độ mạng thật
[3] Demo mode
[4] Xem lịch sử log
[5] Giải thích chi tiết
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

            real_speed_test()

        elif choice == '3':

            demo_mode()

        elif choice == '4':

            view_logs()

        elif choice == '5':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Network Speed Test Tool.

Kiến thức đạt được:
   ✓ Download Speed
   ✓ Upload Speed
   ✓ Ping
   ✓ ISP
   ✓ Internet Monitoring
   ✓ Network Performance
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
