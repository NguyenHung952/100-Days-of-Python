# =========================================================
#            AUTO FILE ORGANIZER - PYTHON
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Tổ chức file tự động
#
# Chức năng:
#   ✓ Tự động phân loại file
#   ✓ Sắp xếp theo đuôi file
#   ✓ Sắp xếp theo loại dữ liệu
#   ✓ Tạo folder tự động
#   ✓ Dọn dẹp thư mục Downloads/Desktop
#   ✓ Hiển thị thống kê file
#   ✓ Tìm file trùng lặp
#   ✓ Đổi tên file tự động
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
# python auto_file_organizer.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import shutil
import hashlib
import time
import random

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
# PHÂN LOẠI FILE
# =========================================================

FILE_CATEGORIES = {

    "Images": [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp"
    ],

    "Videos": [
        ".mp4",
        ".mkv",
        ".avi",
        ".mov"
    ],

    "Documents": [
        ".pdf",
        ".docx",
        ".doc",
        ".txt",
        ".xlsx",
        ".pptx"
    ],

    "Music": [
        ".mp3",
        ".wav",
        ".flac"
    ],

    "Archives": [
        ".zip",
        ".rar",
        ".7z"
    ],

    "Programs": [
        ".exe",
        ".msi",
        ".apk"
    ]
}

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU AUTO FILE ORGANIZER")

    print(Fore.WHITE + """
Auto File Organizer giúp:

   ✓ Tự động sắp xếp file
   ✓ Dọn dẹp thư mục
   ✓ Phân loại dữ liệu
   ✓ Quản lý file thông minh

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Sort by Extension
✓ Auto Folder Creation
✓ Duplicate Detection
✓ Auto Rename
✓ File Statistics

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Dọn Downloads
✓ Quản lý tài liệu
✓ Backup Organization
✓ NAS Storage
✓ Data Management

=========================================================
LỢI ÍCH
=========================================================

✓ Gọn gàng
✓ Dễ tìm file
✓ Tiết kiệm thời gian
✓ Tăng hiệu suất làm việc
""")

    line()


# =========================================================
# TÌM CATEGORY
# =========================================================

def get_category(extension):

    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:

            return category

    return "Others"


# =========================================================
# TỔ CHỨC FILE
# =========================================================

def organize_files():

    clear()

    title("TỔ CHỨC FILE TỰ ĐỘNG")

    folder = input(
        Fore.YELLOW +
        "Nhập thư mục cần tổ chức: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    moved_files = 0

    try:

        for file in os.listdir(folder):

            file_path = os.path.join(
                folder,
                file
            )

            if os.path.isfile(file_path):

                extension = os.path.splitext(file)[1]

                category = get_category(extension)

                category_folder = os.path.join(
                    folder,
                    category
                )

                os.makedirs(
                    category_folder,
                    exist_ok=True
                )

                destination = os.path.join(
                    category_folder,
                    file
                )

                shutil.move(
                    file_path,
                    destination
                )

                moved_files += 1

                print(Fore.GREEN +
                      f"[MOVED] {file} -> {category}")

        line()

        print(Fore.CYAN +
              f"\nĐã tổ chức {moved_files} file.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# THỐNG KÊ FILE
# =========================================================

def file_statistics():

    clear()

    title("THỐNG KÊ FILE")

    folder = input(
        Fore.YELLOW +
        "Nhập thư mục: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    stats = {}

    total_files = 0

    total_size = 0

    for root, dirs, files in os.walk(folder):

        for file in files:

            total_files += 1

            path = os.path.join(
                root,
                file
            )

            size = os.path.getsize(path)

            total_size += size

            ext = os.path.splitext(file)[1].lower()

            stats[ext] = stats.get(ext, 0) + 1

    line()

    print(Fore.GREEN +
          f"\nTổng file: {total_files}")

    print(Fore.YELLOW +
          f"Tổng dung lượng: {total_size} bytes")

    print(Fore.CYAN +
          "\nTHỐNG KÊ ĐUÔI FILE\n")

    for ext, count in sorted(
        stats.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(Fore.GREEN +
              f"{ext or '[NO EXT]':<10} {count}")

    line()

    pause()


# =========================================================
# HASH FILE
# =========================================================

def file_hash(filepath):

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as f:

        while True:

            chunk = f.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# =========================================================
# TÌM FILE TRÙNG
# =========================================================

def find_duplicates():

    clear()

    title("TÌM FILE TRÙNG LẶP")

    folder = input(
        Fore.YELLOW +
        "Nhập thư mục: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    hashes = {}

    duplicates = []

    print(Fore.CYAN +
          "\nĐang quét file...\n")

    for root, dirs, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            try:

                h = file_hash(path)

                if h in hashes:

                    duplicates.append(
                        (path, hashes[h])
                    )

                else:

                    hashes[h] = path

            except:
                pass

    if duplicates:

        print(Fore.RED +
              "\nFILE TRÙNG LẶP\n")

        for file1, file2 in duplicates:

            print(Fore.YELLOW +
                  f"\nDuplicate:")

            print(Fore.GREEN + file1)

            print(Fore.CYAN + file2)

            line()

    else:

        print(Fore.GREEN +
              "\nKhông có file trùng.")

    pause()


# =========================================================
# AUTO RENAME
# =========================================================

def auto_rename():

    clear()

    title("AUTO RENAME FILE")

    folder = input(
        Fore.YELLOW +
        "Nhập thư mục: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    prefix = input(
        Fore.YELLOW +
        "Prefix mới: "
    )

    counter = 1

    try:

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            if os.path.isfile(path):

                ext = os.path.splitext(file)[1]

                new_name = f"{prefix}_{counter}{ext}"

                new_path = os.path.join(
                    folder,
                    new_name
                )

                os.rename(path, new_path)

                print(Fore.GREEN +
                      f"{file} -> {new_name}")

                counter += 1

        line()

        print(Fore.GREEN +
              "\nĐổi tên hoàn tất.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# DỌN DOWNLOADS
# =========================================================

def clean_downloads():

    clear()

    title("DỌN DẸP DOWNLOADS")

    downloads = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    if not os.path.exists(downloads):

        print(Fore.RED +
              "\nKhông tìm thấy Downloads.")

        pause()

        return

    print(Fore.CYAN +
          f"\nDownloads Path:\n{downloads}")

    confirm = input(
        Fore.YELLOW +
        "\nTổ chức Downloads? (y/n): "
    )

    if confirm.lower() == 'y':

        organize_downloads(downloads)

    else:

        print(Fore.RED +
              "\nĐã hủy.")

        pause()


def organize_downloads(folder):

    moved = 0

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if os.path.isfile(path):

            ext = os.path.splitext(file)[1]

            category = get_category(ext)

            target = os.path.join(
                folder,
                category
            )

            os.makedirs(target, exist_ok=True)

            shutil.move(
                path,
                os.path.join(target, file)
            )

            moved += 1

            print(Fore.GREEN +
                  f"[MOVED] {file}")

    print(Fore.CYAN +
          f"\nĐã dọn {moved} file.")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO AUTO ORGANIZER")

    demo_folder = "demo_files"

    os.makedirs(demo_folder, exist_ok=True)

    demo_files = [
        "photo.jpg",
        "movie.mp4",
        "report.pdf",
        "music.mp3",
        "archive.zip"
    ]

    for file in demo_files:

        path = os.path.join(
            demo_folder,
            file
        )

        with open(path, "w") as f:

            f.write("demo")

    print(Fore.GREEN +
          f"\nĐã tạo demo folder: {demo_folder}")

    time.sleep(1)

    organize_downloads(demo_folder)


# =========================================================
# GIẢI THÍCH FILE ORGANIZATION
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH FILE ORGANIZATION")

    print(Fore.WHITE + """
=========================================================
1. FILE ORGANIZATION
=========================================================

Là quá trình:
   ✓ Phân loại file
   ✓ Sắp xếp dữ liệu

=========================================================
2. FILE EXTENSION
=========================================================

Ví dụ:
   .jpg
   .pdf
   .mp4

=========================================================
3. AUTOMATION
=========================================================

Python tự động:
   ✓ Tạo folder
   ✓ Di chuyển file

=========================================================
4. HASHING
=========================================================

SHA256 dùng để:
   ✓ Tìm file trùng

=========================================================
5. DUPLICATE FILE
=========================================================

File trùng:
   ✓ Tốn dung lượng

=========================================================
6. FILE MANAGEMENT
=========================================================

✓ Organize
✓ Rename
✓ Cleanup
✓ Sort

=========================================================
7. ỨNG DỤNG THỰC TẾ
=========================================================

✓ NAS Storage
✓ Backup Server
✓ Media Library
✓ Downloads Cleanup

=========================================================
8. LỢI ÍCH
=========================================================

✓ Gọn gàng
✓ Dễ quản lý
✓ Tiết kiệm thời gian
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("AUTO FILE ORGANIZER")

        print(Fore.CYAN + """
[1] Giới thiệu Auto Organizer
[2] Tổ chức file tự động
[3] Thống kê file
[4] Tìm file trùng lặp
[5] Auto rename file
[6] Dọn Downloads
[7] Demo mode
[8] Giải thích chi tiết
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

            organize_files()

        elif choice == '3':

            file_statistics()

        elif choice == '4':

            find_duplicates()

        elif choice == '5':

            auto_rename()

        elif choice == '6':

            clean_downloads()

        elif choice == '7':

            demo_mode()

        elif choice == '8':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Auto File Organizer.

Kiến thức đạt được:
   ✓ File Management
   ✓ Automation
   ✓ Duplicate Detection
   ✓ File Statistics
   ✓ Auto Sorting
   ✓ Python OS Module
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
