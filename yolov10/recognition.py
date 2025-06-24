import tkinter as tk
from tkinter import ttk
from navbar import Navbar
import os, logging, cv2
from utilities import center_window
from PIL import Image, ImageTk, ImageGrab
from plate_detector import PlateDetector
from ocr_processor import OCRProcessor
from datetime import datetime, timedelta
import mysql.connector
import threading
import queue
import time

def update_padding(event):
    navbar_height = 60
    frame_navbar.place(x=0, y=0, relwidth=1, height=navbar_height)
    frame_main.place(x=0, y=navbar_height, relwidth=1, height=root.winfo_height()-navbar_height)

root = tk.Tk()
root.title("Nhận diện biển số xe")
root.geometry("1400x700")
root.config(bg="white")
center_window(root)

try:
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="project001")
    cursor = conn.cursor(buffered=True)
except mysql.connector.Error as err:
    print(f"Lỗi kết nối MySQL: {err}")
    exit(1)

style = ttk.Style()
style.configure("TButton", font=("Space Grotesk Medium", 20), relief="ridge", bd=1, background="white")

# Khi bảo vệ nhấn checkin / checkout
# Cần tạm ngừng cập nhật thông tin xe 1 lúc cho bảo vệ đọc
# Nhưng nếu có xe mới vào / ra thì cập nhật luôn
pause_updates = False 

frame_navbar = Navbar(root)

frame_main = tk.Frame(root, bg="white")
frame_main.columnconfigure(0, weight=1)
frame_main.columnconfigure(1, weight=1)
frame_main.rowconfigure(0, weight=1)

# -------------------- Frame 1 - Camera nhận diện biển số xe -----------------------------
# Tắt các thông báo, warning trong terminal
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
logging.getLogger('ppocr').setLevel(logging.WARNING)

# Đường dẫn đến model YOLO
model_path = r"yolov10\runs\detect\train17\weights\best.pt"

# Khởi tạo detector và OCR
plate_detector = PlateDetector(model_path)
ocr_processor = OCRProcessor()

# Khởi tạo camera
cap = cv2.VideoCapture(0)

# Tạo các Queue để truyền dữ liệu giữa các luồng
frame_queue = queue.Queue(maxsize=1)  # Chỉ giữ frame mới nhất
result_queue = queue.Queue(maxsize=1)  # Chỉ giữ kết quả mới nhất

# Biến toàn cục để theo dõi trạng thái
running = True
latest_plate_bbox = None

def camera_thread():
    global running
    while running:
        ret, frame = cap.read()
        if ret:
            if frame_queue.full():
                try:
                    frame_queue.get_nowait()  # Loại bỏ frame cũ nhất nếu queue đầy
                except queue.Empty:
                    pass
            frame_queue.put(frame)
        time.sleep(0.01)  # Giảm tải CPU

def detection_thread():
    global running
    while running:
        try:
            frame = frame_queue.get(timeout=1)
            
            # Phát hiện biển số, trả về (plate_img, (x, y, w, h))
            plate_regions = plate_detector.detect_from_frame(frame)
            detected_text = ""
            bbox = None

            for plate_img, plate_bbox in plate_regions:
                result = ocr_processor.paddle_ocr(plate_img)
                if result:
                    detected_text = result
                    bbox = plate_bbox
                    break
                    
            # Định dạng biển số xe
            formatted_text = ""
            vehicle_type = "Chưa xác định"
            
            if detected_text:
                if len(detected_text) == 8:
                    formatted_text = detected_text[:3].strip() + "-" + detected_text[3:].strip()
                    vehicle_type = "Ô tô"
                elif len(detected_text) == 9:
                    formatted_text = detected_text[:4].strip() + "-" + detected_text[4:].strip()
                    vehicle_type = "Xe máy"
                elif len(detected_text) == 10:
                    formatted_text = detected_text[:5].strip() + "-" + detected_text[5:].strip()
                    formatted_text = formatted_text.replace("D", "Đ")
                    vehicle_type = "Xe máy điện"
            
            # Đưa kết quả vào queue
            if result_queue.full():
                try:
                    result_queue.get_nowait()  # Loại bỏ kết quả cũ nhất nếu queue đầy
                except queue.Empty:
                    pass
            
            result_queue.put((vehicle_type, formatted_text, bbox))
            
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Lỗi trong detection_thread: {e}")
        
        time.sleep(0.125)  # Chỉ xử lý 8 lần/giây

def show_camera():
    global latest_plate_bbox
    try:
        frame = frame_queue.get_nowait()
        
        # Vẽ khung nếu có
        if latest_plate_bbox:
            x, y, w, h = latest_plate_bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        width = frame_main_camera_cap.winfo_width()
        height = frame_main_camera_cap.winfo_height()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        img_width = int(width - 30)
        img_width = max(img_width, 1)
        img_height = int(img_width * 480 / 640)
        img_height = max(img_height, 1)

        img = img.resize((img_width, img_height))
        imgtk = ImageTk.PhotoImage(image=img)
        frame_main_camera_cap.imgtk = imgtk
        frame_main_camera_cap.create_image(width / 2, height / 2, anchor="center", image=imgtk)
        
    except queue.Empty:
        pass
    except Exception as e:
        print(f"Lỗi trong show_camera: {e}")
    
    root.after(25, show_camera)  # Cập nhật UI 40 lần/giây

def update_results():
    global latest_plate_bbox
    global pause_updates
    
    if pause_updates:
        root.after(250, update_results)
        return
        
    try:
        vehicle_type, plate_text, bbox = result_queue.get_nowait()
        
        if plate_text:
            frame_main_camera_detected.config(text=f"Biển số: {plate_text}")
            update_vehicle_info(vehicle_type, plate_text)
            latest_plate_bbox = bbox
        else:
            frame_main_camera_detected.config(text="Chưa xác định ra biển số xe")
            update_vehicle_info("Chưa xác định", "Chưa xác định")
            latest_plate_bbox = None
            
    except queue.Empty:
        pass
    except Exception as e:
        print(f"Lỗi trong update_results: {e}")
    
    root.after(250, update_results)  # Cập nhật kết quả 4 lần/giây

frame_main_camera = tk.Frame(frame_main, bg="white", relief="ridge", bd=1)
frame_main_camera.grid(row=0, column=0, sticky="nswe", padx=16, pady=16)

frame_main_camera_label = tk.Label(frame_main_camera, text="Camera nhận diện biển số xe", background="steel blue", font=("Space Grotesk Medium", 20), fg="white")
frame_main_camera_label.pack(fill="x")

frame_main_camera_cap = tk.Canvas(frame_main_camera, bg="white")
frame_main_camera_cap.pack(fill="both", expand=True, padx=10, pady=10)

frame_main_camera_detected = tk.Label(frame_main_camera, text="Chưa xác định ra biển số xe", background="white", font=("Space Grotesk Medium", 24), relief="ridge", bd=1)
frame_main_camera_detected.pack(fill="x", padx=10, pady=(0, 10))

# -------------------------------------- Frame 2 - Thông tin nhận diện xe -----------------------------------------

def update_status_var():
    cursor.execute("SELECT COUNT(*) FROM vehicles WHERE license_plate_number = %s", (plate_number_var.get(),))
    result = cursor.fetchone()
    # Nếu tồn tại biển số tức là xe đang trong nhà xe -> Muốn rời nhà xe
    if result and result[0] > 0:
        status_var.set("Đang chờ được \nra khỏi nhà xe...")
    else: 
        status_var.set("Đang chờ được \nvào nhà xe...")

def update_time_var():
    if status_var.get() == "Đang chờ được \nvào nhà xe...":
        time_checkin_var.set(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        time_checkout_var.set("00:00:00 00/00/0000")
    else:
        cursor.execute("SELECT time from vehicles WHERE license_plate_number = %s", (plate_number_var.get(),))
        result = cursor.fetchone()
        if result:  # Thêm kiểm tra result
            time_checkin_var.set(result[0].strftime("%H:%M:%S %d/%m/%Y"))
            time_checkout_var.set(datetime.now().strftime("%H:%M:%S %d/%m/%Y"))
        else:
            time_checkin_var.set("Chưa xác định") # Xử lý trường hợp không tìm thấy
            time_checkout_var.set("Chưa xác định")
        
def update_ticket_type_var():
    cursor.execute("SELECT COUNT(*) FROM monthly_pass WHERE license_plate_number = %s", (plate_number_var.get(),))
    result = cursor.fetchone()
    
    # Nếu sửa danh sách loại vé thì phải sửa cả ở đây
    if result and result[0] > 0:
        ticket_type_var.set("Vé tháng")
    # Nếu không tồn tại
    else:
        ticket_type_var.set("Vé lượt")

def calculate_parking_fee():
    # Nếu sửa danh sách loại vé thì phải sửa cả ở đây
    day_price = night_price = 0

    # Lấy giá vé theo loại xe
    cursor.execute("SELECT price FROM ticket_types WHERE vehicle_type = %s AND time = 'Ngày'", (vehicle_type_var.get(),))
    result = cursor.fetchone()
    if result:
        day_price = result[0]

    cursor.execute("SELECT price FROM ticket_types WHERE vehicle_type = %s AND time = 'Đêm'", (vehicle_type_var.get(),))
    result = cursor.fetchone()
    if result:
        night_price = result[0]

    # Parse thời gian
    try:
        checkin = datetime.strptime(time_checkin_var.get(), "%H:%M:%S %d/%m/%Y")
        checkout = datetime.strptime(time_checkout_var.get(), "%H:%M:%S %d/%m/%Y")
    except ValueError:
        return "Lỗi định dạng thời gian"

    total_fee = 0
    current = checkin

    while current < checkout: # Sử dụng < thay vì <= để tránh tính thêm 1 lần
        current_day = current.replace(hour=6, minute=0, second=0)
        day_end = current.replace(hour=17, minute=59, second=0)
        night_start = current.replace(hour=18, minute=0, second=0)
        next_morning = (current + timedelta(days=1)).replace(hour=5, minute=59, second=0)

        if current < current_day:
            slot_end = min(checkout, current_day)
            total_fee += night_price
            current = slot_end
        elif current < night_start:
            slot_end = min(checkout, night_start)
            total_fee += day_price
            current = slot_end
        else:
            slot_end = min(checkout, next_morning + timedelta(seconds=1))
            total_fee += night_price
            current = slot_end

    return total_fee

def update_price_var():
    cursor.execute("SELECT price FROM ticket_types WHERE vehicle_type = %s AND ticket_type = %s", (vehicle_type_var.get(), ticket_type_var.get(),))
    result = cursor.fetchone()
    if result:
        if ticket_type_var.get() == "Vé tháng":
            price_var.set(0)
        else:
            # Chưa ra khỏi nhà xe thì chưa tính tiền
            # Ra khỏi nhà xe thì tính tiền theo thời gian vào và thời gian ra
            if time_checkout_var.get() == "00:00:00 00/00/0000": 
                price_var.set(0)
            else:
                price_var.set(calculate_parking_fee()) 
    else:
        price_var.set(0)

# Hàm cập nhật thông tin xe
def update_vehicle_info(vehicle_type, plate_number):
    if pause_updates == True:
        return
    if vehicle_type != "Chưa xác định":
        vehicle_type_var.set(vehicle_type)
        plate_number_var.set(plate_number)
        update_status_var()
        update_time_var()
        update_ticket_type_var()
        update_price_var()
        check_in_out_button.config(state="normal")
    else:
        vehicle_type_var.set("Chưa xác định")
        plate_number_var.set("Chưa xác định")
        time_checkin_var.set("Chưa xác định")
        time_checkout_var.set("Chưa xác định")
        ticket_type_var.set("Chưa xác định")
        status_var.set("Chưa xác định")
        price_var.set("Chưa xác định")
        check_in_out_button.config(state="disabled")
        
def screenshot():
    root.update()
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    image = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # Đảm bảo thư mục tồn tại
    os.makedirs("vehicle_logs", exist_ok=True)
    
    path = "vehicle_logs/" + plate_number_var.get() + ".png"
    image.save(path, "PNG")

def check_in_out():
    global pause_updates
    pause_updates = True
    
    if status_var.get() == "Đang chờ được \nra khỏi nhà xe...":
        cursor.execute("DELETE FROM vehicles WHERE license_plate_number = %s", (plate_number_var.get(),))
        status_var.set("Đã ra khỏi nhà xe!!!")
        
        path = "vehicle_logs/" + plate_number_var.get() + ".png"
        if os.path.exists(path):
            os.remove(path)
    else:
        time = datetime.strptime(time_checkin_var.get(), "%H:%M:%S %d/%m/%Y")
        cursor.execute("INSERT INTO vehicles (type, license_plate_number, ticket_type, time) VALUES (%s, %s, %s, %s)", 
                        (vehicle_type_var.get(), plate_number_var.get(), ticket_type_var.get(), time.strftime("%Y-%m-%d %H:%M:%S")))
        status_var.set("Đã vào nhà xe!!!")
        screenshot()
    conn.commit()
    
    check_in_out_button.config(state="disabled")
    
    # Sau 3 giây, bỏ tạm dừng cập nhật
    root.after(3000, lambda: globals().__setitem__('pause_updates', False))
        
        
frame_main_info = tk.Frame(frame_main, bg="white", relief="ridge", bd=1)
frame_main_info.grid(row=0, column=1, sticky="nswe", padx=16, pady=16)

frame_main_info_label = tk.Label(frame_main_info, text="Thông tin nhận diện xe", background="steel blue", font=("Space Grotesk Medium", 20), fg="white")
frame_main_info_label.pack(fill="x")

frame_main_info_detail = tk.Frame(frame_main_info, bg="white", relief="ridge", bd=1)
frame_main_info_detail.pack(fill="both", expand=True, padx=10, pady=10)

for i in range(7):
    frame_main_info_detail.rowconfigure(i, weight=1)
frame_main_info_detail.columnconfigure(0, weight=1)
frame_main_info_detail.columnconfigure(1, weight=2)

vehicle_type_var = tk.StringVar(value="Chưa xác định")
plate_number_var = tk.StringVar(value="Chưa xác định")
time_checkin_var = tk.StringVar(value="Chưa xác định") # Kiểu dữ liệu string định dạng HH:MM:SS dd/mm/yyyy
time_checkout_var = tk.StringVar(value="Chưa xác định") # Kiểu dữ liệu string định dạng HH:MM:SS dd/mm/yyyy
ticket_type_var = tk.StringVar(value="Chưa xác định")
status_var = tk.StringVar(value="Chưa xác định")
price_var = tk.StringVar(value="Chưa xác định")

label_vehicle_type = tk.Label(frame_main_info_detail, text="Loại xe: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_vehicle_type.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
value_vehicle_type = tk.Label(frame_main_info_detail, textvariable=vehicle_type_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_vehicle_type.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

label_plate_number = tk.Label(frame_main_info_detail, text="Biển số: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_plate_number.grid(row=1, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_plate_number = tk.Label(frame_main_info_detail, textvariable=plate_number_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_plate_number.grid(row=1, column=1, sticky="nswe", padx=10, pady=(0, 10))

label_time_checkin = tk.Label(frame_main_info_detail, text="Thời gian checkin: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_time_checkin.grid(row=2, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_time_checkin = tk.Label(frame_main_info_detail, textvariable=time_checkin_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_time_checkin.grid(row=2, column=1, sticky="nswe", padx=10, pady=(0, 10))

label_time_checkout = tk.Label(frame_main_info_detail, text="Thời gian checkout: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_time_checkout.grid(row=3, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_time_checkout = tk.Label(frame_main_info_detail, textvariable=time_checkout_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_time_checkout.grid(row=3, column=1, sticky="nswe", padx=10, pady=(0, 10))

label_ticket_type = tk.Label(frame_main_info_detail, text="Loại vé: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_ticket_type.grid(row=4, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_ticket_type = tk.Label(frame_main_info_detail, textvariable=ticket_type_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_ticket_type.grid(row=4, column=1, sticky="nswe", padx=10, pady=(0, 10))

label_status = tk.Label(frame_main_info_detail, text="Trạng thái: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_status.grid(row=5, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_status = tk.Label(frame_main_info_detail, textvariable=status_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w", justify="left")
value_status.grid(row=5, column=1, sticky="nswe", padx=10, pady=(0, 10))

label_price = tk.Label(frame_main_info_detail, text="Cần thanh toán: ", bg="white", font=("Space Grotesk Medium", 16), anchor="w")
label_price.grid(row=6, column=0, sticky="nswe", padx=10, pady=(0, 10))
value_price = tk.Label(frame_main_info_detail, textvariable=price_var, bg="white", font=("Space Grotesk Medium", 16), anchor="w")
value_price.grid(row=6, column=1, sticky="nswe", padx=10, pady=(0, 10))

check_in_out_button = ttk.Button(frame_main_info, text="Check in / Check out", style="TButton", command=check_in_out)
check_in_out_button.pack(fill="x", padx=10, pady=(0, 10))

# Khởi động các luồng
camera_thread_instance = threading.Thread(target=camera_thread, daemon=True)
detection_thread_instance = threading.Thread(target=detection_thread, daemon=True)

camera_thread_instance.start()
detection_thread_instance.start()

# Khởi động các hàm cập nhật UI
show_camera()
update_results()

# Bắt sự kiện thay đổi kích thước
ttk.Sizegrip(root).place(relx=1, rely=1, anchor="se")
root.bind("<Configure>", update_padding)

# Xử lý khi đóng ứng dụng
def on_closing():
    global running
    running = False
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

# Dọn dẹp tài nguyên
conn.close()
cap.release()
cv2.destroyAllWindows()