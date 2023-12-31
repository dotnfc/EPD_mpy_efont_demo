"""
    [eForeDemo] 天气页面测试
    by .NFC 2023/12/23
"""
import time, datetime
import wlan_helper
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
        import uqr
                
        qr = uqr.make(text)
        
        w, h, data = qr.packed()
        print(f"w {w}, h {h}")
        #fbuf = framebuf.FrameBuffer(bytearray(data), w, h, MONO_HLSB)
        #self.epd.blit(fbuf, x, y, w, h)
        
        _start = time.ticks_ms()
        for yy in range(w * 4):
            for xx in range(w * 4):
                if qr.get(yy // 4, xx // 4):
                    self.epd.pixel(xx + x, yy + y, 0)
        _end = time.ticks_ms()
        print(f"time used {_end - _start}ms")
        
    def drawQRcodeImage(self, epd, x, y, text):
        import uqr                
        qr = uqr.make(text)
        
        _start = time.ticks_ms()
        qr.draw(epd, x, y, 4)
        _end = time.ticks_ms()
        print(f"time2 used {_end - _start}ms")
        
    def start(self):
        """Run the settings loop"""
        log.info("Settings Started")
        
        self.AP = wlan_helper.WifiAPHelper()
        self.AP.start(AP_NAME, AP_PASS)
        
        self.showInformations(9090)
        
        # self.getQRcodeImage(10, 300, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        # self.getQRcodeImage(500, 300, f'12345hello 你好')
        
        # self.drawQRcodeImage(self.epd, 200, 300, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        # self.drawQRcodeImage(self.epd, 600, 300, f'12345hello 你好')
                        
        while(self.epd.runable()):
            time.sleep_ms(100)

        sys.exit(1)
    
    def hline_dots(self, x, y, width):
        ext = 0
        step= const(10)
        
        while(width > 0):
            if width > step:
                ext = step
            else:
                ext = width
                
            self.epd.line(x, y, x + ext, y, 0)
            x += ext + 4
            width -= ext + 4
            
    def showInformations(self, svc_port):
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        self.epd.clear()
        self.epd.drawText(0, 16, self.epd.WIDTH -1, 48, ALIGN_CENTER, "配置设备", 32)
        self.hline_dots(80, 60, 800)
        
        msg = f"1. 连接热点网络"
        self.epd.drawText(100, 80, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码，连接到此设备的热点"
        self.epd.drawText(100, 110, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工连接以下热点"
        self.epd.drawText(100, 140, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     名称: {AP_NAME}, 密码: {AP_PASS}"
        self.epd.drawText(100, 170, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     提示: 安卓系统使用'扫一扫', iOS 请使用系统相机直接扫。"
        self.epd.drawText(100, 208, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 16)
        
        # self.hline_dots(180, 260, 600)
        
        msg = f"2. 访问配置页面"
        self.epd.drawText(100, 290, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码访问"
        self.epd.drawText(100, 320, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工访问 http://{self.AP.ip()}:{svc_port}"
        self.epd.drawText(100, 350, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        
        # AP 二维码
        self.drawQRcodeImage(self.epd, 652, 80, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        
        # 配置页面
        self.drawQRcodeImage(self.epd, 658, 290, f'http://{self.AP.ip()}:{svc_port}')
        
        self.epd.line(60, 600, 900, 600, 0)
        
        self.epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)
        #self.epd.selectFont("icons")
        #self.epd.drawText(66, 606, self.epd.WIDTH -1, 610, ALIGN_LEFT, ICO_SETTING_SOLID, 24)

        self.epd.refresh(full=False)
        
        