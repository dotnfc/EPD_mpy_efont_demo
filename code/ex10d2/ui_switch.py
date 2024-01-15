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
        
        self.new = settings.HOME_PAGE
        if (self.new == 0) or (self.new > 3):
            self.new = 1
        self.current = -1

    def button_action(self, kid, ishold):
        if (kid == 1):
            self.new = self.new - 1
            if self.new <= 0:
                self.new = 3
        else:
            self.new = self.new + 1
            if self.new > 3:
                self.new = 1

        if ishold:
            print(f"Enter")
        
    async def startUILoop(self):        
        if sys.platform == 'linux':
            while(self.epd.runable()):
                await asyncio.sleep(0.01)
                self.updateDisplay()
            sys.exit(0)
        else:
            while(True):
                await asyncio.sleep(0.01)
                self.updateDisplay()

    async def buttonCheckLoop(self):
        KeyA.set_callback(self.button_action)    
        KeyB.set_callback(self.button_action)        
        while(True):
            await asyncio.sleep(0.01)
            KeyA.update_state()
            KeyB.update_state()
                    
    async def runTasks(self):
        t1 = asyncio.create_task(self.startUILoop())
        t2 = asyncio.create_task(self.buttonCheckLoop())
        await asyncio.gather(t1, t2)

    # def rounded_rect(self, x, y
    def start(self):
        """Run the switch loop"""
        log.info("Switch Started")
                
        asyncio.run(self.runTasks())

    def drawItem(self, icon, title, description, x, y, id):
        self.epd.selectFont("icons")
        self.epd.drawText(x + 10, y + 10, 132, 132, ALIGN_LEFT, icon, 64)
        
        self.epd.selectFont("simyou")
        self.epd.drawText(x + 94, y + 8, 96, 132, ALIGN_LEFT, title, 32)
        self.epd.drawText(x + 94, y + 46, 96, 132, ALIGN_LEFT, description, 24)
        
        if self.current == id:
            # self.epd.rounded_rect(140, 110, 114, 192, 20, 0)
            self.epd.rounded_rect(x, y, 600, 86, 16, 0)

    def updateDisplay(self):
        
        if self.current == self.new:
            return
        
        self.current = self.new

        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        self.epd.clear()
        
        # header
        self.epd.drawText(0, 16, self.epd.WIDTH -1, 48, ALIGN_CENTER, "选择启动页面", 32)
        self.epd.hline_dots(80, 60, 800)
        
        # body
        self.drawItem(ICO_SETTING, "设置", "使用浏览器或者蓝牙 App 配置设备", 100, 120, 1)
        self.drawItem(ICO_CALENDAR_MONTH, "月历", "显示一个月历及节假日、家人生日信息", 100, 220, 2)
        self.drawItem(QW_102, "天气", "未来 5 天的天气，今天和室内的温度、湿度", 100, 320, 3)

        # footer
        if sys.platform == "linux":
            strTip = "按键 W：向上 | 按键 S：向下 | 长按 W/S：确认"
        else:
            strTip = "按键1：向上 | 按键2：向下 | 长按1/2：确认"
        self.epd.drawText(100, 576, 760, 606, ALIGN_CENTER, strTip, 16)

        self.epd.line(60, 600, 900, 600, 0)
        
        self.epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)
        #self.epd.selectFont("icons")
        #self.epd.drawText(66, 606, self.epd.WIDTH -1, 610, ALIGN_LEFT, ICO_SETTING_SOLID, 24)

        self.epd.refresh(full=False)        