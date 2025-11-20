import cv2
import os
import logging
from plate_detector import PlateDetector
from ocr_processor import OCRProcessor

# Đường dẫn model
model_path = r"yolov10\runs\detect\train17\weights\best.pt"

# Tắt warning từ PaddleOCR
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
logging.getLogger('ppocr').setLevel(logging.WARNING)

# Khởi tạo detector và OCR
plate_detector = PlateDetector(model_path)
ocr_processor = OCRProcessor()

# Mở camera
cap = cv2.VideoCapture(r"yolov10/test.MOV")

frame_id = 0
detected_text = ""

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không lấy được hình từ camera.")
        break

    frame_id += 1

    # Phát hiện biển số trực tiếp từ frame
    plate_regions = plate_detector.detect_from_frame(frame)

    for i, plate in enumerate(plate_regions):
        result = ocr_processor.paddle_ocr(plate)
        if result:
            detected_text = result  # Gán biển số vừa nhận được
            print(f"Biển số phát hiện: {result}")
            break  # chỉ lấy 1 biển đầu tiên

    # Vẽ chữ lên camera
    if detected_text:
        cv2.putText(frame, f"Bien so: {detected_text}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # Hiển thị frame
    cv2.imshow("Camera", frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()