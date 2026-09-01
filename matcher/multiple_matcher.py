"""
Implementation of Matching Algorithm (Unoptimized)
- Assumes using type separated hashmaps (driver and passenger)
- Matches multiple passengers to driver
"""
import pygeohash as pgh

PRECISION = 6
MAX_DISTANCE_IN_M = 1000

def nearby_drivers(drivers, passengers, max_distance_in_m = MAX_DISTANCE_IN_M):
    matches = []

    for driver in drivers:
        for passenger in passengers:
            distance = pgh.geohash_haversine_distance(
                pgh.encode(driver["lat"], driver["lng"], PRECISION),
                pgh.encode(passenger["lat"], passenger["lng"], PRECISION)
            )

            if distance <= max_distance_in_m:
                matches.append((driver["uuid"], passenger["uuid"]))
    return matches