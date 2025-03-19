import csv, os, glob, re
from datetime import datetime
from sqlmodel import Session
from models import WeatherStation, Measurement, DataPoint, Variable
from database import create_db_and_tables, engine


def create_weather_stations():
    with Session(engine) as session:
        with open('sample_data/weather_stations.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                weatherstation = WeatherStation(id=row[0], name=row[1], site=row[2], portfolio=row[3], state=row[4], latitude=row[5], longitude=row[6])
                session.add(weatherstation)
                
            session.commit()
        
def create_variables():
    with Session(engine) as session:
        with open('sample_data/variables.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            variable_mapping = {}
            for row in reader:
                #need to figure this nested dictionary creation out!!!!!!
                current_value = variable_mapping.get(row[1])
                if current_value == None:
                    variable_mapping[row[1]] = {row[2]: row[0]}
                else:
                    variable_mapping[row[1]][row[2]] = row[0]
                variable = Variable(id=row[0], weatherstation_id=row[1], name=row[2], unit=row[3], long_name=row[4])
                session.add(variable)
                
            session.commit()

    return variable_mapping

def create_measurements(variable_mapping):
    with Session(engine) as session:
        for filename in glob.glob('sample_data/data_*.csv'):
            with open(filename, 'r') as file:
                match = re.search(r'data_(\d+)\.csv', filename)
                if match:
                    reader = csv.reader(file)
                    header = next(reader)
                    for row in reader:
                        measurement = Measurement(weatherstation_id=match.group(1), timestamp=datetime.strptime(row[-1], '%d/%m/%Y %H:%M:%S'))
                        #add measurement to session
                        session.add(measurement)
                        session.commit()
                        session.refresh(measurement)
                        for index, col in enumerate(row[:-1]):
                            print("WS:", measurement.weatherstation_id)
                            print(variable_mapping)
                            datapoint = DataPoint(value=col, measurement_id=measurement.id, variable_id=variable_mapping[str(measurement.weatherstation_id)][header[index]])
                            session.add(datapoint)
                        session.commit()
                        
                    #for each item in list except last
                    #find header in variable mapping, set variable id
                    #create datapoint
                    #add to session
                    #commit session
                    
                                  




def main():
    create_db_and_tables()
    create_weather_stations()
    variable_mapping = create_variables()
    create_measurements(variable_mapping)


if __name__ == "__main__":
    main()

