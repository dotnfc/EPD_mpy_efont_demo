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
        self.entered = False
        self.running = False
                
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
            self.entered = True

    async def startUILoop(self):        
        if sys.platform == 'linux':
            while(self.epd.runable()):
                await asyncio.sleep(0.01)
                self.updateDisplay()
                
                if not self.running:
                    self.epd.closeWindow()
                    return
            sys.exit(0)
        else:
            while(self.running):
                await asyncio.sleep(0.01)
                self.updateDisplay()
                
    async def buttonCheckLoop(self):
        KeyA.set_callback(self.button_action)    
        KeyB.set_callback(self.button_action)
        
        try:
            while(self.running):
                await asyncio.sleep(0.01)
                KeyA.update_state()
                KeyB.update_state()
        finally:
            KeyA.set_callback(None)    
            KeyB.set_callback(None)
                        
    async def runTasks(self):
        self.running = True
        t1 = asyncio.create_task(self.startUILoop())
        t2 = asyncio.create_task(self.buttonCheckLoop())
        await asyncio.gather(t1, t2)

        print("task end")
        
    # def rounded_rect(self, x, y
    def start(self):
        """Run the switch loop"""
        log.info("Switch Started")
        
        self.drawContents()
        asyncio.run(self.runTasks())
        
        return self.current
    
    def drawItem(self, icon, title, description, x, y, id, all=True):
        if all:
            self.epd.selectFont("icons")
            self.epd.drawText(x + 10, y + 10, 132, 132, ALIGN_LEFT, icon, 64)
            
            self.epd.selectFont("simyou")
            self.epd.drawText(x + 94, y + 8, 96, 132, ALIGN_LEFT, title, 32)
            self.epd.drawText(x + 94, y + 46, 96, 132, ALIGN_LEFT, description, 24)
        
        if self.current == id:
            # self.epd.rounded_rect(140, 110, 114, 192, 20, 0)
            self.epd.rounded_rect(x, y, 580, 86, 16, 0)

    def getLaunchPageName(self):
        '''get launch page name'''
        for item in UI_PAGES:
            if item['id'] == self.current:
                return item['name']
        
        return None
    
    def drawContents(self):
        '''render contents double buffer, so to reduce total update time
        3.2s to about 1s
        '''
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        self.epd.clear()
        
        # header
        self.epd.drawText(0, 16, self.epd.WIDTH -1, 48, ALIGN_CENTER, "选择启动页面", 32)
        self.epd.hline_dots(60, 60, 840)

        # body
        self.drawItem(ICO_SETTING, "设置", "使用浏览器或者蓝牙 App 配置设备", 290, 120, 1)
        self.drawItem(ICO_CALENDAR_MONTH, "月历", "显示一个月历及节假日、家人生日信息", 290, 220, 2)
        self.drawItem(QW_102, "天气", "未来 5 天的天气，今天和室内的温度、湿度", 290, 320, 3)

        self.epd.drawImage(60, 80, "image/song_he_d1.jpg")  
        # self.epd.rounded_rect(60, 80, 200, 500, 16, 0)
                
        # footer
        if sys.platform == "linux":
            strTip = "按键 W：向上 | 按键 S：向下 | 长按 W/S：确认"
        else:
            strTip = "按键1：向上 | 按键2：向下 | 长按1/2：确认"
        self.epd.drawText(100, 576, 760, 606, ALIGN_CENTER, strTip, 16)

        self.epd.line(60, 600, 900, 600, 0)
        
        self.epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)

        # double buffering
        self.rbuf = bytearray(self.epd.buffer)        
        self.fmbuf = framebuf.FrameBuffer(self.rbuf, self.epd.WIDTH, self.epd.HEIGHT, MONO_HLSB)
        
    def updateDisplay(self):
        '''draw contents'''
        if self.entered:
            strItem = self.getLaunchPageName()
            if strItem is not None:
                self.epd.selectFont("simyou")
                self.epd.drawText(0, 532, self.epd.WIDTH, 24, ALIGN_CENTER, f"启动 {strItem} 中", 20)
                self.epd.refresh(full=False)
                
                self.running = False
                time.sleep_ms(2000)
            return
        elif (self.current == self.new) or (not self.running):
            return
        
        self.current = self.new

        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        self.epd.clear()

        self.epd.blit(self.fmbuf, 0, 0)

        # body
        self.drawItem(ICO_SETTING, "设置", "使用浏览器或者蓝牙 App 配置设备", 290, 120, 1, all=False)
        self.drawItem(ICO_CALENDAR_MONTH, "月历", "显示一个月历及节假日、家人生日信息", 290, 220, 2, all=False)
        self.drawItem(QW_102, "天气", "未来 5 天的天气，今天和室内的温度、湿度", 290, 320, 3, all=False)

        self.epd.refresh(full=False)

