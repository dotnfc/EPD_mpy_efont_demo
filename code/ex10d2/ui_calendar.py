
import time
import json
import urequests as requests
from  wifi_sta_helper import wifiHelper
import logging as log
import calender
from display3c import *
from efont import *
from qw_icons import *
import ulunar
import gc

gc.enable()

week_day_number_cn = ("日", "一", "二", "三", "四", "五", "六")
zodiac_icon_line = (ZODIAC_SHU, ZODIAC_NIU, ZODIAC_HU, ZODIAC_TU, ZODIAC_LONG, ZODIAC_SHE, 
                   ZODIAC_MA, ZODIAC_YANG, ZODIAC_HOU, ZODIAC_JI, ZODIAC_GOU, ZODIAC_ZHU)
zodiac_icon_fill = (ZODIAC_SHU_FILL, ZODIAC_NIU_FILL, ZODIAC_HU_FILL, ZODIAC_TU_FILL, ZODIAC_LONG_FILL, ZODIAC_SHE_FILL, 
                   ZODIAC_MA_FILL, ZODIAC_YANG_FILL, ZODIAC_HOU_FILL, ZODIAC_JI_FILL, ZODIAC_GOU_FILL, ZODIAC_ZHU_FILL)

x_pos = [4, 140, 276, 412, 548, 684, 820, 956]

class uiCalendar(object):
        
    def __init__(self,**kwargs):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE, EPD_WHITE)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.loadFont("icons")
        self.epd.loadFont("7seg")
        self.epd.loadFont("swissel")
        self.epd.selectFont("simyou")
    
    def test_calendar(self):
        year = 2023
        month = 12

        cald = calender.Calender(6)

        print("Su  Mo  Tu  We  Th  Fr  Sa")
        days = 0
        for i in cald.itermonthdates(year, month):
            print(f"{i.day:2d}  ", end="")
            days += 1
            if days == 7:
                days = 0
                print("")
    
    def getZodiacIcon(self, lunar):
        return zodiac_icon_fill[lunar.dizhi]
    
    def drawTitleBar(self, month, mday, lunar):
        # 显示 月份
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(4, 8, 180, 88, 1, True)
        self.epd.setColor(EPD_WHITE, EPD_RED)
        s = "%2d月" % (month)
        self.epd.drawText(4, 10, 180, 88, ALIGN_CENTER, s, 80)
        
        # 阴历年份/生肖 日子
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        ganzhi = lunar.getGanZhi()
        shengxiao = lunar.getZodiac()
        ymon = lunar.getMonth()
        yday = lunar.getDate()
        s = "农历 %s(%s)年 %s%s" % (ganzhi, shengxiao, ymon, yday)
        self.epd.drawText(4, 40, self.epd.WIDTH - 1, 48, ALIGN_CENTER, s, 32)
        
        # 显示生肖图标
        self.epd.selectFont("icons")
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.drawText(self.epd.WIDTH - 104, 10, 100, 100, ALIGN_RIGHT, self.getZodiacIcon(lunar), 80)

        self.epd.selectFont("simyou")
        # 显示周几的背景条
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.rect_3c(0, 100, self.epd.WIDTH-1, 48, 1, True)

        # 显示周几
        i = 0
        w = x_pos[1] - x_pos[0]
        self.epd.setColor(EPD_WHITE, EPD_BLACK)
        for dayName in week_day_number_cn:
            self.epd.drawText(x_pos[i], 102, w, 48, ALIGN_CENTER, dayName, 40)
            i = i + 1

    def drawOneDay(self, nmon, nday, idate, rect):
        # print(f"({rect[0]},{rect[1]},{rect[2]},{rect[3]})", end="")
        lunar = ulunar.Lunar(idate.year, idate.month, idate.day)
        
        # 阳历
        if idate.weekday() == 5 or idate.weekday() == 6:
            self.epd.setColor(EPD_RED, EPD_WHITE)   # 周六、日
        else:
            self.epd.setColor(EPD_BLACK, EPD_WHITE)
        sday = f"{idate.day}"
        self.epd.selectFont("swissel")
        self.epd.drawText(rect[0], rect[1], rect[2], rect[3], ALIGN_CENTER, sday, 46)
        self.epd.selectFont("simyou")
        
        # 农历
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        lday = f"{lunar.getDate()}"
        self.epd.drawText(rect[0], rect[1] + 50, rect[2], rect[3], ALIGN_CENTER, lday, 20)
        
        # 今天
        if nmon == idate.month and nday == idate.day:
            self.epd.setColor(EPD_BLACK, EPD_WHITE)
            self.epd.rect_3c(rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2, 1)
        
    
    def drawBody(self, year, month, mday, lunar):
        x_pos = (4, 140, 276, 412, 548, 684, 820, 956 )
        y_pos = (154, 234, 314, 394, 474, 554, 634)
        x_span= 136
        y_span= 80
        cald = calender.Calender(6) # 6 - Sunday as the beginning of a week
        rcDate = [] # drawing box for a date
        x = 0
        y = 0
        
        for iDate in cald.itermonthdates(year, month):
            rcDate = (x_pos[x], y_pos[y], x_span, y_span)   # (x, y, w, h)
            self.drawOneDay(month, mday, iDate, rcDate)
            x += 1
            if x == 7:
                x = 0
                y += 1
        
    def start(self):
        """Run the weather station display loop"""
        log.info("uiTest Started")
        wifiHelper.connect("DOTNF-HOS", "20180903")

        year, month, mday, hour, minute, second, weekday, yearday, *_ = time.localtime()
        lunar = ulunar.Lunar(year, month, mday)
        
        self.drawTitleBar(month, mday, lunar)
        self.drawBody(year, month, mday, lunar)

        self.epd.refresh()
        self.epd.deepSleep(15000)