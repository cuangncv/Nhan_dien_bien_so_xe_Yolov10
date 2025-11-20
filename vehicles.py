import tkinter as tk
from tkinter import ttk
from navbar import Navbar
import mysql.connector
from utilities import center_window, fetch_data, draw_horizontal_gradient

def update_layout(event):
    w = root.winfo_height()
    h = root.winfo_height()
    frame_navbar.place(x=0, y=0, relwidth=1, height=60)
    frame_treeview.place(x=0, y=60, relwidth=1, height=h-60)

def search_data():
    # Xóa dữ liệu cũ
    for item in treeview.get_children():
        treeview.delete(item)
        
    keyword = search_var.get().lower()
    data = fetch_data(f"SELECT type, license_plate_number, ticket_type, DATE_FORMAT(time, '%H:%i:%s %d/%m/%Y') AS formatted_time FROM vehicles WHERE LOWER(license_plate_number) LIKE '%{keyword}%' ORDER BY time DESC")
    
    for index, row in enumerate(data, start=1):
        treeview.insert("", "end", values=(index, *row))


# Setup UI
root = tk.Tk()
root.title("Danh sách xe đang gửi")
root.geometry("1200x600")
root.minsize(800, 400)
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
style.configure("TButton", font=("Space Grotesk Medium", 12), background="white")

# Navbar
frame_navbar = Navbar(root)
frame_navbar.place(x=0, y=0, relwidth=1, height=60)

# Main content area
frame_treeview = tk.Frame(root, bg="white")

# Search bar
frame_treeview_navbar = tk.Frame(frame_treeview, bg="white")
frame_treeview_navbar.pack(fill="both")

treeview_label = tk.Canvas(frame_treeview_navbar, height=40, width=500, bg="white", highlightthickness=0)
treeview_label.pack(side="left", padx=16, pady=10)
draw_horizontal_gradient(treeview_label, "steel blue", "white", height=40, width=500)
treeview_label.create_text(10, 20, anchor="w", text="Danh sách xe đang gửi", font=("Space Grotesk Medium", 16), fill="white")

search_var = tk.StringVar()
search_entry = ttk.Entry(frame_treeview_navbar, textvariable=search_var, 
                         width=30, font=("Space Grotesk", 12))
search_entry.pack(side="right", padx=16, pady=10)

search_button = ttk.Button(frame_treeview_navbar, text="Tìm kiếm", command=search_data)
search_button.pack(side="right", pady=10)
root.bind("<Return>", lambda event: search_data())

# Treeview setup

data = fetch_data("SELECT type, license_plate_number, ticket_type, DATE_FORMAT(time, '%H:%i:%s %d/%m/%Y') AS formatted_time FROM vehicles ORDER BY time DESC")
columns = ("STT", "Loại xe", "Biển số", "Loại vé", "Gửi từ")
treeview = ttk.Treeview(frame_treeview, columns=columns, show="headings", height=len(data))

# Configure columns
column_widths = {"STT": 50, "Loại xe": 100, "Biển số": 100, "Loại vé": 100, "Gửi từ": 150}

for col in columns:
    treeview.heading(col, text=col)
    treeview.column(col, width=column_widths[col], anchor="center")

for index, row in enumerate(data, start=1):
    treeview.insert("", "end", values=(index, *row))


# Tạo scrollbar cho treeview
scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side='right', fill='y')

treeview.pack(expand=True, fill="both", padx=(16, 0), pady=(0, 16))

# Sizegrip and layout binding
size_grip = ttk.Sizegrip(root)
size_grip.place(relx=1, rely=1, anchor="se")
root.bind("<Configure>", update_layout)

root.mainloop()