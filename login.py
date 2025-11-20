import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess
from utilities import center_window

def check_login():
    username = username_entry.get()
    password = password_entry.get()

    # Kết nối đến cơ sở dữ liệu MySQL
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Thay bằng tên người dùng của bạn
            password='',  # Thay bằng mật khẩu của bạn
            database='project001'  # Tên cơ sở dữ liệu
        )

        cursor = connection.cursor()

        # Truy vấn để kiểm tra tài khoản và mật khẩu
        query = "SELECT * FROM employees WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        # Kiểm tra kết quả trả về
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            subprocess.Popen(["python", "home.py"])
            root.quit()

        else:
            # Đăng nhập không thành công
            messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không đúng!")
            username_entry.focus_set()

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {err}")
        username_entry.focus_set()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

root = tk.Tk()
root.title("Đăng nhập")
root.geometry("1200x675")
root.resizable(False, False)
center_window(root)

# Load ảnh nền
bg_image = Image.open(r"image\bg.png")
bg_image = ImageTk.PhotoImage(bg_image)

# Load và resize logo
logo_image = Image.open(r"image\logo.png")
logo_image = logo_image.resize((100, 100), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(logo_image)

# Đặt ảnh nền
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Form login
login_form = tk.Frame(root, relief="raised", borderwidth=5, bg="white")
login_form.place(x=400, y=75, width=400, height=500)

# Cấu hình lưới
for i in range(10):
    login_form.rowconfigure(i, weight=1)
login_form.columnconfigure(0, weight=1)

# Widgets
logo = ttk.Label(login_form, image=logo_image, background="white")
label_1 = ttk.Label(login_form, text="Đăng nhập hệ thống", font=("Space Grotesk Medium", 20, "bold"), background="white", foreground="navy", anchor="center")
label_2 = ttk.Label(login_form, text="Nhận diện biển số xe", font=("Space Grotesk Medium", 16, "bold"), background="white", foreground="tomato", anchor="center")
separator = ttk.Separator(login_form, orient="horizontal")

style = ttk.Style()
style.configure("TButton", font=("Space Grotesk Medium", 14))

username_label = ttk.Label(login_form, text="Tài khoản", font=("Segoe UI", 12, "bold"), background="white", anchor="center")
username_entry = ttk.Entry(login_form, font=("Segoe UI", 12))
username_entry.focus_set() # Đưa con trỏ vào ngay khi mở app

password_label = ttk.Label(login_form, text="Mật khẩu", font=("Segoe UI", 12, "bold"), background="white", anchor="center")
password_entry = ttk.Entry(login_form, show="*", font=("Segoe UI", 12))

submit = ttk.Button(login_form, text="Đăng nhập", command=check_login)
root.bind("<Return>", lambda event: check_login())

# Đặt widget
logo.grid(row=0, rowspan=2, column=0)
label_1.grid(row=2, column=0, sticky="nswe")
label_2.grid(row=3, column=0, sticky="nswe")
separator.grid(row=4, column=0, sticky="ew", padx=10)
username_label.grid(row=5, column=0, sticky="w", padx=20)
username_entry.grid(row=6, column=0, sticky="ew", padx=20)
password_label.grid(row=7, column=0, sticky="w", padx=20)
password_entry.grid(row=8, column=0, sticky="ew", padx=20)
submit.grid(row=9, column=0, sticky="ew", padx=50, pady=(10, 20))

root.mainloop()
