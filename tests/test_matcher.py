import pytest
from utils import matcher
from models import model
from utils import geo
import numpy as np

greedy_trap_passengers = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.75, -122.438639),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.75, -122.462497),
]

greedy_trap_drivers = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
    model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6", model.PersonType.DRIVER, 37.75, -122.404556),
]

GREEDY_TOTAL = 6.0931
HUNGARIAN_TOTAL = 4.0953


# the 2x2 trap plus an isolated pair 20km east, which greedy and hungarian agree on
# positions in km along lat 37.75: P2 -1.1, D1 0, P1 +1.0, D2 +4.0, D3 +20.0, P3 +20.5
greedy_trap_3x3_passengers = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.75, -122.438639),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.75, -122.462497),
    model.DataPoint("1ebb5085-357b-4d7b-b9f6-256401cfcc81", model.PersonType.PASSENGER, 37.75, -122.217097),
]

greedy_trap_3x3_drivers = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
    model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6", model.PersonType.DRIVER, 37.75, -122.404556),
    model.DataPoint("3276a226-53b5-4b7a-a082-29e42a29939b", model.PersonType.DRIVER, 37.75, -122.222778),
]

EXPECTED_MATRIX_3X3 = [[0.9989, 2.9966, 18.9786],
                       [1.0987, 5.0942, 21.0762],
                       [20.4770, 16.4815, 0.4995]]

# hungarian pairs P1-D2, P2-D1, P3-D3
GREEDY_TOTAL_3X3 = 6.5926
HUNGARIAN_TOTAL_3X3 = 4.5948
EXPECTED_PAIRS_3X3 = [(0, 1), (1, 0), (2, 2)]


single_passenger = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.75, -122.438639),
]

single_driver = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
]


# 3 passengers, 2 drivers: one passenger must go unmatched
more_passengers_than_drivers = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.75, -122.438639),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.75, -122.462497),
    model.DataPoint("1ebb5085-357b-4d7b-b9f6-256401cfcc81", model.PersonType.PASSENGER, 37.75, -122.404556),
]

# 3 drivers, 2 passengers: one driver must go unmatched
more_drivers_than_passengers = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
    model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6", model.PersonType.DRIVER, 37.75, -122.404556),
    model.DataPoint("3276a226-53b5-4b7a-a082-29e42a29939b", model.PersonType.DRIVER, 37.75, -122.375),
]


# a driver smuggled into the passenger list, and vice versa
passengers_with_a_driver = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.75, -122.438639),
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
]

drivers_with_a_passenger = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.75, -122.45),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.75, -122.462497),
]


# expected cost matrices, rows = passengers, cols = drivers
EXPECTED_MATRIX_2X2 = [[0.9989, 2.9966],
                       [1.0987, 5.0942]]

EXPECTED_MATRIX_1X1 = [[0.9989]]

# more_passengers_than_drivers x greedy_trap_drivers
EXPECTED_MATRIX_3X2 = [[0.9989, 2.9966],
                       [1.0987, 5.0942],
                       [3.9955, 0.0]]

# greedy_trap_passengers x more_drivers_than_passengers
EXPECTED_MATRIX_2X3 = [[0.9989, 2.9966, 5.5952],
                       [1.0987, 5.0942, 7.6928]]


def test_populate_matrix_2x2():
    matrix = matcher.populate_matrix(greedy_trap_passengers, greedy_trap_drivers) 
    assert matrix == pytest.approx(np.array(EXPECTED_MATRIX_2X2), abs=1e-4)
    assert len(matrix) == len(greedy_trap_passengers)
    assert len(matrix[0]) == len(greedy_trap_drivers)


def test_populate_matrix_1x1():
    matrix = matcher.populate_matrix(single_passenger, single_driver) 
    assert matrix == pytest.approx(np.array(EXPECTED_MATRIX_1X1), abs=1e-4)
    assert len(matrix) == len(single_passenger)
    assert len(matrix[0]) == len(single_driver)

def test_populate_matrix_3x2():
    matrix = matcher.populate_matrix(more_passengers_than_drivers, greedy_trap_drivers) 
    assert matrix == pytest.approx(np.array(EXPECTED_MATRIX_3X2), abs=1e-4)
    assert len(matrix) == len(more_passengers_than_drivers)
    assert len(matrix[0]) == len(greedy_trap_drivers)

def test_populate_matrix_2x3():
    matrix = matcher.populate_matrix(greedy_trap_passengers, more_drivers_than_passengers) 
    assert matrix == pytest.approx(np.array(EXPECTED_MATRIX_2X3), abs=1e-4)
    assert len(matrix) == len(greedy_trap_passengers)
    assert len(matrix[0]) == len(more_drivers_than_passengers)

# happy path match

def total_distance(results):
    return sum(geo.haversine_dist(p, d) for p, d in results)

def test_match_2x2_finds_hungarian_not_greedy():
    results = matcher.match(greedy_trap_passengers, greedy_trap_drivers)
    assert len(results) == 2
    assert total_distance(results) == pytest.approx(HUNGARIAN_TOTAL, abs=1e-4)
    assert total_distance(results) != pytest.approx(GREEDY_TOTAL, abs=1e-4)

def test_match_3x3_finds_hungarian_not_greedy():
    results = matcher.match(greedy_trap_3x3_passengers, greedy_trap_3x3_drivers)
    assert len(results) == 3
    assert total_distance(results) == pytest.approx(HUNGARIAN_TOTAL_3X3, abs=1e-4)
    assert total_distance(results) != pytest.approx(GREEDY_TOTAL_3X3, abs=1e-4)

def test_match_3x3_pairs_the_expected_people():
    results = matcher.match(greedy_trap_3x3_passengers, greedy_trap_3x3_drivers)
    for (passenger, driver), (i, j) in zip(results, EXPECTED_PAIRS_3X3):
        assert passenger is greedy_trap_3x3_passengers[i]
        assert driver is greedy_trap_3x3_drivers[j]

def test_match_returns_datapoints_not_indices():
    results = matcher.match(single_passenger, single_driver)
    passenger, driver = results[0]
    assert passenger.type == model.PersonType.PASSENGER
    assert driver.type == model.PersonType.DRIVER



def test_match_3x2_returns_two_pairs():
    results = matcher.match(more_passengers_than_drivers, greedy_trap_drivers)
    assert len(results) == min(len(more_passengers_than_drivers), len(greedy_trap_drivers))

def test_match_2x3_returns_two_pairs():
    results = matcher.match(greedy_trap_passengers, more_drivers_than_passengers)
    assert len(results) == min(len(greedy_trap_passengers), len(more_drivers_than_passengers))

def test_match_never_reuses_a_driver():
    results = matcher.match(greedy_trap_passengers, more_drivers_than_passengers)
    matched = [driver.UUID for _passenger, driver in results]
    assert len(matched) == len(set(matched))

def test_match_never_reuses_a_passenger():
    results = matcher.match(more_passengers_than_drivers, greedy_trap_drivers)
    matched = [passenger.UUID for passenger, _driver in results]
    assert len(matched) == len(set(matched))


# sad path match

def test_match_rejects_empty_passengers():
    with pytest.raises(TypeError):
        matcher.match([], greedy_trap_drivers)

def test_match_rejects_empty_drivers():
    with pytest.raises(TypeError):
        matcher.match(greedy_trap_passengers, [])

def test_match_rejects_both_empty():
    with pytest.raises(TypeError):
        matcher.match([], [])

def test_match_rejects_driver_in_passenger_list():
    with pytest.raises(TypeError):
        matcher.match(passengers_with_a_driver, greedy_trap_drivers)

def test_match_rejects_passenger_in_driver_list():
    with pytest.raises(TypeError):
        matcher.match(greedy_trap_passengers, drivers_with_a_passenger)
