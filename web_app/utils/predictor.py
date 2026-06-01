import os
from PIL import Image
import numpy as np

try:
    import tensorflow as tf
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False

def resnet_preprocess(x):
    import tensorflow as tf
    return tf.keras.applications.resnet50.preprocess_input(x * 255.0)

class Predictor:
    def __init__(self):
        self.classes = ['Glass', 'Metal', 'Paper', 'Plastic']
        self.model = None
        self.img_size = 128

        if TF_AVAILABLE:
            model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model'))
            weights_path = os.path.join(model_dir, 'resnet_weights.weights.h5')
            
            if os.path.exists(weights_path):
                try:
                    resnet_base = tf.keras.applications.ResNet50(
                        input_shape=(128, 128, 3), 
                        include_top=False, 
                        weights=None
                    )
                    self.model = tf.keras.models.Sequential([
                        tf.keras.layers.InputLayer(input_shape=(128, 128, 3)),
                        tf.keras.layers.Lambda(resnet_preprocess),
                        resnet_base,
                        tf.keras.layers.GlobalAveragePooling2D(),
                        tf.keras.layers.Dense(256, activation='relu'),
                        tf.keras.layers.Dropout(0.5),
                        tf.keras.layers.Dense(128, activation='relu'),
                        tf.keras.layers.Dropout(0.3),
                        tf.keras.layers.Dense(4, activation='softmax')
                    ])
                    self.model.load_weights(weights_path)
                    print(f"Predictor: ResNet50 model loaded OK from weights")
                except Exception as e:
                    print(f"Predictor: Failed to load weights: {e}")
                    self.model = None
            else:
                print(f"Predictor: {weights_path} not found; running DEMO mode.")
        else:
            print('Predictor: TensorFlow not available; running DEMO mode.')

    def preprocess(self, path):
        img = Image.open(path).convert('RGB')
        img = img.resize((self.img_size, self.img_size))
        arr = np.array(img, dtype=np.float32)
        # Convert to [0, 1] because the model's Lambda layer expects [0, 1]
        arr = arr / 255.0
        arr = np.expand_dims(arr, axis=0)
        return arr

    def predict_image(self, path):
        if self.model is not None:
            x = self.preprocess(path)
            preds = self.model.predict(x, verbose=0)[0]
            idx = int(np.argmax(preds))
            conf = float(preds[idx])
            return self.classes[idx], f"{conf*100:.1f}%"
        else:
            rnd = np.random.RandomState(seed=os.path.basename(path).__hash__() & 0xffffffff)
            probs = rnd.rand(len(self.classes))
            probs = probs / probs.sum()
            idx = int(np.argmax(probs))
            conf = probs[idx]
            return self.classes[idx], f"{conf*100:.1f}%"
