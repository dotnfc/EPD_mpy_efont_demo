"""
    [eForeDemo] 天气页面测试
    by .NFC 2023/12/23
"""
import time, gc, platform, sys
from micropython import const
import asyncio
import json
import wlan_helper
import logging as log
from display import *
from efont import *
from efore.qw_icons import *
from .settings import *
from .sensor import *
from .button import *


WWW_PORT = const(80) if sys.platform == 'linux' else const(2222)

class uiSettings(object):
        
    def __init__(self,**kwargs):
        self.epd = EpdImage()
        self.epd.init()
        self.epd.clear(EPD_WHITE)
        self.epd.setColor(EPD_BLACK, EPD_WHITE)

        self.epd.loadFont("simyou")
        self.epd.loadFont("icons")
        self.epd.loadFont("7seg")
        self.epd.loadFont("swissel")
        self.epd.selectFont("simyou")
        
    def drawQRcodeImage(self, epd, x, y, text):
        '''show QR at specified location'''
        import uqr                
        qr = uqr.make(text)
        
        _start = time.ticks_ms()
        qr.draw(epd, x, y, 4)
        _end = time.ticks_ms()
        print(f"time2 used {_end - _start}ms")
    
    async def startUILoop(self):
        while(self.epd.runable()):
            await asyncio.sleep(0.1)

        # now, quit the game
        sys.exit(0)

    def start(self):
        """Run the settings loop"""
        log.info("Settings Started")
        
        self.AP = wlan_helper.WifiAPHelper()
        self.AP.start(AP_NAME, AP_PASS)
        
        self.showInformations()

        if sys.platform == 'linux':
            asyncio.run(self.startUILoop())
        
        self.runWebServer()
    
    def hline_dots(self, x, y, width):
        ext = 0
        step= const(10)
        
        while(width > 0):
            if width > step:
                ext = step
            else:
                ext = width
                
            self.epd.line(x, y, x + ext, y, 0)
            x += ext + 4
            width -= ext + 4
            
    def showInformations(self):
        self.epd.setColor(EPD_BLACK, EPD_WHITE)
        self.epd.selectFont("simyou")
        
        sUrl = f"http://{self.AP.ip()}"
        if WWW_PORT != 80:
            sUrl = f"{sUrl}:{WWW_PORT}"
        
        self.epd.clear()
        self.epd.drawText(0, 16, self.epd.WIDTH -1, 48, ALIGN_CENTER, "配置设备", 32)
        self.hline_dots(80, 60, 800)
        
        msg = f"1. 连接热点网络"
        self.epd.drawText(100, 80, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码，连接到此设备的热点"
        self.epd.drawText(100, 110, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工连接以下热点"
        self.epd.drawText(100, 140, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     名称: {AP_NAME}, 密码: {AP_PASS}"
        self.epd.drawText(100, 170, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"     提示: 安卓系统使用'扫一扫', iOS 请使用系统相机直接扫。"
        self.epd.drawText(100, 208, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 16)
        
        # self.hline_dots(180, 260, 600)
        
        msg = f"2. 访问配置页面"
        self.epd.drawText(100, 290, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 右侧扫码访问"
        self.epd.drawText(100, 320, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        msg = f"   - 手工访问 {sUrl}"
        self.epd.drawText(100, 350, self.epd.WIDTH -1, 48, ALIGN_LEFT, msg, 24)
        
        # AP 二维码
        self.drawQRcodeImage(self.epd, 652, 80, f'WIFI:S:{AP_NAME};T:WPA;P:{AP_PASS};H:false;;')
        
        # 配置页面
        self.drawQRcodeImage(self.epd, 658, 290, sUrl)
        
        self.epd.line(60, 600, 900, 600, 0)
        
        self.epd.drawText(100, 606, 760, 606, ALIGN_CENTER, "eForecast by .NFC, firmware version: 1.0.00", 16)
        #self.epd.selectFont("icons")
        #self.epd.drawText(66, 606, self.epd.WIDTH -1, 610, ALIGN_LEFT, ICO_SETTING_SOLID, 24)

        self.epd.refresh(full=False)
    
    # refer https://microdot.readthedocs.io/en/stable/index.html
    def runWebServer(self):
        
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
            '''复位设备'''
            asyncio.create_task(resetTask())
            return {"msg":"done"}
        
        @wwwbot.get('/dev/info')
        async def onGetDeviceInfo(request):
            '''获取设备信息'''
            res = {}
            res["平台"] = platform.platform()
            res["内存"] = f"已用 {gc.mem_alloc()}，可用 {gc.mem_free()} (字节)"
            res["室温"] = f"{snsTemprHumidity.getTemperature()} ℃"
            res["湿度"] = f"{snsTemprHumidity.getHumidity()} %"
            res["电量"] = snsBattery.getWebInfo(); 
            return res
        
        @wwwbot.get('/wifi/scan')
        async def onGetWiFiScan(request):
            '''获取可用热点,返回 list object'''
            wifis = await wlan_helper.wifiHelper.scan()
            return wifis # json.dumps(wifis)
        
        @wwwbot.get('/settings')
        async def onGetSettings(request):
            '''获取配置, 返回 json list'''
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
            '''更新配置'''
            print(f"update {request.json}")
            return {"msg":"done"}

        @wwwbot.route('/shutdown')
        async def shutdown(request):
            request.app.shutdown()
            return 'The server is shutting down...'
        
        wwwbot.run(debug=True, port=WWW_PORT)

        async def resetTask():
            '''task for delayed resetting'''
            await asyncio.sleep_ms(300)
            if sys.platform == 'esp32':
                machine.reset()
            else:
                print('sys reset')

        