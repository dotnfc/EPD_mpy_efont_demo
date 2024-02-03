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
    print(f"battery {voltage} V")
    
    voltage_table = [
        (4.2, 100),
        (4.14, 99),
        (4.12, 98),
        (4.10, 97),
        (4.08, 96),
        (4.02, 95),
        (3.98, 94),
        (3.94, 93),
        (3.90, 92),
        (3.88, 91),
        (3.86, 90),
        (3.84, 89),
        (3.82, 88),
        (3.80, 86),
        (3.78, 85),
        (3.76, 83),
        (3.74, 81),
        (3.72, 79),
        (3.70, 76),
        (3.68, 74),
        (3.66, 71),
        (3.64, 68),
        (3.62, 65),
        (3.60, 62),
        (3.58, 59),
        (3.56, 55),
        (3.54, 52),
        (3.52, 48),
        (3.50, 44),
        (3.48, 41),
        (3.46, 37),
        (3.44, 33),
        (3.42, 29),
        (3.40, 26),
        (3.38, 22),
        (3.36, 19),
        (3.34, 15),
        (3.32, 12),
        (3.30, 9),
        (3.28, 7),
        (3.26, 4),
        (3.24, 2),
        (3.20, 0),
    ]
    for threshold, percentage in voltage_table:
        if voltage >= threshold:
            return percentage
    return 0

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

