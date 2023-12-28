#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# epd sdl simulator 10.2' (960x480 red/black/white)
# by dotnfc, 2023/09/26
#

from .epd_sdl import * 
from framebuf import *
from micropython import const

# RAM Black(0) & White(1)
RBW_BLACK = const(1)
RBW_WHITE = const(0)

# RAM Red(1) & White(0)
RRW_RED = const(1)
RRW_WHITE = const(0)

class FrameBufferEx(FrameBuffer):
    def __init__(self, buf, w, h, mode):
        super().__init__(buf, w, h, mode)

class EPD(EpdSDLBase, FrameBuffer):
    
    # Display resolution
    WIDTH  = const(960)
    HEIGHT = const(640)
    BUF_SIZE = const(WIDTH * HEIGHT // 8)
    
    def __init__(self, zoom = 1):
        self.colorful = True  # default 3-colors
        self.buf_bw = bytearray(self.BUF_SIZE)
        self.buf_rw = bytearray(self.BUF_SIZE)
        self.fb_rw = FrameBuffer(self.buf_rw, self.WIDTH, self.HEIGHT, MONO_HLSB)
        
        EpdSDLBase.__init__(self, self.WIDTH, self.HEIGHT, zoom)
        FrameBufferEx.__init__(self, self.buf_bw, self.WIDTH, self.HEIGHT, MONO_HLSB)
    
    def setColorful(self, mono: bool):
        self.colorful = not mono
        
    def init(self):
        pass
    
    def reset(self):
        pass
    
    def sleep(self):
        pass
        
    def refresh(self, buf=None, full=True):
        if self.colorful:
            self.updateSubWindow3Color(self.buf_bw, self.buf_rw, 0, 0, self.WIDTH, self.HEIGHT)
        else:
            self.updateSubWindowBW(self.buf_bw, 0, 0, self.WIDTH, self.HEIGHT)
            
        self.updateScreen()
