from sensor import *
import gc, platform

def DeviceInfo(isForApp = False) ->dict:
    '''获取设备信息'''
    res = {}
    res["平台"] = platform.platform()
    res["内存"] = f"已用 {gc.mem_alloc()}，可用 {gc.mem_free()} (字节)"
    res["室温"] = f"{snsTemprHumidity.getTemperature()} ℃"
    res["湿度"] = f"{snsTemprHumidity.getHumidity()} %"
    res["电量"] = snsBattery.getVoltageForApp if isForApp else snsBattery.getWebInfo(); 
    return res
