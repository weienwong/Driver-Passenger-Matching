from matcher.multiple_matcher import nearby_drivers

def test_nearby_drivers():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674}]
    passengers = [{"uuid": "p1", "lat": 1.292759, "lng": 103.857702}]

    result = nearby_drivers(drivers, passengers)

    assert result == [("d1","p1")]


def test_excludes_drivers_outside_max_distance():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674}]
    passengers = [{"uuid": "p1", "lat": 1.294433, "lng": 103.852581}]

    result = nearby_drivers(drivers, passengers)

    assert result == []

def test_no_drivers_returns_empty():
    drivers = []
    passengers = [{"uuid": "p1", "lat": 1.294433, "lng": 103.852581}]

    result = nearby_drivers(drivers, passengers)

    assert result == []

def test_no_passengers_returns_empty():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674}]
    passengers = []

    result = nearby_drivers(drivers, passengers)

    assert result == []

## This naturally matches one driver to multiple passengers
def test_multiple_drivers_passengers():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674},{"uuid": "d2", "lat": 1.293625, "lng": 103.851986},{"uuid": "d3", "lat": 1.298037, "lng": 103.849573}]
    passengers = [{"uuid": "p1", "lat": 1.292759, "lng": 103.857702}, {"uuid": "p2", "lat": 1.292759, "lng": 103.857702}]

    result = nearby_drivers(drivers, passengers)

    assert result == [('d1', 'p1'), ('d1', 'p2')]
