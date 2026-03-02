import pandas as pd

POLLUTANTS = ["pm25", "pm10", "no2", "so2", "co", "o3", "nh3", "pb"]

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename = {}
    for c in df.columns:
        key = str(c).strip().lower()
        key2 = key.replace(" ", "").replace("-", "").replace(".", "")
        if key2 in ("pm25", "pm2_5", "pm25_"):
            rename[c] = "pm25"
        elif key2 == "pm10":
            rename[c] = "pm10"
        else:
            rename[c] = key
    return df.rename(columns=rename)

def preprocess_csv(input_path: str, output_path: str) -> None:
    df = pd.read_csv(input_path)
    df = normalize_columns(df)

    for col in POLLUTANTS + ["aqi"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    present = [c for c in POLLUTANTS if c in df.columns]
    if present:
        df = df.dropna(subset=present, how="all")

    df.to_csv(output_path, index=False)