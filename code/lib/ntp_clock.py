'''
   sync local time and rtc from ntp server
'''
import machine, sys

try:
    import time
except:
    import utime as time

try:
    import usocket as socket
except:
    import socket
try:
    import ustruct as struct
except:
    import struct


ntp_hosts = ["cn.pool.ntp.org", "ntp1.aliyun.com", "cn.ntp.org.cn", "pool.ntp.org"]

# The NTP socket timeout can be configured at runtime by doing: ntptime.timeout = 2
timeout = 1
timezone_offset = 28800    # UTC+8
newDT = None

def ntp_clock_time(host):
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(timeout)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    print(f"ntp {val}")
    EPOCH_YEAR = time.gmtime(0)[0]
    if EPOCH_YEAR == 2000:
        # (date(2000, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 3155673600
    elif EPOCH_YEAR == 1970:
        # (date(1970, 1, 1) - date(1900, 1, 1)).days * 24*60*60
        NTP_DELTA = 2208988800
    else:
        raise Exception("Unsupported epoch: {}".format(EPOCH_YEAR))

    return val - NTP_DELTA + timezone_offset


# There's currently no timezone support in MicroPython, and the RTC is set in UTC time.
def ntp_clock_settime(host):
    global newDT
    import machine
    
    t = ntp_clock_time(host)
    print(t)
    
    tm = time.gmtime(t)

    newDT = (tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0)
    return newDT

def ntp_sync_host(host) ->bool:
    try:
        newDT = ntp_clock_settime(host)
        print("time synced")
        return True
    except Exception as e:
        print(f"Failed to sync time with {host}. ")
        print(f"Exception: {e}")
        return False

def ntp_sync_via_wifi() ->bool:
    '''connect to wifi first, and sync time from ntp server'''
    if sys.platform == 'linux':
        return True
    
    year, *_ = time.localtime()
    if year >= 2024:
        return True

    result = False
    for host in ntp_hosts:
        if ntp_sync_host(host):
            result = True
            break
    
    return result

def test():
    ssid = "DOTNFC-HOS"
    password = "********"
    
    import network
    wifi = network.WLAN(network.STA_IF)
    
    wifi.active(False)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        pass
    print("wifi connected")
        
    if not ntp_sync_via_wifi():
        print("Test Failed")
        return

    local_time = time.localtime()
    print("Adjusted time:", local_time)
    
if __name__ == "__main__":
    test()

