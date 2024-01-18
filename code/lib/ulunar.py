# lunar infomation from solar(yy-mm-dd)
# based on https://github.com/hungtcs/traditional-chinese-calendar-database
# by .NFC 2023/08/30
# 
# NOTE to save fw size, we have lunar_data since 1980-01-01 only!!!
#      see script/lunar/convert-to-binary.js

import time, sys
from efore.lunar_data import _lunar_data

# 天干地支之地支速查表<=>生肖
ZODIAC = [
    "鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"
]

# 天干地支-天干速查表
TIAN_GAN = [
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"
]

# 天干地支-地支速查表
DI_ZHI = [
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
]

# static const char* GAN_ZHI[60] = {
# 	"甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
# 	"甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
# 	"甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
# 	"甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
# 	"甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
# 	"甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥",
# };

# # 月份转农历称呼速查表 nStr3
# static const char* LUNAR_MONTHS[12] = {
# 	"正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"
# };

LUNAR_MONTHS_ALIAS = [
    "正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"
]

LUNAR_DATES = [
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十",
]

# 24节气速查表
JIE_QI = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
    "春节", "端午", "中秋"
]

class Lunar():
    def __init__(self, year, month, day):
        '''阳历转阴历
        @param year, 年份
        @param month, 月份
        @param day, 日期
        '''
        tm_now = (year, month, day, 0, 0, 0, 0, 0)
        now = time.mktime(tm_now)
        
        # for unix,  1970/01/01 08:00:00
        # for esp32, 2000/01/01 00:00:00
        
        if sys.platform == 'linux':
            start = 315504000  # 1980-01-01 00:00:00
            offset = (now - start) // (60 * 60 * 24) * 5
        else: # esp32, stm32
            # t80 = time.mktime((1980, 1, 1, 0, 0, 0, 0, 0, 0))
            # t2k = time.mktime((2000, 1, 1, 0, 0, 0, 0, 0, 0))
            # (t2k - t80 ) // (60 * 60 * 24) * 5 = 36525

            offset = 36525 + (now // (60 * 60 * 24) * 5)
            
        if offset < 0 or offset > len(_lunar_data) - 5:
            raise RuntimeError("invlaid dateTime to get lunar!")
        
        byte0 = _lunar_data[offset + 0]
        byte1 = _lunar_data[offset + 1]
        byte2 = _lunar_data[offset + 2]
        byte3 = _lunar_data[offset + 3]
        byte4 = _lunar_data[offset + 4]
        
        self.year = byte0 + 1900
        self.month = byte1 >> 4
        self.date = ((byte1 & 0x0F) << 1) + (byte2 >> 7)
        self.tiangan = (byte2 >> 3) & 0x0F
        self.dizhi = ((byte2 << 1) & 0x0F) + (byte3 >> 7)
        self.lunarMonth = (byte3 & 0x7F) >> 3
        self.lunarDate = ((byte3 & 0x07) << 2) + (byte4 >> 6)
        self.leap = ((byte4 >> 5) & 0x01) == 0x01  # 闰月？
        self.solarTerm = byte4 & 0x1F  # 24 节气

        # !!! lunarMonth, lunarDate, solarTerm are all 1 based.
        
        # 四大传统节日: 春节、清明节、端午节、中秋节
        if self.lunarMonth == 1 and self.lunarDate == 1:    # 正月初一，春节
            self.solarTerm = 25
        elif self.lunarMonth == 5 and self.lunarDate == 5:  # 五月初五，端午
            self.solarTerm = 26
        elif self.lunarMonth == 8 and self.lunarDate == 15: # 八月十五，中秋
            self.leap = 1
            self.solarTerm = 27

    def getGanZhi(self):    
        '''获取干支信息'''
        gan_zhi = TIAN_GAN[self.tiangan] + DI_ZHI[self.dizhi]
        return gan_zhi

    def getZodiac(self):
        '''获取生肖年份信息'''
        zodiac = ZODIAC[self.dizhi]
        return zodiac
        
    def getMonth(self):
        '''获取农历月份信息'''
        month = LUNAR_MONTHS_ALIAS[self.lunarMonth - 1]
        return month

    def getDate(self):
        '''获取农历日期信息'''
        if self.lunarDate > 1:
            date = LUNAR_DATES[self.lunarDate - 1]
        else:
            date = self.getMonth()
        return date

    def getTerm(self):
        '''获取二十四节气信息'''
        term = JIE_QI[self.solarTerm - 1]
        return term
    
if __name__ == "__main__":
    import utime
    # year, month, day, hour, minute, second, ms, dayinyear = utime.localtime()
    year, month, day, *_ = utime.localtime()
    lunar = Lunar(year, month, day)
    print(lunar.getGanZhi())
    print(lunar.getZodiac())
    print(lunar.getMonth())
    print(lunar.getDate())
    if lunar.leap:
        print(lunar.getTerm())
    
    pass