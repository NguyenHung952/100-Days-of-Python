# =========================================================
#             SPEECH TO NOTE AI SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : Chuyển giọng nói thành note bằng Python
#
# Chức năng:
#   ✓ Speech-to-Text AI
#   ✓ Ghi âm từ microphone
#   ✓ Chuyển giọng nói -> văn bản
#   ✓ Hỗ trợ tiếng Việt + English
#   ✓ Lưu note tự động
#   ✓ Tạo timestamp note
#   ✓ Tóm tắt note AI đơn giản
#   ✓ Quản lý note
#   ✓ Demo mode
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install SpeechRecognition pyaudio colorama
#
# =========================================================
# NẾU LỖI PYAUDIO WINDOWS
# =========================================================
#
# pip install pipwin
# pipwin install pyaudio
#
# =========================================================
# CHẠY
# =========================================================
#
# python speech_to_note.py
#
# =========================================================

from colorama import Fore, Style, init

import speech_recognition as sr

import datetime
import os
import time

init(autoreset=True)

# =========================================================
# THƯ MỤC NOTE
# =========================================================

NOTE_FOLDER = "voice_notes"

os.makedirs(
    NOTE_FOLDER,
    exist_ok=True
)

# =========================================================
# SPEECH RECOGNIZER
# =========================================================

recognizer = sr.Recognizer()

# =========================================================
# GIAO DIỆN
# =========================================================

def clear():

    os.system(
        "cls" if os.name == "nt"
        else "clear"
    )


def line():

    print(Fore.CYAN + "=" * 100)


def title(text):

    line()

    print(
        Fore.GREEN +
        Style.BRIGHT +
        text.center(100)
    )

    line()


def pause():

    input(
        Fore.YELLOW +
        "\nNhấn ENTER để tiếp tục..."
    )


# =========================================================
# GIỚI THIỆU
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU SPEECH TO NOTE")

    print(Fore.WHITE + """
Speech-to-Note là hệ thống AI giúp:

   ✓ Ghi chú bằng giọng nói
   ✓ Chuyển speech -> text
   ✓ Tạo note tự động
   ✓ Hỗ trợ học tập/làm việc

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Meeting Notes
✓ Lecture Notes
✓ Voice Assistant
✓ Podcast Transcript
✓ AI Dictation

=========================================================
AI CÔNG NGHỆ
=========================================================

✓ Speech Recognition
✓ NLP
✓ AI Transcription

=========================================================
CHỨC NĂNG
=========================================================

✓ Record Voice
✓ Convert Speech to Text
✓ Save Notes
✓ View Notes
✓ Vietnamese Support
""")

    line()


# =========================================================
# SAVE NOTE
# =========================================================

def save_note(text):

    timestamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = os.path.join(
        NOTE_FOLDER,
        f"note_{timestamp}.txt"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

    return filename


# =========================================================
# SPEECH TO TEXT
# =========================================================

def speech_to_text():

    clear()

    title("SPEECH TO TEXT")

    language = input(
        Fore.YELLOW +
        "Ngôn ngữ (vi-VN / en-US): "
    )

    try:

        with sr.Microphone() as source:

            print(Fore.CYAN +
                  "\nĐang điều chỉnh noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print(Fore.GREEN +
                  "\n🎤 Hãy nói...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=20
            )

            print(Fore.CYAN +
                  "\nĐang xử lý AI Speech Recognition...")

            text = recognizer.recognize_google(
                audio,
                language=language
            )

            line()

            print(Fore.GREEN +
                  "\nTEXT NHẬN DIỆN\n")

            print(Fore.WHITE + text)

            line()

            save = input(
                Fore.YELLOW +
                "\nLưu note? (y/n): "
            )

            if save.lower() == 'y':

                filename = save_note(text)

                print(Fore.GREEN +
                      f"\nĐã lưu: {filename}")

    except sr.WaitTimeoutError:

        print(Fore.RED +
              "\nKhông phát hiện giọng nói.")

    except sr.UnknownValueError:

        print(Fore.RED +
              "\nAI không nhận diện được speech.")

    except sr.RequestError as e:

        print(Fore.RED +
              f"\nLỗi API:\n{e}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# XEM NOTES
# =========================================================

def view_notes():

    clear()

    title("VOICE NOTES")

    files = os.listdir(NOTE_FOLDER)

    if not files:

        print(Fore.RED +
              "\nChưa có note.")

        pause()

        return

    for index, file in enumerate(files, start=1):

        print(Fore.GREEN +
              f"[{index}] {file}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn note: "
        ))

        selected = files[choice - 1]

        path = os.path.join(
            NOTE_FOLDER,
            selected
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            content = f.read()

        line()

        print(Fore.WHITE + content)

        line()

    except:

        print(Fore.RED +
              "\nLựa chọn không hợp lệ.")

    pause()


# =========================================================
# DELETE NOTE
# =========================================================

def delete_note():

    clear()

    title("DELETE NOTE")

    files = os.listdir(NOTE_FOLDER)

    if not files:

        print(Fore.RED +
              "\nKhông có note.")

        pause()

        return

    for index, file in enumerate(files, start=1):

        print(Fore.GREEN +
              f"[{index}] {file}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn note cần xóa: "
        ))

        selected = files[choice - 1]

        path = os.path.join(
            NOTE_FOLDER,
            selected
        )

        os.remove(path)

        print(Fore.GREEN +
              f"\nĐã xóa: {selected}")

    except:

        print(Fore.RED +
              "\nLỗi xóa note.")

    pause()


# =========================================================
# NOTE STATISTICS
# =========================================================

def note_statistics():

    clear()

    title("NOTE STATISTICS")

    files = os.listdir(NOTE_FOLDER)

    total_notes = len(files)

    total_size = 0

    total_words = 0

    for file in files:

        path = os.path.join(
            NOTE_FOLDER,
            file
        )

        total_size += os.path.getsize(path)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

            total_words += len(text.split())

    print(Fore.GREEN +
          f"\nTổng notes: {total_notes}")

    print(Fore.CYAN +
          f"Tổng words: {total_words}")

    print(Fore.YELLOW +
          f"Tổng dung lượng: {total_size} bytes")

    pause()


# =========================================================
# SIMPLE AI SUMMARY
# =========================================================

def summarize_note():

    clear()

    title("AI NOTE SUMMARY")

    files = os.listdir(NOTE_FOLDER)

    if not files:

        print(Fore.RED +
              "\nKhông có note.")

        pause()

        return

    for index, file in enumerate(files, start=1):

        print(Fore.GREEN +
              f"[{index}] {file}")

    try:

        choice = int(input(
            Fore.YELLOW +
            "\nChọn note: "
        ))

        selected = files[choice - 1]

        path = os.path.join(
            NOTE_FOLDER,
            selected
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        sentences = text.split(".")

        summary = ".".join(sentences[:3])

        line()

        print(Fore.GREEN +
              "\nAI SUMMARY\n")

        print(Fore.WHITE + summary)

        line()

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi:\n{e}")

    pause()


# =========================================================
# EXPORT ALL NOTES
# =========================================================

def export_notes():

    clear()

    title("EXPORT ALL NOTES")

    files = os.listdir(NOTE_FOLDER)

    if not files:

        print(Fore.RED +
              "\nKhông có notes.")

        pause()

        return

    output = "all_notes_export.txt"

    try:

        with open(
            output,
            "w",
            encoding="utf-8"
        ) as out:

            for file in files:

                path = os.path.join(
                    NOTE_FOLDER,
                    file
                )

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    content = f.read()

                out.write(
                    f"\n===== {file} =====\n"
                )

                out.write(content + "\n")

        print(Fore.GREEN +
              f"\nĐã export: {output}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO SPEECH TO NOTE")

    print(Fore.WHITE + """
Demo Speech-to-Note:

=========================================================
CÁCH TEST
=========================================================

1. Chọn Speech to Text
2. Nói vào microphone
3. AI nhận diện speech
4. Lưu thành note

=========================================================
HỖ TRỢ NGÔN NGỮ
=========================================================

✓ vi-VN
✓ en-US

=========================================================
ỨNG DỤNG
=========================================================

✓ Meeting Notes
✓ Study Notes
✓ AI Assistant
✓ Voice Journal
""")

    pause()


# =========================================================
# GIẢI THÍCH AI SPEECH
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH SPEECH RECOGNITION")

    print(Fore.WHITE + """
=========================================================
1. SPEECH RECOGNITION
=========================================================

AI nhận diện:
   ✓ Giọng nói
   ✓ Chuyển thành text

=========================================================
2. NLP
=========================================================

Natural Language Processing

=========================================================
3. MICROPHONE INPUT
=========================================================

Thu âm từ:
   ✓ Mic
   ✓ Audio Device

=========================================================
4. TRANSCRIPTION
=========================================================

Speech -> Text

=========================================================
5. AI ASSISTANT
=========================================================

Ứng dụng:
   ✓ Siri
   ✓ Google Assistant
   ✓ Alexa

=========================================================
6. SPEECH AI
=========================================================

AI học:
   ✓ Accent
   ✓ Pronunciation
   ✓ Language

=========================================================
7. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Voice Notes
✓ Meeting Transcript
✓ AI Chatbot
✓ Accessibility Tools

=========================================================
8. COMPUTER AUDIO AI
=========================================================

Lĩnh vực:
   ✓ AI
   ✓ Audio Processing
   ✓ Speech Recognition
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    while True:

        clear()

        title("SPEECH TO NOTE AI SYSTEM")

        print(Fore.CYAN + """
[1] Giới thiệu Speech-to-Note
[2] Speech -> Text
[3] Xem notes
[4] Xóa note
[5] Note statistics
[6] AI summarize note
[7] Export all notes
[8] Demo mode
[9] Giải thích Speech AI
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

            speech_to_text()

        elif choice == '3':

            view_notes()

        elif choice == '4':

            delete_note()

        elif choice == '5':

            note_statistics()

        elif choice == '6':

            summarize_note()

        elif choice == '7':

            export_notes()

        elif choice == '8':

            demo_mode()

        elif choice == '9':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng Speech-to-Note System.

Kiến thức đạt được:
   ✓ Speech Recognition
   ✓ AI Audio Processing
   ✓ NLP
   ✓ Voice Notes
   ✓ Speech-to-Text
   ✓ AI Assistant
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
