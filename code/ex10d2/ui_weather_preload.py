"""
    preload weather info [.NFC 2023/12/18]
"""
import sys, machine, time
import logging as log
from  wlan_helper import wifiHelper
from settings import *
from display import *
import qw_api
#from qw_api_fake import *

class uiWeatherPreload(object):
        
    def __init__(self):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.selectFont("simyou")
        self.epd.initTextFast("simyou", self.epd.WIDTH, 20)
        
    def start(self):
        """Run the weather preloading"""
        log.info("Preload Weather")
        
        self.epd.drawTextFast(f"正在连接网络 {WIFI_SSID}", 4)
        if not wifiHelper.connect(WIFI_SSID, WIFI_PASS):
            self.epd.drawTextFast(f"无法连接到 {WIFI_SSID}", 4)
            self.epd.deepSleep(APP_DEEP_SLEEP_TIME_MS)
            return
        
        self.epd.drawTextFast(f"正在请求天气信息", 4)
        print("req weathers")
        try:
            qw_now = qw_api.now(QW_API_CITY, QW_API_KEY)
            qw_future = qw_api.future(QW_API_CITY, QW_API_KEY)
            qw_future_air = qw_api.future_air(QW_API_CITY, QW_API_KEY)
            qw_hourly = qw_api.hourly(QW_API_CITY, QW_API_KEY)
            yi_yan = qw_api.yiyan()
            self.epd.drawTextFast(f"天气信息获取完毕，准备更新显示", 4)
        except Exception as e:
            self.epd.drawTextFast(f"请求天气信息失败 {str(e)}", 4)
            self.epd.deepSleep(APP_DEEP_SLEEP_TIME_MS)
            return
        
        wifiHelper.disconnect()
        if sys.platform == 'linux':
            self.epd.closeWindow()
        return qw_now, qw_future, qw_future_air, qw_hourly, yi_yan

