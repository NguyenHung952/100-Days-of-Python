# 📅 Day 4 – Random hóa & Danh sách trong Python

## 🎯 Mục tiêu
- Làm quen với thư viện `random` và các hàm: `randint()`, `choice()`, `shuffle()`
- Tạo, thao tác và in ra danh sách (`list`)
- Kết hợp random + list để tạo ra các ứng dụng nhỏ mang tính mô phỏng hoặc trò chơi

---

## 🛠 Bài tập đã thực hiện

### ✅ 1. Mô phỏng tung đồng xu
In ra kết quả ngẫu nhiên: "Mặt ngửa" hoặc "Mặt sấp"

👉 *File*: `Day4.ipynb`

---

### ✅ 2. Ai trả tiền hôm nay?
Chọn ngẫu nhiên một người trong danh sách tên nhập vào.

👉 *File*: `Day4.ipynb`

---

### ✅ 3. Trò chơi Bản đồ kho báu
- Tạo lưới 3x3 bằng danh sách lồng nhau
- Người dùng nhập vị trí để đánh dấu "X"

👉 *File*: `Day4.ipynb`

---

## 📌 Ghi chú học tập

- `import random` là thư viện chuẩn, không cần cài đặt
- Một số hàm quan trọng:
  ```python
  random.randint(1, 10)        # Số ngẫu nhiên từ 1 đến 10
  random.choice(list_name)    # Lấy phần tử ngẫu nhiên trong list
  random.shuffle(list_name)   # Xáo trộn danh sách
