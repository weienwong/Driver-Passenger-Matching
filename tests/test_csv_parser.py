import pytest
from utils import csv_parser
from models import model

csv_happy_stub_1 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532,-122.370635"
csv_happy_stub_2 = """5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532,-122.370635
ec85eb88-f29f-4a66-afe4-883396601cf3,driver,37.735754,-122.476518"""
csv_happy_stub_3 = """5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532,-122.370635

ec85eb88-f29f-4a66-afe4-883396601cf3,driver,37.735754,-122.476518"""
csv_happy_stub_4 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,PASSENGER,37.702532,-122.370635"
csv_happy_stub_5 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,PaSsengeR,37.702532,-122.370635"
csv_happy_stub_6 = "5b7ba204-5309-4e8b-a892-5138a6f3374b, passenger, 37.702532, -122.370635"
csv_happy_stub_7 = "       "
csv_happy_stub_8 = "\n\n\n"


csv_sad_stub_1 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,pasenger,37.702532,-122.370635"
csv_sad_stub_2 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532"
csv_sad_stub_3 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532,-122.370635,-122.370635"
csv_sad_stub_4 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.70253a,-122.370635"
csv_sad_stub_5 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,passenger,37.702532,-122.37063b"
csv_sad_stub_6 = ",passenger,37.702532,-122.370635"
csv_sad_stub_7 = "5b7ba204-5309-4e8b-a892-5138a6f3374b,,37.702532,-122.370635"
csv_sad_stub_8 = "banana,passenger,37.702532,-122.370635"

def test_csv_parser_says_hello_world():
    assert csv_parser.hello() == "Hello, world!"


# happy path

def test_csv_parser_returns_object():
    assert csv_parser.parse(csv_happy_stub_1) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635)]

def test_csv_parser_returns_objects():
    assert csv_parser.parse(csv_happy_stub_2) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635), model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518)]
    assert len(csv_parser.parse(csv_happy_stub_2)) == 2

def test_csv_parser_returns_objects_despite_emptylines():
    assert csv_parser.parse(csv_happy_stub_3) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635), model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518)]
    assert len(csv_parser.parse(csv_happy_stub_3)) == 2

def test_csv_parser_returns_empty_array_on_empty_csv():
    assert csv_parser.parse("") == []
    assert len(csv_parser.parse("")) == 0

def test_csv_parser_returns_object_despite_upper_lower_case_person_type():
    assert csv_parser.parse(csv_happy_stub_4) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635)]
    assert csv_parser.parse(csv_happy_stub_5) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635)]

def test_csv_parser_returns_object_despite_space_after_coma():
    assert csv_parser.parse(csv_happy_stub_6) == [model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635)]

def test_csv_parser_returns_empty_array_on_csv_with_empty_spaces():
    assert csv_parser.parse(csv_happy_stub_7) == []
    assert len(csv_parser.parse(csv_happy_stub_7)) == 0

def test_csv_parser_returns_empty_array_on_csv_with_empty_lines():
    assert csv_parser.parse(csv_happy_stub_8) == []
    assert len(csv_parser.parse(csv_happy_stub_8)) == 0


# sad path

def test_csv_parser_rejects_typo_on_enum_values():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_1)

def test_csv_parser_rejects_insufficient_arguments():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_2)

def test_csv_parser_rejects_too_many_arguments():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_3)

def test_csv_parser_rejects_non_numeric_string_for_lat():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_4)


def test_csv_parser_rejects_non_numeric_string_for_lng():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_5)

def test_csv_parser_rejects_missing_uuid():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_6)

def test_csv_parser_rejects_missing_person_type():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_7)

def test_csv_parser_rejects_invalid_uuid():
    with pytest.raises(ValueError):
        csv_parser.parse(csv_sad_stub_8)

