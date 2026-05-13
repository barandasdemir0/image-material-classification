import os
from PIL import Image
import numpy as np

# TensorFlow / Keras yüklenemeyebilir; bu yüzden güvenli şekilde import etmeye çalışıyoruz.
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False


class Predictor:
    """Model yükleme, ön-işleme ve tahmin için basit bir yardımcı sınıf.

    - Eğer `model.h5` bulunup TensorFlow yüklenmişse gerçek tahmin döner.
    - Aksi halde demo amaçlı rastgele fakat deterministik (dosya adına bağlı) bir sonuç döner.
    """

    def __init__(self):
        # Sınıf etiketleri (gösterim amacıyla büyük harfli)
        self.classes = ['Glass', 'Metal', 'Paper', 'Plastic']
        self.model = None
        self.img_size = 128

        # Model yolunu çalışma dizinine göre çöz
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model', 'model.h5'))
        if TF_AVAILABLE and os.path.exists(model_path):
            try:
                # Gerçek model varsa yükle (yavaş olabilir)
                self.model = load_model(model_path)
            except Exception:
                # Herhangi bir hata olursa gracefully devam et (demo modunda)
                self.model = None

    def preprocess(self, path):
        """Girdi görüntüsünü modele uygun numpy array'e dönüştürür.

        - RGB'ye çevirir, yeniden boyutlandırır, normalize eder ve batch ekseni ekler.
        """
        img = Image.open(path).convert('RGB')
        img = img.resize((self.img_size, self.img_size))
        arr = np.array(img, dtype=np.float32) / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict_image(self, path):
        """Verilen dosya yoluna göre sınıf ve güven skoru döndürür.

        Eğer gerçek model yüklüyse onun çıktısını kullanır; yoksa demo amaçlı
        deterministik rasgele bir dağılım üretir (test ve gösterim için).
        """
        if self.model is not None:
            x = self.preprocess(path)
            preds = self.model.predict(x)[0]
            idx = int(np.argmax(preds))
            conf = float(preds[idx])
            return self.classes[idx], f"{conf*100:.1f}%"
        else:
            # Demo: dosya adına bağlı pseudorastgele, her zaman aynı sonuç verir
            rnd = np.random.RandomState(seed=os.path.basename(path).__hash__() & 0xffffffff)
            probs = rnd.rand(len(self.classes))
            probs = probs / probs.sum()
            idx = int(np.argmax(probs))
            conf = probs[idx]
            return self.classes[idx], f"{conf*100:.1f}%"
