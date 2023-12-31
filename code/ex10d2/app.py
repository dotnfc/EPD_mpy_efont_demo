"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys, machine, time
import asyncio
import logging as log
from .button import *
from .ui_calendar import uiCalendar
from .ui_weather import uiWeather
from .ui_settings import uiSettings

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
    wwwbot = Microdot()
    CORS(wwwbot, allowed_origins=['*'], allow_credentials=True)
    
    @wwwbot.route('/')
    def index(request):
        return send_file('www/index.html') # , compressed=True, file_extension='.gz'

    @wwwbot.route('/<path:path>')
    def static(request, path):
        if '..' in path:
            # directory traversal is not allowed
            return 'Not found', 404
        
        filtered = captivePortalFilter(request, path)
        if filtered:
            return redirect(f'http://192.168.19.43:5000')
        return send_file('www/' + path, compressed=True, file_extension='.gz')
    
    @wwwbot.post('/dev/reset')
    async def onPostDeviceReset(request):
        asyncio.create_task(resetTask())
        return '{"msg":"done"}'
    
    @wwwbot.get('/dev/info')
    async def onGetDeviceInfo(request):
        return 'get invoices'
    
    @wwwbot.get('/wifi/scan')
    async def onGetWiFiScan(request):
        return 'get invoices'
    
    @wwwbot.get('/settings')
    async def onGetSettings(request):
        return 'get invoices'

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
