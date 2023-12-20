# from https://github.com/OPN48/cnlunar/tree/master/cnlunar

legalsolarTermsHolidayDic={'清明':'清明节'}
legalHolidaysDic={(1,1):'元旦节',(5,1):'国际劳动节',(10,1):'国庆节'}
legalLunarHolidaysDic={(1,1):'春节',(5,5):'端午节',(8,15):'中秋节'}

otherHolidaysList=[
    {8: '周恩来逝世', 10: '中国公安110宣传日', 21: '列宁逝世', 26: '国际海关日'}, #1月
    {2: '世界湿地日', 4: '世界抗癌日', 7: '京汉铁路罢工纪念', 10: '国际气象节', 14: '情人节', 19: '邓小平逝世', 21: '国际母语日', 24: '第三世界青年日'},
    {1: '国际海豹日', 3: '全国爱耳日', 5: '周恩来诞辰纪念日,中国青年志愿者服务日', 6: '世界青光眼日', 8: '国际劳动妇女节', 12: '孙中山逝世纪念日,中国植树节', 14: '马克思逝世', 15: '国际消费者权益日', 17: '国际航海日', 18: '全国科技人才活动日', 21: '世界森林日,世界睡眠日', 22: '世界水日', 23: '世界气象日', 24: '世界防治结核病日'},
    {1: '国际愚人节', 2: '国际儿童图书日', 7: '世界卫生日', 22: '列宁诞辰纪念日', 23: '世界图书和版权日', 26: '世界知识产权日'},
    {3: '世界新闻自由日', 4: '中国青年节', 5: '马克思诞辰纪念日', 8: '世界红十字日', 11: '世界肥胖日', 23: '世界读书日', 27: '上海解放日', 31: '世界无烟日'},
    {1: '国际儿童节', 5: '世界环境日', 6: '全国爱眼日', 8: '世界海洋日', 11: '中国人口日', 14: '世界献血日'},
    {1: '中国共产党诞生日,香港回归纪念日', 7: '抗日战争纪念日', 11: '世界人口日'},
    {1: '中国人民解放军建军节', 5: '恩格斯逝世', 6: '国际电影节', 12: '国际青年日', 22: '邓小平诞辰'},
    {3: '抗日战争胜利', 8: '世界扫盲日', 9: '毛泽东逝世', 10: '中国教师节', 14: '世界清洁地球日', 18: '“九·一八”事变', 20: '全国爱牙日', 21: '国际和平日', 27: '世界旅游日'},
    {4: '世界动物日', 10: '辛亥革命', 13: '中国少年先锋队', 25: '抗美援朝'},
    {12: '孙中山诞辰', 28: '恩格斯诞辰'},
    {1: '世界艾滋病日', 12: '西安事变', 13: '南京大屠杀', 24: '平安夜', 25: '圣诞节', 26: '毛泽东诞辰'} #12月
]

def get_otherHolidays(year, month, day):
    import datetime
    date = datetime.datetime(year, month, day, 10, 30)
    tempList, y, m, d, wn, w = [], date.year, date.month, date.day, date.isoWeekNumber(), date.weekday()
    eastHolidays = {5: (2, 7, '母亲节'), 6: (3, 7, '父亲节')}
    if m in eastHolidays:
        t1dwn = datetime.datetime(y, m, 1).isoWeekNumber()
        if ((wn - t1dwn + 1), w) == (eastHolidays[m][0], eastHolidays[m][1]):
            tempList.append(eastHolidays[m][2])
    holidayDic = otherHolidaysList[m - 1]
    if d in holidayDic:
        tempList.append(holidayDic[d])
    if tempList != []:
        return ','.join(tempList)
    else:
        return ''

