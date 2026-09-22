from models import model
import uuid as Uuid

def hello():
    return "Hello, world!"

def csv_file_handler(pathToCsv, has_header):
    with open(pathToCsv) as f:
        lines = f.read().splitlines()
    if has_header:
        lines = lines[1:]
    return "\n".join(lines)

def parse(csv_text):
    rows = []
    for line in csv_text.strip().splitlines():
        if line.strip() == "":
            continue
        rows.append(line.split(","))
    data_points = []
    for row in rows:
        try:
            uuid, type_str, lat, lng = row
        except ValueError:
            raise ValueError(f"malformed row, expected 4 fields: {row!r}")
        uuid = uuid.strip()
        if uuid == "":
            raise ValueError()
        try:
            Uuid.UUID(uuid)
        except ValueError:
            raise ValueError()
        try:
            person_type = model.PersonType(type_str.lower().strip())
        except ValueError:
            raise ValueError(f"invalid type {type_str!r} for row {row}")
        try:
            lat_float = float(lat.strip())
        except ValueError:
            raise ValueError(f"malformed lat, expected numeric string: {row!r}")
        try:
            lng_float = float(lng.strip())
        except ValueError:
            raise ValueError(f"malformed lng, expected numeric string: {row!r}")
        data_points.append(model.DataPoint(uuid, person_type, lat_float, lng_float))
    return data_points


def split_by_type(data_points): 
    if len(data_points) == 0: 
        return ([], []) 
    passengers = []
    drivers = []
    for dp in data_points:
        if dp.type == model.PersonType.PASSENGER:
            passengers.append(dp)
        elif dp.type == model.PersonType.DRIVER:
            drivers.append(dp)
    return (passengers, drivers)


