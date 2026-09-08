# Driver-Passenger-Matching
A proof of concept driver and passenger matching service for a ride hailing platform.

## Development

Format the code:

```bash
ruff format .
```

Run the app:

```bash
source .venv/bin/activate
python -m uvicorn app.main:app --reload
```

Redis must be running on `localhost:6379` (or set `REDIS_URL`). Driver locations
can then be stored and searched with:

```text
PUT /drivers/{driver_id}/location?latitude=1.3521&longitude=103.8198
GET /drivers/nearby?latitude=1.3521&longitude=103.8198&radius_km=5
```
