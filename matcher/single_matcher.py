"""
Implementation of Matching Algorithm (Greedy)
- Assumes using type separated hashmaps (driver and passenger)
- Matches closest driver to passenger
"""
import pygeohash as pgh

PRECISION = 6
MAX_DISTANCE_IN_M = 1000

def match_single_driver(drivers,passengers,max_distance_in_m = MAX_DISTANCE_IN_M):
    available_drivers = list(drivers)
    matches = []

    for passenger in passengers:
        selected_driver = None
        best_distance = float('inf')

        for driver in available_drivers:
            distance = pgh.geohash_haversine_distance(
                pgh.encode(driver["lat"], driver["lng"], PRECISION),
                pgh.encode(passenger["lat"], passenger["lng"], PRECISION)
            )

            if distance < max_distance_in_m and distance < best_distance:
                best_distance = distance
                selected_driver = driver

        if selected_driver:
            matches.append((selected_driver["uuid"], passenger["uuid"]))
            available_drivers.remove(selected_driver)
    return matches
