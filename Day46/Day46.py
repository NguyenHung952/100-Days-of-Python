# ============================================================
#   MINI VOICE ASSISTANT TIẾNG VIỆT
# ============================================================
#
# PHIÊN BẢN:
#   Vietnamese Voice Assistant 2026
#
# CHỨC NĂNG:
#   ✓ Nhận diện giọng nói tiếng Việt
#   ✓ Trợ lý ảo mini
#   ✓ Text To Speech tiếng Việt
#   ✓ Trả lời thời gian
#   ✓ Mở website
#   ✓ Tìm kiếm Google
#   ✓ Mở YouTube
#   ✓ Kể giờ hiện tại
#   ✓ Chào hỏi thông minh
#   ✓ Logging hệ thống
#
# CÔNG NGHỆ:
#   - SpeechRecognition
#   - Google Speech API
#   - gTTS
#   - playsound
#
# CÀI ĐẶT:
#
#   pip install SpeechRecognition
#   pip install gtts
#   pip install playsound==1.2.2
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
#   python voice_assistant_vn.py
#
# THOÁT:
#
#   Nói:
#   "tạm biệt"
#   hoặc
#   "thoát"
#
# ============================================================

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

import os
import webbrowser
import datetime
import time

# ============================================================
# FILE LOG
# ============================================================

LOG_FILE = "assistant_log.txt"

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 70)
    print("          MINI VOICE ASSISTANT TIẾNG VIỆT")
    print("             MODERN EDITION 2026")
    print("=" * 70)

    features = [

        "Vietnamese Speech Recognition",
        "Text To Speech",
        "Google Search",
        "Open YouTube",
        "Voice Commands",
        "Time Assistant",
        "Smart Greetings",
        "Realtime Listening",
        "Logging System",
        "Vietnamese AI Assistant"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nLỆNH HỖ TRỢ:")
    print("- xin chào")
    print("- mấy giờ")
    print("- mở youtube")
    print("- mở google")
    print("- tìm kiếm ...")
    print("- hôm nay ngày mấy")
    print("- tạm biệt")

    print("\nĐang khởi động trợ lý ảo...\n")

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

def speak(text):

    print(f"\n🤖 Assistant: {text}")

    tts = gTTS(
        text=text,
        lang='vi'
    )

    filename = "voice.mp3"

    tts.save(filename)

    playsound(filename)

    os.remove(filename)

# ============================================================
# NHẬN DIỆN GIỌNG NÓI
# ============================================================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("\n🎤 Đang lắng nghe...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=8
        )

    try:

        print("🔄 Đang nhận diện...")

        text = recognizer.recognize_google(
            audio,
            language="vi-VN"
        )

        print(f"👤 Bạn nói: {text}")

        write_log(f"USER: {text}")

        return text.lower()

    except sr.UnknownValueError:

        print("❌ Không nghe rõ!")

        return ""

    except sr.RequestError:

        print("❌ Không kết nối được Google Speech API!")

        return ""

# ============================================================
# XỬ LÝ LỆNH
# ============================================================

def process_command(command):

    # ========================================================
    # XIN CHÀO
    # ========================================================

    if "xin chào" in command:

        speak("Xin chào, tôi là trợ lý ảo tiếng Việt.")

    # ========================================================
    # GIỜ HIỆN TẠI
    # ========================================================

    elif "mấy giờ" in command:

        now = datetime.datetime.now().strftime(
            "%H giờ %M phút"
        )

        speak(f"Bây giờ là {now}")

    # ========================================================
    # NGÀY THÁNG
    # ========================================================

    elif "ngày mấy" in command:

        today = datetime.datetime.now().strftime(
            "%d tháng %m năm %Y"
        )

        speak(f"Hôm nay là ngày {today}")

    # ========================================================
    # MỞ YOUTUBE
    # ========================================================

    elif "mở youtube" in command:

        speak("Đang mở YouTube")

        webbrowser.open(
            "https://www.youtube.com"
        )

    # ========================================================
    # MỞ GOOGLE
    # ========================================================

    elif "mở google" in command:

        speak("Đang mở Google")

        webbrowser.open(
            "https://www.google.com"
        )

    # ========================================================
    # TÌM KIẾM
    # ========================================================

    elif "tìm kiếm" in command:

        search_text = command.replace(
            "tìm kiếm",
            ""
        )

        if search_text.strip() != "":

            speak(f"Đang tìm kiếm {search_text}")

            url = (
                "https://www.google.com/search?q="
                + search_text
            )

            webbrowser.open(url)

        else:

            speak("Bạn muốn tìm kiếm gì?")

    # ========================================================
    # GIỚI THIỆU
    # ========================================================

    elif "bạn là ai" in command:

        speak(
            "Tôi là trợ lý ảo mini tiếng Việt viết bằng Python."
        )

    # ========================================================
    # THỜI TIẾT
    # ========================================================

    elif "thời tiết" in command:

        speak(
            "Bạn có thể xem thời tiết trên trình duyệt."
        )

        webbrowser.open(
            "https://www.google.com/search?q=thời+tiết"
        )

    # ========================================================
    # THOÁT
    # ========================================================

    elif (
        "tạm biệt" in command
        or
        "thoát" in command
    ):

        speak("Tạm biệt. Hẹn gặp lại.")

        return False

    # ========================================================
    # KHÔNG HIỂU
    # ========================================================

    else:

        speak(
            "Xin lỗi, tôi chưa hiểu câu lệnh đó."
        )

    return True

# ============================================================
# MAIN
# ============================================================

def main():

    show_intro()

    speak(
        "Xin chào. Trợ lý ảo tiếng Việt đã sẵn sàng."
    )

    running = True

    while running:

        try:

            command = listen()

            if command != "":

                running = process_command(
                    command
                )

            time.sleep(1)

        except KeyboardInterrupt:

            print("\n⚠ Đã dừng trợ lý.")

            break

        except Exception as e:

            print(f"\n❌ Lỗi: {e}")

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
