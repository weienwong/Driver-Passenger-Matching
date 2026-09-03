import os
import time
import redis
from dotenv import load_dotenv
from app.integrations.lta_client import get_lta_taxi_availability

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

POLLING_INTERVAL = 300  # 5 mins


def run_poller():
    while True:
        try:
            snapshot = get_lta_taxi_availability()
            store_coordinates_to_redis(snapshot)
            count = r.zcard("taxi_locations")
            print(f"{count} Taxi locations loaded into Redis")
        except Exception as e:
            print(f"Something went wrong: {e}")
        print(f"Sleeping for {POLLING_INTERVAL} seconds")
        time.sleep(POLLING_INTERVAL)


def store_coordinates_to_redis(snapshot):
    # Batch the requests to perform faster writes to redis
    pipe = r.pipeline()

    # Delete previous coordinates loaded 5 minutes ago.
    pipe.delete("taxi_locations")

    for index, coordinates in enumerate(snapshot):
        longitude = coordinates[0]
        lattitude = coordinates[1]
        pipe.geoadd("taxi_locations", [longitude, lattitude, index])
    pipe.expire("taxi_locations", 300)
    pipe.execute()


if __name__ == "__main__":
    run_poller()
