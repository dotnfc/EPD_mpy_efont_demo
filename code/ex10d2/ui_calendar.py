"""
    [eForeDemo] 日历页面测试
    by .NFC 2023/12/20
"""
import time
import logging as log
import calender
from display3c import *
from efont import *
from efore.qw_icons import *
import ulunar, holidays, birthdays
from button import *
from settings import *
import asyncio, sensor

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
    
        self.draw_mday = 1
        self.draw_month = 1
        self.draw_year = 2024
        self.redraw = True
        self.entered = False
        
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
    
    def getZodiacIcon(self, lunar):
        '''依据地支，获取生肖的图标'''
        return zodiac_icon_fill[lunar.dizhi]
    
    def drawTitle(self, year, month, mday, lunar):
        '''显示页面的标题栏'''
        # 显示 月份
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(4, 8, 180, 88, 1, True)
        self.epd.setColor(EPD_WHITE, EPD_RED)
        s = "%2d月" % (month)
        self.epd.drawText(4, 10, 180, 88, ALIGN_CENTER, s, 80)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        
        # 阳历年份
        s = "%s年%s月%s日" % (year, month, mday)
        self.epd.drawText(4, 16, self.epd.WIDTH - 1, 32, ALIGN_CENTER, s, 28)
        
        # 阴历年份/生肖/日子
        ganzhi = lunar.getGanZhi()
        shengxiao = lunar.getZodiac()
        ymon = lunar.getMonth()
        yday = lunar.getDate()
        s = "农历 %s(%s)年 %s%s" % (ganzhi, shengxiao, ymon, yday)
        self.epd.drawText(4, 50, self.epd.WIDTH - 1, 48, ALIGN_CENTER, s, 32)
        
        # 电量
        self.epd.selectFont("icons")
        bat_info, bat_icon = sensor.getBatInfo()
        self.epd.drawText(448, 84, 64, 32, ALIGN_CENTER, bat_icon, 32)
        
        # 显示生肖图标
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
        '''显示某一天'''
        
        if nmon != idate.month:
            return
        
        lunar = ulunar.Lunar(idate.year, idate.month, idate.day)
        
        day_foreColor = EPD_RED
        day_backColor = EPD_WHITE
        
        # 国家放假安排
        strHoliday = holidays.get_nationHolidayArrangement(idate.year, idate.month, idate.day)
        if strHoliday == '假':
            day_foreColor = EPD_RED
            day_backColor = EPD_WHITE
        elif strHoliday == '班':
            day_foreColor = EPD_BLACK
            day_backColor = EPD_WHITE
        else:
            if idate.weekday() == 5 or idate.weekday() == 6:
                day_foreColor = EPD_RED   # 周六、日
                day_backColor = EPD_WHITE
            else:
                day_foreColor = EPD_BLACK
                day_backColor = EPD_WHITE
                
        # 显示阳历日
        self.epd.setColor(day_foreColor, day_backColor)
        sday = f"{idate.day}"
        self.epd.selectFont("swissel")
        day_x = self.epd.drawText(rect[0], rect[1], rect[2], rect[3], ALIGN_CENTER, sday, 46)
        self.epd.selectFont("simyou")
        
        # 假/班
        if strHoliday == '假':
            self.epd.setColor(EPD_RED, EPD_WHITE)
            # self.epd.rect_3c(day_x, rect[1]+ 4, 24, 21, 1, True)
            self.epd.rounded_rect(day_x, rect[1]+ 4, 24, 21, 3, 1, True)
            self.epd.setColor(EPD_WHITE, EPD_RED)
            self.epd.drawText(day_x, rect[1] + 6, 24, rect[3], ALIGN_CENTER, strHoliday, 16)
            self.epd.setColor(EPD_RED, EPD_WHITE)
        elif strHoliday == '班':
            self.epd.setColor(EPD_BLACK, EPD_WHITE)
            # self.epd.rect_3c(day_x, rect[1]+ 4, 24, 21, 1, True)
            self.epd.rounded_rect(day_x, rect[1]+ 4, 24, 21, 3, 1, True)
            self.epd.setColor(EPD_WHITE, EPD_BLACK)
            self.epd.drawText(day_x, rect[1] +6, 24, rect[3], ALIGN_CENTER, strHoliday, 16)
            self.epd.setColor(EPD_BLACK, EPD_WHITE)
            
        # 家人生日
        str = birthdays.get_familyBirthday(lunar)
        if str != '':
            self.epd.selectFont("icons")
            self.epd.setColor(EPD_RED, EPD_WHITE)
            self.epd.drawText(day_x + 2, rect[1] + 28, rect[2] // 2, rect[3], ALIGN_LEFT, ICO_GIFT, 18)
            self.epd.selectFont("simyou")
        else: 
            # 农历
            str = holidays.get_Holidays(lunar, idate.year, idate.month, idate.day)            

        if str == '' or len(str) > 7:
            lday = f"{lunar.getDate()}"
            self.epd.drawText(rect[0], rect[1] + 50, rect[2], rect[3], ALIGN_CENTER, lday, 20)
        else:
            self.epd.drawText(rect[0], rect[1] + 50, rect[2], rect[3], ALIGN_CENTER, str, 20)
        
        # 今天画一个外框
        if nmon == idate.month and nday == idate.day:
            self.epd.setColor(EPD_BLACK, EPD_WHITE)
            # self.epd.rect_3c(rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2, 1)
            self.epd.rounded_rect(rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2, 10, 1)
            
    def drawBody(self, year, month, mday, lunar):
        '''显示主体内容，阳历、农历日期，节假日信息等'''
        x_pos = (4, 140, 276, 412, 548, 684, 820, 956 ) # 星期 列 X 坐标
        y_pos = (154, 234, 314, 394, 474, 554, 634)     # 周   行 Y 坐标
        x_span= 136 # 水平间隔
        y_span= 80  # 垂直间隔
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

    def button_action(self, kid, ishold):
        '''按键事件回调处理，调整日期供显示'''
        if (kid == 1):
            self.redraw = True
            self.draw_mday = 1
            self.draw_month = self.draw_month - 1
            if self.draw_month <= 0:
                self.draw_year = self.draw_year - 1
                self.draw_month = 12
            if self.draw_year <= 2020:
                self.draw_year = 2020
        else:
            self.redraw = True
            self.draw_mday = 1
            self.draw_month = self.draw_month + 1
            if self.draw_month >= 13:
                self.draw_year = self.draw_year + 1
                self.draw_month = 1
            if self.draw_year >= 2025:
                self.draw_year = 2025
        
        if ishold:
            self.entered = True
            
    async def startUILoop(self):
        '''UI 绘制任务'''
        self.draw_year, self.draw_month, self.draw_mday, *_ = time.localtime()
        # year, month, mday = 2024, 10, 22
        self.redraw = True
        
        if sys.platform == 'linux':
            while(self.epd.runable()):
                await asyncio.sleep(0.01)
                self.updateDisplay()
            sys.exit(0)
        else:
            #while(True):
            #    await asyncio.sleep(0.01)
            #    self.updateDisplay()
            
            self.updateDisplay() # 硬件上，绘完就休眠
            self.epd.deepSleep(APP_DEEP_SLEEP_CALENDAR_MS)
            
    async def buttonCheckLoop(self):
        '''按键处理任务'''
        KeyA.set_callback(self.button_action)    
        KeyB.set_callback(self.button_action)        
        while(True):
            await asyncio.sleep(0.01)
            KeyA.update_state()
            KeyB.update_state()
                    
    async def runTasks(self):
        '''创建/运行子任务'''
        t1 = asyncio.create_task(self.startUILoop())
        t2 = asyncio.create_task(self.buttonCheckLoop())
        await asyncio.gather(t1, t2)
        
    def start(self):
        """Run the weather station display loop"""
        log.info("Calendar Started")
        
        asyncio.run(self.runTasks())
        
    def updateDisplay(self):
        '''屏幕绘制'''
        if self.redraw:
            lunar = ulunar.Lunar(self.draw_year, self.draw_month, self.draw_mday)
            
            # self.epd.init() # if refresh multi times, uncomment this line.
            self.epd.clear()
            self.drawTitle(self.draw_year, self.draw_month, self.draw_mday, lunar)
            self.drawBody(self.draw_year, self.draw_month, self.draw_mday, lunar)
            self.epd.refresh() # this will do deep-sleep. use init() to refresh again.
            self.redraw = False
