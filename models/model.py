from dataclasses import dataclass
from enum import Enum

class PersonType(Enum):
    PASSENGER = "passenger"
    DRIVER = "driver"

@dataclass
class DataPoint:
    UUID: str
    type: PersonType
    lat: str
    lng: str
