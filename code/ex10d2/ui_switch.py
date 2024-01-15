"""
    [eForeDemo] 启动时候，临时修改加载页面
    by .NFC 2024/01/15
"""
import time, gc, platform, sys
from micropython import const
import asyncio
import wlan_helper
import logging as log
from display import *
from efont import *
from efore.qw_icons import *
from settings import *
from sensor import *
from button import *
import settings

class uiSwitch(object):
        
    def __init__(self,**kwargs):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.loadFont("icons")
        self.epd.selectFont("simyou")
        self.epd.initTextFast("simyou", self.epd.WIDTH, 20)
        
        self.current = settings.HOME_PAGE
        if (self.current == 0) or (self.current > 3):
            self.current = 1
    
    def button_action(self, kid, ishold):
        if (kid == 1):
            print(f"A {ishold}")
        else:
            print(f"B {ishold}")
        
    async def startUILoop(self):
        KeyA.set_callback(self.button_action)
        print(f"keya {KeyA.action_cb}")
        print(f"keyb {KeyB.action_cb}")
        
        KeyB.set_callback(self.button_action)
        print(f"keya {KeyA.action_cb}")
        print(f"keyb {KeyB.action_cb}")
        
        if sys.platform == 'linux':
                    
            while(self.epd.runable()):
                await asyncio.sleep(0.01)
                KeyA.update_state()
                KeyB.update_state()
            
            sys.exit(0)
        else:
            while(True):
                await asyncio.sleep(0.01)
                KeyA.update_state()
                KeyB.update_state()
    
    # def rounded_rect(self, x, y
    def start(self):
        """Run the switch loop"""
        log.info("Switch Started")
        self.updateDisplay()
        
        asyncio.run(self.startUILoop())

    def drawItem(self, icon, title, description, x, y, id):
        self.epd.selectFont("icons")
        self.epd.drawText(x + 10, y + 10, 132, 132, ALIGN_LEFT, icon, 96)
        
        self.epd.selectFont("simyou")
        self.epd.drawText(x + 120, y + 16, 96, 132, ALIGN_LEFT, title, 42)
        self.epd.drawText(x + 120, y + 66, 96, 132, ALIGN_LEFT, description, 32)
        
        if self.current == id:
            # self.epd.rounded_rect(140, 110, 114, 192, 20, 0)
            self.epd.rounded_rect(x, y, 760, 120, 20, 0)

    def updateDisplay(self):
        
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        self.epd.clear()
        
        # header
        self.epd.drawText(0, 16, self.epd.WIDTH -1, 48, ALIGN_CENTER, "选择启动页面", 32)
        self.epd.hline_dots(80, 60, 800)
        
        # body
        self.drawItem(ICO_SETTING, "设置", "使用浏览器或者蓝牙 App 配置设备", 100, 120, 1)
        self.drawItem(ICO_CALENDAR_MONTH, "月历", "显示一个月历及节假日、家人生日信息", 100, 270, 2)
        self.drawItem(QW_102, "天气", "未来 5 天的天气，今天和室内的温度、湿度", 100, 420, 3)
        
        # self.epd.selectFont("icons")
        
        # self.epd.drawText(150, 120, 132, 132, ALIGN_LEFT, ICO_SETTING, 96)
        # self.epd.drawText(400, 120, 132, 132, ALIGN_LEFT, ICO_CALENDAR_MONTH, 96)
        # self.epd.drawText(650, 120, 132, 132, ALIGN_LEFT, QW_102, 96)
        
        # self.epd.selectFont("simyou")
        # self.epd.drawText(150, 250, 96, 132, ALIGN_CENTER, "设置", 42)
        # self.epd.drawText(400, 250, 96, 132, ALIGN_CENTER, "月历", 42)
        # self.epd.drawText(650, 250, 96, 132, ALIGN_CENTER, "天气", 42)
                
        # footer
        self.epd.line(60, 600, 900, 600, 0)
        
        self.epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)
        #self.epd.selectFont("icons")
        #self.epd.drawText(66, 606, self.epd.WIDTH -1, 610, ALIGN_LEFT, ICO_SETTING_SOLID, 24)

        self.epd.refresh(full=False)        