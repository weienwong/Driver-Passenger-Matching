from fastapi import FastAPI

from app.matching_algorithm.naive import execute_static_naive_matching

app = FastAPI()


@app.get("/health")
def healthcheck():
    return {"message": "healthy"}


@app.get("/match")
def matching_service():
    matches = execute_static_naive_matching
    return {"data": matches}
