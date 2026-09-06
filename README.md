# Driver-Passenger-Matching

A proof-of-concept Python service for driver-passenger matching. It supports a
static CSV-based matcher and a Redis-bounded matcher backed by LTA Taxi
Availability coordinates.

## Prerequisites

- Python 3 and Docker Desktop
- An LTA API-capable internet connection for the ingestion worker

## Setup

From the repository root, create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create your local configuration from the tracked template:

```bash
cp .env.example .env
```

`app/config.py` validates settings from `.env` and environment variables. Do not
commit `.env`; it is intentionally ignored by Git.

## Run the Full Local Stack

The local stack has three separate services:

```text
api           FastAPI HTTP server
lta-ingestor  Background worker that refreshes taxi locations
redis         Shared Redis GEO index and reservation store
```

Start all services and view their logs in one terminal:

```bash
docker compose up --build
```

To run the stack in the background instead:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f
```

Inspect one service when troubleshooting:

```bash
docker compose logs -f api
docker compose logs -f lta-ingestor
docker compose logs -f redis
```

The ingestor fetches LTA taxi locations and writes them to the `taxi_locations`
Redis GEO index. Wait for the "Taxi locations loaded into Redis" log before
making a bounded matching request.

> **Note:** `api` and `lta-ingestor` are configured to build from the project
> root. Add a `Dockerfile` before running the full-stack command for the first
> time. Inside Docker Compose, these services use `redis://redis:6379/0`; the
> `redis` hostname refers to the Redis service. Local Python processes outside
> Docker should continue using `redis://localhost:6379/0` from `.env`.

## Run the Matching Algorithms

The static naive matcher uses `data/geolocations.csv` and does not require
Redis:

```bash
python -c 'from app.matching_algorithm.naive import execute_static_naive_matching; print(execute_static_naive_matching())'
```

The bounded naive matcher searches the Redis `taxi_locations` GEO index. With
the full stack running, execute it inside the API container:

```bash
docker compose exec api python -m app.matching_algorithm.bounded_naive
```

## Run the HTTP API

With Docker Compose, the API is available at `http://127.0.0.1:8000`. Check
that it and its Redis dependency are available:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
```

Create a bounded match with a typed JSON request:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/matches \
  -H "Content-Type: application/json" \
  -d '{
    "ride_id": "417ddc5d-e556-4d27-95dd-a34d84e46a50",
    "passenger_latitude": 1.282302,
    "passenger_longitude": 103.858528
  }'
```

## Development

Format the code:

```bash
python -m ruff format .
python -m ruff check app
```

Stop the local stack when finished:

```bash
docker compose down
```

The current Redis service has no configured volume, so `docker compose down`
also removes its local data. Add a named volume before relying on Redis data
across container recreation.
