import os
import sys
from uuid import uuid4
from influxdb_client import Authorization, InfluxDBClient, Permission, PermissionResource, Point, WriteOptions
from influxdb_client.client.authorizations_api import AuthorizationsApi
from influxdb_client.client.bucket_api import BucketsApi
from influxdb_client.client.flux_table import FluxStructureEncoder
from influxdb_client.client.query_api import QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_client.domain.dialect import Dialect

from dotenv import load_dotenv

sys.path.append('../controller')

from sensors import Sensors

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
        self.schema = []

    def get_schema(self):
        query = f"""
        import \"influxdata/influxdb/schema"

        schema.measurements(bucket: \"{self.bucket}\")
        """
        self.schema = []
        tables = self.query_api.query(query=query, org=self.org)
        measurements = [row.values["_value"] for table in tables for row in table]
        print(measurements)
        
        for measurement in measurements:
            print(measurement)
            query = f"""
            import \"influxdata/influxdb/schema\"

            schema.measurementFieldKeys(
                bucket: \"{self.bucket}\",
                measurement: \"{measurement}\"
            )
            """
            tables = self.query_api.query(query=query, org=self.org)
            fields = [row.values["_value"] for table in tables for row in table]
            print(fields)
            schema_measure = { 'measurement': measurement, 'fields': fields }
            self.schema.append(schema_measure)
        print(self.schema)

    def get_measurement_form_field(self, field):
        for schema in self.schema:
            if field in schema['fields']:
                return schema['measurement']
        return None

    def upload_data(self, data):
        try:
            key   = data[0]
            value = data[1]
            # field_exists = True
            # if self.get_measurement_form_field(key) is None:
            #     field_exists = False
            if key == 'Photoresistor':
                measurement = "light"
                field = "light"
                value = int(value)
            elif key == 'Card UID':
                measurement = "street"
                field = "RFID"
            point = Point(measurement).tag("name", self.name).field(field, value)
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
        except Exception as e:
            print("ERROR:{}".format(e))

if __name__ == '__main__':
    influx = Influx(name="autocloud-1")
    sensors = Sensors(name='autocloud-1')
    try:
        while True:
            key, value = sensors.read_line()
            influx.upload_data((key, value))
    except Exception as e:
        print("Exception:{}".format(e))
    # influx.get_schema()