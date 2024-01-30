#-*- coding:utf-8 -*-
#----------------------------------------------------------------
# temperature from SHT sensor and the ESP chip internal sensor
#
import board
import time, sys
from efore.qw_icons import *
try:
    from machine import ADC
    from machine import Pin
except:
    import uADC as ADC
    from usdl2_pin import * # Pin

class TemprHumiditySensor(object):

    def __init__(self):
        self.measure_data = [0, 0]
        self.loaded = False
        
    def read(self):
        '''Read temperature and humidity from device'''
        if sys.platform == 'linux':
            return self.measure_data
        
        from sht30 import SHT3x_Sensor
        sens_en = Pin(board.SENSOR_EN)
        sens_en.init(sens_en.OUT, value=1)
        sens_en(1)
        time.sleep_ms(10)

        sht3x_sensor = SHT3x_Sensor(freq=100000, sdapin=38, sclpin=39)
        self.measure_data = sht3x_sensor.read_temp_humd()

        sens_en(0)
        
        self.loaded = True
        return self.measure_data
    
    def getTemperature(self):
        if not self.loaded:
            self.read()
        return int(self.measure_data[0])
    
    def getHumidity(self):
        if not self.loaded:
            self.read()
        return int(self.measure_data[1]) # round(num, 2)


class BatterySensor(object):

    def __init__(self):
        self.measure_data = 4.2

    def read(self) ->float:
        '''Read battery level from external circuit'''
        if sys.platform == 'linux':
            return self.measure_data
    
        sens_en = Pin(board.BATTERY_ADC_EN)
        sens_en.init(sens_en.OUT, value=1)
        sens_en(1)
        time.sleep_ms(30)

        adc = ADC(board.BATTERY_ADC)
        adc.atten(ADC.ATTN_11DB)   # 设置衰减比 满量程3.3v
        adc.width(ADC.WIDTH_12BIT) # 设置数据宽度为12bit

        sample_times = const(3)
        
        adv = sum([adc.read() for i in range(sample_times)])/sample_times
        adv = adv / 4095 * 3.3
        adv = adv * 3 / 2 # {100K / 200K}
        self.measure_data = round(adv, 2) 
        
        sens_en(0)

        return self.measure_data
    
    def getVoltageForApp(self):
        vol = self.read()
        vol = round(vol, 1)
        svol = f"{vol} V"
        return svol
    
    def getWebInfo(self):
        vol = self.read()
        icon = 0

        if vol >= 4.2:          icon = 10
        elif vol >= 4.1:        icon = 9
        elif vol >= 4.0:        icon = 8
        elif vol >= 3.9:        icon = 7
        elif vol >= 3.8:        icon = 6
        elif vol >= 3.7:        icon = 5
        elif vol >= 3.6:        icon = 4
        elif vol >= 3.5:        icon = 3
        elif vol >= 3.3:        icon = 2
        elif vol >= 3.2:        icon = 1
        elif vol < 3.2:         icon = 0

        c = 'e' # normal
        if isUSBPowered():
            c = 'c' # charging

        str = f"{vol:.1f} V <span class=\"qi-ico-bat{c}{icon}\"></span>"
        return str

def voltage_to_percentage(voltage):
    min_voltage = 3.2
    max_voltage = 4.2
    percentage = ((voltage - min_voltage) / (max_voltage - min_voltage)) * 100
    return int(max(0, min(100, percentage)))

def getBatInfo():
    vol = snsBattery.read()
    icon = 0

    if isUSBPowered():
        if vol >= 4.2:          icon = ICO_BATC10
        elif vol >= 4.1:        icon = ICO_BATC9
        elif vol >= 4.0:        icon = ICO_BATC8
        elif vol >= 3.9:        icon = ICO_BATC7
        elif vol >= 3.8:        icon = ICO_BATC6
        elif vol >= 3.7:        icon = ICO_BATC5
        elif vol >= 3.6:        icon = ICO_BATC4
        elif vol >= 3.5:        icon = ICO_BATC3
        elif vol >= 3.3:        icon = ICO_BATC2
        elif vol >= 3.2:        icon = ICO_BATC1
        elif vol < 3.2:         icon = ICO_BATC0
    else: 
        if vol >= 4.2:          icon = ICO_BAT10
        elif vol >= 4.1:        icon = ICO_BAT9
        elif vol >= 4.0:        icon = ICO_BAT8
        elif vol >= 3.9:        icon = ICO_BAT7
        elif vol >= 3.8:        icon = ICO_BAT6
        elif vol >= 3.7:        icon = ICO_BAT5
        elif vol >= 3.6:        icon = ICO_BAT4
        elif vol >= 3.5:        icon = ICO_BAT3
        elif vol >= 3.3:        icon = ICO_BAT2
        elif vol >= 3.2:        icon = ICO_BAT1
        elif vol < 3.2:         icon = ICO_BAT0
    
    bat_info = f"{voltage_to_percentage(vol)}%"
    return bat_info, icon

def isUSBPowered():
    '''USB 上电检测'''
    if sys.platform == 'linux':
        return True

    sens_in = Pin(board.USB_PWR_SENSE)
    sens_in.init(sens_in.IN)
    return (sens_in.value() == 1)

def isNFCPowered():
    '''USB 上电检测'''
    if sys.platform == 'linux':
        return True

    sens_en = Pin(board.NFC_PWR_SENSE)
    sens_en.init(sens_en.IN)
    return (sens_en.value() == 1)

snsTemprHumidity = TemprHumiditySensor()
snsBattery = BatterySensor()

if __name__ == '__main__':
    # snsTemprHumidity.read()
    print(snsBattery.getVoltageForApp())

