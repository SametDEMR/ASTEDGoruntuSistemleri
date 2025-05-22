def detect_defects_by_diff_images(clean_img, defect_img,
                                  threshold=70, min_area=300,
                                  scale_percent=100, border_margin=15):
    import cv2
    import numpy as np

    def resize_image(image, scale_percent):
        w = int(image.shape[1] * scale_percent / 100)
        h = int(image.shape[0] * scale_percent / 100)
        return cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)

    # --- 1) GREY & RESIZE & HIST EQ ---
    clean = cv2.cvtColor(clean_img, cv2.COLOR_BGR2GRAY)
    defect = cv2.cvtColor(defect_img, cv2.COLOR_BGR2GRAY)

    clean = resize_image(clean, scale_percent)
    defect = resize_image(defect, scale_percent)

    if clean.shape != defect.shape:
        defect = cv2.resize(defect, (clean.shape[1], clean.shape[0]))

    clean = cv2.equalizeHist(clean)
    defect = cv2.equalizeHist(defect)

    # --- 2) ABS DIFF + THRESH + MORPH CLOSE ---
    diff = cv2.absdiff(clean, defect)
    _, diff_thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    diff_morph = cv2.morphologyEx(diff_thresh,
                                  cv2.MORPH_CLOSE,
                                  kernel, iterations=2)

    # --- 3) NESNE MASKESI OLUŞTUR ---
    _, obj_bin = cv2.threshold(clean, 10, 255, cv2.THRESH_BINARY)
    obj_bin = cv2.morphologyEx(obj_bin,
                               cv2.MORPH_CLOSE,
                               np.ones((15,15),np.uint8),
                               iterations=2)
    cnts, _ = cv2.findContours(obj_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_obj = np.zeros_like(obj_bin)
    if cnts:
        big = max(cnts, key=cv2.contourArea)
        cv2.drawContours(mask_obj, [big], -1, 255, -1)

    # --- 4) MASKEYI ERODE ET ---
    eroded_mask = cv2.erode(mask_obj,
                            np.ones((border_margin,border_margin),np.uint8),
                            iterations=1)

    # --- 5) DIFF_MORPH'I MASKEYLE TEMİZLE ---
    diff_clean = cv2.bitwise_and(diff_morph, diff_morph,
                                 mask=eroded_mask)

    # --- 6) KONTURLARI BUL VE ÇİZ ---
    contours, _ = cv2.findContours(diff_clean,
                                   cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)

    defect_color = resize_image(defect_img, scale_percent)
    if defect_color.shape[:2] != clean.shape:
        defect_color = cv2.resize(defect_color,
                                  (clean.shape[1], clean.shape[0]))

    defects = 0
    for cnt in contours:
        if cv2.contourArea(cnt) < min_area:
            continue
        x,y,w_box,h_box = cv2.boundingRect(cnt)
        cv2.rectangle(defect_color, (x,y),
                      (x+w_box, y+h_box),
                      (0,0,255), 2)
        defects += 1

    print(f"Toplam {defects} adet yapısal bozukluk tespit edildi.")
    return defect_color
