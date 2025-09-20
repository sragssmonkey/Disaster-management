import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib


df = pd.read_csv("earthquake_india_2000_2025.csv")


df["lat_bin"] = (df["latitude"] // 0.5) * 0.5
df["lon_bin"] = (df["longitude"] // 0.5) * 0.5
df["cell_id"] = df["lat_bin"].astype(str) + "_" + df["lon_bin"].astype(str)

# Save a copy with cell_id for downstream use
df.to_csv("earthquake_india_2000_2025_with_cells.csv", index=False)
print("✅ Saved historical dataset with cell_id -> earthquake_india_2025_with_cells.csv")


agg = df.groupby("cell_id").agg(
    count_m4=("magnitude", lambda x: (x >= 4.0).sum()),
    count_m5=("magnitude", lambda x: (x >= 5.0).sum()),
    max_mag=("magnitude", "max"),
    mean_mag=("magnitude", "mean"),
    std_mag=("magnitude", "std"),
    mean_depth=("depth_km", "mean"),
    shallow_ratio=("depth_km", lambda x: (x < 70).mean())
).reset_index()

agg = agg.fillna(0)

def label_zone(row):
    if row["count_m4"] >= 25 or row["max_mag"] >= 6.0:
        return "High"
    elif row["count_m4"] >= 10 or row["max_mag"] >= 5.0:
        return "Moderate"
    else:
        return "Low"

agg["label"] = agg.apply(label_zone, axis=1)


features = ["count_m4","count_m5","max_mag","mean_mag",
            "std_mag","mean_depth","shallow_ratio"]

X = agg[features]
y = agg["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    class_weight="balanced",
    random_state=42
)

rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
print("Feature Importances:\n", importances)

joblib.dump(rf, "earthquake_risk_model.pkl")
print("odel saved as earthquake_risk_model.pkl")


def fetch_live_earthquakes():
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=30)

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%d"),
        "endtime": end_time.strftime("%Y-%m-%d"),
        "minlatitude": 5,
        "maxlatitude": 38,
        "minlongitude": 65,
        "maxlongitude": 100
    }

    r = requests.get(url, params=params)
    data = r.json()

    records = []
    for feat in data.get("features", []):
        props = feat["properties"]
        coords = feat["geometry"]["coordinates"]
        records.append({
            "time": datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
            "place": props.get("place"),
            "magnitude": props.get("mag"),
            "longitude": coords[0],
            "latitude": coords[1],
            "depth_km": coords[2]
        })

    df_live = pd.DataFrame(records)
    if df_live.empty:
        print("No live earthquakes found in the last 30 days.")
        return df_live

 
    df_live["lat_bin"] = (df_live["latitude"] // 0.5) * 0.5
    df_live["lon_bin"] = (df_live["longitude"] // 0.5) * 0.5
    df_live["cell_id"] = df_live["lat_bin"].astype(str) + "_" + df_live["lon_bin"].astype(str)

    return df_live


def classify_live_data(df_live, model):
    if df_live.empty:
        return df_live


    agg_live = df_live.groupby("cell_id").agg(
        count_m4=("magnitude", lambda x: (x >= 4.0).sum()),
        count_m5=("magnitude", lambda x: (x >= 5.0).sum()),
        max_mag=("magnitude", "max"),
        mean_mag=("magnitude", "mean"),
        std_mag=("magnitude", "std"),
        mean_depth=("depth_km", "mean"),
        shallow_ratio=("depth_km", lambda x: (x < 70).mean())
    ).reset_index()

    agg_live = agg_live.fillna(0)

    agg_live["predicted_risk"] = model.predict(agg_live[features])
    return agg_live

print("\n🌍 Fetching live earthquakes...")
df_live = fetch_live_earthquakes()
if not df_live.empty:
    live_results = classify_live_data(df_live, rf)
    print("\n✅ Classified Live Earthquake Grid Cells:")
    print(live_results.head())

    live_results.to_csv("classified_live_earthquakes.csv", index=False)
    print("📁 Saved classified live results -> classified_live_earthquakes.csv")

