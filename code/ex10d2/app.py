"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys, machine, time, gc, platform
import asyncio
import logging as log
from .button import *
from .ui_calendar import uiCalendar
from .ui_weather import uiWeather
from .ui_settings import uiSettings
from .sensor import *
from .settings import *

def main():
    log.setLevel(log.INFO)
    log.info("EFore Demo Started")
    
    webTest()
    if checkGoSetting():
        uiSettings().start()    # never return

    try:
        #uiCalendar().start()
        uiWeather().start()
    except Exception as e:
        log.exception(e,'Exception in main.py')
    
        if sys.platform == 'esp32':
            machine.reset()
    
def checkGoSetting() ->bool:
    '''按键检测，是否进设置页面'''
    
    if sys.platform == 'linux':
        return True
    
    if KeyA.is_pressed():
        time.sleep_ms(100)
        if KeyA.is_pressed():
            return True
    
    return False

# class TestWifiCreation():
#     # https://github.com/zxing/zxing/wiki/Barcode-Contents#wi-fi-network-config-android-ios-11
#     from uQR import QRCode

#     qr = QRCode()
#     ssid, password = 'test', 'test'
#     qr.add_data('WIFI:S:{};T:WPA;P:{};H:false;;'.format(ssid, password))
#     matrix = qr.get_matrix()
#     matrix = qr.render_matrix()
#     print(matrix)

def webTest():
    # https://microdot.readthedocs.io/en/stable/index.html
    # https://github.com/miguelgrinberg/microdot/tree/main
    from microdot import Microdot, send_file, redirect
    from cors import CORS

    snsTemprHumidity.read()
    wwwbot = Microdot()
    CORS(wwwbot, allowed_origins=['*'], allow_credentials=True)
    
    @wwwbot.route('/')
    def index(request):
        return send_file('www/index.html') # , compressed=True, file_extension='.gz'

    @wwwbot.route('/js/<path:path>')
    def static_js(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        print(f'path: %s' % path)
        return send_file('www/js/' + path, compressed=True, file_extension='.gz')

    @wwwbot.route('/css/<path:path>')
    def static_css(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        print(f'path: %s' % path)
        return send_file('www/css/' + path, compressed=True, file_extension='.gz')

    @wwwbot.route('/fonts/<path:path>')
    def static_fonts(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        print(f'path: %s' % path)
        return send_file('www/fonts/' + path, compressed=True, file_extension='.gz')
      
    @wwwbot.post('/dev/reset')
    async def onPostDeviceReset(request):
        asyncio.create_task(resetTask())
        return {"msg":"done"}
    
    @wwwbot.get('/dev/info')
    async def onGetDeviceInfo(request):
        res = {}
        res["平台"] = platform.platform()
        res["内存"] = f"已用 {gc.mem_alloc()}，可用 {gc.mem_free()} (字节)"
        res["室温"] = f"{snsTemprHumidity.getTemperature()} ℃"
        res["湿度"] = f"{snsTemprHumidity.getHumidity()} %"
        res["电量"] = snsBattery.getWebInfo(); 
        return res
    
    @wwwbot.get('/wifi/scan')
    async def onGetWiFiScan(request):
        return 'get invoices'
    
    @wwwbot.get('/settings')
    async def onGetSettings(request):
        print("Setting")
        doc = {}
        doc["ssid"] = WIFI_SSID
        doc["passwd"] = WIFI_PASS

        doc["we_key"] = QW_API_KEY
        doc["we_city"] = QW_API_CITY
        doc["page_nbr"] = 1
        # doc["page_list"] = [ 
        #         {"name": "首页", "ico": "qi-ico-home", "id": 1}, 
        #         {"name": "月历", "ico": "qi-ico-calendarmonth", "id": 2}, 
        #         {"name": "天气", "ico": "qi-ico-sunny", "id": 3}, 
        #     ]
        doc["page_list"] = '[{"name":"首页","ico":"qi-ico-home","id":1},{"name":"月历","ico":"qi-ico-calendarmonth","id":2},{"name":"天气","ico":"qi-ico-sunny","id":3}]'
        return doc

    @wwwbot.post('/settings')
    async def onPostSettings(request):
        # request.json
        return 'create an invoice'
        
    @wwwbot.get('/wifi')
    async def onGetWiFiInfo(request):
        return 'get invoices'
    
    @wwwbot.route('/shutdown')
    async def shutdown(request):
        request.app.shutdown()
        return 'The server is shutting down...'
       
    wwwbot.run(debug=True)

async def resetTask():
    await asyncio.sleep_ms(300)
    if sys.platform == 'esp32':
        machine.reset()
    else:
        print('sys reset')
        
def captivePortalFilter(request, path):
    '''Captive Portals
       based on https://github.com/yash-sanghvi/ESP32/blob/master/Captive_Portal/Captive_Portal.ino
    '''
    filtered = False
    

    return filtered

if __name__ == '__main__':
    #TestWifiCreation()
    main()
