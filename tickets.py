import tkinter as tk
from tkinter import ttk, messagebox
from navbar import Navbar
import mysql.connector, subprocess
from utilities import center_window, fetch_data

def update_padding(event):
    # Đặt các frame vào place
    w = root.winfo_width()
    h = root.winfo_height()
    frame_navbar.place(x = 0, y = 0, relwidth = 1, height = 60)
    frame_main_2.place(x = 16, y = 60 + 16, width = w/3*2 - 24, height = h - 92)
    frame_main_1.place(x = w/3*2 + 8, y = 60 + 16, width = w/3 - 16 - 8, height = (h - 60 - 16*3) / 2)
    frame_main_3.place(x = w/3*2 + 8, y = 60 + 16 + frame_main_1.winfo_height() + 16, width = w/3 - 16 - 8, height = (h - 60 - 16*3) / 2)

def refresh():
    root.destroy()
    subprocess.Popen(["python", "tickets.py"])
    
def update_ticket_type_tree(cursor):
    # Bước 1: Lưu dữ liệu cũ vào dict với key là (vehicle_type, time)
    cursor.execute("SELECT vehicle_type, time, ticket_type, price FROM ticket_types")
    old_ticket_data = cursor.fetchall()
    old_ticket_dict = {
        (row[0], row[1]): (row[2], row[3])
        for row in old_ticket_data
    }

    # Bước 2: Xoá sạch bảng
    cursor.execute("DELETE FROM ticket_types")

    # Bước 3: Lấy dữ liệu để chèn lại
    cursor.execute("SELECT name, start, end FROM time_types")
    time_type_data = cursor.fetchall()

    cursor.execute("SELECT name FROM vehicle_types")
    vehicle_type_data = cursor.fetchall()

    # Bước 4: Chèn lại dữ liệu, dùng lại ticket_type và price nếu có
    for time_type in time_type_data:
        for vehicle_type in vehicle_type_data:
            key = (vehicle_type[0], time_type[0])
            ticket_type, price = old_ticket_dict.get(key, ("", 0))

            cursor.execute(
                "INSERT INTO ticket_types (vehicle_type, time, start, end, ticket_type, price) VALUES (%s, %s, %s, %s, %s, %s)",
                (vehicle_type[0], time_type[0], time_type[1], time_type[2], ticket_type, price)
            )


root = tk.Tk()
root.title("Quản lý giá vé")
root.geometry("1500x600")
root.minsize(800, 600)
root.config(bg="white")
center_window(root)

style = ttk.Style()
style.configure("Treeview",
                font=('Segoe UI', 12),
                background="#f0f0f0",
                foreground="black",
                rowheight=30,
                fieldbackground="#f0f0f0")
style.configure("Treeview.Heading",
                font=('Segoe UI', 12, 'bold'),
                background="#d9d9d9",
                foreground="black")
style.configure("TButton", font=("Space Grotesk Medium", 11), background="white")

frame_navbar = Navbar(root)

# -------------------- Frame 1 - Thông tin thời gian -----------------------------

# --- Hàm add_time_type ---
def add_time_type():
    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO time_types (name, start, end) VALUES (%s, %s, %s)", (name_entry.get(), start_entry.get(), end_entry.get()))
        update_ticket_type_tree(cursor)
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Thêm loại thời gian thành công!")
        refresh()
    def cancel():
        window.destroy()
        
    """Hiện form thêm loại thời gian mới."""
    window = tk.Toplevel()
    window.title("Thêm Loại Thời Gian Mới")
    window.geometry("400x200")
    window.transient(root) # Keep on top of main window
    window.grab_set()    # Modal window
    window.resizable(False, False)
    center_window(window)
    
    for i in range(4):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)
    
    name_label = ttk.Label(window, text="Tên loại thời gian", font=("Space Grotesk Medium", 12))
    name_label.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    name_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    name_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    start_label = ttk.Label(window, text="Bắt đầu", font=("Space Grotesk Medium", 12))
    start_label.grid(row=1, column=0, sticky="we", padx=10, pady=10)
    start_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    start_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    end_label = ttk.Label(window, text="Kết thúc", font=("Space Grotesk Medium", 12))
    end_label.grid(row=2, column=0, sticky="we", padx=10, pady=10)
    end_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    end_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save, )
    save_button.grid(row=3, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=cancel)
    cancel_button.grid(row=3, column=2, sticky="we", padx=10, pady=10)

def modify_time_type():
    selected = frame_main_1_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa.")
        return

    values = frame_main_1_tree.item(selected[0], "values")
    old_name, old_start, old_end = values

    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("UPDATE time_types SET name=%s, start=%s, end=%s WHERE name=%s AND start=%s AND end=%s",
                       (name_entry.get(), start_entry.get(), end_entry.get(), old_name, old_start, old_end))
        update_ticket_type_tree(cursor)
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        window.destroy()
        refresh()

    window = tk.Toplevel()
    window.title("Sửa Loại Thời Gian")
    window.geometry("400x200")
    window.transient(root)
    window.grab_set()
    window.resizable(False, False)
    center_window(window)
    
    for i in range(4):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)

    name_label = ttk.Label(window, text="Tên loại thời gian", font=("Space Grotesk Medium", 12))
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    name_entry.insert(0, old_name)
    name_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

    start_label = ttk.Label(window, text="Bắt đầu", font=("Space Grotesk Medium", 12))
    start_label.grid(row=1, column=0, padx=10, pady=10)
    start_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    start_entry.insert(0, old_start)
    start_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    end_label = ttk.Label(window, text="Kết thúc", font=("Space Grotesk Medium", 12))
    end_label.grid(row=2, column=0, padx=10, pady=10)
    end_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    end_entry.insert(0, old_end)
    end_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=3, column=1, padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=window.destroy)
    cancel_button.grid(row=3, column=2, padx=10, pady=10)
    
def delete_time_type():
    selected = frame_main_1_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xoá.")
        return

    values = frame_main_1_tree.item(selected[0], "values")
    name, start, end = values

    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá loại thời gian '{name}'?")
    if not confirm:
        return

    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="project001")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM time_types WHERE name=%s AND start=%s AND end=%s", (name, start, end))
    update_ticket_type_tree(cursor)
    conn.commit()
    conn.close()

    messagebox.showinfo("Thông báo", "Đã xoá thành công.")
    refresh()
    
frame_main_1 = tk.Frame(root, bg="white", relief="ridge", bd=1)

frame_main_1_label = tk.Label(frame_main_1, text="Thông tin loại thời gian", background="steel blue", font=("Space Grotesk Medium", 16), fg="white")
frame_main_1_label.pack(fill="x")

frame_main_1_data = fetch_data("SELECT name, start, end FROM time_types")
frame_main_1_tree = ttk.Treeview(frame_main_1, columns=("name", "start", "end"), show="headings", height=len(frame_main_1_data))

column_details = {
    "name": {"text": "Thời gian", "width": 50},
    "start": {"text": "Bắt đầu", "width": 50},
    "end": {"text": "Kết thúc", "width": 50}
}
for col, details in column_details.items():
    frame_main_1_tree.heading(col, text=details["text"])
    frame_main_1_tree.column(col, anchor="center", width=details["width"])
    
for row in frame_main_1_data:
    frame_main_1_tree.insert("", "end", values=row)
    
frame_main_1_tree.pack(fill="both", expand=True, padx=10, pady=10)

frame_main_1_delete_button = ttk.Button(frame_main_1, text="Xoá loại thời gian", command=delete_time_type)
frame_main_1_delete_button.pack(side="right", padx=10, pady=(0, 10))

frame_main_1_modify_button = ttk.Button(frame_main_1, text="Sửa loại thời gian", command=modify_time_type)
frame_main_1_modify_button.pack(side="right", padx=(10, 0), pady=(0, 10))

frame_main_1_add_button = ttk.Button(frame_main_1, text="Thêm loại thời gian", command=add_time_type)
frame_main_1_add_button.pack(side="right", padx=(10, 0), pady=(0, 10))

# ------------------------------ Frame 2 - Thông tin loại xe và giá vé ---------------------------------------
"""
def add_ticket_type():
    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ticket_types (vehicle_type, time, start, end, ticket_type, price) VALUES (%s, %s, %s, %s, %s, %s)", (vehicle_type_entry.get(), time_entry.get(), start_entry.get(), end_entry.get(), ticket_type_entry.get(), price_entry.get()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Thêm loại thời gian thành công!")
        refresh()
    def cancel():
        window.destroy()
        
    window = tk.Toplevel()
    window.title("Thêm Loại Thời Gian Mới")
    window.geometry("400x400")
    window.transient(root) # Keep on top of main window
    window.grab_set()    # Modal window
    window.resizable(False, False)
    center_window(window)
    
    for i in range(7):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)
    
    vehicle_type_label = ttk.Label(window, text="Loại xe", font=("Space Grotesk Medium", 12))
    vehicle_type_label.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    vehicle_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    vehicle_type_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    time_label = ttk.Label(window, text="Thời gian", font=("Space Grotesk Medium", 12))
    time_label.grid(row=1, column=0, sticky="we", padx=10, pady=10)
    time_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    time_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    start_label = ttk.Label(window, text="Bắt đầu", font=("Space Grotesk Medium", 12))
    start_label.grid(row=2, column=0, sticky="we", padx=10, pady=10)
    start_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    start_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    end_label = ttk.Label(window, text="Kết thúc", font=("Space Grotesk Medium", 12))
    end_label.grid(row=3, column=0, sticky="we", padx=10, pady=10)
    end_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    end_entry.grid(row=3, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    ticket_type_label = ttk.Label(window, text="Loại vé", font=("Space Grotesk Medium", 12))
    ticket_type_label.grid(row=4, column=0, sticky="we", padx=10, pady=10)
    ticket_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    ticket_type_entry.grid(row=4, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    price_label = ttk.Label(window, text="Giá", font=("Space Grotesk Medium", 12))
    price_label.grid(row=5, column=0, sticky="we", padx=10, pady=10)
    price_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    price_entry.grid(row=5, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save, )
    save_button.grid(row=6, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=cancel)
    cancel_button.grid(row=6, column=2, sticky="we", padx=10, pady=10)
"""
    
def modify_ticket_type():
    selected = frame_main_2_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa.")
        return
    values = frame_main_2_tree.item(selected[0], "values")
    old_vehicle_type, old_time, old_start, old_end, old_ticket_type, old_price = values
    
    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE ticket_types 
            SET vehicle_type=%s, time=%s, start=%s, end=%s, ticket_type=%s, price=%s 
            WHERE vehicle_type=%s AND time=%s AND start=%s AND end=%s AND ticket_type=%s AND price=%s
        """, (
            vehicle_type_entry.get(), time_entry.get(), start_entry.get(), end_entry.get(), ticket_type_entry.get(), price_entry.get(),
            old_vehicle_type, old_time, old_start, old_end, old_ticket_type, old_price
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        window.destroy()
        refresh()
    
    window = tk.Toplevel()
    window.title("Sửa Loại Vé")
    window.geometry("400x400")
    window.transient(root)
    window.grab_set()
    window.resizable(False, False)
    center_window(window)
    
    for i in range(7):
        window.rowconfigure(i, weight=1)
    for i in range(3):
        window.columnconfigure(i, weight=1)
        
    vehicle_type_label = ttk.Label(window, text="Loại xe", font=("Space Grotesk Medium", 12))
    vehicle_type_label.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    vehicle_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    vehicle_type_entry.insert(0, old_vehicle_type)
    vehicle_type_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    time_label = ttk.Label(window, text="Thời gian", font=("Space Grotesk Medium", 12))
    time_label.grid(row=1, column=0, sticky="we", padx=10, pady=10)
    time_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    time_entry.insert(0, old_time)
    time_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    start_label = ttk.Label(window, text="Bắt đầu", font=("Space Grotesk Medium", 12))
    start_label.grid(row=2, column=0, sticky="we", padx=10, pady=10)
    start_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    start_entry.insert(0, old_start)
    start_entry.grid(row=2, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    end_label = ttk.Label(window, text="Kết thúc", font=("Space Grotesk Medium", 12))
    end_label.grid(row=3, column=0, sticky="we", padx=10, pady=10)
    end_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    end_entry.insert(0, old_end)
    end_entry.grid(row=3, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    ticket_type_label = ttk.Label(window, text="Loại vé", font=("Space Grotesk Medium", 12))
    ticket_type_label.grid(row=4, column=0, sticky="we", padx=10, pady=10)
    ticket_type_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    ticket_type_entry.insert(0, old_ticket_type)
    ticket_type_entry.grid(row=4, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    price_label = ttk.Label(window, text="Giá", font=("Space Grotesk Medium", 12))
    price_label.grid(row=5, column=0, sticky="we", padx=10, pady=10)
    price_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    price_entry.insert(0, old_price)
    price_entry.grid(row=5, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=6, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=window.destroy)
    cancel_button.grid(row=6, column=2, sticky="we", padx=10, pady=10)
    
"""
def delete_ticket_type():
    selected = frame_main_2_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xoá.")
        return

    values = frame_main_2_tree.item(selected[0], "values")
    vehicle_type, time, start, end, ticket_type, price = values

    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá loại vé này?")
    if not confirm:
        return

    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="project001")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ticket_types WHERE vehicle_type=%s AND time=%s AND start=%s AND end=%s AND ticket_type=%s AND price=%s", (vehicle_type, time, start, end, ticket_type, price))
    conn.commit()
    conn.close()

    messagebox.showinfo("Thông báo", "Đã xoá thành công.")
    refresh()
"""
    
frame_main_2 = tk.Frame(root, bg="white", relief="ridge", bd=1)

frame_main_2_label = tk.Label(frame_main_2, text="Thông tin loại vé", background="steel blue", font=("Space Grotesk Medium", 16), fg="white")
frame_main_2_label.pack(fill="x")

frame_main_2_data = fetch_data("SELECT vehicle_type, time, start, end, ticket_type, price FROM ticket_types")
frame_main_2_tree = ttk.Treeview(frame_main_2, columns=("vehicle_type", "time", "start", "end", "ticket_type", "price"), show="headings", height=len(frame_main_2_data))

column_details = {
    "vehicle_type": {"text": "Loại xe", "width": 50},
    "time": {"text": "Thời gian", "width": 50},
    "start": {"text": "Bắt đầu", "width": 50},
    "end": {"text": "Kết thúc", "width": 50},
    "ticket_type": {"text": "Loại vé", "width": 50},
    "price": {"text": "Giá", "width": 50}
}
for col, details in column_details.items():
    frame_main_2_tree.heading(col, text=details["text"])
    frame_main_2_tree.column(col, anchor="center", width=details["width"])

for row in frame_main_2_data:
    frame_main_2_tree.insert("", "end", values=row)

# Tạo scrollbar cho treeview
frame_main_2_scrollbar = ttk.Scrollbar(frame_main_2, orient="vertical", command=frame_main_2_tree.yview)
frame_main_2_tree.configure(yscrollcommand=frame_main_2_scrollbar.set)
frame_main_2_scrollbar.pack(side='right', fill='y')

frame_main_2_tree.pack(fill="both", expand=True, padx=10, pady=10)

"""
frame_main_2_delete_button = ttk.Button(frame_main_2, text="Xoá loại vé", command=delete_ticket_type)
frame_main_2_delete_button.pack(side="right", padx=10, pady=(0, 10))
"""

frame_main_2_modify_button = ttk.Button(frame_main_2, text="Sửa loại vé", command=modify_ticket_type)
frame_main_2_modify_button.pack(side="right", padx=10, pady=(0, 10))

"""
frame_main_2_add_button = ttk.Button(frame_main_2, text="Thêm loại vé", command=add_ticket_type)
frame_main_2_add_button.pack(side="right", padx=(10, 0), pady=(0, 10))
"""

# -------------------------------------- Frame 3 - Danh sách loại xe -----------------------------------------
def add_vehicle_type():
    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicle_types (name) VALUES (%s)", (name_entry.get(),))
        update_ticket_type_tree(cursor)
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Thêm loại xe thành công!")
        refresh()
    def cancel():
        window.destroy()
        
    """Hiện form thêm loại xe mới."""
    window = tk.Toplevel()
    window.title("Thêm Loại Xe Mới")
    window.geometry("400x100")
    window.transient(root) # Keep on top of main window
    window.grab_set()    # Modal window
    window.resizable(False, False)
    center_window(window)
    
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)
    
    name_label = ttk.Label(window, text="Tên loại xe", font=("Space Grotesk Medium", 12))
    name_label.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    name_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    name_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)
    
    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=1, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=cancel)
    cancel_button.grid(row=1, column=2, sticky="we", padx=10, pady=10)

def modify_vehicle_type():
    selected = frame_main_3_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa.")
        return

    old_name = frame_main_3_tree.item(selected[0], "values")[0]

    def save():
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="project001")
        cursor = conn.cursor()
        cursor.execute("UPDATE vehicle_types SET name=%s WHERE name=%s", (name_entry.get(), old_name))
        update_ticket_type_tree(cursor)
        conn.commit()
        conn.close()
        messagebox.showinfo("Thông báo", "Cập nhật thành công!")
        window.destroy()
        refresh()

    window = tk.Toplevel()
    window.title("Sửa Loại Xe")
    window.geometry("400x100")
    window.transient(root)
    window.grab_set()
    window.resizable(False, False)
    center_window(window)

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)

    name_label = ttk.Label(window, text="Tên loại xe", font=("Space Grotesk Medium", 12))
    name_label.grid(row=0, column=0, sticky="we", padx=10, pady=10)
    name_entry = ttk.Entry(window, font=("Space Grotesk Medium", 12))
    name_entry.insert(0, old_name)
    name_entry.grid(row=0, column=1, columnspan=2, sticky="we", padx=10, pady=10)

    save_button = ttk.Button(window, text="Lưu", command=save)
    save_button.grid(row=1, column=1, sticky="we", padx=10, pady=10)
    window.bind("<Return>", lambda event: save())
    cancel_button = ttk.Button(window, text="Huỷ", command=window.destroy)
    cancel_button.grid(row=1, column=2, sticky="we", padx=10, pady=10)
    
def delete_vehicle_type():
    selected = frame_main_3_tree.selection()
    if not selected:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xoá.")
        return

    name = frame_main_3_tree.item(selected[0], "values")[0]

    confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xoá loại xe '{name}'?")
    if not confirm:
        return

    conn = mysql.connector.connect(host="localhost", user="root", password="", database="project001")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicle_types WHERE name=%s", (name,))
    update_ticket_type_tree(cursor)
    conn.commit()
    conn.close()

    messagebox.showinfo("Thông báo", "Đã xoá thành công.")
    refresh()

frame_main_3 = tk.Frame(root, bg="white", relief="ridge", bd=1)

frame_main_3_label = tk.Label(frame_main_3, text="Thông tin loại xe", background="steel blue", font=("Space Grotesk Medium", 16), fg="white")
frame_main_3_label.pack(fill="x")

frame_main_3_data = fetch_data("SELECT name FROM vehicle_types")
frame_main_3_tree = ttk.Treeview(frame_main_3, columns=("vehicle_type"), show="headings", height=len(frame_main_3_data))

frame_main_3_tree.heading("vehicle_type", text="Loại xe")
frame_main_3_tree.column("vehicle_type", anchor="center", width=50)

for row in frame_main_3_data:
    frame_main_3_tree.insert("", "end", values=row)
frame_main_3_tree.pack(fill="both", expand=True, padx=10, pady=10)

frame_main_3_delete_button = ttk.Button(frame_main_3, text="Xoá loại xe", command=delete_vehicle_type)
frame_main_3_delete_button.pack(side="right", padx=10, pady=(0, 10))

frame_main_3_modify_button = ttk.Button(frame_main_3, text="Sửa loại xe", command=modify_vehicle_type)
frame_main_3_modify_button.pack(side="right", padx=(10, 0), pady=(0, 10))

frame_main_3_add_button = ttk.Button(frame_main_3, text="Thêm loại xe", command=add_vehicle_type)
frame_main_3_add_button.pack(side="right", padx=(10, 0), pady=(0, 10))

# Đặt các frame vào place
w = root.winfo_width()
h = root.winfo_height()
frame_navbar.place(x = 0, y = 0, relwidth = 1, height = 60)
frame_main_2.place(x = 16, y = 60 + 16, width = w/2 - 24, height = h - 92)
frame_main_1.place(x = w/2 + 8, y = 60 + 16, width = w/2 - 16 - 8, height = (h - 60 - 16*3) / 2)
frame_main_3.place(x = w/2 + 8, y = 60 + 16 + frame_main_1.winfo_height() + 16, width = w/2 - 16 - 8, height = (h - 60 - 16*3) / 2)


# Bắt sự kiện thay đổi kích thước
ttk.Sizegrip(root).place(relx=1, rely=1, anchor="se")
root.bind("<Configure>", update_padding)

root.mainloop()