# from https://blog.csdn.net/jd3096/article/details/129784182
# 

from micropython import const
import math

RX8025T_I2C_ADDRESS  = const(50)
RX8025T_REG_SECOND   = const(0)
RX8025T_REG_MINUTE   = const(1)
RX8025T_REG_HOUR     = const(2)
RX8025T_REG_WEEKDAY  = const(3)
RX8025T_REG_DAY      = const(4)
RX8025T_REG_MONTH    = const(5)
RX8025T_REG_YEAR     = const(6)

class RX8025T():
    def __init__(self, i2c):
        self.i2c = i2c
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.buf = bytearray(7)
        self.DT = [0] * 8
 
    def	setReg(self, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(RX8025T_I2C_ADDRESS, reg, self.tb)
 
    def	getReg(self, reg):
        self.i2c.readfrom_mem_into(RX8025T_I2C_ADDRESS, reg, self.rb)
        return self.rb[0]
 
    def TOBCD(self, dat):
        n0=n1=0
        n0=dat%10
        n1=(dat//10)%10
        return (n1<<4|n0)
 
    def FROMBCD(self, dat):
        n0=n1=0
        n0=dat&0x0f
        n1=(dat>>4)*10
        return n0+n1
 
    def year(self, year = None):
        if year == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_YEAR)) + 2000
        else:
            self.setReg(RX8025T_REG_YEAR, self.TOBCD(year%100))
 
    def month(self, month = None):
        if month == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_MONTH))
        else:
            self.setReg(RX8025T_REG_MONTH, self.TOBCD(month))
 
    def day(self, day = None):
        if day == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_DAY))
        else:
            self.setReg(RX8025T_REG_DAY, self.TOBCD(day))
 
    def weekday(self, weekday = None):
        if weekday == None:
            return int(math.log2(self.getReg(RX8025T_REG_WEEKDAY)))
        else:
            d=1<<weekday
            self.setReg(RX8025T_REG_WEEKDAY, d)
 
    def hour(self, hour = None):
        if hour == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_HOUR))
        else:
            self.setReg(RX8025T_REG_HOUR, self.TOBCD(hour))
 
    def minute(self, minute = None):
        if minute == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_MINUTE))
        else:
            self.setReg(RX8025T_REG_MINUTE, self.TOBCD(minute))
 
    def second(self, second = None):
        if second == None:
            return self.FROMBCD(self.getReg(RX8025T_REG_SECOND))
        else:
            self.setReg(RX8025T_REG_SECOND, self.TOBCD(second))
 
    def datetime(self, DT=None):
        if DT == None:
            self.i2c.readfrom_mem_into(RX8025T_I2C_ADDRESS, RX8025T_REG_SECOND, self.buf)
            self.DT[0] = self.FROMBCD(self.buf[6]) + 2000 
            self.DT[1] = self.FROMBCD(self.buf[5])
            self.DT[2] = self.FROMBCD(self.buf[4])
            self.DT[3] = int(math.log2(self.buf[3]))
            self.DT[4] = self.FROMBCD(self.buf[2]) 
            self.DT[5] = self.FROMBCD(self.buf[1]) 
            self.DT[6] = self.FROMBCD(self.buf[0]) 
            self.DT[7] = 0
            return self.DT
        else:
            self.buf[0] = self.TOBCD(DT[6])   
            self.buf[1] = self.TOBCD(DT[5])  
            self.buf[2] = self.TOBCD(DT[4])  
            self.buf[3] = 1<<DT[3] 
            self.buf[4] = self.TOBCD(DT[2])   
            self.buf[5] = self.TOBCD(DT[1])   
            self.buf[6] = self.TOBCD(DT[0]) 
            self.i2c.writeto_mem(RX8025T_I2C_ADDRESS, RX8025T_REG_SECOND, self.buf) 
 

#example   0->Sunday 1->Monday....  6->Saturday
if __name__ =='__main__':
    from machine import SoftI2C,Pin
    import time
    i2c = SoftI2C(scl=Pin(39),sda=Pin(38))
    rr = RX8025T(i2c)
    #rr.datetime((2024,1,25,4,18,00,00,0))
    print(rr.datetime())

