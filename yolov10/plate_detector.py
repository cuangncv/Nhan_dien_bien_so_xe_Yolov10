from ultralytics import YOLOv10

class PlateDetector:
    def __init__(self, model_path):
        self.model = YOLOv10(model_path)

    def detect_from_frame(self, frame):
        results = self.model.predict(source=frame, verbose=False)[0]
        plate_regions = []

        for box in results.boxes:
            
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Cắt biển số
            plate_crop = frame[y1:y2, x1:x2]
            bbox = (x1, y1, x2 - x1, y2 - y1)  # định dạng (x, y, w, h)
            plate_regions.append((plate_crop, bbox))

        return plate_regions
