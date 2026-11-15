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
    },
    {
        "name": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777
    },
    {
        "name": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090
    },
    {
        "name": "Hyderabad",
        "latitude": 17.3850,
        "longitude": 78.4867
    },
    {
        "name": "Kolkata",
        "latitude": 22.5726,
        "longitude": 88.3639
    },
    {
        "name": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567
    },
    {
        "name": "Jaipur",
        "latitude": 26.9124,
        "longitude": 75.7873
    },
    {
        "name": "Kochi",
        "latitude": 9.9312,
        "longitude": 76.2673
    },
    {
        "name": "Ahmedabad",
        "latitude": 23.0225,
        "longitude": 72.5714
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
