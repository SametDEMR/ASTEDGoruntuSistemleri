import cv2
import numpy as np
import random

def inward_distort_image(image_path, scale_percent=100, size=15, num_points_each_side=1, rotation_angle=0):
    image = cv2.imread(image_path)
    if image is None:
        print("Resim yüklenemedi:", image_path)
        return None

    # Görüntüyü yeniden boyutlandır
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    distorted_image = image.copy()

    # Ana konturu bul
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("Kontur bulunamadı.")
        return None
    contour = max(contours, key=cv2.contourArea)

    # Kontur merkezi
    M = cv2.moments(contour)
    if M["m00"] == 0:
        print("Kontur alanı sıfır.")
        return None
    center = np.array([int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])])

    # Noktaları ayır
    left = [p[0] for p in contour if p[0][0] < center[0]]
    right = [p[0] for p in contour if p[0][0] >= center[0]]

    # Distortion uygulayan iç fonksiyon
    def distort(point):
        x, y = point
        direction = center - point
        norm = np.linalg.norm(direction)
        if norm == 0:
            return
        direction = direction / norm
        for dx in range(-size, size + 1):
            for dy in range(-size, size + 1):
                px, py = x + dx, y + dy
                if 0 <= px < image.shape[1] and 0 <= py < image.shape[0]:
                    shift = int(20 * (1 - (abs(dx)/size + abs(dy)/size)/2))
                    nx, ny = int(px + direction[0] * shift), int(py + direction[1] * shift)
                    if 0 <= nx < image.shape[1] and 0 <= ny < image.shape[0]:
                        distorted_image[ny, nx] = image[py, px]

    # Nokta seçip bozulma uygula
    for _ in range(num_points_each_side):
        lp = random.choice(left) if left else None
        rp = random.choice(right) if right else None
        if lp is not None: distort(lp)
        if rp is not None: distort(rp)

    # Görüntüyü döndür
    if rotation_angle != 0:
        (h, w) = distorted_image.shape[:2]
        center_rot = (w // 2, h // 2)
        M_rot = cv2.getRotationMatrix2D(center_rot, rotation_angle, 1.0)
        distorted_image = cv2.warpAffine(distorted_image, M_rot, (w, h))

    return distorted_image
