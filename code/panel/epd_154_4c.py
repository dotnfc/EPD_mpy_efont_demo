#-*- coding:utf-8 -*-
# panel driver, 
# FPC Label: HINK-E0154A05-A2
# Panel    : GDEY0154D67 (200 x 200)
# IC       : SSD1681
# Product  : 
# by dotnfc, 2024/12/02, wangshujun Boost FrameBuffer required
# https://github.com/wangshujun-tj/mpy-Framebuf-boost-code/tree/main
#-------------------------------------------------------------------

from micropython import const
from machine import SPI, Pin
from time import sleep_ms
import time
from framebuf import *
from logger import *
from board import *
import ustruct

BUSY = const(0)  # 0 = busy, 1=idle

class EPD(FrameBuffer):
    # Display resolution
    WIDTH  = const(200)
    HEIGHT = const(200)
    BUF_SIZE = const(WIDTH * HEIGHT // 4)
    
    def __init__(self):
        self.spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=EPD_PIN_SCK, mosi=EPD_PIN_SDA)
        self.spi.init()
        
        self.cs = EPD_PIN_CS
        self.dc = EPD_PIN_DC
        self.rst = EPD_PIN_RST
        self.busy = EPD_PIN_BUSY
        
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        
        self.black = 0x00
        self.white = 0xff
        
        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.buffer = bytearray(BUF_SIZE)        
        super().__init__(self.buffer, self.WIDTH, self.HEIGHT, GS2_HMSB)
       
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

    def display(self, buf):
        pass

    def display_partial(self, buf):
        pass

    def refresh(self, buf = None, full=False):
        self._command(0x10)
        self._data(self.buffer)
        
        self._command(0x12) #Display Update Control
        self._data(0x00) 
        self.wait_until_idle()
    
    def clear_screen(self, color=0):
        self.fill(color)
        self._command(0x10)
        self._data(self.buffer)
        self.refresh() 

    def power_on(self):
        self.wait_until_idle()
        
    def power_off(self):
        self.wait_until_idle()
    
    def init(self):
        self.reset()

        self.wait_until_idle()
        self._command(0x4D)
        self._data(0x78)

        self._command(0x00)  # PSR
        self._data(0x03)  # 0x0F
        self._data(0x29)

        self._command(0x06)  # BST_P
        self._data(0x0D)  # 47uH
        self._data(0x12)
        self._data(0x30)
        self._data(0x20)
        self._data(0x19)
        self._data(0x2A)
        self._data(0x22)

        self._command(0x50)  # CDI
        self._data(0x37)

        self._command(0x61)  # TRES
        source_bits = self.WIDTH  # 假设Source_BITS和Gate_BITS是之前定义的变量
        gate_bits = self.HEIGHT
        self._data(source_bits // 256)  # Source_BITS_H
        self._data(source_bits % 256)  # Source_BITS_L
        self._data(gate_bits // 256)   # Gate_BITS_H
        self._data(gate_bits % 256)    # Gate_BITS_L

        self._command(0xE9)
        self._data(0x01)

        self._command(0x30)
        self._data(0x08)

        self._command(0x04) # Power on
        self.wait_until_idle()

    def wait_until_idle(self, timeout=30000):
        while self.busy.value() == BUSY:
            sleep_ms(10)
            timeout = timeout - 10
            if timeout <=0 :
                raise RuntimeError("Timeout out for waiting busy signal")
        
        sleep_ms(2)

    def reset(self):
        '''reset panel'''
        self.rst(0)
        sleep_ms(12)

        self.rst(1)
        sleep_ms(12)
        
    def sleep(self):
        self._command(0X02) #power off
        self._data(0x00)
        self.wait_until_idle() # waiting for the electronic paper IC to release the idle signal
    
        self._command(0X07) # deep sleep
        self._data(0xA5)

def clear_screen(epd, msg, color):
    print(msg)
    _start = time.ticks_ms()
    epd.clear_screen(color) # black
    _stop = time.ticks_ms()
    print("clear screen used: %d ms" % (_stop - _start))
    sleep_ms(1000)
    
def main():
    BLACK = 0
    RED = 3
    WHITE = 1
    YELLOW = 2
    
    epd = EPD()
    
    _start = time.ticks_ms()
    epd.init()
    _stop = time.ticks_ms()
    print("init used: %d ms" % (_stop - _start))

    #clear_screen(epd, "black", 0x00)
    #clear_screen(epd, "white", 0x55)
    #clear_screen(epd, "yellow", 0xaa)
    #clear_screen(epd, "red", 0xff)
    
    print("text test begin")
    epd.fill(0x5)
    epd.text('Hello world!', 10, 60, BLACK)
    epd.line(0, 10, 180, 10, BLACK)
    
    epd.line(0, 20, 180, 20, YELLOW)
    epd.line(0, 0, 199, 199, RED)
    epd.text('Hello world!', 10, 80, RED)
    
    _start = time.ticks_ms()
    epd.refresh()
    _stop = time.ticks_ms()
    print("time used: %d ms" % (_stop - _start))
    
    epd.sleep()

if __name__ == "__main__":
    main()



