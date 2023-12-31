#-*- coding:utf-8 -*-
# network stub for unix port
# by dotnfc, 2023/09/20

STA_IF = 1
AP_IF = 2

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
        pass
    
    def active(self, is_active : int) -> None:
        pass
    
    def connect(self, ssid: str, password : str) -> None:
        pass
    
    def disconnect(self) -> None:
        pass
    
    def scan(self) -> None:
        pass
    
    def status(self, param : str) -> None:
        pass
    
    def isconnected(self) -> bool:
        return True
    
    def ifconfig(self, config: tuple = None):
        if config == None:
            return '192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8'
        
    def config(self, mac : str = None, essid : str = None, password : str = None, hidden : int = 0, channel : int = 0) -> None:
        pass
    