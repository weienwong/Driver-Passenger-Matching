from uuid import UUID

from fastapi import FastAPI, Query

from app.integrations.redis_geo import (
    find_nearby_drivers,
    update_driver_location,
)
from app.matching_algorithm.naive import execute_static_naive_matching

app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"message": "healthy"}


@app.put("/drivers/{driver_id}/location")
def update_location(
    driver_id: UUID,
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
):
    update_driver_location(str(driver_id), longitude, latitude)
    return {"driver_id": driver_id, "latitude": latitude, "longitude": longitude}


@app.get("/drivers/nearby")
def nearby_drivers(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius_km: float = Query(default=5.0, gt=0),
):
    return {
        "data": find_nearby_drivers(longitude, latitude, radius_km),
    }


@app.get("/match")
def matching_service():
    matches = execute_static_naive_matching
    return {"data": matches}
