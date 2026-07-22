# 🏙️ Istanbul Smart Real-Estate & Roommate Platform (AI-Powered)

A data-driven web platform for Istanbul's dynamic, hyper-inflationary and
opaque rental market.

The project pairs the classic "find a roommate" idea with machine-learning
models: it offers landlords a **Fair Value** rent estimate at market standards,
and shows renters which neighborhoods fit their budget through a **dynamic
affordability heatmap**.

---

## 🚀 Core Features & Modules

### 1. AI Fair-Price Estimator (Regression Engine)
When a landlord posts a listing, a machine-learning model (XGBoost / LightGBM)
runs in the background.
* **How it works:** thousands of current listings (district, neighborhood, m²,
  building age, room count) are analyzed to predict the rent a unit "should"
  command.
* **Benefit:** if the asking price is well above the market, the user is warned
  ("this is 30% above the area average") and nudged toward a fair band.

### 2. Dynamic Budget Heatmap (Affordability Heatmap)
A visual analysis module that changes how budget-constrained renters see the city.
* **How it works:** the user enters a maximum monthly budget (e.g. 12,000 TL) and
  Istanbul's neighborhoods are colored on the map.
* **Visualization:** neighborhoods comfortably within budget are green, "on the
  edge" ones yellow, and over-budget ones red — a data-backed search experience.

### 3. Smart Alternative-Neighborhood Suggestions (Transit Routing)
If the user is searching in a popular, expensive area (e.g. Beşiktaş) but their
budget falls short, the system suggests budget-friendly alternative
neighborhoods that are easily reachable by rail transit (Metro/Marmaray) — e.g.
Üsküdar — using a transfer-weighted shortest path over the transit network.

---

## 🛠️ Architecture & Tech Stack

* **Machine Learning:** Python, Pandas, scikit-learn, XGBoost, LightGBM (price
  estimation and modeling).
* **Backend API:** Python, FastAPI (serving the ML models to the frontend).
* **Frontend:** single-file HTML + vanilla JS with **Leaflet** for the
  interactive map (`web/index.html`).
* **Transit data:** OpenStreetMap via the Overpass API.

> A polished React/Vite roommate UI is integrated with this backend in a
> separate monorepo: **[istanbul-roommate-platform](https://github.com/bariskiratt/istanbul-roommate-platform)**.

---

## 📌 Current Status (What Actually Works)

| Status | Component |
|---|---|
| ✅ | Data-cleaning pipeline (`scripts/build_market_values.py`) |
| ✅ | Neighborhood-level market values (`data/processed/`) |
| ✅ | FastAPI heatmap service (`app/`) |
| ✅ | Leaflet interactive map (`web/index.html`) |
| ✅ | Fair-price prediction model (`app/pricing.py`, `scripts/train_model.py`) |
| ✅ | Alternative-neighborhood suggestions (Module 3) — `app/transit.py` |
| ⬜ | Roommate matching (see the roommate-platform repo) |

## 📂 Project Structure

```
app/                        FastAPI application
  config.py                 all file paths in one place
  main.py                   API endpoints
  heatmap.py                price index + coloring
  transit.py                transit graph + alternative-neighborhood suggestions
  pricing.py                model data prep (shared by training and serving)
  normalize.py              Turkish-aware address matching
scripts/                    offline scripts (do not run on the server)
  build_market_values.py    builds neighborhood medians from raw listings
  train_model.py            trains the fair-price model
  explore.py                data exploration
  repair_geojson.py         one-off broken-GeoJSON repair
  fetch_transit.py          downloads metro/Marmaray stations from OSM
data/
  raw/                      untouched source data
  processed/                generated data
models/                     trained model (not committed)
web/index.html              frontend
```

Paths are resolved in `app/config.py` via `__file__`, so scripts find the data
no matter which directory they are run from.

## ▶️ Setup & Run

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python -m scripts.build_market_values   # market values (optional, CSV is committed)
python -m scripts.train_model           # fair-price model (~1 min, required)
python -m app.main                      # API + UI: http://127.0.0.1:8000
```

For auto-reload during development: `uvicorn app.main:app --reload`

On macOS, LightGBM needs OpenMP: `brew install libomp`.

The model file (`models/fair_price_model.joblib`, ~6 MB) is not committed; it is
produced by `python -m scripts.train_model`. Without it the map still works —
only the fair-price tab is disabled.

## 🔌 API

| Endpoint | Description |
|---|---|
| `GET /api/geojson` | Neighborhood boundaries + prices. Budget-independent, downloaded once (~900 KB gzip). |
| `GET /api/heatmap?budget=25000` | Per-neighborhood status list for a budget (~600 B gzip). |
| `GET /api/legend` | Color/label dictionary. |
| `GET /api/locations` | District → neighborhood list (for filling forms). |
| `POST /api/estimate` | Fair rent range from listing features. |
| `GET /api/alternatives` | Budget-friendly neighborhoods near a target, reachable by rail. |

Because geometry and coloring are decoupled, changing the budget only downloads
a few hundred bytes — the boundaries are not redrawn.

## ⚠️ Data-Quality Notes

The raw `istanbulApartmentForRent.csv` is messy: alongside monthly rents it mixes
for-sale prices (up to 23,000,000 TL) and values entered in thousands (40, 60).
`scripts/build_market_values.py` therefore:

* clamps listings to a **3,000 – 500,000 TL** rent band,
* uses the **median** instead of the mean (so one extreme listing can't distort a
  neighborhood),
* drops neighborhoods with fewer than **3 listings**.

Result: **489 of 968** neighborhoods (91% of the 539 with price data) are colored
on the map. The rest lack enough listing data and show as "No Data".

## 🤖 Fair-Price Model (Module 1)

`scripts/train_model.py` compares four approaches with 5-fold cross-validation.
The target is `log(price)`; errors are reported in the TL space the user sees:

| Model | MAE | MedAE | Median error | R² |
|---|---|---|---|---|
| Baseline (neighborhood median) | 19,655 | 7,000 | 25.0% | 0.36 |
| Ridge (one-hot) | 14,112 | 5,243 | 18.3% | 0.58 |
| XGBoost | 13,103 | 4,566 | 16.0% | 0.53 |
| LightGBM | 13,391 | 4,655 | 16.3% | 0.54 |
| **LightGBM q50 (served)** | **11,573** | **4,442** | **15.1%** | **0.67** |

The baseline ("just predict the neighborhood's median rent") is deliberate: if
the model can't beat it, the features add no value. The real gain is
**25% → 15.1%** median error.

**Why quantile regression:** instead of a single number, q25/q50/q75 models are
trained to give a *range*. Saying "this unit is worth 38,710 TL" is a precision
claim the data doesn't support; "the fair range is 36,231 – 46,509 TL" is honest.

**Features:** room, living room, `log(area)`, building age, floor, district,
neighborhood (571 neighborhoods, as native categoricals in the tree models).

### Known limitations

* **The data's date is unknown.** The CSV has no date column; we don't know which
  period these prices belong to. Given Istanbul's inflation rate this is a serious
  caveat — if deployed, the data period should be shown in the UI.
* **Re-listings of the same unit aren't detected.** Only exact duplicate rows were
  dropped; near-duplicate listings may make the CV score slightly optimistic.
* **Location is represented by name only.** Distance to metro, Bosphorus views,
  seafront proximity — variables that strongly affect price — are not in the model.
* **No extrapolation beyond the training range:** 20–1000 m², 0–100 years,
  3,000–500,000 TL. The API rejects out-of-range inputs with 422.

## 🚇 Transit Data (Module 3 infrastructure)

```bash
python -m scripts.fetch_transit    # data/raw/transit_stations.json
```

**Source:** OpenStreetMap, via the [Overpass API](https://overpass-api.de). No
account or API key required, ODbL license. Result: **261 stations, 18 lines**
(M1A–M11, T4/T5/T7, F3 and B1 Marmaray), **56 interchange stations**.

The official alternative [data.ibb.gov.tr](https://data.ibb.gov.tr) (GTFS) is more
complete — it also includes buses, ferries and minibuses — but requires an account
and manual download. Rail transit is sufficient here, so OSM was preferred.

### Two pitfalls hit while fetching this data

**1. Route relations don't contain station nodes.** In OSM, `railway=station`
nodes and the `public_transport=stop_position` nodes that carry the lines are
separate. Querying stations separately and matching them to lines connected only
22 of 566 stations. The fix is to derive stations directly from the route
relations' members (`node(r.routes)`).

**2. Without a `network` filter, intercity lines leak in.** An unfiltered query
also returns Ankara/Konya/Sivas high-speed rail lines, which are meaningless for
in-city accessibility.

Also, because each line direction carries its own stop node, in the raw data
"Üsküdar" appears as 3 separate records, each on a single line.
`merge_duplicate_stops` merges same-named nodes within ~500 m; only after that
does the interchange structure come out correctly (Üsküdar = B1 + M5).

**Note:** Overpass's free mirrors are often busy (they can even return an HTML
error page with a 200 status). The script tries three mirrors in sequence with
increasing backoff; if it still fails, run it again a few minutes later.

## 🧭 Alternative-Neighborhood Suggestions (Module 3)

If a user wants to live near an expensive neighborhood (e.g. Levent, 152,500 TL)
but their budget falls short, they click that neighborhood on the map and choose
**"🚇 Affordable alternatives nearby"** to see budget-friendly neighborhoods that
are easy to reach by rail.

**Why not straight-line distance:** in Istanbul, as-the-crow-flies proximity is
misleading. Beşiktaş and Üsküdar are ~1.9 km apart in a straight line, but the
Bosphorus is between them; without a direct rail link the trip takes half an hour.
So suggestions are based not on distance but on **transfer-weighted stop cost over
the rail network**.

**How it works:**
1. Each neighborhood's area centroid is computed and its nearest station found.
   Neighborhoods more than 1.2 km from a station are "not within walking distance
   of rail" (e.g. the Princes' Islands → no suggestions).
2. The inter-station network is built from line orderings. Walking the network
   from the target: advancing one stop costs 1 unit, **a transfer costs +5 units**
   (wait + walk). So "3 stops but 2 transfers" ends up costlier than "5 stops but
   no transfer".
3. Budget-friendly neighborhoods within walking distance of easily-reached
   stations are ranked first by ease of transit, then by cheapness.

Example: Levent (152,500 TL) → with a 30,000 TL budget, neighborhoods in
Kağıthane/Şişli on the M2/M7 lines at 18,000–25,000 TL, 0–2 stops away.

**Verification:** the far side of the Bosphorus isn't suggested because it's not
reachable without a transfer; the islands (Nizam Mah., 6.1 km from a station)
return "unreachable". The transit graph was also tested on a synthetic network
where the transfer penalty is applied correctly.

### Limitations

* **Rail only.** No buses/metrobüs/ferries; IETT data exists on data.ibb.gov.tr
  but requires an account. The metrobüs is a notable gap (the one fast line
  crossing the Bosphorus by road).
* **Stop count ≠ minutes.** The cost unit is stops; real travel time (speed
  differences between lines, waiting times) is not modeled.
* **Walking distance is straight-line.** Not a real pedestrian route — just the
  centroid-to-station straight distance (1.2 km threshold).
