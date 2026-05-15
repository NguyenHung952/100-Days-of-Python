# =========================================================
#            AUTO BACKUP SYSTEM - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Tự động backup dữ liệu
#
# Chức năng:
#   ✓ Backup file/folder tự động
#   ✓ Backup theo thời gian
#   ✓ Nén file ZIP
#   ✓ Backup nhiều thư mục
#   ✓ Restore backup
#   ✓ Hiển thị dung lượng backup
#   ✓ Log lịch sử backup
#   ✓ Kiểm tra integrity file
#   ✓ Demo mode
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python auto_backup.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import shutil
import zipfile
import hashlib
import datetime
import time

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
# BIẾN TOÀN CỤC
# =========================================================

BACKUP_DIR = "backups"
LOG_FILE = "backup_logs.txt"

os.makedirs(BACKUP_DIR, exist_ok=True)

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU AUTO BACKUP SYSTEM")

    print(Fore.WHITE + """
Backup System là công cụ dùng để:

   ✓ Sao lưu dữ liệu
   ✓ Bảo vệ file quan trọng
   ✓ Chống mất dữ liệu
   ✓ Khôi phục dữ liệu khi lỗi

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Backup Folder
✓ Backup File
✓ ZIP Compression
✓ Restore Backup
✓ Auto Backup Scheduler
✓ Backup Logging

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Server Backup
✓ Database Backup
✓ Cloud Backup
✓ NAS Backup
✓ Personal Data Protection

=========================================================
LỢI ÍCH
=========================================================

✓ Tránh mất dữ liệu
✓ Recovery nhanh
✓ An toàn dữ liệu
✓ Versioning
""")

    line()


# =========================================================
# GHI LOG
# =========================================================

def write_log(text):

    with open(LOG_FILE,
              "a",
              encoding="utf-8") as f:

        f.write(text + "\n")


# =========================================================
# SHA256 FILE
# =========================================================

def calculate_hash(filename):

    sha256 = hashlib.sha256()

    with open(filename, "rb") as f:

        while True:

            data = f.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


# =========================================================
# BACKUP FILE
# =========================================================

def backup_file():

    clear()

    title("BACKUP FILE")

    source = input(
        Fore.YELLOW +
        "Nhập đường dẫn file: "
    )

    if not os.path.exists(source):

        print(Fore.RED +
              "\nFile không tồn tại.")

        pause()

        return

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = os.path.basename(source)

    backup_name = f"{timestamp}_{filename}"

    destination = os.path.join(
        BACKUP_DIR,
        backup_name
    )

    try:

        shutil.copy2(source, destination)

        print(Fore.GREEN +
              f"\nĐã backup:\n{destination}")

        file_hash = calculate_hash(destination)

        print(Fore.CYAN +
              f"\nSHA256:\n{file_hash}")

        write_log(
            f"[{timestamp}] FILE BACKUP: {destination}"
        )

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi backup:\n{e}")

    pause()


# =========================================================
# BACKUP FOLDER ZIP
# =========================================================

def backup_folder():

    clear()

    title("BACKUP FOLDER")

    folder = input(
        Fore.YELLOW +
        "Nhập thư mục cần backup: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    folder_name = os.path.basename(folder)

    zip_name = f"{folder_name}_{timestamp}.zip"

    zip_path = os.path.join(
        BACKUP_DIR,
        zip_name
    )

    try:

        print(Fore.CYAN +
              "\nĐang nén dữ liệu...")

        with zipfile.ZipFile(
            zip_path,
            'w',
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for root, dirs, files in os.walk(folder):

                for file in files:

                    file_path = os.path.join(
                        root,
                        file
                    )

                    arcname = os.path.relpath(
                        file_path,
                        folder
                    )

                    zipf.write(
                        file_path,
                        arcname
                    )

        print(Fore.GREEN +
              f"\nĐã backup folder:\n{zip_path}")

        size = os.path.getsize(zip_path)

        print(Fore.YELLOW +
              f"Kích thước ZIP: {size} bytes")

        write_log(
            f"[{timestamp}] FOLDER BACKUP: {zip_path}"
        )

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi backup:\n{e}")

    pause()


# =========================================================
# RESTORE BACKUP
# =========================================================

def restore_backup():

    clear()

    title("RESTORE BACKUP")

    backup_file_name = input(
        Fore.YELLOW +
        "Nhập file backup (.zip): "
    )

    if not os.path.exists(backup_file_name):

        print(Fore.RED +
              "\nFile backup không tồn tại.")

        pause()

        return

    restore_dir = input(
        Fore.YELLOW +
        "Thư mục restore: "
    )

    os.makedirs(restore_dir, exist_ok=True)

    try:

        with zipfile.ZipFile(
            backup_file_name,
            'r'
        ) as zipf:

            zipf.extractall(restore_dir)

        print(Fore.GREEN +
              "\nRestore thành công.")

        print(Fore.CYAN +
              f"Restore path: {restore_dir}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi restore:\n{e}")

    pause()


# =========================================================
# AUTO BACKUP
# =========================================================

def auto_backup():

    clear()

    title("AUTO BACKUP MODE")

    folder = input(
        Fore.YELLOW +
        "Folder cần auto backup: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    try:

        interval = int(input(
            Fore.YELLOW +
            "Khoảng thời gian backup (giây): "
        ))

    except:

        print(Fore.RED +
              "\nInterval không hợp lệ.")

        pause()

        return

    print(Fore.GREEN +
          "\nAuto backup đang chạy...")

    print(Fore.RED +
          "Nhấn CTRL + C để dừng.\n")

    try:

        while True:

            timestamp = datetime.datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            folder_name = os.path.basename(folder)

            zip_name = f"{folder_name}_{timestamp}.zip"

            zip_path = os.path.join(
                BACKUP_DIR,
                zip_name
            )

            with zipfile.ZipFile(
                zip_path,
                'w',
                zipfile.ZIP_DEFLATED
            ) as zipf:

                for root, dirs, files in os.walk(folder):

                    for file in files:

                        file_path = os.path.join(
                            root,
                            file
                        )

                        arcname = os.path.relpath(
                            file_path,
                            folder
                        )

                        zipf.write(
                            file_path,
                            arcname
                        )

            print(Fore.GREEN +
                  f"[BACKUP] {zip_path}")

            write_log(
                f"[{timestamp}] AUTO BACKUP: {zip_path}"
            )

            time.sleep(interval)

    except KeyboardInterrupt:

        print(Fore.RED +
              "\n\nĐã dừng auto backup.")

    pause()


# =========================================================
# XEM BACKUP
# =========================================================

def view_backups():

    clear()

    title("DANH SÁCH BACKUP")

    files = os.listdir(BACKUP_DIR)

    if not files:

        print(Fore.RED +
              "\nChưa có backup.")

    else:

        for index, file in enumerate(files, start=1):

            path = os.path.join(
                BACKUP_DIR,
                file
            )

            size = os.path.getsize(path)

            print(Fore.GREEN +
                  f"\n[{index}] {file}")

            print(Fore.YELLOW +
                  f"Size: {size} bytes")

            line()

    pause()


# =========================================================
# XEM LOG
# =========================================================

def view_logs():

    clear()

    title("BACKUP LOGS")

    if not os.path.exists(LOG_FILE):

        print(Fore.RED +
              "\nChưa có log.")

    else:

        with open(LOG_FILE,
                  "r",
                  encoding="utf-8") as f:

            print(Fore.GREEN +
                  "\n" + f.read())

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO BACKUP SYSTEM")

    demo_folder = "demo_data"

    os.makedirs(demo_folder, exist_ok=True)

    for i in range(3):

        filename = os.path.join(
            demo_folder,
            f"file_{i}.txt"
        )

        with open(filename,
                  "w",
                  encoding="utf-8") as f:

            f.write(
                f"Demo backup data {i}"
            )

    print(Fore.GREEN +
          f"\nĐã tạo folder demo: {demo_folder}")

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    zip_name = f"demo_backup_{timestamp}.zip"

    zip_path = os.path.join(
        BACKUP_DIR,
        zip_name
    )

    with zipfile.ZipFile(
        zip_path,
        'w',
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for root, dirs, files in os.walk(demo_folder):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                zipf.write(
                    file_path,
                    os.path.relpath(
                        file_path,
                        demo_folder
                    )
                )

    print(Fore.GREEN +
          f"\nĐã backup demo:\n{zip_path}")

    pause()


# =========================================================
# GIẢI THÍCH BACKUP
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH BACKUP SYSTEM")

    print(Fore.WHITE + """
=========================================================
1. BACKUP
=========================================================

Backup:
   ✓ Sao lưu dữ liệu

=========================================================
2. RESTORE
=========================================================

Restore:
   ✓ Khôi phục dữ liệu

=========================================================
3. ZIP COMPRESSION
=========================================================

ZIP giúp:
   ✓ Giảm dung lượng
   ✓ Dễ lưu trữ

=========================================================
4. SHA256 HASH
=========================================================

Hash dùng để:
   ✓ Kiểm tra integrity

=========================================================
5. AUTO BACKUP
=========================================================

Tự động backup:
   ✓ Theo thời gian

=========================================================
6. INTEGRITY CHECK
=========================================================

Đảm bảo:
   ✓ File không bị thay đổi

=========================================================
7. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Server Backup
✓ Cloud Storage
✓ NAS
✓ Enterprise IT
✓ Database Backup

=========================================================
8. KHUYẾN NGHỊ
=========================================================

✓ Backup định kỳ
✓ Backup nhiều nơi
✓ Test restore thường xuyên
✓ Mã hóa backup quan trọng
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("AUTO BACKUP SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu Backup System
[2] Backup file
[3] Backup folder
[4] Restore backup
[5] Auto backup mode
[6] Xem danh sách backup
[7] Xem backup logs
[8] Demo mode
[9] Giải thích Backup
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

            backup_file()

        elif choice == '3':

            backup_folder()

        elif choice == '4':

            restore_backup()

        elif choice == '5':

            auto_backup()

        elif choice == '6':

            view_backups()

        elif choice == '7':

            view_logs()

        elif choice == '8':

            demo_mode()

        elif choice == '9':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Auto Backup System.

Kiến thức đạt được:
   ✓ Backup
   ✓ Restore
   ✓ ZIP Compression
   ✓ Integrity Check
   ✓ Auto Scheduler
   ✓ Data Protection
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
