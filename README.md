# istanbul-real-estate-heatmap
# 🏙️ İstanbul Akıllı Emlak ve Ev Arkadaşı Eşleştirme Platformu (AI-Powered)

İstanbul gibi dinamik, hiper-enflasyonist ve şeffaf olmayan bir emlak pazarına veri odaklı (data-driven) bir çözüm getiren akıllı web platformu. 

Bu proje, klasik "ev arkadaşı arama" konseptini makine öğrenmesi (Machine Learning) algoritmalarıyla birleştirerek; hem oda kiralayan ev sahiplerine pazar standartlarında **Adil Fiyat (Fair Value)** önerileri sunar, hem de oda arayan kullanıcılara bütçelerine uygun semtleri harita üzerinde **Dinamik Isı Haritası (Heatmap)** ile görselleştirir.

---

## 🚀 Temel Özellikler ve Modüller

### 1. AI-Tabanlı Adil Fiyat Tahminleyicisi (Regression Engine)
Ev sahipleri veya oda kiralayanlar ilan verirken, uygulamanın arka planında çalışan makine öğrenmesi modeli (XGBoost / LightGBM) devreye girer.
* **Nasıl Çalışır:** İstanbul genelindeki binlerce güncel emlak verisi (İlçe, Mahalle, m², Bina Yaşı, Oda Sayısı) analiz edilerek, o odanın "olması gereken" adil piyasa değeri tahmin edilir.
* **Faydası:** İlan veren kullanıcı, fiyatı pazar ortalamasının çok üzerindeyse uyarılır ("Bu fiyat bölge ortalamasının %30 üzerinde") ve adil bir fiyat bandına yönlendirilir.

### 2. Dinamik Bütçe Isı Haritası (Affordability Heatmap)
Oda veya ev arayan kullanıcıların bütçe algısını değiştiren görsel analiz modülü.
* **Nasıl Çalışır:** Kullanıcı maksimum aylık bütçesini (Örn: 12.000 TL) sisteme girdiğinde, harita API'si (Mapbox/Google Maps) üzerinde İstanbul'daki mahalleler renklendirilir.
* **Görselleştirme:** Bütçenin rahatça yettiği "Güvenli" bölgeler yeşil, ucu ucuna yeten "Sınırda" bölgeler sarı, bütçeyi aşan bölgeler ise kırmızı ile işaretlenerek kullanıcıya veri destekli bir arama deneyimi sunulur.

### 3. Akıllı Alternatif Rota Önerileri (Clustering)
Kullanıcı popüler ve pahalı bir lokasyonda (Örn: Beşiktaş) ev arıyorsa, sistem K-Nearest Neighbors (KNN) mantığıyla kullanıcının bütçesine uygun ve hedef lokasyona toplu taşımayla (Metro/Marmaray) kolayca ulaşabileceği alternatif ilçeleri (Örn: Üsküdar) otomatik olarak önerir.

---

## 🛠️ Mimari ve Teknoloji Yığını (Tech Stack)

Bu proje, sağlam bir veri boru hattı (data pipeline) ve modern bir web mimarisi üzerine inşa edilmiştir.

* **Veri Toplama (Scraping):** Python, Selenium / Playwright (Büyük emlak platformlarından düzenli ve otomatik veri çekimi).
* **Makine Öğrenmesi (ML Model):** Python, Pandas, Scikit-learn, XGBoost (Fiyat tahminlemesi ve modelleme).
* **Backend API:** Python, FastAPI (ML modellerinin hızlı ve asenkron olarak frontend'e servis edilmesi).
* **Frontend:** React.js / Next.js, TailwindCSS (Modern, swipe tabanlı kullanıcı arayüzü).
* **Harita Entegrasyonu:** Mapbox GL JS veya Google Maps API (Isı haritası ve lokasyon bazlı görselleşt
