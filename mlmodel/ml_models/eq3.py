import pandas as pd
import requests
import joblib
from datetime import datetime, timedelta, timezone
import json

# -------------------------------
# 1. Load trained model
# -------------------------------
rf = joblib.load("earthquake_risk_model.pkl")
print("✅ Loaded trained risk model")

# -------------------------------
# 2. Fetch Live Earthquakes (30 days)
# -------------------------------
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

    return pd.DataFrame(records)

# -------------------------------
# 3. Aggregate into grid features
# -------------------------------
def aggregate_features(df):
    if df.empty:
        return pd.DataFrame()

    df["lat_bin"] = (df["latitude"] // 0.5) * 0.5
    df["lon_bin"] = (df["longitude"] // 0.5) * 0.5
    df["cell_id"] = df["lat_bin"].astype(str) + "_" + df["lon_bin"].astype(str)

    agg = df.groupby("cell_id").agg(
        count_m4=("magnitude", lambda x: (x >= 4.0).sum()),
        count_m5=("magnitude", lambda x: (x >= 5.0).sum()),
        max_mag=("magnitude", "max"),
        mean_mag=("magnitude", "mean"),
        std_mag=("magnitude", "std"),
        mean_depth=("depth_km", "mean"),
        shallow_ratio=("depth_km", lambda x: (x < 70).mean())
    ).reset_index()

    return agg.fillna(0)

# -------------------------------
# 4. Predict Risk using ML Model
# -------------------------------
def classify_risk(agg_df):
    features = ["count_m4","count_m5","max_mag","mean_mag",
                "std_mag","mean_depth","shallow_ratio"]

    X = agg_df[features]
    preds = rf.predict(X)
    agg_df["predicted_risk"] = preds

    # Probability that an earthquake is likely (Moderate or High)
    try:
        proba = rf.predict_proba(X)
        class_labels = list(rf.classes_)
        positive_classes = {"Moderate", "High"}
        pos_indices = [i for i, c in enumerate(class_labels) if c in positive_classes]
        if pos_indices:
            agg_df["quake_probability"] = proba[:, pos_indices].sum(axis=1)
        else:
            agg_df["quake_probability"] = 0.0
    except Exception:
        agg_df["quake_probability"] = 0.0

    return agg_df

# -------------------------------
# 4b. Derive binary prediction (Yes/No)
# -------------------------------
def derive_binary_quake_flag(agg_df, positive_levels=("Moderate", "High"), threshold: float = 0.5):
    if agg_df.empty:
        return agg_df
    # Prefer probability-based threshold when available
    if "quake_probability" in agg_df.columns:
        agg_df["will_quake"] = (agg_df["quake_probability"] >= threshold).map({True: "Yes", False: "No"})
    else:
        agg_df["will_quake"] = agg_df["predicted_risk"].isin(positive_levels).map({True: "Yes", False: "No"})
    return agg_df

# -------------------------------
# 5. Visualize on Map
# -------------------------------
def make_map(df_live, agg_df, save_path="earthquake_risk_map.html", threshold: float = 0.5, template_path="map_template.html"):
    # Build data points for JS (one representative lat/lon per cell)
    points = []
    for _, row in agg_df.iterrows():
        sample = df_live[df_live["cell_id"] == row["cell_id"]].iloc[0]
        points.append({
            "cell_id": row["cell_id"],
            "lat": float(sample["latitude"]),
            "lon": float(sample["longitude"]),
            "prob": float(row.get("quake_probability", 0.0)),
            "yes": str(row.get("will_quake", "No")),
            "pred": str(row.get("predicted_risk", "Low")),
            "max_mag": float(row.get("max_mag", 0.0)),
            "count_m4": int(row.get("count_m4", 0)),
            "count_m5": int(row.get("count_m5", 0))
        })
    # Load template and replace placeholders
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
    html = html.replace("__POINTS_JSON__", json.dumps(points))
    html = html.replace("__THRESHOLD_PERCENT__", str(int(threshold * 100)))
    # Save output
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Risk map saved: {save_path}")

# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    df_live = fetch_live_earthquakes()
    if df_live.empty:
        print("⚠️ No live earthquake data available.")
    else:
        df_live["lat_bin"] = (df_live["latitude"] // 0.5) * 0.5
        df_live["lon_bin"] = (df_live["longitude"] // 0.5) * 0.5
        df_live["cell_id"] = df_live["lat_bin"].astype(str) + "_" + df_live["lon_bin"].astype(str)

        agg_df = aggregate_features(df_live)
        classified = classify_risk(agg_df)
        threshold = 0.5
        classified = derive_binary_quake_flag(classified, threshold=threshold)

        classified.to_csv("classified_live_risk.csv", index=False)
        classified[["cell_id", "will_quake", "quake_probability", "predicted_risk", "max_mag", "count_m4", "count_m5"]].to_csv("earthquake_binary_predictions.csv", index=False)
        print("✅ Classified risk zones saved to classified_live_risk.csv")
        print("✅ Binary predictions saved to earthquake_binary_predictions.csv")

        make_map(df_live, classified, threshold=threshold)
