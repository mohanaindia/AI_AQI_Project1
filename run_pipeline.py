import os
import pandas as pd
from src.preprocess import preprocess_csv, POLLUTANTS
from src.cpcb_aqi import compute_aqi

RAW_DIR = "data/raw"
CLEAN_PATH = "data/processed/clean.csv"
OUT_PATH = "outputs/predictions.csv"

def pick_input_file() -> str:
    for name in ["station_day.csv", "city_day.csv", "station_hour.csv", "city_hour.csv"]:
        p = os.path.join(RAW_DIR, name)
        if os.path.exists(p):
            return p

    for f in os.listdir(RAW_DIR):
        if f.lower().endswith(".csv"):
            return os.path.join(RAW_DIR, f)

    raise FileNotFoundError("No CSV found in data/raw/")

def main():
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    inp = pick_input_file()
    preprocess_csv(inp, CLEAN_PATH)

    df = pd.read_csv(CLEAN_PATH)

    computed = []
    for _, row in df.iterrows():
        readings = {p: (row[p] if p in df.columns else None) for p in POLLUTANTS}
        res = compute_aqi(readings)
        computed.append(res)

    out = df.copy()
    out["aqi_computed"] = [r["aqi"] for r in computed]
    out["aqi_bucket_computed"] = [r["bucket"] for r in computed]
    out["dominant_pollutant"] = [r["dominant"] for r in computed]

    out.to_csv(OUT_PATH, index=False)

    # quick validation if dataset has AQI column
    if "aqi" in out.columns:
        d = out.dropna(subset=["aqi", "aqi_computed"])
        if len(d) > 0:
            mae = (d["aqi"] - d["aqi_computed"]).abs().mean()
            print(f"MAE vs dataset AQI: {mae:.2f}")
        else:
            print("No rows with both dataset AQI and computed AQI.")

    print(f"Saved: {OUT_PATH}")

if __name__ == "__main__":
    main()