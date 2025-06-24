import tkinter as tk
from tkinter import ttk, messagebox
from navbar import Navbar
from utilities import center_window, fetch_data, draw_horizontal_gradient
from tkcalendar import DateEntry
import mysql.connector, subprocess

def update_layout(event):
    w = root.winfo_height()
    h = root.winfo_height()
    frame_navbar.place(x=0, y=0, relwidth=1, height=60)
    frame_treeview.place(x=0, y=60, relwidth=1, height=h-60)

def refresh():
    root.destroy()
    subprocess.Popen(["python", "monthly_pass.py"])

def search_data():
    keyword = search_var.get().lower()
    data = fetch_data(f"SELECT * FROM monthly_pass WHERE LOWER(license_plate_number) LIKE '%{keyword}%'")
    treeview.delete(*treeview.get_children())
    
    for row in data:
        treeview.insert("", "end", values=row)

def add_monthly_pass():
    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO monthly_pass (vehicle_type, license_plate_number, expired_date) VALUES (%s, %s, %s)", (vehicle_type_entry.get(), license_plate_number_entry.get(), expired_date_entry.get_date()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Thêm loại thời gian thành công!")
        refresh()
    def cancel():
        window.destroy()
    
    """Hiện form thêm loại vé tháng mới."""
    window = tk.Toplevel()
    window.title("Thêm Loại Thời Gian Mới")
    window.geometry("500x250")
    window.transient(root) # Keep on top of main window
    window.grab_set()    # Modal window
    window.resizable(False, False)
    center_window(window)
    
    for i in range(5):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)
        
    window_label = ttk.Label(window, text="Thêm vé tháng mới", font=("Space Grotesk Medium", 16), anchor="center")
    window_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
    
    vehicle_type_label = ttk.Label(window, text="Loại xe", font=("Space Grotesk Medium", 12))
    vehicle_type_label.grid(row=1, column=0, sticky="we", padx=10, pady=10)  
    vehicle_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    vehicle_type_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    license_plate_number_label = ttk.Label(window, text="Biển số xe", font=("Space Grotesk Medium", 12))
    license_plate_number_label.grid(row=2, column=0, sticky="we", padx=10, pady=10)
    license_plate_number_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    license_plate_number_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    expired_date_label = ttk.Label(window, text="Ngày hết hạn", font=("Space Grotesk Medium", 12))
    expired_date_label.grid(row=3, column=0, sticky="we", padx=10, pady=10)
    expired_date_entry = DateEntry(window, date_pattern="dd/mm/yyyy", font=("Space Grotesk Medium", 12))
    expired_date_entry.get_date().strftime("%Y-%m-%d")
    expired_date_entry.grid(row=3, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=4, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=cancel)
    cancel_button.grid(row=4, column=2, sticky="we", padx=10, pady=10)
    
def modify_monthly_pass():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa.")
        return

    values = treeview.item(selected[0], "values")
    id, old_vehicle_type, old_license_plate, old_expired_date = values

    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("UPDATE monthly_pass SET vehicle_type=%s, license_plate_number=%s, expired_date=%s WHERE id=%s",
                       (vehicle_type_entry.get(), license_plate_number_entry.get(), expired_date_entry.get_date(), id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        window.destroy()
        refresh()

    window = tk.Toplevel()
    window.title("Sửa Vé Tháng")
    window.geometry("500x250")
    window.transient(root)
    window.grab_set()
    window.resizable(False, False)
    center_window(window)
    
    for i in range(5):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)

    window_label = ttk.Label(window, text="Sửa vé tháng", font=("Space Grotesk Medium", 16), anchor="center")
    window_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
    
    vehicle_type_label = ttk.Label(window, text="Loại xe", font=("Space Grotesk Medium", 12))
    vehicle_type_label.grid(row=1, column=0, sticky="we", padx=10, pady=10)  
    vehicle_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    vehicle_type_entry.insert(0, old_vehicle_type)
    vehicle_type_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    license_plate_number_label = ttk.Label(window, text="Biển số xe", font=("Space Grotesk Medium", 12))
    license_plate_number_label.grid(row=2, column=0, sticky="we", padx=10, pady=10)
    license_plate_number_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    license_plate_number_entry.insert(0, old_license_plate)
    license_plate_number_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    expired_date_label = ttk.Label(window, text="Ngày hết hạn", font=("Space Grotesk Medium", 12))
    expired_date_label.grid(row=3, column=0, sticky="we", padx=10, pady=10)
    expired_date_entry = DateEntry(window, date_pattern="dd/mm/yyyy", font=("Space Grotesk Medium", 12))
    try:
        # Cố gắng đặt ngày từ chuỗi ngày cũ
        expired_date_entry.set_date(old_expired_date)
    except:
        # Nếu không thành công, sử dụng ngày hiện tại
        pass
    expired_date_entry.grid(row=3, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=4, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=window.destroy)
    cancel_button.grid(row=4, column=2, sticky="we", padx=10, pady=10)

def delete_monthly_pass():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xoá.")
        return

    values = treeview.item(selected[0], "values")
    id, vehicle_type, license_plate = values[:3]

    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá vé tháng cho xe '{license_plate}'?")
    if not confirm:
        return

    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="project001")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM monthly_pass WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Thông báo", "Đã xoá thành công.")
    refresh()
    

# Setup UI
root = tk.Tk()
root.title("Quản lý vé tháng")
root.geometry("1200x600")
root.minsize(1200, 300)
root.config(bg="white")
style = ttk.Style(root)
center_window(root)

style.configure("Treeview",
                font=('Segoe UI', 12),
                background="#f0f0f0",
                foreground="black",
                rowheight=28,
                fieldbackground="#f0f0f0")
style.configure("Treeview.Heading",
                font=('Segoe UI', 12, 'bold'),
                background="#d9d9d9",
                foreground="black")
style.configure("TButton", font=("Space Grotesk Medium", 10), background="white")

# Navbar
frame_navbar = Navbar(root)
frame_navbar.place(x=0, y=0, relwidth=1, height=60)

# Main content area
frame_treeview = tk.Frame(root, bg="white")

# Search bar
frame_treeview_navbar = tk.Frame(frame_treeview, bg="white")
frame_treeview_navbar.pack(fill="both")

treeview_label = tk.Canvas(frame_treeview_navbar, height=40, width=420, bg="white", highlightthickness=0)
treeview_label.pack(side="left", padx=16, pady=10)
draw_horizontal_gradient(treeview_label, "steel blue", "white", height=40, width=420)
treeview_label.create_text(10, 20, anchor="w", text="Danh sách xe đăng ký vé tháng", font=("Space Grotesk Medium", 16), fill="white")

search_var = tk.StringVar()
search_entry = ttk.Entry(frame_treeview_navbar, textvariable=search_var, width=30, font=("Space Grotesk Medium", 10))
search_entry.pack(side="right", padx=16, pady=10)

search_button = ttk.Button(frame_treeview_navbar, text="Tìm kiếm", command=search_data)
search_button.pack(side="right", pady=10)
root.bind("<Return>", lambda event: search_data())

delete_button = ttk.Button(frame_treeview_navbar, text="Xóa vé tháng", command=delete_monthly_pass)
delete_button.pack(side="right", padx=(0, 16), pady=10)

modify_button = ttk.Button(frame_treeview_navbar, text="Sửa vé tháng", command=modify_monthly_pass)
modify_button.pack(side="right", padx=(0, 16), pady=10)

add_button = ttk.Button(frame_treeview_navbar, text="Thêm vé tháng", command=add_monthly_pass)
add_button.pack(side="right", padx=(0, 16), pady=10)

# Treeview setup

data = fetch_data("SELECT id, vehicle_type, license_plate_number, expired_date FROM monthly_pass")
columns = ("STT", "Loại xe", "Biển số", "Ngày hết hạn")
treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings", height=len(data))

# Configure columns
column_widths = {"STT": 50, "Loại xe": 100, "Biển số": 100, "Ngày hết hạn": 100}

for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=column_widths[col], anchor="center")

for row in data:
    treeview.insert("", "end", values=row)


# Tạo scrollbar cho treeview
scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y',)

treeview.pack(expand=True, fill="both", padx=(16, 0), pady=(0, 16))

# Sizegrip and layout binding
size_grip = ttk.Sizegrip(root)
size_grip.place(relx=1, rely=1, anchor="se")
root.bind("<Configure>", update_layout)

root.mainloop()