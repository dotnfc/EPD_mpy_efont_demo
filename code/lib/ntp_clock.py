'''
   sync local time and rtc from ntp server
'''
import machine

try:
    import ntptime
except:
    import usdl2_ntptime as ntptime

try:
    import time
except:
    import utime as time


ntp_hosts = ["cn.pool.ntp.org", "ntp1.aliyun.com", "cn.ntp.org.cn", "pool.ntp.org"]

# change timeout, default 1s
# ntptime.timeout = 2

def ntp_sync_via_wifi(timezone_offset) ->bool:
    '''connect to wifi first, and sync time from ntp server'''
    year, *_ = time.localtime()
    if year >= 2024:
        return True

    for host in ntp_hosts:
        try:
            ntptime.host = host
            ntptime.settime()
            print("time synced")
            
            # set timezone
            utc_time = time.localtime()
            adjusted_time = time.mktime(utc_time) + timezone_offset
            rtc = machine.RTC()
            rtc.datetime(time.localtime(adjusted_time))
            
            break
        except Exception as e:
            print(f"Failed to sync time with {host}. ")
            print(f"Exception: {e}")
            print("retry")
            return False
    
    return True

def test():
    ssid = "DOTNFC-HOS"
    password = "********"
    
    import network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        pass

    ntp_sync_via_wifi(28800)

    local_time = utime.localtime()
    print("Adjusted time:", local_time)
    
if __name__ == "__main__":
    test()

