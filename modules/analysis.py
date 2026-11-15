import pandas as pd
import numpy as np
from scipy.stats import theilslopes


CLIMATE_COLUMNS = [
    "Temperature",
    "Rainfall",
    "Humidity",
    "Wind Speed"
]


def climate_fingerprint(df):

    fingerprint = {}

    for column in CLIMATE_COLUMNS:

        if column not in df.columns:
            continue

        values = df[column].dropna()

        if len(values) == 0:
            continue

        fingerprint[column] = {
            "average": round(values.mean(), 3),
            "variability": round(values.std(), 3),
            "minimum": round(values.min(), 3),
            "maximum": round(values.max(), 3),
            "median": round(values.median(), 3)
        }

    return fingerprint


def detect_climate_anomalies(df):

    result = df.copy()

    for column in CLIMATE_COLUMNS:

        if column not in result.columns:
            continue

        values = result[column]

        median = values.median()

        mad = np.median(
            np.abs(values.dropna() - median)
        )

        if mad == 0 or pd.isna(mad):
            result[column + "_Anomaly"] = False
            result[column + "_Score"] = 0.0
            continue

        robust_score = (
            0.6745 * (values - median) / mad
        )

        result[column + "_Score"] = robust_score

        result[column + "_Anomaly"] = (
            robust_score.abs() > 3.5
        )

    return result


def discover_climate_relationships(df):

    available = [
        column for column in CLIMATE_COLUMNS
        if column in df.columns
    ]

    return df[available].corr(method="spearman")


def calculate_long_term_trend(df):

    trends = {}

    for column in CLIMATE_COLUMNS:

        if column not in df.columns:
            continue

        values = df[column].dropna()

        if len(values) < 3:
            continue

        slope, intercept, low, high = theilslopes(
            values.to_numpy()
        )

        if slope > 0:
            direction = "Increasing"

        elif slope < 0:
            direction = "Decreasing"

        else:
            direction = "Stable"

        trends[column] = {
            "direction": direction,
            "monthly_change": round(float(slope), 5),
            "lower_slope": round(float(low), 5),
            "upper_slope": round(float(high), 5)
        }

    return trends


def compare_climate_fingerprints(df):

    comparison = {}

    for location in df["Location"].unique():

        location_data = df[
            df["Location"] == location
        ]

        comparison[location] = climate_fingerprint(
            location_data
        )

    return comparison
