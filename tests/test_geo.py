import pytest
from utils import geo
from models import model
import uuid

passenger = model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, "", "")
driver = model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, "", "")

known_haversine_distances_stub = [
    [
        ["1.3501", "103.994"],
        ["1.2828", "103.8609"],
        16.62,
        "Changi Airport to Marina Bay Sands"
    ],
    [
        ["1.4428", "103.7695"],
        ["1.3490", "103.6366"],
        18.08,
        "Woodlands Checkpoint to Tuas Checkpoint"
    ],
    [
        ["1.2543", "103.8211"],
        ["1.4184", "103.9189"],
        21.24,
        "Sentosa to Punggol Point Jetty"
    ],
    [
        ["51.4700", "-0.4543"],
        ["40.6413", "-73.7781"],
        5540.01,
        "LHR to JFK Airport"
    ],
    [
        ["1.3501", "103.9944"],
        ["-33.9461", "151.1772"],
        6293.42,
        "Changi Airport to Sydney Kingsford Smith Airport"
    ],
    [
        ["35.5494", "139.7798"],
        ["-33.9461", "151.1772"],
        7817.84,
        "Haneda to Sydney Kingsford Smith Airport"
    ], 
    [
        ["1.3501", "103.994"],
        ["1.3510", "103.994"],
        0.10,
        "~100m apart, same longitude"
    ],
    [
        ["1.3501", "103.994"],
        ["1.35019", "103.994"],
        0.01,
        "~10m apart, same longitude"
    ],
    [
        ["0", "0"],
        ["0", "180"],
        20015.09,
        "Antipodal points on equator (max possible distance)"
    ],
]

def insert_distance_helper(idx): 
    stub = known_haversine_distances_stub[idx]
    passenger.lat = stub[0][0]
    passenger.lng = stub[0][1]
    driver.lat = stub[1][0]
    driver.lng = stub[1][1]
    expected_dist = stub[2]
    description = stub[3]
    return [passenger, driver, expected_dist, description]

# happy path
@pytest.mark.parametrize("idx", range(len(known_haversine_distances_stub)))
def test_haversine_dist_returns_correctly(idx):
    passenger, driver, expected_dist, description = insert_distance_helper(idx)
    assert geo.haversine_dist(passenger, driver) == pytest.approx(expected_dist, abs=1.0)

@pytest.mark.parametrize("idx", range(len(known_haversine_distances_stub)))
def test_haversine_dist_reversed_order_returns_same_answer(idx):
    passenger, driver, expected_dist, description = insert_distance_helper(idx)
    assert geo.haversine_dist(passenger, driver) == pytest.approx(expected_dist, abs=1.0)
    assert geo.haversine_dist(driver, passenger) == pytest.approx(expected_dist, abs=1.0)

def test_haversine_dist_returns_zero_for_same_lat_lng():
    passenger, driver, expected_dist, description = insert_distance_helper(1)
    driver.lat = passenger.lat
    driver.lng = passenger.lng
    assert geo.haversine_dist(passenger, driver) == pytest.approx(0, abs=1e-6)

def test_haversine_dist_does_not_raise_for_lat_90():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lat = "90"
    geo.haversine_dist(passenger, driver)  

def test_haversine_dist_does_not_raise_for_lat_neg_90():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lat = "-90"
    geo.haversine_dist(passenger, driver)

def test_haversine_dist_does_not_raise_for_lng_180():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lng = "180"
    geo.haversine_dist(passenger, driver)

def test_haversine_dist_does_not_raise_for_lng_neg_180():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lng = "-180"
    geo.haversine_dist(passenger, driver)
# sad path

def test_haversine_dist_does_not_process_2_passengers():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    with pytest.raises(TypeError):
        geo.haversine_dist(passenger, passenger)

def test_haversine_dist_does_not_process_2_drivers():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    with pytest.raises(TypeError):
        geo.haversine_dist(driver, driver)

def test_haversine_dist_raise_ValueError_for_empty_string_lat():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lat=""
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_lat_greater_than_90():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lat="90.01"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_lat_lesser_than_neg_90():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lat="-90.01"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_lng_greater_than_180():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lng="180.01"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_lng_lesser_than_neg_180():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    passenger.lng="-180.01"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_non_numerical_lat():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    driver.lat="1a"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_ValueError_for_non_numerical_lng():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    driver.lng="2b"
    with pytest.raises(ValueError):
        geo.haversine_dist(passenger,driver)

def test_haversine_dist_raise_TypeError_for_nan_lat():
    passenger, driver, expected_dist, description = insert_distance_helper(0)
    driver.lat="nan"
    with pytest.raises(TypeError):
        geo.haversine_dist(passenger,driver)
