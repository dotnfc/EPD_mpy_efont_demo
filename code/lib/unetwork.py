#-*- coding:utf-8 -*-
# network stub for unix port
# by dotnfc, 2023/09/20

STA_IF = 1
AP_IF = 2

AUTH_OPEN = 0
AUTH_WEP = 1
AUTH_OWE = 10

AUTH_WPA_PSK = 2
AUTH_WPA2_PSK = 3
AUTH_WPA_WPA2_PSK = 4
AUTH_WPA3_PSK = 5
AUTH_WAPI_PSK = 7
AUTH_MAX = 9

class WLAN(object):
    STAT_ASSOC_FAIL = 203
    STAT_BEACON_TIMEOUT = 200
    STAT_CONNECTING = 1001
    STAT_GOT_IP = 1010
    STAT_HANDSHAKE_TIMEOUT = 204
    STAT_IDLE = 1000
    STAT_NO_AP_FOUND = 201
    STAT_WRONG_PASSWORD = 202
    STA_IF = 0
    STAT_CONNECT_FAIL = 1002
    
    def __init__(self, interface_id : int) -> None:
        self.ap_scan_flag = 0
    
    def active(self, is_active : int) -> None:
        pass
    
    def connect(self, ssid: str, password : str) -> None:
        pass
    
    def disconnect(self) -> None:
        pass
    
    def scan(self):
        if self.ap_scan_flag == 0:
            self.ap_scan_flag = 1
            return [(b'XPS15-WIN11', b'\xde\xfbH\xe9R\xeb', 11, -45, 3, False), (b'7Days', b'bt\x13\x0fo\x9c', 6, -50, 3, False), (b'OrangeHouse', b'x`[\xef3$', 1, -73, 4, False), (b'HUAWEI-7x8Y', b'p\x89\xccw\x8f!', 8, -92, 4, False)]
        else:
            self.ap_scan_flag = 0
            return [(b'XPS15-WIN11', b'\xde\xfbH\xe9R\xeb', 11, -65, 3, False), (b'7Days', b'bt\x13\x0fo\x9c', 6, -55, 3, False), (b'ChinaNet-2m3q', b'*\xe5\xb0@\x80L', 6, -92, 4, False), (b'CMCC-6d5L', b'p\x89\xccw\x8f!', 8, -52, 4, False)]
        
    def status(self, param : str) -> None:
        pass
    
    def isconnected(self) -> bool:
        return True
    
    def ifconfig(self, config: tuple = None):
        if config == None:
            return '192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'
        
    def config(self, mac : str = None, essid : str = None, password : str = None, hidden : int = 0, channel : int = 0, authmode: int = 0) -> None:
        pass
    