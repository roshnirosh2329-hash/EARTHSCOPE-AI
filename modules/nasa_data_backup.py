import requests
import pandas as pd
import json
from pathlib import Path

NASA_API = "https://power.larc.nasa.gov/api/temporal/monthly/point"

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

    print(f"Collecting NASA data for {location}...")

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

        for date, value in values.items():

            if not date.isdigit() or len(date) != 6:
                continue

            climate_records.setdefault(date, {})

            if value == -999:
                value = None

            climate_records[date][
                CLIMATE_PARAMETERS[parameter]
            ] = value

    df = pd.DataFrame.from_dict(
        climate_records,
        orient="index"
    )

    if df.empty:
        raise ValueError("No climate records received from NASA.")
    # Convert NASA date values into proper datetime format
    parsed_dates = []

    for date_value in df.index:
        date_text = 
    str(date_value).strip()

        parsed = pd.to_datetime(
            date_text,
            format="%Y%m",
            errors="coerce"
        )  

        if pd.isna(parsed):
            parsed = pd.to_datetime(
                date_text,
                errors="coerce"
            )

        if pd.isna(parsed):
            raise 
    ValueError(f"Invalid NASA date 
    format: {date_text}")

        parsed_dates.append(parsed)

     df.index =
     pd.DatetimeIndex(parsed_dates)
     df.index.name = "Date"

     df = df.sort_index()

      df["Location"] = location
      df["Latitude"] = latitude
      df["Longitude"] = longitude

    output_folder = Path("data/processed")
    raw_folder = Path("data/raw")

    output_folder.mkdir(parents=True, exist_ok=True)
    raw_folder.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in location
    ).lower()

    df.to_csv(
        output_folder / f"{safe_name}_climate.csv"
    )

    with open(
        raw_folder / f"{safe_name}_raw.json",
        "w"
    ) as file:

        json.dump(
            nasa_response,
            file,
            indent=4
        )

    print(f"Successfully collected {len(df)} records.")

    return df


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
        raise ValueError("No locations were provided.")

    combined_data = pd.concat(all_data)

    combined_data.to_csv(
        "data/processed/multi_location_climate.csv"
    )

    return combined_data
