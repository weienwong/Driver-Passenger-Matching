from fastapi import FastAPI, HTTPException, status
from redis.exceptions import RedisError

from app.matching_algorithm.bounded_naive import execute_bounded_naive_matching
from app.redis_client import get_redis_client
from app.schemas import MatchRequest, MatchResponse, ServiceStatus

app = FastAPI(title="Driver-Passenger Matching Service")


@app.get("/health")
def healthcheck() -> ServiceStatus:
    """Report whether the API process is running."""

    return ServiceStatus(status="ok")


@app.get("/ready", response_model=ServiceStatus)
def readiness() -> ServiceStatus:
    """Report whether dependencies required for matching are reachable."""

    try:
        get_redis_client().ping()
    except RedisError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis is unavailable",
        ) from error

    return ServiceStatus(status="ready")


@app.post("/api/v1/matches", response_model=MatchResponse)
def create_match(request: MatchRequest) -> MatchResponse:
    """Find and temporarily reserve a nearby driver for one ride request."""

    match = execute_bounded_naive_matching(
        passenger_latitude=request.passenger_latitude,
        passenger_longitude=request.passenger_longitude,
        ride_id=request.ride_id,
    )

    if match is None:
        return MatchResponse(status="no_driver_available")

    return MatchResponse(status="matched", match=match)
