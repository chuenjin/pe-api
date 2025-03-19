from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship
from typing import Annotated
from decimal import Decimal
from datetime import datetime

class WeatherStation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    site: str
    portfolio: str
    state: str = Field(index=True)
    latitude: Decimal = Field(default=0, max_digits=8, decimal_places=6)
    longitude: Decimal = Field(default=0, max_digits=9, decimal_places=6)
    measurements: list["Measurement"] = Relationship(back_populates="weatherstation")

class Measurement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(index=True)

    weatherstation_id: int | None = Field(default=None, foreign_key="weatherstation.id")
    weatherstation: WeatherStation | None = Relationship(back_populates="measurements")
    datapoints: list["DataPoint"] = Relationship(back_populates="measurement")

class Variable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    weatherstation_id: int | None = Field(default=None, foreign_key="weatherstation.id")
    name: str
    unit: str
    long_name: str
    datapoints: list["DataPoint"] = Relationship(back_populates="variable")
    
class DataPoint(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    value: Decimal
    measurement_id: int | None = Field(default=None, foreign_key="measurement.id")
    measurement: Measurement | None = Relationship(back_populates="datapoints")
    variable_id: int | None = Field(default=None, foreign_key="variable.id")
    variable: Variable | None = Relationship(back_populates="datapoints")
    

