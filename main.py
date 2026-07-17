from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import pandas as pd
import copy
import asyncio
from heatmap import build_budget_heatmap

app = FastAPI()

# Frontend'in API'ye bağlanabilmesi için CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Verileri sunucu açılırken bir kez yükle (Hız için)
print("🚀 Veriler yükleniyor...")
with open('mahalle_geojson.json', 'r', encoding='utf-8') as f:
    RAW_GEOJSON = json.load(f)

df = pd.read_csv('neighborhood_market_values.csv')
# CSV temizleme
df['district'] = df['district'].str.strip().str.upper()
df['neighborhood'] = df['neighborhood'].str.strip().str.upper()
print("✅ Veriler hazır.")

@app.get("/api/heatmap")
async def get_heatmap(budget: float):
    print(f"📥 {budget} TL bütçesi için harita oluşturuluyor...")
    
    # Orijinal veriyi bozmamak için kopyala
    data_to_process = copy.deepcopy(RAW_GEOJSON)
    
    # CPU-ağır işlemi ana event loop'tan çıkar (bloklamayı önler)
    result = await asyncio.to_thread(build_budget_heatmap, data_to_process, df, budget)
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)