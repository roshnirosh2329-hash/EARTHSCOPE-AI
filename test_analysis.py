import pandas as pd

from modules.analysis import (
    climate_fingerprint,
    detect_climate_anomalies,
    discover_climate_relationships,
    calculate_long_term_trend
)

# Load NASA climate data
df = pd.read_csv(
    "data/processed/multi_location_climate.csv"
)

print("\n===== EARTHSCOPE AI =====")
print("INTELLIGENT CLIMATE ANALYSIS")

# Analyse Bengaluru
bengaluru = df[df["Location"] == "Bengaluru"].copy()

print("\n1. CLIMATE FINGERPRINT")
print(climate_fingerprint(bengaluru))

print("\n2. CLIMATE ANOMALIES")
print(detect_climate_anomalies(bengaluru))

print("\n3. CLIMATE RELATIONSHIPS")
print(discover_climate_relationships(bengaluru))

print("\n4. LONG-TERM CLIMATE TREND")
print(calculate_long_term_trend(bengaluru))