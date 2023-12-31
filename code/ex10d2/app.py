"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys, machine, time
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
    from microdot import Microdot
    wwwbot = Microdot()
    
    html = '''<!DOCTYPE html>
    <html>
        <head>
            <title>Microdot Example Page</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <div>
                <h1>Microdot Example Page</h1>
                <p>Hello from Microdot!</p>
                <p><a href="/shutdown">Click to shutdown the server</a></p>
            </div>
        </body>
    </html>
    '''


    @wwwbot.route('/')
    async def hello(request):
        return html, 200, {'Content-Type': 'text/html'}


    @wwwbot.route('/shutdown')
    async def shutdown(request):
        request.app.shutdown()
        return 'The server is shutting down...'


    wwwbot.run(debug=True)
    
if __name__ == '__main__':
    #TestWifiCreation()
    main()
