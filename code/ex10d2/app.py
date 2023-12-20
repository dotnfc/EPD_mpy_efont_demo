"""
    Main script for EFore Demo [.NFC 2023/12/18]
"""
import sys
import machine
import logging as log
from .ui_calendar import uiCalendar

def main():
    log.setLevel(log.INFO)
    log.info("EFore Demo Started")
    
    try:
        uiCalendar().start()
    except Exception as e:
        log.exception(e,'Exception in main.py')
    
        if sys.platform == 'esp32':
            machine.reset()
        
if __name__ == '__main__':
    main()
