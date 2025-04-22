import os
from uuid import uuid4
from influxdb_client import Authorization, InfluxDBClient, Permission, PermissionResource, Point, WriteOptions
from influxdb_client.client.authorizations_api import AuthorizationsApi
from influxdb_client.client.bucket_api import BucketsApi
from influxdb_client.client.flux_table import FluxStructureEncoder
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client.domain.dialect import Dialect

from dotenv import load_dotenv

from influx_api.schema import Schema

class Influx:
    def __init__(self, name='nodevice'):
        load_dotenv()
        self.name = name
        self.bucket = os.getenv("INFLUX_BUCKET")
        self.token  = os.getenv("INFLUX_TOKEN")
        self.org    = os.getenv("INFLUX_ORG")
        self.url    = os.getenv("INFLUX_URL")
        self.client = InfluxDBClient(
            url   = self.url,
            token = self.token,
            org   = self.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.schema = Schema()
        print('Getting schema...')
        sensors = self.schema.update_sensors()
        measurements = self.schema.update_measurement()
        if sensors is True and measurements is True:
            print('Successfully obtained schema!')

    def upload_data(self, data: tuple[str, str]):
        try:
            measure = self.schema.parse_measurement_value(data[0], data[1])
            field = measure['units']
            value = measure['value']
            measurement = measure['name']

            point = Point(measurement).tag("name", self.name).field(field, value)
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            print("ERROR:{}".format(e))