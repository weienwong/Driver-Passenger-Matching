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


# happy path csv parser

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


# sad path csv parser

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


split_stub_1 = [
      model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b",
  model.PersonType.PASSENGER, 37.702532, -122.370635),
      model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3",
  model.PersonType.DRIVER, 37.735754, -122.476518),
      model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6",
  model.PersonType.DRIVER, 37.708259, -122.452757),
  ]

split_stub_order = [
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.729762, -122.374187),
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518),
    model.DataPoint("1ebb5085-357b-4d7b-b9f6-256401cfcc81", model.PersonType.PASSENGER, 37.779166, -122.487074),
    model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6", model.PersonType.DRIVER, 37.708259, -122.452757),
]

split_stub_all_passengers = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.729762, -122.374187),
    model.DataPoint("293f66ee-3fea-44f7-8724-99235314bdbd", model.PersonType.PASSENGER, 37.711135, -122.437101),
]

split_stub_all_drivers = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518),
    model.DataPoint("3276a226-53b5-4b7a-a082-29e42a29939b", model.PersonType.DRIVER, 37.824438, -122.459511),
    model.DataPoint("7c238612-82f2-44f7-9dde-799e8a133bd8", model.PersonType.DRIVER, 37.710373, -122.475081),
]

split_stub_single_passenger = [
    model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635),
]

split_stub_single_driver = [
    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518),
]

# happy path split by type

def test_split_by_type():
    assert csv_parser.split_by_type(split_stub_1) == ([model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b",
  model.PersonType.PASSENGER, 37.702532, -122.370635)
], [model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3",
  model.PersonType.DRIVER, 37.735754, -122.476518),
      model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6",
  model.PersonType.DRIVER, 37.708259, -122.452757)
])
    assert len(split_stub_1) == 3

def test_split_by_type_empty_returns_tupe_with_2_empty_arrays():
    assert csv_parser.split_by_type([]) == ([],[])


def test_split_by_type_returns_1_passenger_1_driver():
    parsed_set = csv_parser.split_by_type(csv_parser.parse(csv_happy_stub_2)) 
    assert parsed_set == ([model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635)],[model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518)])
    assert len(parsed_set[0]) == 1
    assert len(parsed_set[1])== 1


def test_split_by_type_returns_in_order():
    assert csv_parser.split_by_type(split_stub_order) == ([model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.729762, -122.374187),    model.DataPoint("1ebb5085-357b-4d7b-b9f6-256401cfcc81", model.PersonType.PASSENGER, 37.779166, -122.487074)], [    model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518),    model.DataPoint("f40284d5-ab7c-4678-8fef-f4d92e95b3f6", model.PersonType.DRIVER, 37.708259, -122.452757)])
    assert csv_parser.split_by_type(split_stub_all_passengers) == ([model.DataPoint("5b7ba204-5309-4e8b-a892-5138a6f3374b", model.PersonType.PASSENGER, 37.702532, -122.370635),
    model.DataPoint("1db4d345-d69a-45ab-8798-e708490b5228", model.PersonType.PASSENGER, 37.729762, -122.374187),
    model.DataPoint("293f66ee-3fea-44f7-8724-99235314bdbd", model.PersonType.PASSENGER, 37.711135, -122.437101)], [])
    assert csv_parser.split_by_type(split_stub_all_drivers) == ([], [model.DataPoint("ec85eb88-f29f-4a66-afe4-883396601cf3", model.PersonType.DRIVER, 37.735754, -122.476518),
    model.DataPoint("3276a226-53b5-4b7a-a082-29e42a29939b", model.PersonType.DRIVER, 37.824438, -122.459511),
    model.DataPoint("7c238612-82f2-44f7-9dde-799e8a133bd8", model.PersonType.DRIVER, 37.710373, -122.475081)])

def test_split_by_type_single_passenger():
    assert csv_parser.split_by_type(split_stub_single_passenger) == (split_stub_single_passenger,[])

def test_split_by_type_single_driver():
    assert csv_parser.split_by_type(split_stub_single_driver) == ([], split_stub_single_driver)
