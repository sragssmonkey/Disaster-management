import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render
import json

def earthquake_risk_map(request):
    return render(request,"mlmodel/earthquake_risk_map.html")

def disaster_map(request):
    # File paths
    earthquake_file = os.path.join(settings.BASE_DIR, "data", "earthquake_india_2000_2025.csv")
    cyclone_file = os.path.join(settings.BASE_DIR, "data", "cyclone_india_2000_2025.csv")

    # Load data
    earthquakes = pd.read_csv(earthquake_file)
    cyclones = pd.read_csv(cyclone_file)

    # -------------------
    # Clean Data
    # -------------------
    earthquakes.columns = earthquakes.columns.str.strip().str.lower()
    earthquakes = earthquakes.dropna(subset=["latitude", "longitude"])
    earthquakes["magnitude"] = earthquakes["magnitude"].round(1)
    earthquakes["place"] = earthquakes["place"].str.title()

    cyclones.columns = cyclones.columns.str.strip()
    cyclones = cyclones.dropna(subset=["LAT", "LON"])
    cyclones["NAME"] = cyclones["NAME"].str.title().fillna("Unknown")

    # -------------------
    # Filters from GET parameters
    # -------------------
    min_mag = float(request.GET.get("min_mag", 0))
    max_mag = float(request.GET.get("max_mag", 10))
    earthquakes = earthquakes[(earthquakes["magnitude"] >= min_mag) & (earthquakes["magnitude"] <= max_mag)]

    min_year = int(request.GET.get("min_year", cyclones["YEAR"].min()))
    max_year = int(request.GET.get("max_year", cyclones["YEAR"].max()))
    cyclones = cyclones[(cyclones["YEAR"] >= min_year) & (cyclones["YEAR"] <= max_year)]

    # -------------------
    # Convert to JSON
    # -------------------
    earthquake_data = earthquakes[["latitude", "longitude", "magnitude", "place", "time"]].to_dict(orient="records")
    cyclone_data = cyclones[["LAT", "LON", "NAME", "YEAR", "WMO_WIND"]].to_dict(orient="records")

    context = {
        "earthquake_data": json.dumps(earthquake_data),
        "cyclone_data": json.dumps(cyclone_data),
        "min_mag": min_mag,
        "max_mag": max_mag,
        "min_year": min_year,
        "max_year": max_year,
        "min_year_global": cyclones["YEAR"].min(),
        "max_year_global": cyclones["YEAR"].max(),
    }

    return render(request, "mlmodel/disaster_map.html", context)
