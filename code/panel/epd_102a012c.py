#-*- coding:utf-8 -*-
# panel driver, based on {github}/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico-ePaper-3.7.py
# FPC Label: HINK-E075A01-A8
# Panel    : GDEW075Z09 (960 x 640)
# IC       : SSD1677
# Product  : Stellar-XXXL
# by dotnfc, 2023/09/20
#----------------------------------------------------------------

from micropython import const
from machine import SPI, Pin
from time import sleep_ms
import time
from framebuf import *
from logger import *
from board import *
import ustruct

BUSY = const(1)  # 1=busy, 0=idle

# gray clear
EPD_3IN7_lut_4Gray_GC =[
0x2A,0x06,0x15,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#1
0x28,0x06,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#2
0x20,0x06,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#3
0x14,0x06,0x28,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#4
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#5
0x00,0x02,0x02,0x0A,0x00,0x00,0x00,0x08,0x08,0x02,#6
0x00,0x02,0x02,0x0A,0x00,0x00,0x00,0x00,0x00,0x00,#7
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#8
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#9
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#10
0x22,0x22,0x22,0x22,0x22
]

# gray clear
EPD_3IN7_lut_1Gray_GC =[
0x2A,0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#1
0x05,0x2A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#2
0x2A,0x15,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#3
0x05,0x0A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#4
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#5
0x00,0x02,0x03,0x0A,0x00,0x02,0x06,0x0A,0x05,0x00,#6
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#7
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#8
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#9
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#10
0x22,0x22,0x22,0x22,0x22
]

# display update
EPD_3IN7_lut_1Gray_DU =[
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#1
0x01,0x2A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x0A,0x55,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#3
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#5
0x00,0x00,0x05,0x05,0x00,0x05,0x03,0x05,0x05,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#7
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#9
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x22,0x22,0x22,0x22,0x22
]

EPD_3IN7_lut_1Gray_A2 =[
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#1
0x0A,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#2
0x05,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#3
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#4
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#5
0x00,0x00,0x03,0x05,0x00,0x00,0x00,0x00,0x00,0x00,#6
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#7
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#8
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#9
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,#10
0x22,0x22,0x22,0x22,0x22
]

class EPD(FrameBuffer):
    # Display resolution
    WIDTH  = const(960)
    HEIGHT = const(640)
    BUF_SIZE = const(WIDTH * HEIGHT // 4)
    
    def __init__(self):
        self.spi = SPI(2, baudrate=2000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
        self.lut_4Gray_GC = EPD_3IN7_lut_4Gray_GC
        self.lut_1Gray_GC = EPD_3IN7_lut_1Gray_GC
        self.lut_1Gray_DU = EPD_3IN7_lut_1Gray_DU
        self.lut_1Gray_A2 = EPD_3IN7_lut_1Gray_A2
        
        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.buffer = bytearray(self.height * self.width // 8)        
        super().__init__(self.buffer, self.WIDTH, self.HEIGHT, MONO_HLSB)
       
    def Load_LUT(self,lut):
        self._command(0x32)
        for count in range(0, 105):
            if lut == 0 :
                self._data(self.lut_4Gray_GC[count])
            elif lut == 1 :
                self._data(self.lut_1Gray_GC[count])
            elif lut == 2 :
                self._data(self.lut_1Gray_DU[count])
            elif lut == 3 :
                self._data(self.lut_1Gray_A2[count])
            else:
                print("There is no such lut ")

    def _command(self, command, data=None):

        self.dc(0)
        self.cs(0)
        if isinstance(command, int):
            command = bytearray([command])
        self.spi.write(command)
        self.cs(1)
        if data is not None:
            if isinstance(data, int):
                data = bytearray([data])
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        if isinstance(data, int):
            data = bytearray([data])
        self.spi.write(data)
        self.cs(1)
        
    def EPD_3IN7_4Gray_init(self):
    
        self.reset()              # SWRESET

        self._command(0x12)
        sleep_ms(300)   

        self._command(0x46)
        self._data(0xF7)
        self.wait_until_idle()
        self._command(0x47)
        self._data(0xF7)
        self.wait_until_idle()
        
        self._command(0x01)   # setting gaet number
        self._data(0xDF)
        self._data(0x01)
        self._data(0x00)

        self._command(0x03)   # set gate voltage
        self._data(0x00)

        self._command(0x04)   # set source voltage
        self._data(0x41)
        self._data(0xA8)
        self._data(0x32)

        self._command(0x11)   # set data entry sequence
        self._data(0x03)

        self._command(0x3C)   # set border 
        self._data(0x03)

        self._command(0x0C)   # set booster strength
        self._data(0xAE)
        self._data(0xC7)
        self._data(0xC3)
        self._data(0xC0)
        self._data(0xC0)  

        self._command(0x18)   # set internal sensor on
        self._data(0x80)
         
        self._command(0x2C)   # set vcom value
        self._data(0x44)

        self._command(0x37)   # set display option, these setting turn on previous function
        self._data(0x00)
        self._data(0x00)
        self._data(0x00)
        self._data(0x00)
        self._data(0x00) 
        self._data(0x00)
        self._data(0x00)
        self._data(0x00)
        self._data(0x00)
        self._data(0x00) 

        self._command(0x44)   # setting X direction start/end position of RAM
        self._data(0x00)
        self._data(0x00)
        self._data(0x17)
        self._data(0x01)

        self._command(0x45)   # setting Y direction start/end position of RAM
        self._data(0x00)
        self._data(0x00)
        self._data(0xDF)
        self._data(0x01)

        self._command(0x22)   # Display Update Control 2
        self._data(0xCF)

    def EPD_3IN7_1Gray_init(self):
        self.reset()
        
        self._command(0x12)
        sleep_ms(300)  
        
        #self._command(0x46) # Auto Write RED RAM for Regular Pattern
        #self._data(0xF7)
        #self.wait_until_idle()
        #self._command(0x47) # Auto Write B/W RAM for Regular Pattern
        #self._data(0xF7)
        #self.wait_until_idle()

        # setting gate number
        self._command(0x01, ustruct.pack("<I", self.WIDTH - 1) + b'\x00')
        
        self._command(0x03)   # set gate voltage
        self._data(0x00)

        self._command(0x04)   # set source voltage
        self._data(0x41)
        self._data(0xA8)
        self._data(0x32)

        self._command(0x11)   # set data entry sequence
        self._data(0x03)

        self._command(0x3C)   # set border 
        self._data(0x03)

        self._command(0x0C)   # set booster strength
        self._data(0xAE)
        self._data(0xC7)
        self._data(0xC3)
        self._data(0xC0)
        self._data(0xC0)

        self._command(0x18)   # set internal sensor on
        self._data(0x80)      # use internal sensor
         
        self._command(0x2C)   # set vcom value
        self._data(0x44)

        self._command(0x37)   # set display option, these setting turn on previous function
        self._data(0x00)      # can switch 1 gray or 4 gray
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)  
        self._data(0x4F)
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)  

        # setting X direction start/end position of RAM
        self._command(0x44, b'\x00\x00' + ustruct.pack("<I", self.WIDTH - 1))
        
        # setting Y direction start/end position of RAM
        self._command(0x45, b'\x00\x00' + ustruct.pack("<I", self.HEIGHT - 1))

        self._command(0x22)   # Display Update Control 2
        self._data(0xCF)
        
    def EPD_3IN7_4Gray_Clear(self):    
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1

        self._command(0x49)
        self._data(0x00)
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)
        
        self._command(0x24)
        for j in range(0, high):
            for i in range(0, wide):
                self._data(0Xff)
        
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
         
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)
        
        self._command(0x26)
        for j in range(0, high):
            for i in range(0, wide):
                self._data(0Xff)
          
        self.Load_LUT(0)
        self._command(0x22)
        self._data(0xC7)

        self._command(0x20)
        self.wait_until_idle()    
        
    def EPD_3IN7_1Gray_Clear(self):
        
        self.fill(self.white)

        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)

        self._command(0x24)
        self._data(self.buffer)

        self.fill(self.black)
        self._command(0x26)
        self._data(self.buffer)
        
        self.Load_LUT(1)

        self._command(0x20)
        self.wait_until_idle()
        
    def EPD_3IN7_4Gray_Display(self,Image):
        
        self._command(0x49)
        self._data(0x00)

        
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
        
        
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)
        
        self._command(0x24)
        for i in range(0, 16800):
            temp3=0
            for j in range(0, 2):
                temp1 = Image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01;
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00;
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2
                    
            self._data(temp3)
        # new  data
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
         
        
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)
        
        self._command(0x26)
        for i in range(0, 16800):
            temp3=0
            for j in range(0, 2):
                temp1 = Image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2

            self._data(temp3)
        
        self.Load_LUT(0)
        
        self._command(0x22)
        self._data(0xC7)
        
        self._command(0x20)
        
        self.wait_until_idle()
        
    def EPD_3IN7_1Gray_Display(self,Image):
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1

        self._command(0x49)
        self._data(0x00)
        
        self._command(0x4E)
        self._data(0x00)
        self._data(0x00)
        self._command(0x4F)
        self._data(0x00)
        self._data(0x00)

        self._command(0x24)
        self._data(Image)
        self.Load_LUT(1)
        
        self._command(0x20)
        self.wait_until_idle()
        
    def EPD_3IN7_1Gray_Display_Part(self,Image):
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1

        self._command(0x44, b'\x00\x00' + ustruct.pack("<I", self.WIDTH - 1))
        
        self._command(0x45, b'\x00\x00' + ustruct.pack("<I", self.HEIGHT - 1))
        
        self._command(0x4E)   # SET_RAM_X_ADDRESS_COUNTER
        self._data(0x00)
        self._data(0x00)

        self._command(0x4F)   # SET_RAM_Y_ADDRESS_COUNTER
        self._data(0x00)
        self._data(0x00)
        
        self._command(0x24)
        self._data(Image)
        
        self.Load_LUT(2)
        self._command(0x20)
        self.wait_until_idle()

    def refresh(self, buf = None, full=True):
        '''Update screen contents.
        
        Args:
            - buf: dummy, only internal buffer
            - full: dummy, only full more
        '''
        if not full:
            return

        #self.EPD_3IN7_1Gray_Display(self.buffer)
        self.EPD_3IN7_1Gray_Display_Part(self.buffer)
        
    def power_on(self):
        self._command(0x04)
        self.wait_until_idle()
        
    def power_off(self):
        self._command(0x02)
        self.wait_until_idle()
    
    def init(self):
        self.EPD_3IN7_1Gray_init()
        
    def init_panel(self, reset=True):
        pass
    
    def init_full(self):
        self.init_panel()
        self.power_on()
        
    def init_partial(self):
        self.init_panel()
        self.power_on()
        
    def update_full(self):
        self._command(0x12)
        self.wait_until_idle(45000)

    def update_partial(self):
        self._command(0x12)
        self.wait_until_idle(45000)
        
    def wait_until_idle(self, timeout=10000):
        while self.busy.value() == BUSY:
            sleep_ms(10)
            timeout = timeout - 10
            if timeout <=0 :
                raise RuntimeError("Timeout out for waiting busy signal")
        
        sleep_ms(2)
       
    def reset(self):
        self.rst(1)
        sleep_ms(30)
        
        self.rst(0)
        sleep_ms(30)

        self.rst(1)
        sleep_ms(30)
        
    def sleep(self):
        # self.power_off()        
        self._command(0x10, 0x03)
        
def main():
    BLACK = 0
    RED = 1
    WHITE = 3
    
    epd = EPD()
    
    _start = time.ticks_ms()
    epd.init()
    _stop = time.ticks_ms()
    print("init used: %d ms" % (_stop - _start))

    _start = time.ticks_ms()
    epd.EPD_3IN7_1Gray_Clear()
    _stop = time.ticks_ms()
    print("clear used: %d ms" % (_stop - _start))
    
    epd.fill(WHITE)
    epd.text('Hello world!', 10, 60, BLACK)
    epd.line(0, 10, 380, 10, BLACK)
    
    for i in range(0, 10):
        #print(f"loop {i}")
        epd.rect(i * 10, 430, 280, 10, epd.black)
        epd.text(str(i), 100 + i * 10, 330, epd.black)
    
    epd.line(0, 0, 959, 639, BLACK)
    _start = time.ticks_ms()
    epd.refresh()
    _stop = time.ticks_ms()
    print("time used: %d ms" % (_stop - _start))
    
    epd.sleep()
    
    pass

if __name__ == "__main__":
    main()
