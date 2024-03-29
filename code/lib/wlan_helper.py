""" WifiSTAHelper
    ESP32 WiFi STA helper
    refer: https://docs.micropython.org/en/latest/library/network.WLAN.html
"""

import sys, time
import logging as log
import uasyncio as asyncio

try:
    import network
except ImportError:
    import unetwork as network

class WifiSTAHelper(object):
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)
        self.ssid = ""
        self.passwd = ""
        #self.wlan.disconnect() # may not be needed

    def connect(self, ssid, password, timeout=7000):
        log.info(f'connecting to {ssid} ...')
        
        if self.isconnected() or sys.platform == 'linux':
            log.info("Wifi connected")
            return True
        
        self.wlan.active(True)

        self.wlan.connect(ssid, password)

        while not self.wlan.isconnected():
            time.sleep_ms(200)
            timeout -= 200
            if timeout <= 0:
                break   # time out about 7s

        if self.wlan.isconnected():
            log.info("Wifi connected")
            return True
        else:
            log.info("Unable to connect")
            self.wlan.active(False)
            return False
    
    def connects(self, ssid, password, backups, callback, cb_param) -> bool:
        '''Connect prefered WiFi AP, if failed, try backups in settings'''

        self.ssid = ""
        self.passwd = ""
        
        # normal connection
        callback(cb_param, ssid, password)
        if self.connect(ssid, password):
            self.ssid = ssid
            self.passwd = password
            return True
        
        # failed, try backups
        for bssid, bpass in backups.items():
            if bssid == ssid:
                continue
            
            callback(cb_param, bssid, bpass)
            if self.connect(bssid, bpass):
                self.ssid = bssid
                self.passwd = bpass
                return True
            
        return False
    
    def test_connect(self, ssid, password, disconn = True, timeout=8000) ->bool:
        if self.isconnected():
            self.wlan.disconnect()
        
        result = self.connect(ssid, password, timeout)
        
        if disconn:
            if self.isconnected():
                self.wlan.disconnect()
            self.wlan.active(False)
        
        return result
    
    def isconnected(self):
        if not self.wlan:
            return False
        return self.wlan.isconnected()

    def is_connected(self):
        # should have had this name all along...
        return self.isconnected()

    def disconnect(self):
        if self.wlan:
            self.wlan.disconnect()
            self.wlan.active(False)
        
    def active(self,state=None):
        if not self.wlan:
            return False
        if state and isinstance(state,bool):
            self.wlan.active(state)
            
        return self.wlan.active()
    
    def status(self):
        if not self.wlan:
            return network.STAT_IDLE
        else:
            return self.wlan.status()

    async def scan(self):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        await asyncio.sleep(0.1)
        scan_results = sta.scan()
        wifi_list = []

        for result in scan_results:
            # (ssid, bssid, channel, RSSI, security, hidden)
            ssid = result[0].decode('utf-8')
            rssi = result[3]
            auth_mode = result[4]

            # 将认证模式转换为简化的形式（开放=0，其他=1）
            simplified_auth_mode = 0 if auth_mode == 0 else 1

            # 将热点信息添加到列表中
            wifi_info = {'ssid': ssid, 'rssi': rssi, 'type': simplified_auth_mode}
            wifi_list.append(wifi_info)
        return wifi_list

    def listAP(self):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        scan_results = sta.scan()
        wifi_list = []

        for result in scan_results:
            # (ssid, bssid, channel, RSSI, security, hidden)
            ssid = result[0].decode('utf-8')
            rssi = result[3]
            auth_mode = result[4]

            # 将认证模式转换为简化的形式（开放=0，其他=1）
            simplified_auth_mode = 0 if auth_mode == 0 else 1

            # 将热点信息添加到列表中
            wifi_info = {'ssid': ssid, 'rssi': rssi, 'type': simplified_auth_mode}
            wifi_list.append(wifi_info)
        return wifi_list
    
class WifiAPHelper(object):
    
    def __init__(self):
        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.active(False)

    def start(self, name, password):
        self.wlan.active(True)
        self.wlan.config(essid=name, password=password, authmode=network.AUTH_WPA2_PSK)
    
    def ip(self):
        ip, mask, gate, dns = self.wlan.ifconfig()
        return ip

wifiHelper = WifiSTAHelper() # the connection is not active at this point

