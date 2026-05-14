# ============================================================
#   TEXT TO SPEECH BẰNG PYTHON
# ============================================================
#
# PHIÊN BẢN:
#   Modern Text To Speech 2026
#
# CHỨC NĂNG:
#   ✓ Chuyển văn bản thành giọng nói
#   ✓ Hỗ trợ tiếng Việt
#   ✓ Hỗ trợ nhiều ngôn ngữ
#   ✓ Lưu file MP3
#   ✓ Phát âm thanh tự động
#   ✓ Giao diện terminal hiện đại
#   ✓ Logging hệ thống
#   ✓ Tùy chỉnh nội dung đọc
#   ✓ Chạy trên Windows/Linux/Raspberry Pi
#   ✓ Dễ mở rộng AI Assistant
#
# CÔNG NGHỆ:
#   - gTTS
#   - playsound
#
# CÀI ĐẶT:
#
#   pip install gtts
#   pip install playsound==1.2.2
#
# CHẠY:
#
#   python text_to_speech.py
#
# ============================================================

from gtts import gTTS
from playsound import playsound

import os
import datetime

# ============================================================
# THƯ MỤC OUTPUT
# ============================================================

OUTPUT_FOLDER = "tts_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "tts_log.txt"

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 70)
    print("             TEXT TO SPEECH SYSTEM")
    print("              MODERN EDITION 2026")
    print("=" * 70)

    features = [

        "Vietnamese Text To Speech",
        "Realtime Voice Generation",
        "Save MP3 Audio",
        "Automatic Audio Playback",
        "Multi Language Support",
        "Modern Terminal UI",
        "Speech Synthesis",
        "Raspberry Pi Compatible",
        "Logging System",
        "AI Assistant Ready"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nHỖ TRỢ NGÔN NGỮ:")
    print("- vi  : Tiếng Việt")
    print("- en  : English")
    print("- ja  : Japanese")
    print("- ko  : Korean")
    print("- fr  : French")

    print("\nĐang khởi động Text To Speech System...\n")

# ============================================================
# GHI LOG
# ============================================================

def write_log(message):

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        timestamp = datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(f"[{timestamp}] {message}\n")

# ============================================================
# TEXT TO SPEECH
# ============================================================

def text_to_speech(text, language="vi"):

    try:

        print("\n🔄 Đang tạo giọng nói...")

        # ====================================================
        # TẠO TTS
        # ====================================================

        tts = gTTS(
            text=text,
            lang=language,
            slow=False
        )

        # ====================================================
        # TÊN FILE
        # ====================================================

        filename = datetime.datetime.now().strftime(
            "%Y%m%d_%H%M%S.mp3"
        )

        filepath = os.path.join(
            OUTPUT_FOLDER,
            filename
        )

        # ====================================================
        # LƯU MP3
        # ====================================================

        tts.save(filepath)

        print(f"✅ Đã lưu file: {filepath}")

        # ====================================================
        # PHÁT ÂM THANH
        # ====================================================

        print("🔊 Đang phát âm thanh...")

        playsound(filepath)

        # ====================================================
        # LOG
        # ====================================================

        write_log(
            f"TTS Generated: {filepath}"
        )

        return filepath

    except Exception as e:

        print(f"\n❌ Lỗi Text To Speech: {e}")

        return None

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "-" * 60)

    print("MENU:")

    print("1. Chuyển văn bản thành giọng nói")
    print("2. Demo tiếng Việt")
    print("3. Demo tiếng Anh")
    print("4. Thoát")

    print("-" * 60)

# ============================================================
# DEMO TIẾNG VIỆT
# ============================================================

def demo_vietnamese():

    text = (
        "Xin chào. Đây là hệ thống chuyển văn bản "
        "thành giọng nói bằng Python."
    )

    text_to_speech(text, "vi")

# ============================================================
# DEMO TIẾNG ANH
# ============================================================

def demo_english():

    text = (
        "Hello. This is a modern text to speech "
        "system using Python."
    )

    text_to_speech(text, "en")

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    while True:

        try:

            show_menu()

            choice = input(
                "\n👉 Nhập lựa chọn: "
            )

            # =================================================
            # CUSTOM TEXT
            # =================================================

            if choice == "1":

                text = input(
                    "\n📝 Nhập văn bản cần đọc: "
                )

                print("\nNgôn ngữ:")
                print("vi = Tiếng Việt")
                print("en = English")

                language = input(
                    "\n🌐 Chọn ngôn ngữ: "
                )

                if language.strip() == "":

                    language = "vi"

                text_to_speech(
                    text,
                    language
                )

            # =================================================
            # DEMO VIỆT
            # =================================================

            elif choice == "2":

                demo_vietnamese()

            # =================================================
            # DEMO ANH
            # =================================================

            elif choice == "3":

                demo_english()

            # =================================================
            # THOÁT
            # =================================================

            elif choice == "4":

                print("\n👋 Đang thoát hệ thống...")

                break

            # =================================================
            # KHÔNG HỢP LỆ
            # =================================================

            else:

                print("\n❌ Lựa chọn không hợp lệ!")

        except KeyboardInterrupt:

            print("\n⚠ Chương trình đã dừng")

            break

        except Exception as e:

            print(f"\n❌ Lỗi hệ thống: {e}")

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
