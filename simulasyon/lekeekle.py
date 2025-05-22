import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random
import cv2

def add_stains_and_particles(image_path, scale_percent=100, num_stains=5, num_particles=20):
    # Resmi OpenCV ile oku
    img_cv = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img_cv is None:
        print("Resim yüklenemedi:", image_path)
        return None

    # Yeniden boyutlandır
    width = int(img_cv.shape[1] * scale_percent / 100)
    height = int(img_cv.shape[0] * scale_percent / 100)
    img_cv = cv2.resize(img_cv, (width, height), interpolation=cv2.INTER_AREA)

    # Kenar algılama için gri tonlara çevir
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Kenarları tespit et (Canny)
    edges = cv2.Canny(gray, threshold1=50, threshold2=150)

    # Kenar bölgelerini genişlet (dilate) ki lekeler biraz kenar civarına yayılsın
    kernel = np.ones((5,5), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)

    # Kenar maskesini PIL ile kullanabilmek için RGBA formatına çevir
    mask = Image.fromarray(edges_dilated).convert("L")
    mask_np = np.array(mask)

    # OpenCV BGR -> PIL RGBA'ya çevir
    img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGBA))

    # Lekeler ve partiküller için boş katmanlar
    stain_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    particle_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_stain = ImageDraw.Draw(stain_layer)
    draw_particle = ImageDraw.Draw(particle_layer)

    # Lekeleri sadece kenar maskesi üzerinde oluştur
    for _ in range(num_stains):
        r = random.randint(10, 40)
        # Kenar maskesinde lekelerin konumunu seç
        while True:
            x = random.randint(0, width - r)
            y = random.randint(0, height - r)
            # Maskede en azından bir piksel kenar varsa kabul et
            if np.any(mask_np[y:y+r, x:x+r] > 0):
                break
        color = random.choice([(80, 60, 40, 40), (50, 50, 50, 30), (90, 40, 10, 25)])
        draw_stain.ellipse([x, y, x + r, y + r], fill=color)

    # Lekeleri blurla
    stain_layer = stain_layer.filter(ImageFilter.GaussianBlur(radius=5))

    # Partikülleri de sadece kenar maskesi üzerinde oluştur
    for _ in range(num_particles):
        r = random.randint(1, 3)
        while True:
            x = random.randint(0, width - r)
            y = random.randint(0, height - r)
            if np.any(mask_np[y:y+r, x:x+r] > 0):
                break
        color = random.choice([(0, 0, 0, 180), (50, 50, 50, 150)])
        draw_particle.ellipse([x, y, x + r, y + r], fill=color)

    # Katmanları birleştir
    combined = Image.alpha_composite(img_pil, stain_layer)
    combined = Image.alpha_composite(combined, particle_layer)

    # PIL'den numpy (BGR) formatına çevir (OpenCV ile uyumlu)
    combined_np = cv2.cvtColor(np.array(combined), cv2.COLOR_RGBA2BGR)

    return combined_np
