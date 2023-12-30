"""
    [eForeDemo] 天气页面测试
    by .NFC 2023/12/23
"""
import time, datetime
from  wifi_sta_helper import wifiHelper
import logging as log
from display import *
from efont import *
from efore.qw_icons import *
from efore.city_list import china_citys
from .settings import *
import ulunar, holidays, birthdays
from .button import *
import gc

class uiSettings(object):
        
    def __init__(self,**kwargs):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.loadFont("icons")
        self.epd.loadFont("7seg")
        self.epd.loadFont("swissel")
        self.epd.selectFont("simyou")
        
    def start(self):
        """Run the weather station display loop"""
        log.info("Calendar Started")
        self.epd.drawText(10, 100, self.epd.WIDTH - 10, 24, ALIGN_CENTER, f"正在连接 {WIFI_SSID} ...")
        self.epd.refresh()
    
        if wifiHelper.connect(WIFI_SSID, WIFI_PASS):
            sStat = "已连接"
        else:
            sStat = "连接失败"
        self.epd.drawText(10, 140, self.epd.WIDTH - 10, 24, ALIGN_CENTER, sStat)
        self.epd.refresh(full=False)
        
        while(True):
            time.sleep_ms(100)