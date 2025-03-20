from sqlmodel import Field, SQLModel, Relationship
from typing import Annotated
from decimal import Decimal
from datetime import datetime

class WeatherStationBase(SQLModel):
    name: str = Field(index=True)
    site: str
    portfolio: str
    state: str = Field(index=True)
    latitude: Decimal = Field(default=0, max_digits=8, decimal_places=6)
    longitude: Decimal = Field(default=0, max_digits=9, decimal_places=6)

class WeatherStation(WeatherStationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    measurements: list["Measurement"] = Relationship(back_populates="weatherstation")

class MeasurementBase(SQLModel):
    timestamp: datetime = Field(index=True)
        
class Measurement(MeasurementBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    weatherstation_id: int | None = Field(default=None, foreign_key="weatherstation.id")
    weatherstation: WeatherStation | None = Relationship(back_populates="measurements")
    datapoints: list["DataPoint"] = Relationship(back_populates="measurement")

class VariableBase(SQLModel):
    unit: str
    long_name: str
    
class Variable(VariableBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    weatherstation_id: int | None = Field(default=None, foreign_key="weatherstation.id")
    name: str
    datapoints: list["DataPoint"] = Relationship(back_populates="variable")

class DataPointBase(SQLModel):
    value: str
    
class DataPoint(DataPointBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    measurement_id: int | None = Field(default=None, foreign_key="measurement.id")
    measurement: Measurement | None = Relationship(back_populates="datapoints")
    variable_id: int | None = Field(default=None, foreign_key="variable.id")
    variable: Variable | None = Relationship(back_populates="datapoints")

# public models    
class VariablePublic(VariableBase):
    id: int
    
class DataPointPublic(DataPointBase):
    id: int
    variable: VariablePublic | None = None

class MeasurementPublic(MeasurementBase):
    id: int
    datapoints: list[DataPointPublic] = []
    
class WeatherStationPublic(WeatherStationBase):
    id: int
    measurements: list[MeasurementPublic] = []
