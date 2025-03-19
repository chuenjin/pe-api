from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, Query
from .models import WeatherStationPublic, WeatherStation
from .database import get_session, engine

from sqlmodel import SQLModel, create_engine, Session, select

app = FastAPI()

SessionDep = Annotated[Session, Depends(get_session)]        

@app.get("/weatherstations", response_model=list[WeatherStationPublic])
def read_weatherstations(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100,
        
) -> list[WeatherStation]:
    weatherstations = session.exec(select(WeatherStation).offset(offset).limit(limit)).all()
    return weatherstations
