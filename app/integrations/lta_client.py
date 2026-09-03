import requests

LTA_API_URL = "https://api.data.gov.sg/v1/transport/taxi-availability"


def get_lta_taxi_availability():
    response = requests.get(LTA_API_URL, timeout=10)

    if response.ok:
        data = response.json()
        feature = data["features"][0]

        taxi_count = feature["properties"]["taxi_count"]
        timestamp = feature["properties"]["timestamp"]
        coordinates = feature["geometry"]["coordinates"]
        print(f"Available taxis: {taxi_count}")
        print(f"Timestamp: {timestamp}")
        print(f"Number of coordinates: {len(coordinates)}")
        return coordinates
    else:
        print(f"Request failed: {response.status_code}")
