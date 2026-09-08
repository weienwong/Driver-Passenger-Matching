import os

import redis
from dotenv import load_dotenv


load_dotenv()

DRIVER_GEO_KEY = "drivers:location"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def replace_driver_locations(locations, ttl_seconds: int = 300):
    """Replace the current GEO snapshot with a batch of indexed locations."""
    pipeline = redis_client.pipeline()
    pipeline.delete(DRIVER_GEO_KEY)

    for index, (longitude, latitude) in enumerate(locations):
        pipeline.geoadd(
            DRIVER_GEO_KEY,
            {f"lta-{index}": (longitude, latitude)},
        )

    pipeline.expire(DRIVER_GEO_KEY, ttl_seconds)
    pipeline.execute()
    return len(locations)


def update_driver_location(driver_id: str, longitude: float, latitude: float):
    """Add or update a driver's location in Redis's geospatial index."""
    return redis_client.geoadd(
        DRIVER_GEO_KEY,
        {driver_id: (longitude, latitude)},
    )


def find_nearby_drivers(
    longitude: float,
    latitude: float,
    radius_km: float = 5.0,
):
    """Return nearby drivers ordered from closest to furthest away."""
    results = redis_client.geosearch(
        name=DRIVER_GEO_KEY,
        longitude=longitude,
        latitude=latitude,
        radius=radius_km,
        unit="km",
        withdist=True,
        withcoord=True,
        sort="ASC",
    )

    return [
        {
            "driver_id": driver_id,
            "distance_km": float(distance_km),
            "longitude": float(coordinates[0]),
            "latitude": float(coordinates[1]),
        }
        for driver_id, distance_km, coordinates in results
    ]