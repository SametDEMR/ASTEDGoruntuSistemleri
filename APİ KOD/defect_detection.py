
import cv2
import numpy as np

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def detect_defects_with_ratio(defect_image_path, reference_path="uploads/orn3.png", threshold=70, min_area=300, scale_percent=50):
    clean = cv2.imread(reference_path, cv2.IMREAD_GRAYSCALE)
    defect = cv2.imread(defect_image_path, cv2.IMREAD_GRAYSCALE)

    if clean is None or defect is None:
        return None, 0

    clean = resize_image(clean, scale_percent)
    defect = resize_image(defect, scale_percent)

    if clean.shape != defect.shape:
        defect = cv2.resize(defect, (clean.shape[1], clean.shape[0]))

    clean = cv2.equalizeHist(clean)
    defect = cv2.equalizeHist(defect)

    diff = cv2.absdiff(clean, defect)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    kernel = np.ones((5,5), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    defect_color = cv2.imread(defect_image_path)
    defect_color = resize_image(defect_color, scale_percent)

    if defect_color.shape[:2] != clean.shape:
        defect_color = cv2.resize(defect_color, (clean.shape[1], clean.shape[0]))

    total_defect_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(defect_color, (x, y), (x + w, y + h), (0, 0, 255), 2)
            total_defect_area += area

    total_image_area = defect.shape[0] * defect.shape[1]
    defect_ratio = (total_defect_area / total_image_area) * 100

    output_path = "uploads/orn3.png"
    cv2.imwrite(output_path, defect_color)

    return output_path, round(defect_ratio, 2)

