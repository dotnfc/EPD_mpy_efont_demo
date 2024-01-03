# global configuration
import json


try:
    with open("efore.json", 'r') as file:
        config_data = json.load(file)
        print("Configuration data:", config_data)
        
    HOME_PAGE = config_data['page']
        
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
    HOME_PAGE = 'weather'
        
    # QWeather API Key, get it from: https://dev.qweather.com/
    QW_API_KEY = 'PUT YOUR QWEATHER_API_KEY HERE'
    QW_API_CITY = '101010100'
    
    # WiFi access info
    WIFI_SSID = 'TEST'
    WIFI_PASS = '123456'

    # AP-IF
    AP_NAME = 'eForeConfig'
    AP_PASS = '12345678'



