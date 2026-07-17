# explore.py
import pandas as pd
import numpy as np

def load_and_explore(file_path):
    print("🔄 Veri seti yükleniyor...")
    # Temizlenmiş verini buraya yükle
    df = pd.read_csv(file_path)
    
    # 1. price_per_m2 (Metrekare Başına Fiyat) Hesaplaması
    # m2 alanı 0 olan hatalı satırlar varsa hata almamak için önlem alıyoruz
    print("📊 Metrekare başına fiyat hesaplanıyor...")
    df = df[df['area (m2)'] > 0] # Güvenli bölge
    df['price_per_m2'] = df['price'] / df['area (m2)']
    
    # 2. İlçe (District) ve Mahalle (Neighborhood) Bazlı Ortalama Fiyatlar
    print("\n🏢 İlçe Bazlı Özet (İlk 10):")
    district_summary = df.groupby('district').agg(
        total_listings=('price', 'count'),
        avg_price=('price', 'mean'),
        avg_m2=('area (m2)', 'mean'),
        avg_price_per_m2=('price_per_m2', 'mean')
    ).sort_values(by='avg_price', ascending=False)
    
    print(district_summary.head(10))
    
    print("\n📍 Mahalle Bazlı Özet (İlk 10):")
    neighborhood_summary = df.groupby(['district', 'neighborhood']).agg(
        total_listings=('price', 'count'),
        avg_price=('price', 'mean'),
        avg_price_per_m2=('price_per_m2', 'mean')
    ).sort_values(by='avg_price_per_m2', ascending=False)
    
    print(neighborhood_summary.head(10))
    
    # Analiz sonuçlarını backend ve heatmap için kaydetme
    # Bu CSV, ileride haritayı renklendirirken bütçe kontrolü için çok işimize yarayacak
    neighborhood_summary.reset_index().to_csv('neighborhood_market_values.csv', index=False)
    print("\n💾 Mahalle bazlı piyasa değerleri 'neighborhood_market_values.csv' olarak kaydedildi.")
    
    return df

if __name__ == "__main__":
    # Veri setinin adını kendi dosya adına göre güncelleyebilirsin
    DATA_PATH = "istanbulApartmentForRent.csv" 
    
    try:
        processed_df = load_and_explore(DATA_PATH)
    except FileNotFoundError:
        print(f"❌ Hata: '{DATA_PATH}' dosyası bulunamadı. Lütfen temizlediğin verinin adını kontrol et.")