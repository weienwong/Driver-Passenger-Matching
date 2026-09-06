"""Bounded nearest-driver matching backed by a Redis GEO index."""

import time
from collections.abc import Sequence
from uuid import UUID

from redis import Redis

from app.config import get_settings
from app.redis_client import get_redis_client
from app.schemas import MatchAssignment


def execute_bounded_naive_matching(
    passenger_latitude: float,
    passenger_longitude: float,
    ride_id: UUID,
) -> MatchAssignment | None:
    """Find and temporarily reserve the nearest available Redis GEO member."""

    settings = get_settings()
    redis_client = get_redis_client()

    for attempt in range(settings.matching_max_retries):
        drivers_available = redis_client.geosearch(
            "taxi_locations",
            longitude=passenger_longitude,
            latitude=passenger_latitude,
            radius=settings.matching_search_radius_km,
            unit="km",
            sort="ASC",
            count=settings.matching_candidate_count,
            withcoord=True,
            withdist=True,
        )
        match = find_and_reserve_driver(
            drivers_available=drivers_available,
            ride_id=ride_id,
            reservation_ttl_seconds=settings.matching_reservation_ttl_seconds,
            redis_client=redis_client,
        )

        if match is not None:
            return match

        if attempt < settings.matching_max_retries - 1:
            time.sleep(settings.matching_retry_seconds)

    return None


def find_and_reserve_driver(
    drivers_available: Sequence[tuple[str, float, tuple[float, float]]],
    ride_id: UUID,
    reservation_ttl_seconds: int,
    redis_client: Redis,
) -> MatchAssignment | None:
    """Reserve the first unreserved driver in the nearest-first candidate list."""

    for driver_id, distance_km, _ in drivers_available:
        reservation_key = f"matching:driver:{driver_id}:reservation"
        reservation_succeeded = redis_client.set(
            reservation_key,
            str(ride_id),
            nx=True,
            ex=reservation_ttl_seconds,
        )

        if reservation_succeeded:
            return MatchAssignment(
                ride_id=ride_id,
                driver_id=driver_id,
                distance_km=distance_km,
            )

    return None


if __name__ == "__main__":
    print(
        execute_bounded_naive_matching(
            passenger_latitude=1.282302,
            passenger_longitude=103.858528,
            ride_id=UUID("417ddc5d-e556-4d27-95dd-a34d84e46a50"),
        )
    )
