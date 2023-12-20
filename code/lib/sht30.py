#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# from https://github.com/HAIZAKURA/esp-sht3x-micropython


import sys
import utime
from machine import Pin
from machine import I2C

class SHT3x_Sensor():

    def __init__(self, freq, sdapin, sclpin):
        self.i2c = I2C(0, freq=freq, sda=Pin(sdapin), scl=Pin(sclpin)) 
        addrs = self.i2c.scan()
        if not addrs:
            raise Exception('no SHT3X found at bus on SDA pin %d SCL pin %d' % (sdapin, sclpin))
        self.addr = addrs.pop()	

    def read_temp_humd(self):
        status = self.i2c.writeto(self.addr,b'\x24\x00')
        # delay (20 slow)
        utime.sleep(1)
        # read 6 bytes
        databytes = self.i2c.readfrom(self.addr, 6)
        dataset = [databytes[0],databytes[1]]
        dataset = [databytes[3],databytes[4]]
        temperature_raw = databytes[0] << 8 | databytes[1]
        temperature = (175.0 * float(temperature_raw) / 65535.0) - 45
        # fahreheit
        # temperature = (315.0 * float(temperature_raw) / 65535.0) - 49
        humidity_raw = databytes[3] << 8  | databytes[4]
        humidity = (100.0 * float(humidity_raw) / 65535.0)
        sensor_data = [temperature, humidity]
        return sensor_data

if __name__ == "__main__":
    from machine import Pin
    sens_en = Pin(40)
    sens_en.init(sens_en.OUT, value=1)
    sht3x_sensor = SHT3x_Sensor(freq=100000, sdapin=38, sclpin=39)
    measure_data = sht3x_sensor.read_temp_humd()
    # measure_data = [22.9759, 73.8277]
    # The default decimal place is 4 digits
    temp = measure_data[0]
    humd = measure_data[1]

    print('Temp:', temp)
    print('Humd:', humd)
    

