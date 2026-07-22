# 🗺️ Istanbul Real-Estate Heatmap

An interactive, ML-powered rent affordability map for Istanbul. Enter a monthly
budget and see every neighborhood colored by whether you can afford it — plus a
fair-price estimator for individual listings and transit-based alternative
neighborhood suggestions when your dream area is out of reach.

> This repo is the data/ML backend and map UI. A polished React roommate
> platform built on top of it lives in
> [istanbul-roommate-platform](https://github.com/bariskiratt/istanbul-roommate-platform).

---

## Features

### 1. Budget Heatmap
Enter a maximum monthly budget (e.g. 12,000 TL) and Istanbul's neighborhoods
are colored on a Leaflet map: green = comfortably affordable, yellow = on the
edge, red = over budget. Neighborhood price levels come from median market
values built from thousands of real rental listings.

### 2. AI Fair-Price Estimator
A regression model (LightGBM / XGBoost / Ridge — best of the three chosen by
cross-validation) predicts what a unit *should* rent for from its district,
neighborhood, room count, area, building age and floor. If an asking price is
provided, the API compares it to the predicted band and tells you whether the
listing is overpriced ("30% above the area average") or a good deal.

### 3. Transit-Based Alternative Neighborhoods
If your target neighborhood (e.g. in Beşiktaş) is over budget, the system
suggests affordable alternatives that are easy to reach **by rail**
(Metro/Marmaray). Straight-line distance is misleading in Istanbul — the two
sides of the Bosphorus can be 1–2 km apart as the crow flies but 30+ minutes
apart in practice — so ranking uses a transfer-weighted shortest path over the
rail network (station data pulled from OpenStreetMap via the Overpass API).

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data & ML | Python, pandas, scikit-learn, XGBoost, LightGBM |
| API | FastAPI + Uvicorn |
| Frontend | Single-file HTML + vanilla JS with Leaflet |
| Transit data | OpenStreetMap (Overpass API) |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Serves the map UI |
| GET | `/api/heatmap` | Neighborhood GeoJSON colored for a given budget |
| GET | `/api/geojson` | Raw neighborhood boundaries |
| GET | `/api/legend` | Color legend for the heatmap |
| GET | `/api/locations` | Known district/neighborhood names |
| POST | `/api/estimate` | Fair-rent prediction for a listing |
| GET | `/api/alternatives` | Budget-friendly neighborhoods reachable by rail |

## Project Structure

```
app/                        FastAPI application
  config.py                 all file paths in one place
  main.py                   API endpoints
  heatmap.py                price index + coloring
  transit.py                transit graph + alternative-neighborhood suggestions
  pricing.py                model feature prep (shared by training and serving)
  normalize.py              Turkish-aware address matching
scripts/                    offline scripts (not run by the server)
  build_market_values.py    builds neighborhood medians from raw listings
  train_model.py            trains and compares fair-price models
  fetch_transit.py          downloads metro/Marmaray stations from OSM
  explore.py                data exploration
  repair_geojson.py         one-off broken-GeoJSON repair
data/
  raw/                      listings CSV, district/neighborhood GeoJSON, transit stations
  processed/                generated neighborhood market values
models/                     trained model (generated locally, not committed)
web/index.html              frontend
```

Paths are resolved in `app/config.py` via `__file__`, so scripts work from any
working directory.

## Setup & Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python -m scripts.build_market_values   # market values (optional, CSV is committed)
python -m scripts.train_model           # fair-price model (~1 min, required for /api/estimate)
python -m app.main                      # API + UI: http://127.0.0.1:8000
```

Then open http://127.0.0.1:8000, enter a budget, and explore the map.
