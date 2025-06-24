import tkinter as tk
from tkinter import ttk
from navbar import Navbar
import subprocess, threading, time
from utilities import center_window

root = tk.Tk()
root.title("Trang chủ")
root.geometry("1200x600")
root.minsize(800, 600)
root.config(bg="white")
center_window(root)

def update_padding(event):
    w = root.winfo_width()
    h = root.winfo_height()
    frame_navbar.place(x=0, y=0, relwidth=1, height=50 + h*0.025)
    frame_main.place(x=int(w * 0.1), y=int(h * 0.2), relwidth=0.8, relheight=0.7)

frame_navbar = Navbar(root)
frame_navbar.place(x=0, y=0, relwidth=1, height=60)

frame_main = tk.Frame(root, bg="#B0C4DE", borderwidth=1, relief="solid")
frame_main.place(x=120, y=120, relwidth=0.8, relheight=0.7)

for i in range(3):
    frame_main.rowconfigure(i, weight=1)
for i in range(2):
    frame_main.columnconfigure(i, weight=1)
    
frame_main_label = ttk.Label(frame_main, text="Chào mừng bạn đến với Hệ Thống", background="#B0C4DE", font=("Space Grotesk Medium", 20), anchor="center")
frame_main_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Style cho nút
style = ttk.Style()
style.configure("TButton", font=("Space Grotesk Medium", 16), padding=10, background="#B0C4DE")

# Các nút chức năng
btn_recognition = ttk.Button(frame_main, text="Nhận diện biển số xe", style="TButton")
btn_recognition.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

btn_vehicle_logs = ttk.Button(frame_main, text="Quản lý xe đang gửi", style="TButton")
btn_vehicle_logs.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

btn_tickets = ttk.Button(frame_main, text="Quản lý giá vé", style="TButton")
btn_tickets.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

btn_monthly_pass = ttk.Button(frame_main, text="Quản lý vé tháng", style="TButton")
btn_monthly_pass.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)

size_grip = ttk.Sizegrip(root)
size_grip.place(relx=1, rely=1, anchor="se")

# Progress bar và label thông báo
frame_loading = tk.Frame(root, bg="white", relief="ridge", bd=2)
frame_loading.place(relx=0.5, rely=0.5, anchor="center", width=400, height=100)
frame_loading.lower()  # Ẩn ban đầu

loading_label = ttk.Label(frame_loading, text="Đang khởi động ứng dụng...", background="white", font=("Space Grotesk Medium", 14))
loading_label.pack(pady=10)

progress_bar = ttk.Progressbar(frame_loading, mode="indeterminate", length=300)
progress_bar.pack(pady=10)

root.bind("<Configure>", update_padding)

def open_file_with_loading(filename):
    """Hàm mở một file Python với progress bar loading."""
    # Hiển thị màn hình loading
    frame_main.lower()  # Đẩy frame chính xuống dưới
    frame_loading.lift()  # Đưa frame loading lên trên
    progress_bar.start(10)  # Bắt đầu animation progress bar
    
    # Vô hiệu hóa các nút trong khi loading
    btn_recognition.state(['disabled'])
    btn_vehicle_logs.state(['disabled'])
    btn_tickets.state(['disabled'])
    btn_monthly_pass.state(['disabled'])
    
    def launch_app():
        try:
            # Giả lập thời gian loading (có thể bỏ nếu quá trình mở file đã đủ lâu)
            time.sleep(1.5)
            
            # Khởi động ứng dụng mới
            subprocess.Popen(["python", filename])
            
            # Đóng cửa sổ hiện tại sau khi khởi động thành công
            if filename != r"yolov10/recognition.py":
                root.after(500, root.destroy)
            else:
                root.after(10000, root.destroy)
            
        except Exception as e:
            # Nếu có lỗi, hiển thị thông báo và quay lại giao diện chính
            print(f"Lỗi khi mở {filename}: {e}")
            progress_bar.stop()
            frame_loading.lower()
            frame_main.lift()
            
            # Kích hoạt lại các nút
            btn_recognition.state(['!disabled'])
            btn_vehicle_logs.state(['!disabled'])
            btn_tickets.state(['!disabled'])
            btn_monthly_pass.state(['!disabled'])
            
            tk.messagebox.showerror("Lỗi", f"Không thể mở {filename}.")
    
    # Chạy quá trình mở file trong thread riêng
    threading.Thread(target=launch_app, daemon=True).start()

# Gắn các sự kiện click cho các nút
btn_recognition.bind("<Button-1>", lambda event: open_file_with_loading(r"yolov10/recognition.py"))
btn_vehicle_logs.bind("<Button-1>", lambda event: open_file_with_loading("vehicles.py"))
btn_tickets.bind("<Button-1>", lambda event: open_file_with_loading("tickets.py"))
btn_monthly_pass.bind("<Button-1>", lambda event: open_file_with_loading("monthly_pass.py"))

root.mainloop()