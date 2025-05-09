import os
from time import sleep

from hardware.sensors import Sensors
from influx_api.upload import Influx

from hardware.ADC import Adc

if __name__ == '__main__':
    pid_light = os.fork()

    try:
        if pid_light:   # Parent. Not light.
            print('I am parent')
            influx = Influx(name="autocloud1")
            sensors = Sensors(name='autocloud1')
            last_CardUID = ""
            while True:
                key, value = sensors.read_line()
                upload_ready = True
                if key == "Card UID":
                    if value != last_CardUID:
                        last_CardUID = value
                    else:
                        upload_ready = False
                if upload_ready == True:
                    influx.upload_data((key, value))
        else:           # Child process.
            print('I am child')
            influx = Influx(name="autocloud1")
            adc = Adc()
            last_light = -1
            while True:
                left  = adc.readRawADS7830(0)
                right = adc.readRawADS7830(1)
                light = int((left + right) / 2)
                if light != last_light:
                    last_light = light
                    influx.upload_data(('photoresistor', light))
                sleep(1)
    except Exception as e:
        print("Exception:{}".format(e))
