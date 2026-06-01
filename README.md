# Malzeme Sınıflandırma Projesi

Bu proje, tek nesne tespiti yerine görüntü sınıflandırma yapar ve 4 malzeme türünü ayırır:

- Glass
- Metal
- Paper
- Plastic

Ödevin beklediği temel şartlar projeye eklenmiştir:

- Veri artırma (rotation, shift, zoom, flip) kullanımı
- Aşırı öğrenmeyi azaltmak için `Dropout`
- Eğitilmiş `.h5` model dosyasının web arayüzüne entegre edilmesi
- Basit çalışan bir `Streamlit` arayüzü

## Proje Bileşenleri

- `model_training.ipynb`: Eğitim, değerlendirme ve görselleştirme notebook'u
- `project/api/model/model.h5`: Kaydedilmiş Keras modeli
- `project/api/streamlit_app.py`: Çalışan Streamlit arayüzü
- `project/api/app.py`: Flask tabanlı prediction API
- `project/api/utils/predictor.py`: Model yükleme ve tahmin yardımcı sınıfı
- `İnternetVeriSetleri/`: 4 sınıflı görüntü veri seti klasörü

## Veri Seti

Klasör yapısı yalnızca şu sınıfları içerir:

- `glass`
- `metal`
- `paper`
- `plastic`

Bu klasör üzerinde ekstra sınıf bırakılmamıştır.

## Kullanılan Eğitim Akışı

- Görseller `PIL` ile okunur
- 128x128 boyutuna ölçeklendirilir
- Piksel değerleri 0-1 aralığına normalize edilir
- Veri artırma ile eğitim seti çeşitlendirilir
- CNN / transfer learning katmanlarında `Dropout` ile overfitting azaltılır
- Confusion matrix ve sınıf bazlı metrikler üretilir

## Arayüz

Kullanıcı bir görsel yükler ve model şu bilgileri döndürür:

- Tahmin edilen sınıf
- Güven skoru

Streamlit arayüzünü çalıştırmak için:

```powershell
cd project\api
streamlit run streamlit_app.py
```

Flask API için:

```powershell
cd project\api
python app.py
```

## Kurulum

Gerekli paketler `project/api/requirements.txt` içinde listelenmiştir.

Kurulum örneği:

```powershell
pip install -r project\api\requirements.txt
```

## Notebook Çıktıları

Notebook çalıştırıldığında şu çıktılar üretilir:

- Sınıf dağılım grafikleri
- Eğitim doğruluk / kayıp grafikleri
- Confusion matrix
- F1 score ve classification report
- Yanlış sınıflandırılan örnekler
- Final model kaydı

## Klasör Yapısı

```text
Yeniproje/
├── model_training.ipynb
├── model_results.csv
├── README.md
├── İnternetVeriSetleri/
│   ├── glass/
│   ├── metal/
│   ├── paper/
│   └── plastic/
└── project/
    ├── api/
    │   ├── app.py
    │   ├── streamlit_app.py
    │   ├── requirements.txt
    │   ├── model/model.h5
    │   └── utils/predictor.py
    └── web/
```

## Amaç

Bu proje, görüntü tabanlı malzeme tanıma için eksiksiz bir ödev teslimi sunar: veri seti hazırlığı, model eğitimi, overfitting kontrolü, performans analizi ve çalışan web arayüzü tek yerde toplanmıştır.
