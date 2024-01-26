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
        return True
    
    if KeyA.is_pressed():
        time.sleep_ms(100)
        if KeyA.is_pressed():
            print("k")
            return True
    
    return False

def check_systime(use_ntp=False):
    year, month, mday, hour, minute, second, weekday, *_ = time.localtime()
    log.info(f"local time {year}/{month}/{mday} {hour}:{minute}:{second}")
    
    if year > 2020:
        return
    
    if use_ntp:
        updateRTC_NTP()
    else:
        updateRTC_8025T()

def updateRTC_NTP():
    '''update esp32 rtc time from ntp server'''
    import display, wlan_helper, settings, ntp_clock
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
 
    epd.drawTextFast(f"系统时间需要同步，正在连接网络 {settings.WIFI_SSID}", 4)
    if not wlan_helper.wifiHelper.connect(settings.WIFI_SSID, settings.WIFI_PASS):
        epd.drawTextFast(f"无法连接到 {settings.WIFI_SSID}", 4)
        epd.deepSleep(settings.APP_DEEP_SLEEP_TIME_MS)
        return
    
    epd.drawTextFast(f"正在同步 系统时间", 4) 
    if not ntp_clock.ntp_sync_via_wifi(settings.TIME_ZONE_GMT8):
        epd.drawTextFast(f"同步失败", 4)
        epd.deepSleep(settings.APP_DEEP_SLEEP_TIME_MS)
        return

def updateRTC_8025T():
    '''update esp32 rtc time from ntp server'''
    import rx8025t, board
    from machine import SoftI2C, RTC
    i2c = SoftI2C(scl= board.SENSOR_SCL, sda= board.SENSOR_SDA)
    rtc = rx8025t.RX8025T(i2c)
    rxDT = rtc.datetime()
    RTC().datetime(tuple(rxDT))
    
if __name__ == '__main__':
    main()
