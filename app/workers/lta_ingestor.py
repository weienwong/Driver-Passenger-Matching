import time

from app.integrations.lta_client import get_lta_taxi_availability
from app.integrations.redis_geo import DRIVER_GEO_KEY, redis_client, replace_driver_locations

POLLING_INTERVAL = 300  # 5 mins


def run_poller():
    while True:
        try:
            snapshot = get_lta_taxi_availability()
            store_coordinates_to_redis(snapshot)
            count = redis_client.zcard(DRIVER_GEO_KEY)
            print(f"{count} Taxi locations loaded into Redis")
        except Exception as e:
            print(f"Something went wrong: {e}")
        print(f"Sleeping for {POLLING_INTERVAL} seconds")
        time.sleep(POLLING_INTERVAL)


def store_coordinates_to_redis(snapshot):
    return replace_driver_locations(snapshot)


if __name__ == "__main__":
    run_poller()
