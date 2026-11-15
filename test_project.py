from modules.nasa_data import collect_multiple_locations

locations = [
    {
        "name": "Bengaluru",
        "latitude": 12.9716,
        "longitude": 77.5946
    },
    {
        "name": "Chennai",
        "latitude": 13.0827,
        "longitude": 80.2707
    }
]

print("\n===================================")
print("       EARTHSCOPE AI")
print("   NASA DATA COLLECTION TEST")
print("===================================")

try:

    climate_data = collect_multiple_locations(
        locations,
        start_year=2001,
        end_year=2025
    )

    print("\nDATA COLLECTION SUCCESSFUL!")

    print("\nFirst five records:")
    print(climate_data.head())

    print("\nAvailable columns:")
    print(climate_data.columns.tolist())

    print("\nRecords collected:")
    print(len(climate_data))

    print("\nLocations:")
    print(climate_data["Location"].unique())

except Exception as error:

    print("\nDATA COLLECTION FAILED!")
    print("Error:", error)
