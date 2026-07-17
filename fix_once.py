from json_repair import repair_json

print("⏳ Dosya tamir ediliyor, lütfen bekle...")
with open('mahalle_geojson.json', 'r', encoding='utf-8') as f:
    raw = f.read()

fixed = repair_json(raw)

with open('mahalle_fixed.geojson', 'w', encoding='utf-8') as f:
    f.write(fixed)

print("✅ Tamamlandı! Artık 'mahalle_fixed.geojson' dosyasını kullanabilirsin.")