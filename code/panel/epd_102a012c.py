#-*- coding:utf-8 -*-
# panel driver, based on {github}/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico-ePaper-3.7.py
# FPC Label: HINK-E102A01-A1
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
        self.spi = SPI(2, baudrate=15000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
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
        if lut == 1 :
            self._data(bytearray(self.lut_1Gray_GC))
        elif lut == 2 :
            self._data(bytearray(self.lut_1Gray_DU))
        elif lut == 3 :
            self._data(bytearray(self.lut_1Gray_A2))
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
                
    def clear_screen(self):
        
        self._set_pixel_address(0, 0)

        self._command(0x24)
        self.fill(self.white)
        self._data(self.buffer)

        self._command(0x26)
        self.fill(self.white)
        self._data(self.buffer)
        
        self.Load_LUT(1)

        self._command(0x20)
        self.wait_until_idle()
                
    def display(self, buf):

        self._command(0x49)
        self._data(0x00)
        self.Load_LUT(1)
        
        self._set_pixel_address(0, 0)

        self._command(0x24)
        self._data(buf)
        
        self._command(0x26)
        self._data(buf)
        
        self._command(0x20)
        self.wait_until_idle()
        
    def display_partial(self, buf):

        self.set_partial_area(0, 0, self.WIDTH, self.HEIGHT)
        self.Load_LUT(2)
        
        self._command(0x24)
        self._data(buf)
        #self._command(0x26)
        #self._data(buf)
                
        self._command(0x20)
        self.wait_until_idle()

    def refresh(self, buf = None, full=False):
        '''Update screen contents.
        
        Args:
            - buf: dummy, only internal buffer
            - full: dummy, only full more
        '''
        if full:
            self.display(self.buffer)
        else:
            self.display_partial(self.buffer)
        
    def power_on(self):
        self._command(0x04)
        self.wait_until_idle()
        
    def power_off(self):
        self._command(0x02)
        self.wait_until_idle()
    
    def init(self):
        self.reset()
        
        self._command(0x12)
        sleep_ms(30)  
        
        #self._command(0x46) # Auto Write RED RAM for Regular Pattern
        #self._data(0xF7)
        #self.wait_until_idle()
        #self._command(0x47) # Auto Write B/W RAM for Regular Pattern
        #self._data(0xF7)
        #self.wait_until_idle()

        # setting gate number: A0~A9: Width-1, B0/B1/B2 = 0
        self._command(0x01, ustruct.pack("<HB", self.WIDTH - 1, 0x00))
        
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
        self._data(0x0F)      # DM2 RAM ping-pong [0x4F:en] [0x0F:dis]
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)
        self._data(0xFF)  

        self._set_ram_address_range(0, 0, self.WIDTH -1, self.HEIGHT)

        self._command(0x22)   # Display Update Control 2
        self._data(0xCF)
        
        #self._command(0x21)   # Display Update Control 1
        #self._data(0x00)
        
        self.clear_screen()
        
    def wait_until_idle(self, timeout=10000):
        while self.busy.value() == BUSY:
            sleep_ms(10)
            timeout = timeout - 10
            if timeout <=0 :
                raise RuntimeError("Timeout out for waiting busy signal")
        
        sleep_ms(2)

    def _set_ram_entry_mode(self):
        '''Set the data entry mode'''
        self._command(0x11, 0x03)

    def _set_ram_address_range(self, x, y, w, h):
        # setting X direction start/end position of RAM: XSA = 0, XEA = WIDTH -1
        self._command(0x44, ustruct.pack('<HH', 0x0000, x + w))

        # setting Y direction start/end position of RAM: YSA = 0, YEA = HEIGHT -1
        self._command(0x45, ustruct.pack('<HH', 0x0000, y + h))
        
    def _set_pixel_address(self, x, y):
        self._command(0x4e, ustruct.pack('<H', x))
        self._command(0x4f, ustruct.pack('<H', y))
    
    def set_partial_area(self, x, y, w, h):
        # self._set_ram_entry_mode()
        self._set_ram_address_range(x, y, w, h)
        self._set_pixel_address(x, y)
        
    def reset(self):
        '''reset panel'''
        self.rst(0)
        sleep_ms(10)

        self.rst(1)
        sleep_ms(10)
        
    def sleep(self):
        # self.power_off()        
        self._command(0x10, 0x03)

    def refresh_fast(self, image, x, y, w, h):
        self.Load_LUT(2)
        self.set_partial_area(x, y, w -1, h -1)
        self._command(0x24)
        self._data(image)
        self._command(0x20)
        self.wait_until_idle()
        
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
    epd.clear_screen()
    _stop = time.ticks_ms()
    print("clear used: %d ms" % (_stop - _start))
    
    epd.fill(WHITE)
    epd.text('Hello world!', 10, 60, BLACK)
    epd.line(0, 10, 380, 10, BLACK)
    
    for i in range(0, 10):
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


