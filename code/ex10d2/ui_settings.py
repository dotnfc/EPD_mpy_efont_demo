"""
    [eForeDemo] 天气页面测试
    by .NFC 2023/12/23
"""
import time, datetime
from  wlan_helper import wifiHelper
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
    
    def getQRcodeImage(self, x, y, text):
        from uQR import QRCode

        qr = QRCode()
        ssid, password = 'test', 'test'
        qr.add_data(text)
        matrix = qr.get_matrix()
        # matrix = qr.render_matrix()
        for yy in range(len(matrix)*2):
            for xx in range(len(matrix[0])*2):
                value = not matrix[int(yy/2)][int(xx/2)]
                self.epd.pixel(xx + x, yy + y, value)
                
    def start(self):
        """Run the settings loop"""
        log.info("Settings Started")
        self.epd.drawText(10, 100, self.epd.WIDTH - 10, 24, ALIGN_CENTER, f"正在连接 {WIFI_SSID} ...")
        self.epd.refresh(full=False)
    
        if wifiHelper.connect(WIFI_SSID, WIFI_PASS):
            sStat = "已连接"
        else:
            sStat = "连接失败"
        self.epd.drawText(10, 130, self.epd.WIDTH - 10, 24, ALIGN_CENTER, sStat)
        self.epd.refresh(full=False)
        
        self.getQRcodeImage(10, 300, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        self.getQRcodeImage(400, 300, f'http://192.168.9.10:8090')
        
        self.epd.refresh(full=False)
        
        fbuf = framebuf.FrameBuffer(bytearray(10 * 100 * 2), 10, 100, framebuf.RGB565)
        
        while(True):
            time.sleep_ms(100)