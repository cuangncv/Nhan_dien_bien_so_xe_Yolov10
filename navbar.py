import tkinter as tk
from PIL import Image, ImageTk
import subprocess, os, sys


class Navbar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(bg="steel blue")
        self.parent = parent # Lưu lại parent
        self._create_widgets()
        self._layout_widgets()
        self._bind_events() # Gọi hàm để gắn các sự kiện

    def _create_widgets(self):
        # Load icons
        try:
            self.icon_home = ImageTk.PhotoImage(Image.open(r"image\home.png"))
            self.icon_logout = ImageTk.PhotoImage(Image.open(r"image\logout.png"))
        except FileNotFoundError as e:
            print(f"Lỗi: Không tìm thấy file ảnh: {e}")
            self.icon_home = None
            self.icon_logout = None
            self.icon_admin = None

        # Create buttons
        self.home_button = tk.Button(self, text="Trang chủ", image=self.icon_home, compound="left", font=("Space Grotesk Medium", 16, "bold"), bg="steel blue", fg="white", activebackground="steel blue", activeforeground="white",bd=0, relief="flat", cursor="hand2")
        self.logout_button = tk.Button(self, text="Đăng xuất", image=self.icon_logout, compound="left", font=("Space Grotesk Medium", 12, "bold"), bg="steel blue", fg="white", activebackground="steel blue", activeforeground="white", bd=0, relief="flat", cursor="hand2")

    def _layout_widgets(self):
        for i in range(15):
            self.columnconfigure(i, weight=1)
        self.rowconfigure(0, weight=1)

        self.home_button.pack(side="left", fill="both", padx=10)
        self.logout_button.pack(side="right", fill="both", padx=16)

    def _bind_events(self):
        self.home_button.bind("<Button-1>", self._on_home_click)
        self.logout_button.bind("<Button-1>", self._on_logout_click)

    def _on_home_click(self, event):
        """Mở file home.py và đóng cửa sổ hiện tại."""
        try:
            current_file = os.path.basename(sys.argv[0]) # Lấy tên trang hiện tại
            if current_file == "home.py":
                return  # Đang ở home.py rồi thì không làm gì cả
            
            subprocess.Popen(["python", "home.py"])  # Mở file home.py
            if self.parent.__class__.__name__ != "recognition.py":
               self.parent.destroy() # Đóng cửa sổ hiện tại
        except Exception as e:
            print(f"Lỗi khi mở home.py: {e}")
            tk.messagebox.showerror("Lỗi", "Không thể mở trang chủ.")

    def _on_logout_click(self, event):
        """Hiển thị hộp thoại xác nhận đăng xuất, và mở login.py nếu chọn Yes."""
        if tk.messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            try:
                subprocess.Popen(["python", "login.py"])  # Mở file login.py
                if self.parent.__class__.__name__ != "recognition.py":
                    self.parent.destroy() # Đóng cửa sổ hiện tại
            except Exception as e:
                print(f"Lỗi khi mở login.py: {e}")
                tk.messagebox.showerror("Lỗi", "Không thể đăng xuất.")
