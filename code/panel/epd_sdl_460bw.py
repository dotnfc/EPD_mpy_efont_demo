#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# epd sdl simulator 4.6' (800x480 black and white)
# by dotnfc, 2023/10/25
#

from .epd_sdl import * 
from framebuf import *
from micropython import const

class FrameBufferEx(FrameBuffer):
    def __init__(self, buf, w, h, mode):
        super().__init__(buf, w, h, mode)

class EPD(EpdSDLBase, FrameBuffer):
    
    # Display resolution
    WIDTH  = const(800)
    HEIGHT = const(480)
    BUF_SIZE = const(WIDTH * HEIGHT // 8)
    
    def __init__(self, zoom = 1):
        self.buf = bytearray(self.BUF_SIZE)
        EpdSDLBase.__init__(self, self.WIDTH, self.HEIGHT, zoom)
        FrameBufferEx.__init__(self, self.buf, self.WIDTH, self.HEIGHT, MONO_HLSB)
        
    def init(self):
        pass
    
    def reset(self):
        pass
    
    def sleep(self):
        pass
        
    def refresh(self, buf=None, full=True):
        if buf is None:
            buf = self.buf
        self.updateSubWindowBW(buf, 0, 0, self.WIDTH, self.HEIGHT)
        self.updateScreen()
        pass
