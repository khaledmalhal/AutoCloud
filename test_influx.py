from controller.sensors import Sensors
from influx_api.upload import Influx

if __name__ == '__main__':
    influx = Influx(name="autocloud1")
    sensors = Sensors(name='autocloud1')
    try:
        while True:
            key, value = sensors.read_line()
            influx.upload_data((key, value))
    except Exception as e:
        print("Exception:{}".format(e))