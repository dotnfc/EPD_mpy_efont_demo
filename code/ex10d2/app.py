"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys, machine, time
import logging as log
from button import *
from ui_calendar import uiCalendar
from ui_weather import uiWeather
from ui_settings import uiSettings
from ui_switch import uiSwitch
from ui_weather_preload import uiWeatherPreload
# from sensor import *
import settings, gc

def main():
    log.setLevel(log.INFO)
    log.info("EFore Demo Started")
    checkBatteryLow()
    
    page_id = settings.HOME_PAGE
    
    if checkGoSetting():
        switch_page = uiSwitch()
        page_id = switch_page.start()
    
    check_systime()
    
    try:
        if page_id == 2:
            uiCalendar().start()
        elif page_id == 3:
            preloader = uiWeatherPreload()
            qw_now, qw_future, qw_future_air, qw_hourly, yi_yan = preloader.start()
            uiWeather().start(qw_now, qw_future, qw_future_air, qw_hourly, yi_yan)
        else:
            uiSettings().start()    # never return

    except Exception as e:
        log.exception(e,'Exception in main.py')
    
        if sys.platform == 'esp32':
            machine.reset()
    
def checkGoSetting() ->bool:
    '''按键检测，是否进设置页面'''
    
    if sys.platform == 'linux':
        return False
    
    if KeyA.is_pressed():
        time.sleep_ms(100)
        if KeyA.is_pressed():
            print("k")
            return True
    
    return False

def checkBatteryLow():
    import sensor
    if sensor.isUSBPowered():
        return

    vol = sensor.snsBattery.read()
    print(f"当前电压 {vol}")
    if vol < 3.7:
        print("电量低，请充电")
    elif vol < 3.5:
        print("电量过低，休眠一年")
        machine.deepsleep(1000 * 60 * 60 * 24 * 356)
    
def check_systime():
    year, month, mday, hour, minute, second, weekday, *_ = time.localtime()
    log.info(f"local time {year}/{month}/{mday} {hour}:{minute}:{second}")
    
    if year > 2020:
        return
    
    if not updateRTC_8025T():
        print("ntp used")
        newDT = updateRTC_NTP()

        updateRTC_8025T(newDT)
        machine.reset()

def connect_to_wifi(epd, ssid, passwd):
    import wlan_helper
    epd.drawTextFast(f"系统时间需要同步，正在连接网络 {ssid}", 4)
    if not wlan_helper.wifiHelper.connect(ssid, passwd):
        epd.drawTextFast(f"无法连接到 {ssid}", 4)
            
def updateRTC_NTP():
    '''update esp32 rtc time from ntp server'''
    import display, settings, ntp_clock
    from wlan_helper import wifiHelper
    epd = display.EpdImage()
    epd.init()
    epd.clear(display.EPD_WHITE)
    epd.setColor(display.EPD_BLACK, display.EPD_WHITE)

    epd.loadFont("simyou")
    epd.loadFont("icons")
    epd.loadFont("7seg")
    epd.loadFont("swissel")
    epd.selectFont("simyou")
    epd.initTextFast("simyou", epd.WIDTH, 20)
 
    if wifiHelper.connects(settings.WIFI_SSID, settings.WIFI_PASS, settings.WIFI_BACKUP_AP, connect_to_wifi, epd):
        settings.cfgUpdateWiFi(wifiHelper.ssid, wifiHelper.passwd)
    else:
        epd.drawTextFast(f"无法连接到网络热点，进入休眠", 4)
        epd.deepSleep(settings.APP_DEEP_SLEEP_TIME_MS)
        return None
    
    epd.drawTextFast(f"正在同步 系统时间", 4)
    ntp_clock.timezone_offset = settings.TIME_ZONE_GMT8
    if not ntp_clock.ntp_sync_via_wifi():
        epd.drawTextFast(f"同步失败", 4)
        epd.deepSleep(settings.APP_DEEP_SLEEP_TIME_MS)
        return None
    else:
        return ntp_clock.newDT

def updateRTC_8025T(newDT = None):
    '''update esp32 rtc time from ntp server'''
    import rx8025t, board
    from machine import SoftI2C, RTC
    i2c = SoftI2C(scl= board.SENSOR_SCL, sda= board.SENSOR_SDA)
    rtc = rx8025t.RX8025T(i2c)

    if newDT is not None:
        print("set rxRTC")
        rtc.datetime(newDT) # (2034,1,25,4,18,00,00,0)
        return True
    
    print("get rxRTC")
    rxDT = rtc.datetime()
    if (rxDT[0] < 2023) or (rxDT[0] > 2030):
        print(f"rxRTC not valid {rxDT[0]}")
        return False # ntp update required

    RTC().datetime(tuple(rxDT))
    return True

if __name__ == '__main__':
    main()

