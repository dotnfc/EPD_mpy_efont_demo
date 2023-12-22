'''
  国家节假日安排数据生成工具
  基于 https://github.com/LKI/chinese-calendar/tree/master/chinese_calendar/scripts
  by .NFC 2023/12/21
'''

import datetime

# 2024 节假日安排
arrangement_reset_days = {
'1': (1, 2, 3),
'2': (10, 11, 12, 13, 14, 15, 16, 17),
'4': (4, 5, 6),
'5': (1, 2, 3, 4, 5),
'6': (10,),
'9': (15, 16, 17),
'10': (1, 2, 3, 4, 5, 6, 7),
}
arrangement_work_days = {
'2': (4, 18),
'4': (7, 28),
'5': (11,),
'9': (14, 29),
'10': (12,),
}

class scheduleHoliday():
    def __init__(self):
        self.workDays = {}
        self.resetDays = {}

        self.isRest = False
        self.start_date = datetime.date(2002, 9, 1)
        self.year = 2000
        
    def appendList(self, month, date, isRest:bool):
        if isRest:
            if month not in self.resetDays:
                self.resetDays[month] = []
            self.resetDays[month].append(date)
        else:
            if month not in self.workDays:
                self.workDays[month] = []
            self.workDays[month].append(date)
            
    def genList(self):
        restDaysList = {}
        workDaysList = {}
        
        for month, day_list in sorted(self.resetDays.items()):
            restDaysList[str(month)] = (tuple(day_list))
            
        for month, day_list in sorted(self.workDays.items()):
            workDaysList[str(month)] = (tuple(day_list))
            
        return restDaysList, workDaysList
    
    def printList(self, msg: str, days: dict):
        print(msg)
        for month, dates_tuple in days.items():
            print(f"        '{month}': {dates_tuple},")
        
        print("    }")
        print("}")

    def work(self, month, day):
        self.isRest = False
        self.start_date = datetime.date(year=self.year, month=month, day=day)
        self.appendList(month, day, False) # add this day in anyway
        return self

    def rest(self, month, day):
        self.isRest = True
        self.start_date = datetime.date(year=self.year, month=month, day=day)
        self.appendList(month, day, True)
        return self
    
    def to(self, month, day):
        end_date = datetime.date(year=self.year, month=month, day=day)
        if end_date <= self.start_date:
            raise ValueError("end date should be after start date")
        for i in range((end_date - self.start_date).days):
            the_date = self.start_date + datetime.timedelta(days=i + 1)
            self.appendList(the_date.month, the_date.day, self.isRest)
        return self
    
    def _2024(self):
        """https://www.gov.cn/zhengce/content/202310/content_6911527.htm
        一、元旦：1月1日放假，与周末连休。
        二、春节：2月10日至17日放假调休，共8天。2月4日（星期日）、2月18日（星期日）上班。
        三、清明节：4月4日至6日放假调休，共3天。4月7日（星期日）上班。
        四、劳动节：5月1日至5日放假调休，共5天。4月28日（星期日）、5月11日（星期六）上班。
        五、端午节：6月10日放假，与周末连休。
        六、中秋节：9月15日至17日放假调休，共3天。9月14日（星期六）上班。
        七、国庆节：10月1日至7日放假调休，共7天。9月29日（星期日）、10月12日（星期六）上班。
        """
        self.year = 2024
        self.rest(1, 1).to(1, 3)
        self.rest(2, 10).to(2, 17).work(2, 4).work(2, 18)
        self.rest(4, 4).to(4, 6).work(4, 7)
        self.rest(5, 1).to(5, 5).work(4, 28).work(5, 11)
        self.rest(6, 10)
        self.rest(9, 15).to(9, 17).work(9, 14)
        self.rest(10, 1).to(10, 7).work(9, 29).work(10, 12)

    def _2023(self):
        """ http://www.gov.cn/zhengce/content/2022-12/08/content_5730844.htm
        一、元旦：2022年12月31日至2023年1月2日放假调休，共3天。
        二、春节：1月21日至27日放假调休，共7天。1月28日（星期六）、1月29日（星期日）上班。
        三、清明节：4月5日放假，共1天。
        四、劳动节：4月29日至5月3日放假调休，共5天。4月23日（星期日）、5月6日（星期六）上班。
        五、端午节：6月22日至24日放假调休，共3天。6月25日（星期日）上班。
        六、中秋节、国庆节：9月29日至10月6日放假调休，共8天。10月7日（星期六）、10月8日（星期日）上班。
        """
        self.year = 2023
        self.rest(1, 1).to(1, 2)
        self.rest(1, 21).to(1, 27).work(1, 28).work(1, 29)
        self.rest(4, 5)
        
        self.rest(4, 29).to(5, 3).work(4, 23).work(5, 6)
        self.rest(6, 22).to(6, 24).work(6, 25)
        self.rest(9, 29).to(10, 6).work(10, 7).work(10, 8)

def main():
    date_manager = scheduleHoliday()
    #date_manager._2023()
    date_manager._2024()

    rest, work = date_manager.genList()
    print(f"'{date_manager.year}': {{       # {date_manager.year} 节假日安排")
    date_manager.printList(f"    'rest':  {{  # 假 ", rest)
    date_manager.printList("    'work':  {{  # 班", work)
    
if __name__ == "__main__":
    main()