from matcher.single_matcher import match_single_driver

def test_match_single_driver():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674},{"uuid": "d2", "lat": 1.293625, "lng": 103.851986},{"uuid": "d3", "lat": 1.298037, "lng": 103.849573}]
    passengers = [{"uuid": "p1", "lat": 1.292759, "lng": 103.857702}, {"uuid": "p2", "lat": 1.292759, "lng": 103.857702}]

    result = match_single_driver(drivers, passengers)

    assert result == [('d1', 'p1')]

def test_matched_drivers_removed_from_list():
    drivers = [{"uuid": "d1", "lat": 1.294400, "lng": 103.858674}]
    passengers = [{"uuid": "p1", "lat": 1.292759, "lng": 103.857702}, {"uuid": "p2", "lat": 1.292759, "lng": 103.857702}]

    result = match_single_driver(drivers, passengers)

    assert result == [("d1", "p1")]
