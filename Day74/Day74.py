# =========================================================
#              BULK FILE RENAME TOOL
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Rename file hàng loạt bằng Python
#
# Chức năng:
#   ✓ Rename file hàng loạt
#   ✓ Rename theo prefix/suffix
#   ✓ Đánh số tự động
#   ✓ Replace text trong tên file
#   ✓ Chuyển UPPER/lower case
#   ✓ Đổi extension
#   ✓ Preview trước khi rename
#   ✓ Undo rename
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
# python bulk_rename.py
#
# =========================================================

from colorama import Fore, Style, init

import os
import shutil
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
# UNDO HISTORY
# =========================================================

undo_history = []

# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU BULK FILE RENAME")

    print(Fore.WHITE + """
Bulk Rename Tool giúp:

   ✓ Đổi tên nhiều file cùng lúc
   ✓ Tiết kiệm thời gian
   ✓ Tự động hóa quản lý file

=========================================================
CHỨC NĂNG CHÍNH
=========================================================

✓ Prefix Rename
✓ Suffix Rename
✓ Replace Text
✓ Auto Numbering
✓ Extension Change
✓ Upper/Lower Case

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Rename ảnh
✓ Rename tài liệu
✓ Media Library
✓ Backup File
✓ NAS Storage

=========================================================
LỢI ÍCH
=========================================================

✓ Nhanh
✓ Chính xác
✓ Tự động
✓ Quản lý file dễ hơn
""")

    line()


# =========================================================
# LẤY FILE
# =========================================================

def get_files(folder):

    files = []

    for file in os.listdir(folder):

        path = os.path.join(folder, file)

        if os.path.isfile(path):

            files.append(file)

    return files


# =========================================================
# PREVIEW
# =========================================================

def preview_changes(changes):

    line()

    print(Fore.CYAN +
          "\nPREVIEW RENAME\n")

    for old, new in changes:

        print(Fore.YELLOW +
              f"{old}")

        print(Fore.GREEN +
              f" -> {new}\n")

    line()


# =========================================================
# APPLY CHANGES
# =========================================================

def apply_changes(folder, changes):

    global undo_history

    undo_history.clear()

    try:

        for old_name, new_name in changes:

            old_path = os.path.join(
                folder,
                old_name
            )

            new_path = os.path.join(
                folder,
                new_name
            )

            os.rename(old_path, new_path)

            undo_history.append(
                (new_name, old_name)
            )

            print(Fore.GREEN +
                  f"[RENAMED] "
                  f"{old_name} -> {new_name}")

        print(Fore.CYAN +
              "\nRename hoàn tất.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi rename:\n{e}")

    pause()


# =========================================================
# PREFIX RENAME
# =========================================================

def prefix_rename():

    clear()

    title("PREFIX RENAME")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    prefix = input(
        Fore.YELLOW +
        "Nhập prefix: "
    )

    files = get_files(folder)

    changes = []

    for file in files:

        new_name = prefix + file

        changes.append(
            (file, new_name)
        )

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# SUFFIX RENAME
# =========================================================

def suffix_rename():

    clear()

    title("SUFFIX RENAME")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    suffix = input(
        Fore.YELLOW +
        "Nhập suffix: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    files = get_files(folder)

    changes = []

    for file in files:

        name, ext = os.path.splitext(file)

        new_name = name + suffix + ext

        changes.append(
            (file, new_name)
        )

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# AUTO NUMBERING
# =========================================================

def auto_numbering():

    clear()

    title("AUTO NUMBERING")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    prefix = input(
        Fore.YELLOW +
        "Prefix file: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    files = get_files(folder)

    changes = []

    counter = 1

    for file in files:

        ext = os.path.splitext(file)[1]

        new_name = f"{prefix}_{counter}{ext}"

        changes.append(
            (file, new_name)
        )

        counter += 1

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# REPLACE TEXT
# =========================================================

def replace_text():

    clear()

    title("REPLACE TEXT")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    old_text = input(
        Fore.YELLOW +
        "Text cần thay: "
    )

    new_text = input(
        Fore.YELLOW +
        "Text mới: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    files = get_files(folder)

    changes = []

    for file in files:

        new_name = file.replace(
            old_text,
            new_text
        )

        changes.append(
            (file, new_name)
        )

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# UPPER / LOWER CASE
# =========================================================

def change_case():

    clear()

    title("CHANGE FILE CASE")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    print(Fore.CYAN + """
1. UPPERCASE
2. lowercase
""")

    choice = input(
        Fore.YELLOW +
        "Chọn: "
    )

    files = get_files(folder)

    changes = []

    for file in files:

        if choice == '1':

            new_name = file.upper()

        else:

            new_name = file.lower()

        changes.append(
            (file, new_name)
        )

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# ĐỔI EXTENSION
# =========================================================

def change_extension():

    clear()

    title("CHANGE FILE EXTENSION")

    folder = input(
        Fore.YELLOW +
        "Nhập folder: "
    )

    old_ext = input(
        Fore.YELLOW +
        "Extension cũ (.txt): "
    )

    new_ext = input(
        Fore.YELLOW +
        "Extension mới (.md): "
    )

    if not os.path.exists(folder):

        print(Fore.RED +
              "\nFolder không tồn tại.")

        pause()

        return

    files = get_files(folder)

    changes = []

    for file in files:

        name, ext = os.path.splitext(file)

        if ext == old_ext:

            new_name = name + new_ext

            changes.append(
                (file, new_name)
            )

    preview_changes(changes)

    confirm = input(
        Fore.YELLOW +
        "\nThực hiện rename? (y/n): "
    )

    if confirm.lower() == 'y':

        apply_changes(folder, changes)


# =========================================================
# UNDO
# =========================================================

def undo_rename():

    clear()

    title("UNDO RENAME")

    if not undo_history:

        print(Fore.RED +
              "\nKhông có lịch sử undo.")

        pause()

        return

    folder = input(
        Fore.YELLOW +
        "Nhập folder chứa file: "
    )

    try:

        for current_name, old_name in undo_history:

            current_path = os.path.join(
                folder,
                current_name
            )

            old_path = os.path.join(
                folder,
                old_name
            )

            if os.path.exists(current_path):

                os.rename(
                    current_path,
                    old_path
                )

                print(Fore.GREEN +
                      f"{current_name} -> {old_name}")

        print(Fore.CYAN +
              "\nUndo hoàn tất.")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi undo:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO BULK RENAME")

    demo_folder = "demo_rename"

    os.makedirs(demo_folder, exist_ok=True)

    demo_files = [
        "photo1.jpg",
        "photo2.jpg",
        "photo3.jpg"
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

    changes = []

    counter = 1

    for file in demo_files:

        ext = os.path.splitext(file)[1]

        new_name = f"holiday_{counter}{ext}"

        changes.append(
            (file, new_name)
        )

        counter += 1

    preview_changes(changes)

    pause()


# =========================================================
# GIẢI THÍCH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH BULK RENAME")

    print(Fore.WHITE + """
=========================================================
1. BULK RENAME
=========================================================

Đổi tên nhiều file cùng lúc.

=========================================================
2. PREFIX
=========================================================

Thêm text vào đầu file.

Ví dụ:
   IMG_photo.jpg

=========================================================
3. SUFFIX
=========================================================

Thêm text cuối file.

Ví dụ:
   photo_backup.jpg

=========================================================
4. AUTO NUMBERING
=========================================================

Tự động đánh số:
   file_1
   file_2

=========================================================
5. EXTENSION
=========================================================

Ví dụ:
   .txt
   .jpg
   .pdf

=========================================================
6. FILE MANAGEMENT
=========================================================

✓ Rename
✓ Organize
✓ Sort
✓ Cleanup

=========================================================
7. UNDO
=========================================================

Khôi phục tên file cũ.

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Camera Photos
✓ Backup Files
✓ Documents
✓ Media Library
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("BULK FILE RENAME TOOL")

        print(Fore.CYAN + """
[1] Giới thiệu Bulk Rename
[2] Prefix rename
[3] Suffix rename
[4] Auto numbering
[5] Replace text
[6] Change UPPER/lower case
[7] Change extension
[8] Undo rename
[9] Demo mode
[10] Giải thích chi tiết
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

            prefix_rename()

        elif choice == '3':

            suffix_rename()

        elif choice == '4':

            auto_numbering()

        elif choice == '5':

            replace_text()

        elif choice == '6':

            change_case()

        elif choice == '7':

            change_extension()

        elif choice == '8':

            undo_rename()

        elif choice == '9':

            demo_mode()

        elif choice == '10':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Bulk File Rename Tool.

Kiến thức đạt được:
   ✓ File Rename
   ✓ Automation
   ✓ Prefix/Suffix
   ✓ Extension Handling
   ✓ Undo System
   ✓ File Management
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
