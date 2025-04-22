import os
import requests

from dotenv import load_dotenv

class Schema():
    def __init__(self):
        load_dotenv()
        self.api_host = os.getenv("API_HOST")
        self.api_url  = os.getenv("API_URL")
        self.sensors = []
        self.measurements = []

    def update_measurement(self):
        result = requests.get(self.api_host+self.api_url+"/measurement")
        if result.status_code == 200:
            self.measurements = result.json()
            return True
        raise Exception(f'\nThere was an error updating the measurements:\n'
                        f'Got error from API:\n\t'
                        f'-> Status code: {result.status_code}\n\t'
                        f'-> Details: {result.text}\n')

    def update_sensors(self):
        result = requests.get(self.api_host+self.api_url+"/sensor/sensor_full")
        if result.status_code == 200:
            self.sensors = result.json()
            return True
        raise Exception(f'\nThere was an error updating the sensors:\n'
                        f'Got error from API:\n\t'
                        f'-> Status code: {result.status_code}\n\t'
                        f'-> Details: {result.text}\n')

    def parse_measurement_value(self, measurement, value):
        data  = self.measurements['data']
        count = self.measurements['count']

        measure = next((item for item in data if item['name'] == measurement), None)
        if measure is None:
            raise TypeError(f'There is no data type in the schema for this measure ({measurement}).\n')
        
        data_type = measure['data_type']
        if data_type == 'int'
            value = int(value)
        elif data_type == 'float':
            value = float(value)
        elif data_type == 'string':
            value = str(value)
        else:
            raise TypeError(f'There is no data type in the schema for this measure ({measurement}).\n')
        measure['value'] = value
        return measure

    def parse_sensor_value(self, sensor, measurement, value):
        data  = self.sensors['data']
        count = self.sensors['count']

        sensor_obj = next((obj for obj in data if obj['sensor']['name'] == sensor), None)
        if sensor_obj is None:
            raise f'\nThere is no sensor called {sensor} in the schema\n'

        measure = next((item for item in sensor_obj['sensor']['measurements'] if item['name'] == measurement), None)
        if measure is None:
            raise f'\nThere is no measurement {measurement} in the schema\n'
        data_type = measure['data_type']
        if data_type == 'int'
            value = int(value)
        elif data_type == 'float':
            value = float(value)
        elif data_type == 'string':
            value = str(value)
        else:
            raise TypeError(f'There is no data type in the schema for this measure.\n'
                            f'Measurement: {measure}'
                            f'Sensor: {sensor_obj}')
        measure['value'] = value
        return measure


if __name__ == '__main__':
    test = Schema()
    test.update_measurement()
    test.update_sensors()

    old_value = '28.9'
    new_value = test.parse_measurement_value('temperature', old_value)
    print(f'old_value: {old_value}. Type: {type(old_value)}')
    print(f'new_value: {new_value}. Type: {type(new_value["value"])}')