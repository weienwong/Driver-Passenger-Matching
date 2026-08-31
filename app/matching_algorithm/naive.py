import math

from app.csv_parser import read_csv
from app.models import DataPoint, DataPointType, Match


def execute_naive_matching():
    reader = read_csv()
    drivers, passengers = validate_data(reader)
    matched_drivers_passengers = []
    for passenger in passengers:
        if not drivers:
            break

        match, matched_driver = find_drivers(passenger, drivers)
        matched_drivers_passengers.append(match)
        drivers.remove(
            matched_driver
        )  # 1 driver to 1 passenger so this driver can be removed from the list

    return matched_drivers_passengers


def validate_data(reader):
    drivers = []
    passengers = []
    for row in reader:
        record = DataPoint.model_validate(row)
        if record.type == DataPointType.DRIVER:
            drivers.append(record)
        elif record.type == DataPointType.PASSENGER:
            passengers.append(record)
    return drivers, passengers


def find_drivers(passenger, drivers):
    smallest_distance = math.inf
    matched_driver = None

    for driver in drivers:
        distance = calculate_distance(
            passenger.latitude,
            passenger.longitude,
            driver.latitude,
            driver.longitude,
        )
        if distance < smallest_distance:
            smallest_distance = distance
            matched_driver = driver
    match = Match(
        passenger_id=passenger.id,
        driver_id=matched_driver.id,
        distance=smallest_distance,
    )

    return match, matched_driver


def calculate_distance(
    passenger_latitude,
    passenger_longitude,
    driver_latitude,
    driver_longitude,
):
    return math.sqrt(
        (passenger_latitude - driver_latitude) ** 2
        + (passenger_longitude - driver_longitude) ** 2
    )
