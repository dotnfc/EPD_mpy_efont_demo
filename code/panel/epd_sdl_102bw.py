#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# epd sdl simulator 10.2' (960x480 black/white)
# by dotnfc, 2023/12/30
#

from .epd_sdl import * 
from framebuf import *
from micropython import const

class FrameBufferEx(FrameBuffer):
    def __init__(self, buf, w, h, mode):
        super().__init__(buf, w, h, mode)

class EPD(EpdSDLBase, FrameBuffer):
    
    # Display resolution
    WIDTH  = const(960)
    HEIGHT = const(640)
    BUF_SIZE = const(WIDTH * HEIGHT // 8)
    
    def __init__(self, zoom = 1):
        self.buffer = bytearray(self.BUF_SIZE)
        EpdSDLBase.__init__(self, self.WIDTH, self.HEIGHT, zoom)
        FrameBufferEx.__init__(self, self.buffer, self.WIDTH, self.HEIGHT, MONO_HLSB)
        
    def init(self):
        pass
    
    def reset(self):
        pass
    
    def sleep(self):
        pass
        
    def refresh(self, buf=None, full=True):
        if buf is None:
            buf = self.buffer
        self.updateSubWindowBW(buf, 0, 0, self.WIDTH, self.HEIGHT)
        self.updateScreen()
    
    def refresh_fast(self, image, x, y, w, h):
        if image is None:
            buf = self.buffer
        self.updateSubWindowBW(image, x, y, w, h)
        self.updateScreen()
