from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class DataPointType(str, Enum):
    DRIVER = "driver"
    PASSENGER = "passenger"


class DataPoint(BaseModel):
    id: UUID
    type: DataPointType
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class Match(BaseModel):
    passenger_id: UUID
    driver_id: UUID
    distance: float


class MatchingAlgorithm(str, Enum):
    NAIVE = "naive"
