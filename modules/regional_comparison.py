import pandas as pd
import numpy as np


CLIMATE_VARIABLES = [
    "Temperature",
    "Rainfall",
    "Humidity",
    "Wind Speed"
]


def compare_regions(df, location_a, location_b):

    region_a = df[df["Location"] == location_a].copy()
    region_b = df[df["Location"] == location_b].copy()

    if region_a.empty or region_b.empty:
        raise ValueError("One or both locations have no data.")

    region_a = region_a.set_index("Date")
    region_b = region_b.set_index("Date")

    # Compare only matching months
    common_dates = region_a.index.intersection(
        region_b.index
    )

    region_a = region_a.loc[common_dates]
    region_b = region_b.loc[common_dates]

    if len(common_dates) == 0:
        raise ValueError("No matching dates between locations.")

    results = []

    for variable in CLIMATE_VARIABLES:

        if (
            variable not in region_a.columns
            or variable not in region_b.columns
        ):
            continue

        values_a = region_a[variable].dropna()
        values_b = region_b[variable].dropna()

        if values_a.empty or values_b.empty:
            continue

        mean_a = values_a.mean()
        mean_b = values_b.mean()

        pooled_std = np.sqrt(
            (values_a.var() + values_b.var()) / 2
        )

        if pd.isna(pooled_std) or pooled_std == 0:
            standardized_difference = np.nan
        else:
            standardized_difference = (
                mean_a - mean_b
            ) / pooled_std

        results.append({
            "Variable": variable,
            location_a + "_Average": round(mean_a, 3),
            location_b + "_Average": round(mean_b, 3),
            "Difference": round(mean_a - mean_b, 3),
            "Standardized_Difference": (
                round(standardized_difference, 3)
                if pd.notna(standardized_difference)
                else None
            ),
            "Common_Months": len(common_dates)
        })

    return pd.DataFrame(results)


def investigate_regional_divergence(df, location_a, location_b):

    comparison = compare_regions(
        df,
        location_a,
        location_b
    )

    findings = []

    for _, row in comparison.iterrows():

        score = row["Standardized_Difference"]

        if score is None or pd.isna(score):
            interpretation = "Insufficient variation for comparison"

        elif abs(score) >= 1:
            interpretation = "Large difference in average conditions"

        elif abs(score) >= 0.5:
            interpretation = "Moderate difference in average conditions"

        else:
            interpretation = "Small difference in average conditions"

        findings.append({
            "Variable": row["Variable"],
            "Interpretation": interpretation
        })

    return comparison, pd.DataFrame(findings)	
