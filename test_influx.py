from controller.sensors import Sensors
from influx_api.upload import Influx

from controller.ADC import Adc

if __name__ == '__main__':
    influx = Influx(name="autocloud1")
    sensors = Sensors(name='autocloud1')
    adc = Adc()
    last_light = -1
    try:
        while True:
            key, value = sensors.read_line()
            influx.upload_data((key, value))

            left  = adc.readRawADS7830(0)
            right = adc.readRawADS7830(1)
            light = int((left + right) / 2)
            if light != last_light:
                last_light = light
                influx.upload_data(('photoresistor', light))
    except Exception as e:
        print("Exception:{}".format(e))