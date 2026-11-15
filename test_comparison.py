import pandas as pd
from modules.regional_comparison import compare_regions

# Load NASA climate data
df = pd.read_csv(
    "data/processed/multi_location_climate.csv"
)

# Compare Bengaluru and Chennai
print("\nEARTHSCOPE AI - REGIONAL COMPARISON")

result = compare_regions(
    df,
    "Bengaluru",
    "Chennai"
)

print("\nComparison Results:")
print(result)