import requests

from app.config import get_settings


def get_lta_taxi_availability():
    """Fetch the latest available-taxi coordinates from the LTA data source."""

    settings = get_settings()
    response = requests.get(
        settings.lta_api_url,
        timeout=settings.lta_request_timeout_seconds,
    )
    response.raise_for_status()
    data = response.json()
    feature = data["features"][0]

    taxi_count = feature["properties"]["taxi_count"]
    timestamp = feature["properties"]["timestamp"]
    coordinates = feature["geometry"]["coordinates"]
    print(f"Available taxis: {taxi_count}")
    print(f"Timestamp: {timestamp}")
    print(f"Number of coordinates: {len(coordinates)}")
    return coordinates
