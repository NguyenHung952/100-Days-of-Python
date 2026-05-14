# ============================================================
#   SPEECH TO TEXT TIẾNG VIỆT
# ============================================================
#
# PHIÊN BẢN:
#   Vietnamese Speech Recognition 2026
#
# CHỨC NĂNG:
#   ✓ Nhận diện giọng nói tiếng Việt
#   ✓ Chuyển giọng nói thành văn bản
#   ✓ Hiển thị realtime terminal
#   ✓ Lưu lịch sử nhận diện
#   ✓ Logging hệ thống
#   ✓ Hỗ trợ microphone USB
#   ✓ Hỗ trợ Raspberry Pi
#   ✓ Hỗ trợ nhiều ngôn ngữ
#   ✓ Giao diện terminal hiện đại
#   ✓ Demo AI Voice Input
#
# CÔNG NGHỆ:
#   - SpeechRecognition
#   - Google Speech API
#   - PyAudio
#
# CÀI ĐẶT:
#
#   pip install SpeechRecognition
#   pip install pyaudio
#
# WINDOWS:
#
#   pip install pipwin
#   pipwin install pyaudio
#
# LINUX:
#
#   sudo apt install portaudio19-dev
#
# CHẠY:
#
#   python speech_to_text_vn.py
#
# THOÁT:
#
#   Nhấn CTRL + C
#
# ============================================================

import speech_recognition as sr

import datetime
import time
import os

# ============================================================
# THƯ MỤC OUTPUT
# ============================================================

OUTPUT_FOLDER = "speech_output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "speech_recognition_log.txt"

# ============================================================
# FILE TEXT
# ============================================================

TEXT_OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "recognized_text.txt"
)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 75)
    print("         SPEECH TO TEXT TIẾNG VIỆT")
    print("            MODERN EDITION 2026")
    print("=" * 75)

    features = [

        "Vietnamese Speech Recognition",
        "Realtime Voice To Text",
        "Microphone Input",
        "Text Logging",
        "Speech History",
        "Google Speech API",
        "Terminal Dashboard",
        "Raspberry Pi Compatible",
        "USB Microphone Support",
        "AI Voice Input"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nHƯỚNG DẪN:")
    print("- Nói vào microphone")
    print("- Hệ thống sẽ tự nhận diện")
    print("- Văn bản sẽ lưu tự động")

    print("\nĐang khởi động Speech Recognition...\n")

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
# LƯU TEXT
# ============================================================

def save_text(text):

    with open(
        TEXT_OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        timestamp = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )

        file.write(f"[{timestamp}] {text}\n")

# ============================================================
# NHẬN DIỆN GIỌNG NÓI
# ============================================================

def recognize_speech():

    recognizer = sr.Recognizer()

    microphone = sr.Microphone()

    # ========================================================
    # TÙY CHỈNH
    # ========================================================

    recognizer.energy_threshold = 300

    recognizer.pause_threshold = 1

    recognizer.dynamic_energy_threshold = True

    with microphone as source:

        print("\n🎤 Đang hiệu chỉnh tiếng ồn...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        print("✅ Microphone sẵn sàng!")

    # ========================================================
    # LOOP CHÍNH
    # ========================================================

    while True:

        try:

            with microphone as source:

                print("\n🎤 Đang lắng nghe...")

                audio = recognizer.listen(

                    source,

                    timeout=5,

                    phrase_time_limit=10

                )

            print("🔄 Đang nhận diện...")

            # =================================================
            # GOOGLE SPEECH API
            # =================================================

            text = recognizer.recognize_google(

                audio,

                language="vi-VN"

            )

            # =================================================
            # HIỂN THỊ
            # =================================================

            print("\n" + "-" * 60)

            print(f"👤 Bạn nói:")

            print(f"\n{text}")

            print("-" * 60)

            # =================================================
            # LƯU FILE
            # =================================================

            save_text(text)

            # =================================================
            # GHI LOG
            # =================================================

            write_log(f"Recognized: {text}")

        # =====================================================
        # KHÔNG NGHE ĐƯỢC
        # =====================================================

        except sr.UnknownValueError:

            print("\n❌ Không nhận diện được giọng nói!")

            write_log("Unknown speech")

        # =====================================================
        # API ERROR
        # =====================================================

        except sr.RequestError:

            print(
                "\n❌ Không kết nối được Google Speech API!"
            )

            write_log("API connection error")

        # =====================================================
        # TIMEOUT
        # =====================================================

        except sr.WaitTimeoutError:

            print("\n⌛ Không phát hiện giọng nói...")

        # =====================================================
        # CTRL + C
        # =====================================================

        except KeyboardInterrupt:

            print("\n\n⚠ Đã dừng hệ thống.")

            break

        # =====================================================
        # ERROR KHÁC
        # =====================================================

        except Exception as e:

            print(f"\n❌ Lỗi hệ thống: {e}")

            write_log(f"ERROR: {e}")

        time.sleep(1)

# ============================================================
# MENU
# ============================================================

def show_menu():

    print("\n" + "-" * 60)

    print("MENU:")

    print("1. Bắt đầu nhận diện giọng nói")
    print("2. Xem file text output")
    print("3. Thoát")

    print("-" * 60)

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
            # START RECOGNITION
            # =================================================

            if choice == "1":

                recognize_speech()

            # =================================================
            # SHOW FILE
            # =================================================

            elif choice == "2":

                print(
                    f"\n📄 File output:"
                )

                print(TEXT_OUTPUT_FILE)

            # =================================================
            # EXIT
            # =================================================

            elif choice == "3":

                print("\n👋 Đang thoát hệ thống...")

                break

            # =================================================
            # INVALID
            # =================================================

            else:

                print("\n❌ Lựa chọn không hợp lệ!")

        except KeyboardInterrupt:

            print("\n⚠ Đã dừng hệ thống.")

            break

        except Exception as e:

            print(f"\n❌ Lỗi: {e}")

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
