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


---

## 📌 Mevcut Durum (Ne Çalışıyor?)

Yukarıdaki bölüm projenin **hedef** kapsamını anlatır. Şu an depoda çalışır
durumda olan kısım **Modül 2 — Bütçe Isı Haritası**'dır:

| Durum | Bileşen |
|---|---|
| ✅ | Veri temizleme boru hattı (`scripts/build_market_values.py`) |
| ✅ | Mahalle bazlı piyasa değerleri (`data/processed/`) |
| ✅ | FastAPI ısı haritası servisi (`app/`) |
| ✅ | Leaflet tabanlı interaktif harita (`web/index.html`) |
| ✅ | Adil fiyat tahmin modeli (`app/pricing.py`, `scripts/train_model.py`) |
| 🚧 | Alternatif semt önerileri (Modül 3) — ulaşım verisi hazır, motor yazılıyor |
| ⬜ | Ev arkadaşı eşleştirme |

## 📂 Proje Yapısı

```
app/                        FastAPI uygulaması
  config.py                 tüm dosya yolları tek yerde
  main.py                   API uç noktaları
  heatmap.py                fiyat indeksi + renklendirme
  pricing.py                model veri hazırlığı (eğitim ve servis paylaşır)
  normalize.py              Türkçe adres eşleştirme
scripts/                    offline betikler (sunucuda çalışmaz)
  build_market_values.py    ham ilanlardan mahalle medyanlarını üretir
  train_model.py            adil fiyat modelini eğitir
  explore.py                veri keşfi
  repair_geojson.py         bozuk GeoJSON onarımı (tek seferlik)
  fetch_transit.py          OSM'den metro/Marmaray istasyonlarını indirir
data/
  raw/                      dokunulmamış kaynak veri
  processed/                üretilen veri
models/                     eğitilmiş model (git'e dâhil değil)
web/index.html              arayüz
```

Yollar `app/config.py` içinde `__file__` üzerinden çözülür; betikler hangi
dizinden çalıştırılırsa çalıştırılsın veriyi bulur.

## ▶️ Kurulum ve Çalıştırma

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python -m scripts.build_market_values   # piyasa değerleri (opsiyonel, CSV hazır)
python -m scripts.train_model           # adil fiyat modeli (~1 dk, zorunlu)
python -m app.main                      # API + arayüz: http://127.0.0.1:8000
```

Geliştirirken otomatik yeniden yükleme için:
`uvicorn app.main:app --reload`

macOS'ta LightGBM için OpenMP gerekiyor: `brew install libomp`.

Model dosyası (`models/fair_price_model.joblib`, ~6 MB) depoya dâhil değildir;
`python -m scripts.train_model` ile üretilir. Model yoksa harita yine çalışır, yalnızca
adil fiyat sekmesi devre dışı kalır.

## 🔌 API

| Endpoint | Açıklama |
|---|---|
| `GET /api/geojson` | Mahalle sınırları + fiyatlar. Bütçeden bağımsız, bir kez indirilir (~900 KB gzip). |
| `GET /api/heatmap?budget=25000` | Bütçeye göre mahalle durum listesi (~600 B gzip). |
| `GET /api/legend` | Renk/etiket sözlüğü. |
| `GET /api/locations` | Formu doldurmak için ilçe -> mahalle listesi. |
| `POST /api/estimate` | İlan özelliklerinden adil kira aralığı tahmini. |

Geometri ve renklendirme ayrıştırıldığı için bütçe değiştiğinde tarayıcı
yalnızca birkaç yüz baytlık bir yanıt indirir; sınırlar yeniden çizilmez.

## ⚠️ Veri Kalitesi Notları

Ham `istanbulApartmentForRent.csv` karışık veri içeriyor: aylık kiraların yanında
satılık ilan fiyatları (23.000.000 TL'ye kadar) ve bin cinsinden girilmiş
değerler (40, 60) var. `datalookup.py` bu yüzden:

* İlanları **3.000 – 500.000 TL** kira bandına sınırlar,
* Ortalama yerine **medyan** kullanır (tek bir aşırı ilan mahalleyi bozmasın),
* En az **3 ilanı** olmayan mahalleleri eler.

Sonuç: 968 mahallenin **489'u** (fiyat verisi bulunan 539 mahallenin %91'i)
haritada renklendirilir. Kalan mahallelerde yeterli ilan verisi yoktur ve
"Veri Yok" olarak gösterilir.


## 🤖 Adil Fiyat Modeli (Modül 1)

`scripts/train_model.py` dört yaklaşımı 5-kat çapraz doğrulamayla karşılaştırır.
Hedef `log(fiyat)`, hatalar kullanıcının gördüğü TL uzayında raporlanır:

| Model | MAE | MedAE | Medyan sapma | R² |
|---|---|---|---|---|
| Baseline (mahalle medyanı) | 19.655 | 7.000 | %25.0 | 0.36 |
| Ridge (one-hot) | 14.112 | 5.243 | %18.3 | 0.58 |
| XGBoost | 13.103 | 4.566 | %16.0 | 0.53 |
| LightGBM | 13.391 | 4.655 | %16.3 | 0.54 |
| **LightGBM q50 (servis edilen)** | **11.573** | **4.442** | **%15.1** | **0.67** |

Baseline ("mahallenin medyan kirasını söyle") kasıtlı olarak konuldu: model
bunu geçemiyorsa özelliklerin bir değeri yok demektir. Gerçek kazanç
**%25 → %15.1** medyan sapma.

**Neden çeyreklik regresyonu:** tek bir sayı yerine q25/q50/q75 modelleri
eğitilip bir *aralık* sunuluyor. "Bu ev 38.710 TL eder" demek, veriyle
desteklenmeyen bir kesinlik iddiasıdır; "adil aralık 36.231 – 46.509 TL"
demek dürüsttür.

**Özellikler:** oda, salon, `log(alan)`, bina yaşı, kat, ilçe, mahalle
(571 mahalle, ağaç modellerinde doğal kategorik olarak).

### Bilinen sınırlar

* **Verinin tarihi belli değil.** CSV'de tarih sütunu yok; bu fiyatların hangi
  döneme ait olduğunu bilmiyoruz. İstanbul'daki enflasyon hızında bu ciddi bir
  kısıt — yayına alınacaksa veri dönemi arayüzde belirtilmeli.
* **Aynı dairenin tekrar ilana çıkması** tespit edilmiyor. Yalnızca birebir
  yinelenen satırlar atıldı; benzer ilanlar CV skorunu bir miktar iyimser
  gösteriyor olabilir.
* **Konum yalnızca isimle temsil ediliyor.** Metroya uzaklık, Boğaz manzarası,
  sahil yakınlığı gibi fiyatı ciddi etkileyen değişkenler modelde yok.
* **Eğitim aralığı dışına çıkılamaz:** 20–1000 m², 0–100 yaş, 3.000–500.000 TL.
  API bu sınırların dışındaki girdileri 422 ile reddeder.


## 🚇 Toplu Taşıma Verisi (Modül 3 altyapısı)

```bash
python -m scripts.fetch_transit    # data/raw/transit_stations.json
```

**Kaynak:** OpenStreetMap, [Overpass API](https://overpass-api.de) üzerinden.
Üyelik ve API anahtarı gerektirmez, lisans ODbL. Sonuç: **261 istasyon,
18 hat** (M1A–M11, T4/T5/T7, F3 ve B1 Marmaray), **56 aktarma noktası**.

Resmi alternatif [data.ibb.gov.tr](https://data.ibb.gov.tr) (GTFS) daha
eksiksiz — İETT otobüs, vapur, minibüs de içeriyor — ama üyelik istiyor ve
indirme elle yapılıyor. Raylı sistem yeterli olduğu için OSM tercih edildi.

### Bu veriyi çekerken karşılaşılan iki tuzak

**1. Hat ilişkileri istasyon düğümlerini üye almaz.** OSM'de `railway=station`
düğümleri ile hatları taşıyan `public_transport=stop_position` düğümleri
ayrıdır. İstasyonları ayrı sorgulayıp hatlarla eşleştirmeye çalışınca 566
istasyonun yalnızca 22'si bir hatta bağlanıyordu. Doğrusu, istasyonları
doğrudan hat ilişkilerinin üyelerinden türetmek (`node(r.routes)`).

**2. `network` filtresi olmadan şehirlerarası hatlar geliyor.** Filtresiz
sorgu Ankara/Konya/Sivas YHT hatlarını da döndürüyor; bunlar şehir içi
erişilebilirlik için anlamsız.

Ayrıca her hat yönü kendi durak düğümünü taşıdığı için ham veride "Üsküdar"
3 ayrı kayıt olarak, her biri tek hatla görünür. `merge_duplicate_stops`
aynı adlı ve ~500 m içindeki düğümleri birleştirir; aktarma yapısı ancak
bundan sonra doğru çıkıyor (Üsküdar = B1 + M5).

**Not:** Overpass'in ücretsiz aynaları sık sık meşgul döner (200 yanıtla
HTML hata sayfası bile gelebilir). Betik üç aynayı sırayla, artan beklemeyle
dener; yine de başarısız olursa birkaç dakika sonra tekrar çalıştır.
