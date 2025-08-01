# 📅 Day 2 – Kiểu dữ liệu & Xử lý chuỗi trong Python

## 🎯 Mục tiêu
- Ôn lại và phân biệt các kiểu dữ liệu: `str`, `int`, `float`, `bool`
- Làm quen với thao tác xử lý chuỗi: nối chuỗi, slicing, định dạng
- Áp dụng ép kiểu (`int()`, `float()`, `str()`)
- Sử dụng các hàm chuỗi như `.lower()`, `.upper()`, `.count()`, `len()`

---

## 🛠 Bài tập đã thực hiện

### ✅ 1. Máy tính chỉ số BMI
Tính toán chỉ số BMI từ chiều cao và cân nặng người dùng nhập vào.

👉 *File*: `Day2.ipynb`

---

### ✅ 2. Phân tích số điện thoại
Tách mã vùng và số thuê bao từ chuỗi số điện thoại.

👉 *File*: `Day2.ipynb`

---

### ✅ 3. Bộ đếm ký tự trong chuỗi
Tính độ dài chuỗi và đếm số lần xuất hiện của một ký tự cụ thể.

👉 *File*: `Day2.ipynb`

---

## 📌 Ghi chú học tập

- Hàm `len()` cho biết độ dài chuỗi
- Dùng slicing: `text[0:3]` để lấy ký tự từ vị trí 0 đến 2
- Ép kiểu cần thiết khi dùng `input()`:
  ```python
  age = int(input("Nhập tuổi: "))

