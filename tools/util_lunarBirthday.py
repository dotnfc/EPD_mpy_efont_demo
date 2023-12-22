'''
   家人生日列表
'''

# 农历日期到数字日期的映射字典
lunar_to_numeric = {
    '正月': 1, '二月': 2, '三月': 3, '四月': 4, '五月': 5, '六月': 6,
    '七月': 7, '八月': 8, '九月': 9, '十月': 10, '冬月': 11, '腊月': 12,
    '初一': 1, '初二': 2, '初三': 3, '初四': 4, '初五': 5, '初六': 6,
    '初七': 7, '初八': 8, '初九': 9, '初十': 10, '十一': 11, '十二': 12,
    '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18,
    '十九': 19, '二十': 20, '廿一': 21, '廿二': 22, '廿三': 23, '廿四': 24,
    '廿五': 25, '廿六': 26, '廿七': 27, '廿八': 28, '廿九': 29, '三十': 30,
    '廿': 20, 
}

def lunar_to_numeric_date(lunar_date:str):
    # 分割农历日期中的月份和日
    month, day = lunar_date.split('月')

    month += '月'
    # 查找字典中的映射关系，如果找不到，返回 None
    numeric_month = lunar_to_numeric.get(month)
    numeric_day = lunar_to_numeric.get(day)

    # 如果月份和日都找到了，则返回转换后的数字日期，否则返回 None
    if numeric_month is not None and numeric_day is not None:
        return numeric_month, numeric_day
    else:
        return 0, 0

# 多行农历日期
days = """
张三	四月廿一
李四	正月廿七
王麻子	三月廿四
周五	正月初六
邹武	正月初六
汤正	冬月初五
"""

def append_person(personList, newPerson):
    
    for i in range(len(personList)):
        (day, name) = personList[i]
        
        # 当天有人过生日
        if day == newPerson[0]:
            name += "," + newPerson[1]    # 人名追加
            personList[i] = (day, name)
            return personList

    # 不重复的情况下，追加新人
    personList.append(newPerson)
    return personList

# 将多行农历日期按行分割
lunar_dates = days.strip().split('\n')

birthdays = {}

# 遍历农历日期并输出对应的数字日期
for line in lunar_dates:
    name, lunar_date = line.split('\t')
    month, day = lunar_to_numeric_date(lunar_date)
    if month == 0 or day == 0:
        print(f"{name} 转换失败")
    
    if month not in birthdays:
        birthdays[month] = []
    
    birthdays[month] = append_person (birthdays[month], (day, name))
    # item = (day, name)
    # birthdays[month].append(item)
    
for name, info in sorted(birthdays.items()):
    sortedInfo = sorted(info, key=lambda x: x[0])
    print(f"'{name}': {sortedInfo},")   

# 输出格式
# family = {
#     3: [(26, '名1'), (27, '名2')]
# }

