""" WifiSTAHelper
    ESP32 WiFi STA helper
    refer: https://docs.micropython.org/en/latest/library/network.WLAN.html
"""

import sys, time
import logging as log

try:
    import network
except ImportError:
    import unetwork as network

class WifiSTAHelper(object):
    
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)
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

    def _scan(self):
        scan = self.wlan.scan()
        aps_db = []
        aps_names = []
        result = "Scan found: "
        for x in range(4):
            scan = self.wlan.scan()
            for s in scan:
                name = s[0].decode()
                if name not in aps_names and name != '':
                    aps_names.append(name)
                    x = "000"+str(abs(s[3]))
                    aps_db.append(x[-3:len(x)]+"/"+name) # we want to sort by db
            result += f", {str(len(aps_db))}"
            time.sleep(1)
            
        log.debug(result)
        
        # sort by best signal strength, lowest first
        aps_db.sort()
        log.debug(f"Scaned: {str(aps_db)}")
        scan=[]
        for l in aps_db:
            scan.append(l.split('/')[1])
            
        return scan

class WifiAPHelper(object):
    
    def __init__(self):
        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.active(False)

    def start(self, name, password):
        self.wlan.active(True)
        self.wlan.config(essid=name, password=password)
    
    def ip(self):
        ip, mask, gate, dns = self.wlan.ifconfig()
        return ip
    
wifiHelper = WifiSTAHelper() # the connection is not active at this point
