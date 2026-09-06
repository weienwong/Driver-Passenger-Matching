import time

from redis.exceptions import RedisError
from requests import RequestException

from app.config import get_settings
from app.integrations.lta_client import get_lta_taxi_availability
from app.redis_client import get_redis_client


def run_poller():
    """Continuously refresh the Redis GEO index from LTA taxi locations."""

    settings = get_settings()
    redis_client = get_redis_client()

    while True:
        try:
            snapshot = get_lta_taxi_availability()
            store_coordinates_to_redis(snapshot, redis_client)
            count = redis_client.zcard("taxi_locations")
            print(f"{count} Taxi locations loaded into Redis")
        except (
            IndexError,
            KeyError,
            RedisError,
            RequestException,
            ValueError,
        ) as error:
            print(f"LTA ingestion failed: {error}")
        print(f"Sleeping for {settings.polling_interval_seconds} seconds")
        time.sleep(settings.polling_interval_seconds)


def store_coordinates_to_redis(snapshot, redis_client):
    # Batch the requests to perform faster writes to redis
    settings = get_settings()
    pipe = redis_client.pipeline()

    # Replace the previous snapshot with the newly fetched coordinates.
    pipe.delete("taxi_locations")

    for index, coordinates in enumerate(snapshot):
        longitude = coordinates[0]
        latitude = coordinates[1]
        driver_index = "driver-" + str(index)
        pipe.geoadd("taxi_locations", [longitude, latitude, driver_index])
    pipe.expire("taxi_locations", settings.redis_snapshot_ttl_seconds)
    pipe.execute()


if __name__ == "__main__":
    run_poller()
