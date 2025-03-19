from fastapi import FastAPI, Depends, HTTPException, Query
from .models import WeatherStation, Measurement, DataPoint, Variable


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
