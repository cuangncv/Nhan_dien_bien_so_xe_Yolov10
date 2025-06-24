from paddleocr import PaddleOCR
import re


class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls = True, use_gpu = True)

    def paddle_ocr(self, plate_img):
        result = self.ocr.ocr(plate_img, det=True, rec=True, cls=True)
        text = ""

        if not result:
            return text

        try:
            if isinstance(result, list):
                for line in result:
                    if line is None:
                        continue

                    # line là danh sách các kết quả (mỗi dòng text)
                    if isinstance(line, (list, tuple)) and len(line) > 0:
                        for word_info in line:
                            if isinstance(word_info, (list, tuple)) and len(word_info) >= 2:
                                # Trường hợp format mới: [text, score]
                                if isinstance(word_info[1], (float, int)) and word_info[0]:
                                    score = float(word_info[1])
                                    if score > 0.6:
                                        text += word_info[0] + " "
                                # Trường hợp format cũ: [[box], (text, score)]
                                elif isinstance(word_info[1], tuple) and len(word_info[1]) >= 2:
                                    content, score = word_info[1]
                                    try:
                                        score = float(score)
                                    except:
                                        score = 0
                                    if score > 0.6:
                                        text += content + " "

        except Exception as e:
            print(f"Error in paddle_ocr: {e}")
            return ""

        # Hậu xử lý văn bản
        pattern = re.compile(r'[\W]')
        text = pattern.sub('', text)
        text = text.replace("???", "")
        text = text.replace("O", "0")
        return text.strip()