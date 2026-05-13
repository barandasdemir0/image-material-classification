"""
Basit Flask API - resim yükleyip model ile tahmin döndürür.

Kısa açıklama:
- `/predict` endpoint'i bir resim alır, kaydeder ve `Predictor` sınıfı ile tahmin yapar.
- Hataları JSON olarak döner (400/500 kodları ile).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from utils.predictor import Predictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXT = {'png','jpg','jpeg'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

predictor = Predictor()

def allowed_file(filename):
    """Dosya uzantısını kontrol eder (izin verilen görsel biçimleri).

    Çok sık olmayan basit bir filtre; güvenlik için ek doğrulama yapılabilir.
    """
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/predict', methods=['POST'])
def predict():
    # HTTP çok parçalı/form-data içinde 'file' alanı olmalı
    if 'file' not in request.files:
        return jsonify({'error':'no file part'}), 400

    file = request.files['file']
    # Dosya seçilmemişse hata
    if file.filename == '':
        return jsonify({'error':'no selected file'}), 400

    # Uzantı kontrolü ve dosyanın diske kaydedilmesi
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        try:
            # Predictor sınıfı ile tahmin al
            material, confidence = predictor.predict_image(path)
            return jsonify({'material': material, 'confidence': confidence})
        except Exception as e:
            # Beklenmeyen hata -> 500
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error':'file type not allowed'}), 400

if __name__ == '__main__':
    # Geliştirme amaçlı çalıştırma (prod ortamında debug=False yapın)
    app.run(debug=True)
