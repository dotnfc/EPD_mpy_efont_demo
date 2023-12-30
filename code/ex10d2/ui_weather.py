"""
    [eForeDemo] 天气页面测试
    by .NFC 2023/12/23
"""
import time
#import urequests as requests
import requests
from  wifi_sta_helper import wifiHelper
import logging as log
from display3c import *
from efont import *
from efore.qw_icons import *
from efore.city_list import china_citys
from .settings import *
import datetime
#from .qw_api import *
from .qw_api_fake import *
import ulunar, holidays, birthdays
from .button import *
import gc

_week_day_number_cn = ("一", "二", "三", "四", "五", "六", "日")
_weather_chart_bar_xpos = [316, 445, 574, 703, 832]

class uiWeather(object):
        
    def __init__(self,**kwargs):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE, EPD_BLACK)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.loadFont("icons")
        self.epd.loadFont("7seg")
        self.epd.loadFont("swissel")
        self.epd.selectFont("simyou")
        
        self.qw_now = now(QW_API_CITY, QW_API_KEY)
        self.qw_future = future(QW_API_CITY, QW_API_KEY)
        self.qw_future_air = future_air(QW_API_CITY, QW_API_KEY)
        self.qw_hourly = hourly(QW_API_CITY, QW_API_KEY)
        
    def start(self):
        """Run the weather station display loop"""
        log.info("Weather Started")
        wifiHelper.connect(WIFI_SSID, WIFI_PASS)
        
        year, month, mday, hour, minute, second, weekday, yearday, *_ = time.localtime()
        # year, month, mday = 2024, 10, 22
        lunar = ulunar.Lunar(year, month, mday)
        
        reDraw = True
        while self.epd.runable():
            if reDraw:
                self.epd.clear()
                self.drawLines()
                self.drawTitle(year, month, mday, weekday, lunar)
                self.drawBody(year, month, mday, lunar)
                self.drawFooter()
                self.epd.refresh()
                reDraw = False
            
            if KeyA.is_pressed():
                month = month - 1
                if month <= 0:
                    year = year - 1
                    month = 12
                if year <= 2020:
                    year = 2020
                    continue
                
                lunar = ulunar.Lunar(year, month, mday)
                reDraw = True
            elif KeyB.is_pressed():
                month = month + 1
                if month >= 13:
                    year = year + 1
                    month = 1
                if year >= 2025:
                    year = 2025
                    continue
                
                lunar = ulunar.Lunar(year, month, mday)
                reDraw = True
            
            if KeyA.is_holding() or KeyB.is_holding():
                break
            time.sleep_ms(100)

        self.epd.deepSleep(15000)

    def drawLines(self):
        self.epd.setColor(EPD_RED, EPD_WHITE)
        
        # 水平线
        self.epd.line_3c(0, 160, self.epd.WIDTH-1, 160, 1)
        self.epd.line_3c(0, 200, self.epd.WIDTH-1, 200, 1)
        self.epd.line_3c(0, 402, 315-1, 402, 1)
        self.epd.line_3c(0, 604, self.epd.WIDTH-1, 604, 1)
        self.epd.line_3c(316, 120, self.epd.WIDTH-1, 120, 1)
        
        # 竖直线
        self.epd.line_3c(315, 0, 315, self.epd.HEIGHT -1, 1)
        
    def drawTitleToday(self):        
        # 更新时间
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("7seg")
        
        year, month, mday, hour, minute, *_ = time.localtime()
        sNow = "%02d:%02d" % (hour, minute)
        self.epd.drawText(324, 0, 230, 160, ALIGN_LEFT, sNow, 120)
        
        self.epd.selectFont("icons") # 刷新图标
        self.epd.drawText(604, 10, 30, 30, ALIGN_LEFT, ICO_ARROW_REPEAT2, 24)
        
        # 当天天气图标
        self.epd.selectFont("icons")
        self.epd.setColor(EPD_RED, EPD_WHITE)
        ico = self.getQWIcon(self.qw_now['icon'])
        self.epd.drawText(660, 10, 230, 160, ALIGN_LEFT, ico, 96) # 340
        
        # 天气现象
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou") # 470
        strTemp = self.qw_now['temp'] + "°" #  + self.qw_now['feelsLike'] + "°"
        self.epd.drawText(800, 16, 40, 40, ALIGN_LEFT, "天气 " + self.qw_now['text'], 24)
        self.epd.drawText(800, 48, 40, 40, ALIGN_LEFT, "温度 " + strTemp, 24)
        self.epd.drawText(800, 80, 40, 40, ALIGN_LEFT, "湿度 " + self.qw_now['humidity'] + "%", 24)
        
        # 风
        # self.epd.drawText(800, 16, 40, 40, ALIGN_LEFT, "风向 " + self.qw_now['windDir'], 24)
        # self.epd.drawText(800, 48, 40, 40, ALIGN_LEFT, "风力 " + self.qw_now['windScale'], 24)
        # self.epd.drawText(800, 80, 40, 40, ALIGN_LEFT, "风速 " + self.qw_now['windSpeed'] + "Km/h", 24)
        
        # 其他
        # self.epd.drawText(800, 16, 40, 40, ALIGN_LEFT, "体感  " + self.qw_now['feelsLike'] + "°", 24)
        # self.epd.drawText(800, 48, 40, 40, ALIGN_LEFT, "压强  " + self.qw_now['pressure'] + "HPa", 24)
        # self.epd.drawText(800, 80, 40, 40, ALIGN_LEFT, "能见度 " + self.qw_now['vis'] + "Km", 24)
        

        # 日出、日落
        self.epd.selectFont("simyou")
        self.epd.drawText(360, 130, 40, 40, ALIGN_LEFT, self.qw_future[0]['sunrise'], 24)
        self.epd.drawText(480, 130, 40, 40, ALIGN_LEFT, self.qw_future[0]['sunset'], 24)

        self.epd.selectFont("icons")
        self.epd.drawText(330, 130, 40, 40, ALIGN_LEFT, ICO_SUNRISE_FILL, 24)
        self.epd.drawText(450, 130, 40, 40, ALIGN_LEFT, ICO_SUNSET_FILL, 24)

        # 室外温度、湿度
        self.epd.selectFont("simyou")
        self.epd.drawText(600, 130, 40, 40, ALIGN_LEFT, self.qw_now['temp'] + "°", 24)
        self.epd.drawText(690, 130, 40, 40, ALIGN_LEFT, self.qw_now['humidity'] + '%', 24)
                
        self.epd.selectFont("icons")
        self.epd.drawText(574, 130, 40, 40, ALIGN_LEFT, ICO_TEMP, 24)
        self.epd.drawText(660, 130, 40, 40, ALIGN_LEFT, ICO_HUMIDITY_SOLID, 24)
        
        # 室内温度、湿度
        self.epd.selectFont("simyou")
        self.epd.drawText(790, 130, 40, 40, ALIGN_LEFT, self.getIndoorTemp(), 24)
        self.epd.drawText(882, 130, 40, 40, ALIGN_LEFT, self.getIndoorHumidity(), 24)
                
        self.epd.selectFont("icons")
        self.epd.drawText(758, 124, 40, 40, ALIGN_LEFT, ICO_HOUSE_THERMOMETER, 30)
        self.epd.drawText(850, 124, 40, 40, ALIGN_LEFT, ICO_HOUSE_HUMIDITY, 30)
            
    def drawTitle(self, year, month, mday, weekday, lunar):
        '''顶部标题栏'''
        # 显示 日子 年/月份
        self.epd.selectFont("swissel")
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(0, 0, 315, 159, 1, True)
        self.epd.setColor(EPD_WHITE, EPD_RED)
        s = "%2d" % (mday)
        self.epd.drawText(5, 0, 135, 140, ALIGN_LEFT, s, 140)
            
        self.epd.selectFont("simyou")
        s = "星期%s" % _week_day_number_cn[weekday]
        self.epd.drawText(190, 20, 120, 48, ALIGN_RIGHT, s, 24)
        s = "%4d年" % (year)
        self.epd.drawText(190, 50, 120, 48, ALIGN_RIGHT, s, 24)
        s = "%2d月" % (month)
        self.epd.drawText(190, 90, 120, 48, ALIGN_RIGHT, s, 48)
        
        # 农历
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(0, 160, 315, 40, 1, True)
        
        ganzhi = lunar.getGanZhi()
        shengxiao = lunar.getZodiac()
        ymon = lunar.getMonth()
        yday = lunar.getDate()
        s = "农历 %s(%s)年 %s%s" % (ganzhi, shengxiao, ymon, yday)
        self.epd.setColor(EPD_WHITE, EPD_RED)
        self.epd.drawText(1, 168, 315 - 1, 48, ALIGN_CENTER, s, 24)
        
        # 日期条
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(316, 161, self.epd.WIDTH - 315 - 1, 39, 1, True)
        self.epd.setColor(EPD_WHITE, EPD_RED)
        self.epd.drawText(_weather_chart_bar_xpos[0], 168, 128, 48, ALIGN_CENTER, "今天", 24)
        self.epd.drawText(_weather_chart_bar_xpos[1], 168, 128, 48, ALIGN_CENTER, "明天", 24)
        self.epd.drawText(_weather_chart_bar_xpos[2], 168, 128, 48, ALIGN_CENTER, "后天", 24)
        
        sWeek = "星期" + _week_day_number_cn[self.getDateFromString(self.qw_future[3]['fxDate']).weekday()]
        self.epd.drawText(_weather_chart_bar_xpos[3], 168, 128, 48, ALIGN_CENTER, sWeek, 24)
        
        sWeek = "星期" + _week_day_number_cn[self.getDateFromString(self.qw_future[4]['fxDate']).weekday()]
        self.epd.drawText(_weather_chart_bar_xpos[4], 168, 128, 48, ALIGN_CENTER, sWeek, 24)
    
        self.drawTitleToday()
        
    def getDateFromString(self, date_str):
        # date_str = "2021-11-15"
        year, month, day = map(int, date_str.split('-'))
        return datetime.datetime(year, month, day)

    def getHoursListFromString(self, fx_str):
        calculate_time = lambda hour, val: (hour + val) if (hour + val) <= 24 else (hour + val - 24)
        
        # date_str = "2023-12-28T18:00+08:00"
        hour = int(fx_str[11:13]) # get '18'
        hours = []
        hours.append(hour)
        hours.append(calculate_time (hour, 4))
        hours.append(calculate_time (hour, 4 + 5))
        hours.append(calculate_time (hour, 4 + 5 + 5))
        hours.append(calculate_time (hour, 4 + 5 + 5 + 5))
        hours.append(calculate_time (hour, 4 + 5 + 5 + 5 + 4))
        return hours
    
    def drawTemperatureChart(self, x, y):
        
        self.epd.selectFont("simyou")
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        
        # 取 5 天内的最高温、最低温
        tempLow = int(self.qw_future[0]['tempMin'])
        tempHigh = int(self.qw_future[0]['tempMax'])
        for i in range(1, 5):
            low = int(self.qw_future[i]['tempMin'])
            if tempLow > low:
                tempLow = low
                
            high = int(self.qw_future[i]['tempMax'])
            if tempHigh < high:
                tempHigh = high
        
        Temp_delta = tempHigh - int(tempLow)
        fontH = 24
        CHART_YHIGH = 304   # 图谱 Y 上部
        CHART_YLOW = 498    # 图谱 Y 底部        
        yLow = CHART_YLOW - 24
        yHigh = CHART_YHIGH + 24
        yDelta = abs(yHigh - yLow)
    
        x = 380
        # 绘制低温曲线
        dayInfo = []
        for i in range(0, 5):
            dayInfo.append(self.fill_day_info_temp_low(i, x, tempLow, Temp_delta, yLow, yDelta))
            x += 128
        self.draw_line_chart(dayInfo, False)

        # 绘制高温曲线
        x = 380
        dayInfo = []
        for i in range(0, 5):
            dayInfo.append(self.fill_day_info_temp_high(i, x, tempLow, Temp_delta, yLow, yDelta))
            x += 128
        self.draw_line_chart(dayInfo, True)
        
    def drawOneDay(self, x, y, futureDay, futureAir):
        self.epd.selectFont("simyou")
        
        date = self.getDateFromString(futureDay['fxDate'])
        
        # 日期
        sDate = f"{date.month}/{date.day}"
        self.epd.drawText(x, y, 128, 48, ALIGN_CENTER, sDate, 24)
        
        # 白天/夜晚天气
        self.epd.drawText(x, 236, 128, 48, ALIGN_CENTER, futureDay['textDay'], 24)
        self.epd.drawText(x, 544, 128, 48, ALIGN_CENTER, futureDay['textNight'], 24)
        
        # 空气质量
        self.epd.drawText(x, 572, 128, 48, ALIGN_CENTER, futureAir['category'], 24)
        
        # 白天/夜晚天气图标
        self.epd.selectFont("icons")
        self.epd.drawText(x, 270, 128, 40, ALIGN_CENTER, self.getQWIcon(futureDay['iconDay']), 24)
        self.epd.drawText(x, 510, 128, 40, ALIGN_CENTER, self.getQWIcon(futureDay['iconNight']), 24)
        
    def drawBody(self, year, month, mday, lunar):
        
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        # 未来 5 天温度折线图-数据准备、绘制天气图标
        x = 316
        y = 210
        for i in range(0, 5):
            self.drawOneDay(x, y, self.qw_future[i], self.qw_future_air[i])
            x = x + 128
        
        # 未来 5 天温度折线图
        self.drawTemperatureChart(x, y)
        
        # 左侧 24 小时曲线
        self.drawTempHumidityChart(x, y)
        
    def drawTempHumidityChart(self, x, y):
        '''左侧 24 小时曲线'''
        tempL, tempH = self.get24HTempLowHigh()        
        x_marks = self.getHoursListFromString(self.qw_hourly[0]['fxTime'])
        tempL, tempH, y_marks = self.genTempMarkersList(tempL, tempH)
        x_width = 254  # X 轴长度
        y_height = 140 # Y 轴高度
        
        # 绘制坐标轴
        self.drawAxis("24小时-温度曲线", 38, 376, x_width, y_height, x_marks, y_marks)
        self.drawAxis("24小时-湿度曲线", 38, 580, x_width, y_height, x_marks, [0, 20, 40, 60, 80, 100])
        
        # 绘制曲线
        self.draw24HTempChart(38, 376, tempL, tempH, x_width, y_height)
        self.draw24hHumidityChart(38, 580, x_width, y_height)
    
    def draw24hHumidityChart(self, x, y, x_width, y_height):
        '''左侧绘制 24 小时湿度曲线'''        
        hdtL = 0
        hdtH = 100
        hdtD = hdtH - hdtL
        yLow = y
        yDelta = y_height - 24 # drop top unused pixels
        xw = x_width // 23
        _x = -1
        _y = -1
        for i in range(0, 24):
            txt = self.qw_hourly[i]['humidity']
            xx = x
            yy = self.calc_y_pos(int(txt), hdtL, hdtD, yLow, yDelta)
            x += xw
            
            if _x != -1:
                self.epd.line_3c(_x, _y, xx, yy, 1)
            
            _x = xx
            _y = yy

    def draw24HTempChart(self, x, y, tempL, tempH, x_width, y_height):
        '''绘制 24 小时温度曲线'''        
        tempDelta = tempH - tempL
        yLow = y
        yDelta = y_height
        xw = x_width // 23
        _x = -1
        _y = -1
        for i in range(0, 24):
            txt = self.qw_hourly[i]['temp']
            xx = x
            yy = self.calc_y_pos(int(txt), tempL, tempDelta, yLow, yDelta)
            x += xw
            
            if _x != -1:
                self.epd.line_3c(_x, _y, xx, yy, 1)
            
            _x = xx
            _y = yy
        
    def drawFooter(self):
        '''绘制底部栏'''
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.rect_3c(0, 604, 315, 639, 1, True)
        
        # 定位图标
        self.epd.setColor(EPD_WHITE, EPD_RED)        
        self.epd.selectFont("icons")
        self.epd.drawText(2, 610, 40, 40, ALIGN_LEFT, ICO_GEOALT, 24)
        
        # 电量图标
        self.epd.drawText(254, 592, 60, 60, ALIGN_RIGHT, self.getBatInfo(), 54)
        
        # 城市
        city = china_citys[QW_API_CITY]
        self.epd.selectFont("simyou")
        self.epd.drawText(32, 610, 260, 48, ALIGN_LEFT, city, 24)
        
        # 一句话
        self.epd.setColor(EPD_RED, EPD_WHITE)
        self.epd.selectFont("icons")
        self.epd.drawText(320, 610, 40, 40, ALIGN_LEFT, ICO_BELL, 24)
        
        self.epd.selectFont("simyou")
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.line_3c(350, 610, 350, 614, 1)
        self.epd.line_3c(350, 616, 350, 620, 1)
        self.epd.line_3c(350, 622, 350, 628, 1)
        self.epd.line_3c(350, 630, 350, 634, 1)
        self.epd.drawText(360, 610, 645 - 1, 48, ALIGN_LEFT, yiyan(), 22)
    
    def genTempMarkersList(self, low, high):
        '''依据高低温值，产生坐标值列表'''
        
        if high - low < 6:
            center = (high - low) // 2
            high = center + 3
            low = center - 3 
        
        step = (high - low + 5) // 6
        
        markers = [low, low + step, low + 2 * step, low + 3 * step, low + 4 * step, low + 5 * step]
        high = low + step * 6  # 更新逻辑上的 high
        return low, high, markers
            
    def get24HTempLowHigh(self):
        '''依据24小时数据，获取高低温'''
        tempL = int(self.qw_hourly[0]['temp'])
        tempH = tempL

        for i in range(1, 24):
            temp = int(self.qw_hourly[i]['temp'])
            if tempL > temp:
                tempL = temp
            if tempH < temp:
                tempH = temp

        return tempL, tempH
                
    def getBatInfo(self):
        return ICO_BATE6
    
    def getIndoorTemp(self):
        return "-15°"
    
    def getIndoorHumidity(self):
        return "33.6%"
        
    def getQWIcon(self, index):
        '''依据索引获取天气图标'''
        if index in qw_icons:
            return qw_icons[index]
        return ICO_NA


    # - - - - - - - - - - - - - - -   < CHART_YHIGH
    # -----------------------------   < yHigh Temp_high
    # 
    #               *     <--------   yPos  Temp_pos
    # 
    # -----------------------------   < yLow  Temp_low
    # 
    # - - - - - - - - - - - - - - -   < CHART_YLOW
    # 
    #  Temp_pos - Temp_low      | yPos - yLow |        yLow - yPos
    # ---------------------- = ----------------- ==== --------------
    # Temp_high - Temp_low      | yHigh - yLow |       yLow - yHigh
    # 
    #      <Temp_delta>                                  <yDelta>
    #
    def calc_y_pos(self, temp_pos, temp_low, temp_delta, y_low, y_delta) ->int:
        temp_pos = int(temp_pos)
        y_pos = abs(y_delta * (temp_pos - temp_low) / temp_delta - y_low)
        return int(y_pos)

    def fill_day_info_temp_low(self, i, x, temp_low, temp_delta, y_low, y_delta):
        day_info = {}
        day_info['x'] = x
        day_info['y'] = self.calc_y_pos(self.qw_future[i]['tempMin'], temp_low, temp_delta, y_low, y_delta)
        day_info['temp'] = self.qw_future[i]['tempMin']
        return day_info
    
    def fill_day_info_temp_high(self, i, x, temp_low, temp_delta, y_low, y_delta):
        day_info = {}
        day_info['x'] = x
        day_info['y'] = self.calc_y_pos(self.qw_future[i]['tempMax'], temp_low, temp_delta, y_low, y_delta)
        day_info['temp'] = self.qw_future[i]['tempMax']
        return day_info
    
    def draw_line_chart(self, days_info, txtUp:bool):
        # 画点
        for day_info in days_info:
            self.epd.ellipse_3c(day_info['x'], day_info['y'], 3, 3, 1, True)

        # 画线
        for i in range(len(days_info) - 1):
            left = days_info[i]
            right = days_info[i + 1]
            self.epd.line_3c(left['x'], left['y'], right['x'], right['y'], 1)           

        # 显示度数
        i = 0
        for day_info in days_info:
            str_wd = day_info['temp'] + "°"
            if txtUp == True:
                y = day_info['y'] - 24 - 3
            else:
                y = day_info['y'] + 3

            self.epd.drawText(_weather_chart_bar_xpos[i], y, 128, 30, ALIGN_CENTER, str_wd, 24)
            i = i + 1
    
    def drawAxis(self, title, x, y, cx, cy, x_marks, y_marks):
        '''绘制24小时数据的坐标轴'''
        self.epd.drawText(0, y - 160, 314, 30, ALIGN_CENTER, title, 16)
        
        self.epd.line_3c(x, y, x + cx, y, 1)  # 水平坐标轴
        self.epd.line_3c(x, y, x, y - cy , 1) # 垂直坐标轴

        # 水平坐标
        for i in range(0, 6):
            xx = x + i * 50
            self.epd.drawText(xx- 16, y + 2, 30, 30, ALIGN_CENTER, str(x_marks[i]), 16)
            self.epd.line_3c(xx, y, xx, y-2, 1)
                    
        # 垂直坐标
        for i in range(1, 6):
            self.epd.drawText(4, y - i * 24 - 12, 30, 30, ALIGN_RIGHT, str(y_marks[i]), 16)
            self.epd.dot_hline_3c(x, y - i * 24, x + 250, 1)
