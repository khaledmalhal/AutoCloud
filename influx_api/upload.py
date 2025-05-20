import os
from uuid import uuid4
import threading
from influxdb_client import Authorization, InfluxDBClient, Permission, PermissionResource, Point, WriteOptions
from influxdb_client.client.authorizations_api import AuthorizationsApi
from influxdb_client.client.bucket_api import BucketsApi
from influxdb_client.client.flux_table import FluxStructureEncoder
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client.domain.dialect import Dialect

from dotenv import load_dotenv

from influx_api.schema import Schema
from settings import Settings

class Influx:
    def __init__(self, settings: Settings = None):
        load_dotenv()
        self.settings = settings
        self.name   = settings.get_name()
        self.bucket = settings.get_influx_bucket()
        self.token  = settings.get_influx_token()
        self.org    = settings.get_influx_org()
        self.url    = settings.get_influx_url()
        self.client = InfluxDBClient(
            url   = self.url,
            token = self.token,
            org   = self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.schema = Schema(settings)
        print('Getting schema...')
        self.update_schema()        
        
    def update_schema(self):
        sensors = self.schema.update_sensors()
        measurements = self.schema.update_measurement()
        if sensors is True and measurements is True:
            print('Successfully obtained schema!')
        else:
            print('There has been an error getting schema.')
        threading.Timer(10, self.update_schema).start()

    def upload_data(self, data: tuple[str, str], from_edge: str):
        try:
            measure = self.schema.parse_measurement_value(data[0], data[1])
            field = measure['units']
            value = measure['value']
            measurement = measure['name']

            point = Point(measurement).tag("name", from_edge).field(field, value)
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            print(f'Uploaded successfully {data}')
        except Exception as e:
            print("ERROR:{}".format(e))
