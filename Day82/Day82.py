# =========================================================
#        AI BANK TRANSACTION CLASSIFIER SYSTEM
# =========================================================
#
# Tác giả : ChatGPT
# Chủ đề  : AI phân loại giao dịch ngân hàng
#
# Chức năng:
#   ✓ AI phân loại giao dịch
#   ✓ Quản lý thu nhập/chi tiêu
#   ✓ Tự động nhận diện category
#   ✓ Phân tích transaction
#   ✓ Fraud detection đơn giản
#   ✓ Export report
#   ✓ Dashboard thống kê
#   ✓ Tìm giao dịch bất thường
#   ✓ Lưu dữ liệu CSV + JSON
#   ✓ Giao diện terminal hiện đại
#
# =========================================================
# CÀI ĐẶT
# =========================================================
#
# pip install pandas scikit-learn colorama
#
# =========================================================
# CHẠY
# =========================================================
#
# python ai_bank_classifier.py
#
# =========================================================

from colorama import Fore, Style, init

from sklearn.feature_extraction.text import (
    CountVectorizer
)

from sklearn.naive_bayes import (
    MultinomialNB
)

import pandas as pd

import os
import json
import time

init(autoreset=True)

# =========================================================
# DATABASE
# =========================================================

DATA_FILE = "bank_transactions.json"

# =========================================================
# SAMPLE TRAINING DATA
# =========================================================

training_data = [

    ("Ăn trưa nhà hàng", "Food"),
    ("Mua trà sữa", "Food"),
    ("Đóng học phí", "Education"),
    ("Mua sách Python", "Education"),
    ("Thanh toán Netflix", "Entertainment"),
    ("Mua vé xem phim", "Entertainment"),
    ("Nạp tiền điện thoại", "Utilities"),
    ("Thanh toán điện nước", "Utilities"),
    ("Lương tháng", "Income"),
    ("Freelance payment", "Income"),
    ("Mua laptop", "Technology"),
    ("Mua chuột gaming", "Technology"),
]

# =========================================================
# TRAIN AI MODEL
# =========================================================

texts = [x[0] for x in training_data]

labels = [x[1] for x in training_data]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(texts)

model = MultinomialNB()

model.fit(X, labels)

# =========================================================
# DATABASE
# =========================================================

data = {
    "transactions": []
}

# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    global data

    if os.path.exists(DATA_FILE):

        try:

            with open(
                DATA_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

        except:

            pass


# =========================================================
# SAVE DATA
# =========================================================

def save_data():

    with open(
        DATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# UI
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
# INTRO
# =========================================================

def intro():

    clear()

    title("GIỚI THIỆU AI BANK CLASSIFIER")

    print(Fore.WHITE + """
AI Bank Transaction Classifier giúp:

   ✓ Tự động phân loại giao dịch
   ✓ AI hiểu transaction text
   ✓ Quản lý tài chính thông minh

=========================================================
AI FEATURES
=========================================================

✓ NLP Classification
✓ Machine Learning
✓ Fraud Detection
✓ Financial Analytics

=========================================================
ỨNG DỤNG THỰC TẾ
=========================================================

✓ Banking App
✓ Expense Tracker
✓ Financial AI
✓ Digital Wallet

=========================================================
AI MODEL
=========================================================

✓ Naive Bayes
✓ CountVectorizer
✓ NLP Text Classification
""")

    line()


# =========================================================
# AI CLASSIFY
# =========================================================

def classify_transaction(text):

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)

    return prediction[0]


# =========================================================
# ADD TRANSACTION
# =========================================================

def add_transaction():

    clear()

    title("THÊM GIAO DỊCH")

    description = input(
        Fore.YELLOW +
        "Mô tả giao dịch: "
    )

    try:

        amount = float(input(
            Fore.YELLOW +
            "Số tiền: "
        ))

    except:

        print(Fore.RED +
              "\nSố tiền không hợp lệ.")

        pause()

        return

    category = classify_transaction(
        description
    )

    transaction = {

        "description": description,
        "amount": amount,
        "category": category
    }

    data["transactions"].append(
        transaction
    )

    save_data()

    print(Fore.GREEN +
          f"\nAI Category: {category}")

    print(Fore.CYAN +
          "Đã lưu giao dịch.")

    pause()


# =========================================================
# VIEW TRANSACTIONS
# =========================================================

def view_transactions():

    clear()

    title("BANK TRANSACTIONS")

    if not data["transactions"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    for index, tx in enumerate(
        data["transactions"],
        start=1
    ):

        color = Fore.GREEN

        if tx["category"] == "Food":

            color = Fore.YELLOW

        elif tx["category"] == "Entertainment":

            color = Fore.MAGENTA

        elif tx["category"] == "Income":

            color = Fore.CYAN

        print(color +
              f"\n[{index}] {tx['description']}")

        print(Fore.WHITE +
              f"Số tiền : {tx['amount']}")

        print(color +
              f"Category: {tx['category']}")

        line()

    pause()


# =========================================================
# STATISTICS
# =========================================================

def statistics():

    clear()

    title("TRANSACTION STATISTICS")

    if not data["transactions"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    stats = {}

    total = 0

    for tx in data["transactions"]:

        category = tx["category"]

        amount = tx["amount"]

        total += amount

        stats[category] = (
            stats.get(category, 0)
            + amount
        )

    print(Fore.GREEN +
          f"\nTổng giao dịch: {len(data['transactions'])}")

    print(Fore.CYAN +
          f"Tổng tiền: {total}")

    line()

    print(Fore.YELLOW +
          "\nPHÂN TÍCH CATEGORY\n")

    for category, amount in stats.items():

        print(Fore.GREEN +
              f"{category:<15} {amount}")

    pause()


# =========================================================
# FRAUD DETECTION
# =========================================================

def fraud_detection():

    clear()

    title("FRAUD DETECTION")

    suspicious = []

    for tx in data["transactions"]:

        if tx["amount"] > 10000000:

            suspicious.append(tx)

    if suspicious:

        print(Fore.RED +
              "\n⚠ GIAO DỊCH BẤT THƯỜNG\n")

        for tx in suspicious:

            print(Fore.YELLOW +
                  f"{tx['description']}")

            print(Fore.RED +
                  f"Số tiền: {tx['amount']}")

            line()

    else:

        print(Fore.GREEN +
              "\nKhông phát hiện fraud.")

    pause()


# =========================================================
# SEARCH TRANSACTION
# =========================================================

def search_transaction():

    clear()

    title("SEARCH TRANSACTION")

    keyword = input(
        Fore.YELLOW +
        "Nhập keyword: "
    ).lower()

    found = False

    for tx in data["transactions"]:

        if keyword in tx["description"].lower():

            found = True

            print(Fore.GREEN +
                  f"\n{tx['description']}")

            print(Fore.CYAN +
                  f"{tx['amount']}")

            print(Fore.YELLOW +
                  f"{tx['category']}")

            line()

    if not found:

        print(Fore.RED +
              "\nKhông tìm thấy.")

    pause()


# =========================================================
# EXPORT CSV
# =========================================================

def export_csv():

    clear()

    title("EXPORT CSV REPORT")

    if not data["transactions"]:

        print(Fore.RED +
              "\nKhông có dữ liệu.")

        pause()

        return

    try:

        df = pd.DataFrame(
            data["transactions"]
        )

        filename = "transactions_report.csv"

        df.to_csv(
            filename,
            index=False
        )

        print(Fore.GREEN +
              f"\nĐã export: {filename}")

    except Exception as e:

        print(Fore.RED +
              f"\nLỗi export:\n{e}")

    pause()


# =========================================================
# AI PREDICTION TEST
# =========================================================

def ai_test():

    clear()

    title("AI CLASSIFICATION TEST")

    samples = [

        "Mua pizza tối",
        "Thanh toán tiền điện",
        "Mua khóa học AI",
        "Nhận lương công ty",
        "Mua tai nghe gaming"
    ]

    print(Fore.CYAN +
          "\nAI DEMO PREDICTIONS\n")

    for sample in samples:

        category = classify_transaction(
            sample
        )

        print(Fore.GREEN +
              f"{sample}")

        print(Fore.YELLOW +
              f"-> {category}\n")

    pause()


# =========================================================
# DEMO MODE
# =========================================================

def demo_mode():

    clear()

    title("DEMO AI BANK SYSTEM")

    demo_transactions = [

        {
            "description": "Mua cơm trưa",
            "amount": 50000,
            "category": "Food"
        },

        {
            "description": "Đóng học phí",
            "amount": 5000000,
            "category": "Education"
        },

        {
            "description": "Lương part-time",
            "amount": 3000000,
            "category": "Income"
        }
    ]

    data["transactions"] = demo_transactions

    save_data()

    print(Fore.GREEN +
          "\nĐã tạo dữ liệu demo.")

    pause()


# =========================================================
# EXPLAIN AI
# =========================================================

def explain():

    clear()

    title("GIẢI THÍCH AI CLASSIFICATION")

    print(Fore.WHITE + """
=========================================================
1. MACHINE LEARNING
=========================================================

AI học từ dữ liệu:
   ✓ Training Data
   ✓ Labels

=========================================================
2. NLP
=========================================================

Natural Language Processing

=========================================================
3. TEXT CLASSIFICATION
=========================================================

AI phân loại:
   ✓ Food
   ✓ Education
   ✓ Income

=========================================================
4. NAIVE BAYES
=========================================================

Thuật toán ML:
   ✓ Đơn giản
   ✓ Hiệu quả

=========================================================
5. COUNT VECTORIZER
=========================================================

Chuyển text -> vector số.

=========================================================
6. FRAUD DETECTION
=========================================================

Tìm giao dịch:
   ✓ Bất thường
   ✓ Đáng ngờ

=========================================================
7. FINTECH
=========================================================

Ứng dụng:
   ✓ Banking AI
   ✓ Digital Wallet
   ✓ Expense AI

=========================================================
8. ỨNG DỤNG THỰC TẾ
=========================================================

✓ Banking Apps
✓ Financial Analytics
✓ AI Accounting
✓ Smart Expense Tracking
""")

    pause()


# =========================================================
# MENU
# =========================================================

def menu():

    load_data()

    while True:

        clear()

        title("AI BANK TRANSACTION CLASSIFIER")

        print(Fore.CYAN + """
[1] Giới thiệu AI System
[2] Thêm giao dịch
[3] Xem giao dịch
[4] Transaction statistics
[5] Fraud detection
[6] Search transaction
[7] Export CSV report
[8] AI prediction demo
[9] Demo mode
[10] Giải thích AI
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

            add_transaction()

        elif choice == '3':

            view_transactions()

        elif choice == '4':

            statistics()

        elif choice == '5':

            fraud_detection()

        elif choice == '6':

            search_transaction()

        elif choice == '7':

            export_csv()

        elif choice == '8':

            ai_test()

        elif choice == '9':

            demo_mode()

        elif choice == '10':

            explain()

        elif choice == '0':

            clear()

            title("KẾT THÚC CHƯƠNG TRÌNH")

            print(Fore.GREEN + """
Cảm ơn bạn đã sử dụng AI Bank Classifier.

Kiến thức đạt được:
   ✓ Machine Learning
   ✓ NLP
   ✓ AI Classification
   ✓ Financial Analytics
   ✓ Naive Bayes
   ✓ FinTech AI
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
