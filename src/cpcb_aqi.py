from typing import Dict, List, Optional, Tuple

AQI_BUCKETS = [
    (0, 50, "Good"),
    (51, 100, "Satisfactory"),
    (101, 200, "Moderately polluted"),
    (201, 300, "Poor"),
    (301, 400, "Very poor"),
    (401, 500, "Severe"),
]

def bucket_name(aqi: int) -> str:
    for lo, hi, name in AQI_BUCKETS:
        if lo <= aqi <= hi:
            return name
    return "Out of Range"

# Breakpoints (commonly used in CPCB-style AQI implementations)
# Format: (Clow, Chigh, Ilow, Ihigh)
BREAKPOINTS: Dict[str, List[Tuple[float, float, int, int]]] = {
    "pm10": [(0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200),
             (251, 350, 201, 300), (351, 430, 301, 400), (430.000001, 1e9, 401, 500)],
    "pm25": [(0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200),
             (91, 120, 201, 300), (121, 250, 301, 400), (250.000001, 1e9, 401, 500)],
    "no2":  [(0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200),
             (181, 280, 201, 300), (281, 400, 301, 400), (400.000001, 1e9, 401, 500)],
    "so2":  [(0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200),
             (381, 800, 201, 300), (801, 1600, 301, 400), (1600.000001, 1e9, 401, 500)],
    "co":   [(0.0, 1.0, 0, 50), (1.1, 2.0, 51, 100), (2.1, 10.0, 101, 200),
             (10.0, 17.0, 201, 300), (17.0, 34.0, 301, 400), (34.0, 1e9, 401, 500)],
    "o3":   [(0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200),
             (169, 208, 201, 300), (209, 748, 301, 400), (748.000001, 1e9, 401, 500)],
    "nh3":  [(0, 200, 0, 50), (201, 400, 51, 100), (401, 800, 101, 200),
             (801, 1200, 201, 300), (1200, 1800, 301, 400), (1800.000001, 1e9, 401, 500)],
    "pb":   [(0.0, 0.5, 0, 50), (0.5, 1.0, 51, 100), (1.1, 2.0, 101, 200),
             (2.1, 3.0, 201, 300), (3.1, 3.5, 301, 400), (3.5, 1e9, 401, 500)],
}

def interpolate_subindex(c: float, bps: List[Tuple[float, float, int, int]]) -> Optional[int]:
    for clow, chigh, ilow, ihigh in bps:
        if clow <= c <= chigh:
            aqi = ((ihigh - ilow) / (chigh - clow)) * (c - clow) + ilow
            return int(round(aqi))
    return None

def compute_aqi(readings: Dict[str, Optional[float]]) -> Dict[str, object]:
    sub = {}
    for pol, val in readings.items():
        if val is None:
            continue
        pol = pol.lower()
        if pol not in BREAKPOINTS:
            continue
        try:
            c = float(val)
        except Exception:
            continue
        s = interpolate_subindex(c, BREAKPOINTS[pol])
        if s is not None:
            sub[pol] = s

    if not sub:
        return {"aqi": None, "bucket": "Insufficient data", "dominant": None, "sub_indices": {}}

    dominant = max(sub, key=sub.get)
    aqi = sub[dominant]
    return {"aqi": aqi, "bucket": bucket_name(aqi), "dominant": dominant, "sub_indices": sub}