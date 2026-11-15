import requests
import pandas as pd
import json
import re

from pathlib import Path


NASA_API = (
    "https://power.larc.nasa.gov/api/"
    "temporal/monthly/point"
)


CLIMATE_PARAMETERS = {
    "T2M": "Temperature",
    "PRECTOTCORR": "Rainfall",
    "RH2M": "Humidity",
    "WS10M": "Wind Speed"
}


def fetch_climate_data(
    location,
    latitude,
    longitude,
    start_year=2001,
    end_year=2025
):

    print(f"\nCollecting NASA data for {location}...")

    parameters = ",".join(CLIMATE_PARAMETERS.keys())

    request_parameters = {
        "parameters": parameters,
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_year,
        "end": end_year,
        "format": "JSON"
    }

    try:

        response = requests.get(
            NASA_API,
            params=request_parameters,
            timeout=120
        )

        response.raise_for_status()

        nasa_response = response.json()

        parameter_data = nasa_response["properties"]["parameter"]

        climate_records = {}

        for parameter, values in parameter_data.items():

            if parameter not in CLIMATE_PARAMETERS:
                continue

            for date, value in values.items():

                date = str(date).strip()

                if not re.fullmatch(r"\d{6}", date):
                    continue

                climate_records.setdefault(date, {})

                if value == -999:
                    value = None

                climate_records[date][
                    CLIMATE_PARAMETERS[parameter]
                ] = value

        if not climate_records:
            raise ValueError(
                "No valid climate records received from NASA."
            )

        df = pd.DataFrame.from_dict(
            climate_records,
            orient="index"
        )

        # Convert NASA YYYYMM dates into datetime

        df.index = pd.to_datetime(
            df.index.astype(str) + "01",
            format="%Y%m%d",
            errors="coerce"
        )

        df.index.name = "Date"

        df = df.loc[df.index.notna()]

        if df.empty:
            raise ValueError(
                "NASA returned no valid date records."
            )

        df = df.sort_index()

        # Add location information

        df["Location"] = location
        df["Latitude"] = latitude
        df["Longitude"] = longitude

        # Create folders

        output_folder = Path("data/processed")
        raw_folder = Path("data/raw")

        output_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        raw_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_name = "".join(
            character if character.isalnum() else "_"
            for character in location
        ).lower()

        # Save processed CSV

        df.to_csv(
            output_folder / f"{safe_name}_climate.csv"
        )

        # Save original NASA JSON

        with open(
            raw_folder / f"{safe_name}_raw.json",
            "w"
        ) as file:

            json.dump(
                nasa_response,
                file,
                indent=4
            )

        print(
            f"SUCCESS: {len(df)} records collected "
            f"for {location}."
        )

        return df

    except Exception as error:

        raise RuntimeError(
            f"Failed to collect NASA data for {location}: {error}"
        ) from error


def collect_multiple_locations(
    locations,
    start_year=2001,
    end_year=2025
):

    all_data = []

    for location in locations:

        climate_data = fetch_climate_data(
            location["name"],
            location["latitude"],
            location["longitude"],
            start_year,
            end_year
        )

        all_data.append(climate_data)

    if not all_data:
        raise ValueError(
            "No locations were provided."
        )

    combined_data = pd.concat(all_data)

    combined_data = combined_data.sort_index()

    output_folder = Path("data/processed")

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    combined_data.to_csv(
        output_folder / "multi_location_climate.csv"
    )

    print("\nAll locations collected successfully!")

    return combined_data