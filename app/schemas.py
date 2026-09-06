"""HTTP request and response schemas."""

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    """A request to find and temporarily reserve a nearby driver."""

    ride_id: UUID
    passenger_latitude: float = Field(ge=-90, le=90)
    passenger_longitude: float = Field(ge=-180, le=180)


class MatchAssignment(BaseModel):
    """A successful temporary driver reservation."""

    ride_id: UUID
    driver_id: str
    distance_km: float = Field(ge=0)


class MatchResponse(BaseModel):
    """The outcome of a matching attempt."""

    status: Literal["matched", "no_driver_available"]
    match: MatchAssignment | None = None


class ServiceStatus(BaseModel):
    """Liveness or readiness response returned by the service."""

    status: Literal["ok", "ready"]
