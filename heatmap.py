import pandas as pd

def build_budget_heatmap(geojson_data, df, user_budget):
    # CSV'deki mahalle ve ilçe isimlerini temizle (Eşleşme hatası yapmamak için)
    # Bu işlemi her istekte değil, bir kez yapmak daha hızlıdır ama 
    # şimdilik çalışma mantığını düzeltmek için buraya koyuyorum.
    
    for feature in geojson_data.get('features', []):
        props = feature.get('properties', {})
        address = props.get('address', {})
        
        # GeoJSON'daki mahalle ve ilçe isimlerini al
        geo_neigh = str(address.get('city') or address.get('suburb') or "").strip().upper()
        geo_dist = str(address.get('town') or address.get('archipelago') or "").strip().upper()
        
        # İsim temizleme (MAHALLESİ eklerinden kurtul)
        geo_neigh = geo_neigh.replace("MAHALLESİ", "").replace("MAHALLESI", "").strip()

        # CSV içinde bu mahalleyi ara
        match = df[(df['neighborhood'] == geo_neigh) & (df['district'] == geo_dist)]
        
        if not match.empty:
            avg_price = float(match.iloc[0]['avg_price'])
            props['avg_price'] = avg_price # Fiyatı properties'e geri yaz
            
            # Renklendirme mantığı
            if avg_price <= user_budget:
                props['status'] = 'Safe'
                props['color'] = '#2ecc71'
            elif avg_price <= user_budget * 1.20:
                props['status'] = 'Borderline'
                props['color'] = '#f1c40f'
            else:
                props['status'] = 'Expensive'
                props['color'] = '#e74c3c'
        else:
            # Eşleşme yoksa gri yap (Hangi mahallelerin eşleşmediğini böyle anlarız)
            props['status'] = 'No Data'
            props['color'] = '#95a5a6'
            
    return geojson_data