# global configuration
import io, json, deflate

try:
    with open("efore.json", 'r') as file:
        config_data = json.load(file)
        print("Configuration data:", config_data)
        
    HOME_PAGE = int(config_data['page'])
        
    # QWeather API Key, get it from: https://dev.qweather.com/
    QW_API_KEY = config_data['qw_key']
    QW_API_CITY = config_data['qw_city']
    
    # WiFi access info
    WIFI_SSID = config_data['wifi_ssid']
    WIFI_PASS = config_data['wifi_pass']

    # AP-IF
    AP_NAME = config_data['ap_name']
    AP_PASS = config_data['ap_pass']

except OSError as e:
    print("use the default")
    HOME_PAGE = 1
    
    # QWeather API Key, get it from: https://dev.qweather.com/
    QW_API_KEY = 'PUT YOUR QWEATHER_API_KEY HERE'
    QW_API_CITY = '101010100'
    
    # WiFi access info
    WIFI_SSID = 'TEST'
    WIFI_PASS = '123456'

    # AP-IF
    AP_NAME = 'eForeConfig'
    AP_PASS = '12345678'

# UI 页面描述
UI_PAGES = [
    {"name":"设置", "ico":"qi-ico-home", "id":1},
    {"name":"月历", "ico":"qi-ico-calendarmonth", "id":2},
    {"name":"天气", "ico":"qi-sunny", "id":3}
]

def cfgSave():
    ...

def cfgGet(forWeb: bool = True) -> dict:
    '''Web/App获取配置信息'''
    doc = {}
    doc["ssid"] = WIFI_SSID
    doc["passwd"] = WIFI_PASS

    doc["we_key"] = QW_API_KEY
    doc["we_city"] = QW_API_CITY
    doc["page_nbr"] = HOME_PAGE
    doc["page_list"] = json.dumps(UI_PAGES)
    return doc

def cfgSet(newCfg) -> bool:
    '''Web/App更新配置信息'''
    WIFI_SSID = newCfg["ssid"]
    WIFI_PASS = newCfg["passwd"]

    QW_API_KEY = newCfg["we_key"]
    QW_API_CITY = newCfg["we_city"]
    HOME_PAGE = newCfg["page_nbr"]

    try:
        with open("efore.json", 'w') as file:
            json.dump(newCfg, file)
    except:
        return False
    
    return True
