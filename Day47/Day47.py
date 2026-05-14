# ============================================================
#   ĐIỀU KHIỂN THIẾT BỊ BẰNG GIỌNG NÓI
# ============================================================
#
# PHIÊN BẢN:
#   Smart Voice Control IoT 2026
#
# CHỨC NĂNG:
#   ✓ Điều khiển thiết bị bằng giọng nói
#   ✓ Nhận diện tiếng Việt
#   ✓ Bật / tắt đèn
#   ✓ Bật / tắt quạt
#   ✓ Điều khiển thiết bị ảo
#   ✓ Text To Speech
#   ✓ Logging hệ thống
#   ✓ Dashboard terminal hiện đại
#   ✓ Hỗ trợ Raspberry Pi GPIO
#   ✓ Mô phỏng Smart Home
#
# CÔNG NGHỆ:
#   - SpeechRecognition
#   - gTTS
#   - Python GPIO Simulation
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
# RASPBERRY PI:
#
#   pip install RPi.GPIO
#
# CHẠY:
#
#   python voice_control_iot.py
#
# LỆNH:
#
#   "bật đèn"
#   "tắt đèn"
#   "bật quạt"
#   "tắt quạt"
#   "trạng thái"
#   "thoát"
#
# ============================================================

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

import os
import time
import datetime

# ============================================================
# GPIO CHO RASPBERRY PI
# ============================================================

RASPBERRY_PI = False

try:

    import RPi.GPIO as GPIO

    RASPBERRY_PI = True

except:

    RASPBERRY_PI = False

# ============================================================
# GPIO CONFIG
# ============================================================

LED_PIN = 17
FAN_PIN = 27

# ============================================================
# THIẾT BỊ ẢO
# ============================================================

light_status = False
fan_status = False

# ============================================================
# LOG FILE
# ============================================================

LOG_FILE = "voice_control_log.txt"

# ============================================================
# KHỞI TẠO GPIO
# ============================================================

def setup_gpio():

    if RASPBERRY_PI:

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(LED_PIN, GPIO.OUT)

        GPIO.setup(FAN_PIN, GPIO.OUT)

        GPIO.output(LED_PIN, GPIO.LOW)

        GPIO.output(FAN_PIN, GPIO.LOW)

# ============================================================
# GIỚI THIỆU
# ============================================================

def show_intro():

    print("\n" + "=" * 75)
    print("        SMART VOICE CONTROL SYSTEM")
    print("            MODERN EDITION 2026")
    print("=" * 75)

    features = [

        "Vietnamese Voice Recognition",
        "Smart Home Control",
        "Light Control",
        "Fan Control",
        "Text To Speech",
        "Realtime Listening",
        "IoT Simulation",
        "Raspberry Pi GPIO",
        "Voice Commands",
        "System Logging"

    ]

    print("\nCHỨC NĂNG:")

    for feature in features:
        print(f"✓ {feature}")

    print("\nLỆNH HỖ TRỢ:")
    print("- bật đèn")
    print("- tắt đèn")
    print("- bật quạt")
    print("- tắt quạt")
    print("- trạng thái")
    print("- thoát")

    if RASPBERRY_PI:

        print("\n✅ Raspberry Pi GPIO: ENABLED")

    else:

        print("\n⚠ GPIO Simulation Mode")

    print("\nĐang khởi động Smart Home System...\n")

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
# NGHE GIỌNG NÓI
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
            phrase_time_limit=6
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

    except:

        print("❌ Không nghe rõ!")

        return ""

# ============================================================
# CẬP NHẬT GPIO
# ============================================================

def update_gpio():

    if RASPBERRY_PI:

        GPIO.output(
            LED_PIN,
            GPIO.HIGH if light_status else GPIO.LOW
        )

        GPIO.output(
            FAN_PIN,
            GPIO.HIGH if fan_status else GPIO.LOW
        )

# ============================================================
# HIỂN THỊ TRẠNG THÁI
# ============================================================

def show_status():

    print("\n" + "-" * 50)

    print("TRẠNG THÁI THIẾT BỊ:")

    print(
        f"💡 Đèn: {'BẬT' if light_status else 'TẮT'}"
    )

    print(
        f"🌀 Quạt: {'BẬT' if fan_status else 'TẮT'}"
    )

    print("-" * 50)

# ============================================================
# XỬ LÝ LỆNH
# ============================================================

def process_command(command):

    global light_status
    global fan_status

    # ========================================================
    # BẬT ĐÈN
    # ========================================================

    if "bật đèn" in command:

        light_status = True

        update_gpio()

        speak("Đã bật đèn")

        write_log("LIGHT ON")

    # ========================================================
    # TẮT ĐÈN
    # ========================================================

    elif "tắt đèn" in command:

        light_status = False

        update_gpio()

        speak("Đã tắt đèn")

        write_log("LIGHT OFF")

    # ========================================================
    # BẬT QUẠT
    # ========================================================

    elif "bật quạt" in command:

        fan_status = True

        update_gpio()

        speak("Đã bật quạt")

        write_log("FAN ON")

    # ========================================================
    # TẮT QUẠT
    # ========================================================

    elif "tắt quạt" in command:

        fan_status = False

        update_gpio()

        speak("Đã tắt quạt")

        write_log("FAN OFF")

    # ========================================================
    # TRẠNG THÁI
    # ========================================================

    elif "trạng thái" in command:

        light = (
            "bật" if light_status else "tắt"
        )

        fan = (
            "bật" if fan_status else "tắt"
        )

        speak(
            f"Đèn đang {light}, quạt đang {fan}"
        )

        show_status()

    # ========================================================
    # XIN CHÀO
    # ========================================================

    elif "xin chào" in command:

        speak(
            "Xin chào. Hệ thống điều khiển thông minh đã sẵn sàng."
        )

    # ========================================================
    # THOÁT
    # ========================================================

    elif (
        "thoát" in command
        or
        "tạm biệt" in command
    ):

        speak("Đang tắt hệ thống. Tạm biệt.")

        return False

    # ========================================================
    # KHÔNG HIỂU
    # ========================================================

    else:

        speak(
            "Tôi chưa hiểu lệnh đó."
        )

    return True

# ============================================================
# MAIN
# ============================================================

def main():

    setup_gpio()

    show_intro()

    speak(
        "Hệ thống điều khiển bằng giọng nói đã sẵn sàng."
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

            print("\n⚠ Đã dừng hệ thống.")

            break

        except Exception as e:

            print(f"\n❌ Lỗi: {e}")

    # ========================================================
    # CLEANUP GPIO
    # ========================================================

    if RASPBERRY_PI:

        GPIO.cleanup()

# ============================================================
# CHẠY CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":

    main()
