from flask import Flask, request, jsonify, send_file
from defect_detection import detect_defects_with_ratio
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/check-defect', methods=['POST'])
def check_defect():
    if 'image' not in request.files:
        return jsonify({"error": "Resim dosyası eksik"}), 400

    img_file = request.files['image']
    defect_path = os.path.join(UPLOAD_FOLDER, "input.jpg")
    img_file.save(defect_path)

    result_path, defect_ratio = detect_defects_with_ratio(defect_path)

    if result_path:
        return jsonify({
            "defect_ratio": defect_ratio,
            "image_url": "/result-image"
        })
    else:
        return jsonify({"error": "İşleme başarısız"}), 500

@app.route('/result-image', methods=['GET'])
def get_result_image():
    return send_file("orn3.png", mimetype='image/png')  # burada orn3.png kullanıyoruz

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
