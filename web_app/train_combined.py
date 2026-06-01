"""
Combine Internet and Custom datasets, resize to 224x224, and train MobileNetV2 without Lambda layer.
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split

print("=" * 60)
print("GELİŞMİŞ MODEL EĞİTİMİ (Kombine Veri Seti - 224x224)")
print("=" * 60)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_data_path = os.path.join(project_dir, 'verisetleri')

# Sınıf eşleştirmeleri
class_mapping = {
    'glass': ['İnternetVeriSetleri/glass', 'BenimVeriSetim/1_Cam'],
    'metal': ['İnternetVeriSetleri/metal', 'BenimVeriSetim/3_Metal'],
    'paper': ['İnternetVeriSetleri/paper', 'BenimVeriSetim/2_Kagit'],
    'plastic': ['İnternetVeriSetleri/plastic', 'BenimVeriSetim/0_Plastik']
}

IMG_SIZE = 224
classes = ['glass', 'metal', 'paper', 'plastic']
images = []
labels = []

print("\n1/4 Veri yukleniyor...")

for label, class_name in enumerate(classes):
    paths = class_mapping[class_name]
    class_count = 0
    for rel_path in paths:
        full_path = os.path.join(base_data_path, rel_path.replace('/', os.sep))
        if not os.path.exists(full_path):
            print(f"  WARNING: Bulunamadi -> {full_path}")
            continue
        
        image_files = [f for f in os.listdir(full_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for image_file in image_files:
            try:
                img = Image.open(os.path.join(full_path, image_file)).convert('RGB')
                img = img.resize((IMG_SIZE, IMG_SIZE))
                img_array = np.array(img, dtype=np.float32) / 255.0
                images.append(img_array)
                labels.append(label)
                class_count += 1
            except Exception:
                continue
    print(f"  {class_name.upper()} sinifi: {class_count} goruntu yuklendi")

X = np.array(images)
y = np.array(labels)
print(f"  Toplam: {len(X)} goruntu")

print("\n2/4 Veri boluşturuluyor...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

print("\n3/4 Preprocessing ve egitim...")
import tensorflow as tf
from keras.applications import MobileNetV2
from keras.optimizers import Adam
from keras import models, layers

X_train_prep = tf.keras.applications.mobilenet_v2.preprocess_input(X_train * 255.0)
X_test_prep = tf.keras.applications.mobilenet_v2.preprocess_input(X_test * 255.0)

# Daha zorlayici veri artirmasi (Data Augmentation)
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

mobilenet_base = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
mobilenet_base.trainable = False

model = models.Sequential([
    layers.InputLayer(input_shape=(IMG_SIZE, IMG_SIZE, 3)),
    mobilenet_base,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print("\n  Faz 1: Baslik egitimi (10 epoch)...")
model.fit(
    train_datagen.flow(X_train_prep, y_train, batch_size=32, seed=42),
    epochs=10,
    steps_per_epoch=max(1, len(X_train_prep) // 32),
    validation_data=(X_test_prep, y_test),
    callbacks=[
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True, verbose=0),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=0)
    ],
    verbose=1
)

print("\n  Faz 2: Fine-tuning (son 20 katman, 10 epoch)...")
mobilenet_base.trainable = True
for layer in mobilenet_base.layers[:-20]:
    layer.trainable = False

model.compile(optimizer=Adam(learning_rate=0.00001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(
    train_datagen.flow(X_train_prep, y_train, batch_size=32, seed=42),
    epochs=10,
    steps_per_epoch=max(1, len(X_train_prep) // 32),
    validation_data=(X_test_prep, y_test),
    callbacks=[
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True, verbose=0),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, min_lr=1e-7, verbose=0)
    ],
    verbose=1
)

preds = np.argmax(model.predict(X_test_prep, verbose=0), axis=1)
acc = np.mean(preds == y_test)
print(f"\n  Test Accuracy: {acc:.2%}")

print("\n4/4 Model kaydediliyor...")
save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model')
os.makedirs(save_dir, exist_ok=True)
keras_path = os.path.join(save_dir, 'model.keras')
model.save(keras_path)
print(f"  Kaydedildi: {keras_path}")

print("\nTAMAMLANDI!")
