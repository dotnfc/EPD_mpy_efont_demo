"""Clock class to connect to the NTP server via wifi and set
the Real Time Clock.
    
    A wifi connection will be attempted if one is not already available when
    setting the time. If there is no connection prior to the call the connection
    will be closed and the wifi will be de-activated otherwise the conncetion will
    be used and left as is.
"""

from machine import RTC
from logging import logging as log
from settings.settings import settings
from wifi_sta_helper import connection
from settings.time_functions import Time_Functions
import time as time


class Clock:
    
    def __init__(self,format=12,offset_seconds=None):
        self.format = format #12 or 24 hour display
        self.time_functions = Time_Functions()
        if offset_seconds:
            self.offset_seconds = offset_seconds # seconds before or after UTC
        else:
            try:
                self.offset_seconds = 3600 * self.time_functions.time_zone_offset
            except ValueError:
                self.offset_seconds = -28800
                # -28800 is 8 hours before UTC (PST
        
        self.has_time = False
        self.UTC_time = None
        self.last_sync_seconds = time.time()
        
 
    def set_time(self):
        """Try to access the NTP system to set the real time clock"""
        
        self.has_time = False
        # update to the current time just to show we tried...
        self.last_sync_seconds = time.time() 
   
        connection.connect()
        if connection.is_connected():
            try:
                import ntptime
                ntptime.settime() # always UTC
                self.UTC_time = time.gmtime()
                log.debug(f"ntptime: {time.localtime()}")
                self.has_time = True
                self.set_RTC()
                self.last_sync_seconds = time.time()
            except Exception as e:
                log.exception(e,"unable to connect to time server")
                    
 
    def set_RTC(self):
        """Set the Real Time Clock for the local time
        """
        
        t = time.time() + self.offset_seconds # returns an int
        if self.time_functions.is_daylight_savings:
            t += 3600 # add an hour
            
        t = time.localtime(t) # returns a tuple eg: (Y,M,D,H,m,s,weekday,yearday)

        rtc = RTC()
        #set the RTC date time to adjusted local time
        # Format: (year, month, day, <unknown>, hour, minute, second, tzinfo)
        rtc.datetime((t[0],t[1],t[2],None,t[3],t[4],t[5],None))
        log.debug(f"RTC time: {rtc.datetime()}")
    
    def time_string(self,format=None):
        if not self.has_time:
            return "--:--"
        if not format:
            format = self.format
        # return the time as text
        t = time.localtime() # returns a tuple
        log.debug(f"time_string time: {time.localtime()}")

        hrs = t[3]
        if format == 12 and hrs > 12:
            hrs -= 12
        if format == 12 and hrs == 0:
            hrs = 12
        
        hrs = str(hrs)
        
        if format == 24:
            hrs = ("00" + hrs)[-2:]
            
        return hrs + ":" + ("00" + str(t[4]))[-2:]
        
