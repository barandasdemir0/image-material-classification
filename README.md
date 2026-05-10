# Malzeme Sınıflandırma Projesi

Bu proje, derin öğrenme kullanarak görüntülerden 4 farklı malzeme türünü sınıflandırır:

- Glass (Cam)
- Metal
- Paper (Kağıt)
- Plastic (Plastik)

Proje, Jupyter Notebook içinde eğitilmiş bir CNN modeline dayanır ve model sonuçlarını confusion matrix, F1 score, doğruluk ve sınıf dağılımları ile birlikte sunar.

## Proje İçeriği

- `model_training.ipynb`: Model eğitimi, değerlendirme ve görselleştirme notebook'u
- `İnternetVeriSetleri/`: Görüntü veri seti klasörü
- `model_results.csv`: Eğitim sonunda kaydedilen özet metrikler

## Veri Seti

Veri seti dört sınıftan oluşur:

- `glass` - 501 görüntü
- `metal` - 410 görüntü
- `paper` - 594 görüntü
- `plastic` - 482 görüntü

Toplam: **1987 görüntü**

## Kullanılan Yöntem

- Görseller PIL ile okunur
- 128x128 boyutuna yeniden ölçeklendirilir
- Piksel değerleri 0-1 aralığına normalize edilir
- CNN (Convolutional Neural Network) modeli ile sınıflandırma yapılır
- Test seti üzerinde performans ölçülür

## Model Mimarisi

Model şu katmanlardan oluşur:

- 4 adet `Conv2D` + `MaxPooling2D`
- `Flatten`
- `Dense(128)`
- `Dropout(0.5)`
- `Dense(4, softmax)`

## Elde Edilen Sonuçlar

Notebook çalıştırıldığında elde edilen temel metrikler:

- Accuracy: **59.80%**
- F1 Score (Macro): **0.5904**
- F1 Score (Weighted): **0.5966**
- Precision (Macro): **0.5991**
- Recall (Macro): **0.5903**

### Sınıf Bazında Performans

- Glass: **62.00%**
- Metal: **54.88%**
- Paper: **69.75%**
- Plastic: **49.48%**

## Notebook'ta Üretilen Çıktılar

- Sınıf dağılım grafikleri
- Eğitim doğruluk/kayıp grafikleri
- Confusion matrix
- F1 score grafikleri
- Örnek tahmin görselleri
- Sonuçların CSV dosyasına kaydı

## Çalıştırma

Notebook'u açıp hücreleri sırayla çalıştırabilirsiniz.

Gerekli paketler:

- numpy
- pandas
- matplotlib
- seaborn
- scikit-learn
- pillow
- tensorflow

Eğer ortamınızda eksik paket varsa kurulum için:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn pillow tensorflow
```

## Notlar

- Notebook içinde veri yükleme işlemi `PIL` ile yapılır.
- `cv2` yerine `PIL` kullanıldığı için resim okuma uyumluluğu daha yüksek olur.
- Model sonuçları veri seti ve eğitim ayarlarına göre değişebilir.

## Klasör Yapısı

```text
Yeniproje/
├── model_training.ipynb
├── model_results.csv
├── README.md
└── İnternetVeriSetleri/
    ├── glass/
    ├── metal/
    ├── paper/
    └── plastic/
```

## Amaç

Bu proje, görüntü tabanlı malzeme tanıma için temel bir derin öğrenme akışı sunar. Amaç; veri yükleme, model eğitimi, performans analizi ve görselleştirmeyi tek notebook içinde toplamak ve anlaşılır bir rapor üretmektir.
