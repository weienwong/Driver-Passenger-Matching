#!/usr/bin/env python3
"""Generate sample driver/passenger geolocation data scattered around a city.

Usage:
    python scripts/generate_geolocation_data.py \
        --num-drivers 50 --num-passengers 50 \
        --output data/geolocations.csv --seed 42
"""

import argparse
import csv
import random
import uuid

# Roughly bounds San Francisco proper.
CITY_BOUNDS = {
    "min_lat": 37.70,
    "max_lat": 37.83,
    "min_lng": -122.51,
    "max_lng": -122.36,
}


def random_point(bounds: dict) -> tuple[float, float]:
    lat = random.uniform(bounds["min_lat"], bounds["max_lat"])
    lng = random.uniform(bounds["min_lng"], bounds["max_lng"])
    return round(lat, 6), round(lng, 6)


def generate_rows(num_drivers: int, num_passengers: int, bounds: dict) -> list[dict]:
    rows = []
    for role, count in (("driver", num_drivers), ("passenger", num_passengers)):
        for _ in range(count):
            lat, lng = random_point(bounds)
            rows.append(
                {
                    "id": str(uuid.uuid4()),
                    "type": role,
                    "latitude": lat,
                    "longitude": lng,
                }
            )
    random.shuffle(rows)
    return rows


def write_csv(rows: list[dict], output_path: str) -> None:
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "latitude", "longitude"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--num-drivers", type=int, default=50)
    parser.add_argument("--num-passengers", type=int, default=50)
    parser.add_argument("--output", default="data/geolocations.csv")
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    rows = generate_rows(args.num_drivers, args.num_passengers, CITY_BOUNDS)
    write_csv(rows, args.output)
    print(f"Wrote {len(rows)} records to {args.output}")


if __name__ == "__main__":
    main()
