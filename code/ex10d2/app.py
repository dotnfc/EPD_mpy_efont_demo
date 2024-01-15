"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys, machine, time
import logging as log
from button import *
from ui_calendar import uiCalendar
from ui_weather import uiWeather
from ui_settings import uiSettings
from ui_switch import uiSwitch
# from sensor import *
import settings

def main():
    log.setLevel(log.INFO)
    log.info("EFore Demo Started")
    
    #if checkGoSetting():
    uiSwitch().start()
    uiSettings().start()    # never return

    try:
        if settings.HOME_PAGE == 2:
            uiCalendar().start()
        elif settings.HOME_PAGE == 3:
            uiWeather().start()
        else:
            uiSettings().start()    # never return
            
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

if __name__ == '__main__':
    main()
