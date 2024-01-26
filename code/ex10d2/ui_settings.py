"""
    [eForeDemo] 设置页面
    by .NFC 2023/12/23
"""
import time, gc, platform, sys
from micropython import const
import asyncio
import wlan_helper
import logging as log
from display import *
from efont import *
from efore.qw_icons import *
from settings import *
from sensor import *
from button import *
import devinfo, settings

if sys.platform == 'linux':
    import ble_fake as ble
else:
    import ble
    
WWW_PORT = const(9090) if sys.platform == 'linux' else const(8080)

class uiSettings(object):
        
    def __init__(self,**kwargs):
        if sys.platform == 'linux':
            self.epd = EpdImage()
            self.epd.init()
        
    def drawQRcodeImage(self, epd, x, y, text, scale = 4):
        '''show QR at specified location'''
        import uqr                
        qr = uqr.make(text)
        
        _start = time.ticks_ms()
        qr.draw(epd, x, y, scale)
        _end = time.ticks_ms() 

    def start(self):
        """Run the settings loop"""
        log.info("Settings Started")
        
        self.preLaunch()
                
        self.runWebServer()

    def preLaunch(self):
        if sys.platform == 'linux':
            epd = self.epd
        else:
            epd = EpdImage()
            epd.init()
        epd.clear(EPD_WHITE)
        epd.setColor(EPD_BLACK, EPD_WHITE)

        epd.loadFont("simyou")
        epd.loadFont("icons")
        epd.loadFont("7seg")
        epd.loadFont("swissel")
        epd.selectFont("simyou")
        epd.initTextFast("simyou", epd.WIDTH, 20)
        
        epd.drawTextFast(f"正在启动热点 {AP_NAME}", 4)
        self.AP = wlan_helper.WifiAPHelper()
        self.AP.start(AP_NAME, AP_PASS)
        
        epd.drawTextFast(f"正在启动 WEB/BLE 服务", 5)
        
        self.showInformations(epd) # draw UI
        
    def hline_dots(self, epd, x, y, width):
        ext = 0
        step= const(10)
        
        while(width > 0):
            if width > step:
                ext = step
            else:
                ext = width
                
            epd.line(x, y, x + ext, y, 0)
            x += ext + 4
            width -= ext + 4
            
    def showInformations(self, epd):
        
        epd.setColor(EPD_BLACK, EPD_WHITE)
        epd.selectFont("simyou")
        
        sUrl = f"http://{self.AP.ip()}"
        if WWW_PORT != 80:
            sUrl = f"{sUrl}:{WWW_PORT}"
        
        epd.clear()
        epd.drawText(0, 16, epd.WIDTH -1, 48, ALIGN_CENTER, "配置设备", 32)
        self.hline_dots(epd, 80, 60, 800)
        
        msg = f"1. 连接热点网络"
        epd.drawText(100, 80, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码，连接到此设备的热点"
        epd.drawText(100, 110, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工连接以下热点"
        epd.drawText(100, 140, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     名称: {AP_NAME}, 密码: {AP_PASS}"
        epd.drawText(100, 170, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     提示: 安卓系统使用'扫一扫', iOS 请使用系统相机直接扫。"
        epd.drawText(100, 208, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 16)
        
        # self.hline_dots(180, 260, 600)
        
        msg = f"2. 访问配置页面"
        epd.drawText(100, 300, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码访问"
        epd.drawText(100, 330, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工访问 {sUrl}"
        epd.drawText(100, 360, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        
        msg = f"3. 使用配置应用进行配置（蓝牙）"
        epd.drawText(100, 460, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 下载【e预报】应用，然后通过蓝牙连接设备"
        epd.drawText(100, 490, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 名称：{ble.getBleDevName()}"
        epd.drawText(100, 520, epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        
        # AP 二维码
        self.drawQRcodeImage(epd, 702, 80, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        
        # 配置页面
        self.drawQRcodeImage(epd, 708, 285, sUrl)
        
        # 配置 app
        sUrl = "https://www.123pan.com/s/6nQ9jv-RMrBh.html"
        self.drawQRcodeImage(epd, 702, 460, sUrl)

        epd.line(60, 600, 900, 600, 0)
        
        epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)
        #epd.selectFont("icons")
        #epd.drawText(66, 606, epd.WIDTH -1, 610, ALIGN_LEFT, ICO_SETTING_SOLID, 24)

        epd.refresh(full=False)
    
    # refer https://microdot.readthedocs.io/en/stable/index.html
    def runWebServer(self):
        
        from microdot import Microdot, send_file, cors, redirect

        snsTemprHumidity.read()
        wwwbot = Microdot()
        self.wwwShutdown = wwwbot.shutdown
        
        cors.CORS(wwwbot, allowed_origins=['*'], allow_credentials=True)
        
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
            '''复位设备'''
            asyncio.create_task(resetTask())
            return {"msg":"done"}
        
        @wwwbot.get('/dev/info')
        async def onGetDeviceInfo(request):
            '''获取设备信息'''
            return devinfo.DeviceInfo()
        
        @wwwbot.get('/wifi/scan')
        async def onGetWiFiScan(request):
            '''获取可用热点,返回 list object'''
            wifis = await wlan_helper.wifiHelper.scan()
            return wifis # json.dumps(wifis)
        
        @wwwbot.get('/settings')
        async def onGetSettings(request):
            '''获取配置, 返回 json list'''
            #doc = {}
            #doc["ssid"] = WIFI_SSID
            #doc["passwd"] = WIFI_PASS

            #doc["we_key"] = QW_API_KEY
            #doc["we_city"] = QW_API_CITY
            #doc["page_nbr"] = 1
            # doc["page_list"] = [ 
            #         {"name": "首页", "ico": "qi-ico-home", "id": 1}, 
            #         {"name": "月历", "ico": "qi-ico-calendarmonth", "id": 2}, 
            #         {"name": "天气", "ico": "qi-ico-sunny", "id": 3}, 
            #     ]
            #doc["page_list"] = '[{"name":"首页","ico":"qi-ico-home","id":1},{"name":"月历","ico":"qi-ico-calendarmonth","id":2},{"name":"天气","ico":"qi-sunny","id":3}]'
            return settings.cfgGet()

        @wwwbot.post('/settings')
        async def onPostSettings(request):
            '''更新配置'''
            print(f"update {request.json}")
            return {"msg":"done"}

        @wwwbot.route('/shutdown')
        async def shutdown(request):
            request.app.shutdown()
            return 'The server is shutting down...'

        async def web_app():
            # wwwbot.run(debug=True, port=WWW_PORT)
            await wwwbot.start_server(host='0.0.0.0', port=WWW_PORT, debug=True, ssl=None)

        async def runBleWeb():
            t1 = asyncio.create_task(ble.ble_app())
            t2 = asyncio.create_task(web_app())
            t3 = asyncio.create_task(self.homePageTask())
            await asyncio.gather(t1, t2, t3)
            
        asyncio.run(runBleWeb())
        #wwwbot.run(debug=True, port=WWW_PORT)
        
        async def resetTask():
            '''task for delayed resetting'''
            await asyncio.sleep_ms(300)
            if sys.platform == 'esp32':
                machine.reset()
            else:
                print('sys reset')

    async def homePageTask(self):
        if sys.platform == 'linux':
                    
            while(self.epd.runable()):
                await asyncio.sleep(0.01)
                KeyA.update_state()
                KeyB.update_state()
                    
            # now, quit the game
            self.wwwShutdown() 
            # dont care the ble_fake task
            
            sys.exit(0)
        else:
            while(True):
                await asyncio.sleep(0.01)
                KeyA.update_state()
                KeyB.update_state()

