# -*- coding: utf-8 -*-
'''
   qweather api by .NFC 2023/12/23
'''
 
import json, deflate
import requests

''' official website  https://www.qweather.com '''
'''      dev website  https://dev.qweather.com '''

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/5d'
url_api_yiyan = 'https://v1.hitokoto.cn/?encode=json&min_length=1&max_length=21'

qw_code_desc = {
    '200': "请求成功",
    '204': "地区不支持",
    '400': "参数错误",
    '401': "认证失败",
    '402': "余额不足",
    '403': "无访问权限",
    '404': "查询失败",
    '429': "请求过于频繁",
    '500': "无响应/超时",
}

def api_code(code:int) ->str :
    '''和风天气 API 错误码'''
    if code in qw_code_desc:
        return qw_code_desc[code]
    else:
        return '未知错误'

def requests_deflate(url):
    # print(f"[d] => {url}")
    r = requests.get(url, stream=True)
    d = deflate.DeflateIO(r.raw, deflate.GZIP)
    return json.load(d)

def get_location(api_type, api_key, city_kw='beijing') :
    if api_type == 'top':
        url_v2 = url_api_geo + api_type + '?range=cn&key=' + api_key
    else:
        url_v2 = url_api_geo + api_type + '?location=' + city_kw + "&key=" + api_key
    
    resp = requests_deflate(url_v2)
    if resp['code'] != '200':
        rcode = resp['code']
        raise RuntimeError(f'QW request loc failed {api_code(rcode)}')
    else:
        return resp

def get_air(city_id, api_key):
    url = url_api_air + '?location=' + city_id + "&key=" + api_key + '&lang=cn'
    resp = requests_deflate(url)
    if resp['code'] != '200':
        rcode = resp['code']
        raise RuntimeError(f'QW request air failed {api_code(rcode)}')
    else:
        return resp
        
def get(api_type, city_id, api_key):
    url = url_api_weather + api_type + '?location=' + city_id + "&key=" + api_key + '&lang=cn'
    resp = requests_deflate(url)
    if resp['code'] != '200':
        rcode = resp['code']
        raise RuntimeError(f'QW request failed {api_code(rcode)}')
    else:
        return resp

def get_city(city_kw):
    city = get_location('lookup', city_kw)['location'][0]
    
    city_id = city['id']
    district_name = city['name']
    city_name = city['adm2']
    province_name = city['adm1']
    country_name = city['country']

    return city_id, district_name, city_name, province_name, country_name

def now(city_id, api_key):
    '''实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    {
      "obsTime": "2020-06-30T21:40+08:00", 数据观测时间
      "temp": "24",  温度
      "feelsLike": "26", 体感温度
      "icon": "101", 图标
      "text": "多云", 天气状况
      "wind360": "123",  风向360角
      "windDir": "东南风", 风向
      "windScale": "1", 风力等级
      "windSpeed": "3", 风速
      "humidity": "72", 相对湿度 %
      "precip": "0.0", 累计降水量 mm
      "pressure": "1003", 压强 HPa
      "vis": "16", 能见度 Km
      "cloud": "10", 云量 %
      "dew": "21" 露点温度
    },'''
    result = get('now', city_id, api_key)
    return result['now']

def future(city_id, api_key):
    '''未来 7 天天气 https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
    {
      "fxDate": "2021-11-15",  预报日期
      "sunrise": "06:58",      日出时间
      "sunset": "16:59",       日落时间
      "moonrise": "15:16",     月升时间
      "moonset": "03:40",      月落时间
      "moonPhase": "盈凸月",    月相名称
      "moonPhaseIcon": "803",  月相图标
      "tempMax": "12",  最高温度
      "tempMin": "-1",  最低温度
      "iconDay": "101", 白天天气状况图标
      "textDay": "多云", 白天天气状况
      "iconNight": "150",  夜间天气状况图标
      "textNight": "晴",   夜间天气状况
      "wind360Day": "45",
      "windDirDay": "东北风",
      "windScaleDay": "1-2",
      "windSpeedDay": "3",
      "wind360Night": "0",
      "windDirNight": "北风",
      "windScaleNight": "1-2",
      "windSpeedNight": "3",
      "humidity": "65",  相对湿度 %
      "precip": "0.0", 总降水量 mm
      "pressure": "1020", 大气压强 HPa
      "vis": "25", 能见度 Km
      "cloud": "4", 云量 %
      "uvIndex": "3" 紫外线强度指数
    },
    '''
    result = get('7d', city_id, api_key)
    return result['daily']

def future_air(city_id, api_key):
    '''空气质量5天预报 [...] https://dev.qweather.com/docs/api/air/air-daily-forecast/
    {
      "fxDate": "2021-02-16",
      "aqi": "46",
      "level": "1",
      "category": "优",
      "primary": "NA"
    },
    '''
    result = get_air(city_id, api_key)
    return result['daily']

def hourly(city_id, api_key):
    '''24小时预报 [...] https://dev.qweather.com/docs/api/weather/weather-hourly-forecast/
    {
      "fxTime": "2021-02-17T05:00+08:00", 预报时间
      "temp": "-5",        温度
      "icon": "150",       图标
      "text": "晴",         天气状况
      "wind360": "352",     风向360角
      "windDir": "北风",    风向
      "windScale": "3-4",   风力等级
      "windSpeed": "16",    风速 KM/h
      "humidity": "14",     相对湿度 %
      "pop": "0",          报降水概率 %
      "precip": "0.0",     累计降水量 mm
      "pressure": "1026",  大气压强 百帕
      "cloud": "0",        云量 %
      "dew": "-29"         露点温度
    },
    '''
    result = get('24h', city_id, api_key)
    return result['hourly']

def yiyan() ->str:
    r = requests.get(url_api_yiyan)
    if r.status_code == 200:
        return r.json()['hitokoto']
    else:
        return '...'
