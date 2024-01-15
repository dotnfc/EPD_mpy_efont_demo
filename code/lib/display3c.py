#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# red/black/white epd with image support, based on frameBuffer
#
# by dotnfc, 2023/09/26
#

import sys
from efont import *
import machine
import time
import ufont
if sys.platform == 'linux':
    from panel.epd_sdl_102rbw import *
else:
    from panel.epd_102a013c import *

# color definitions for Monochrome EPD, values correspond to RGB565 values for TFTs
EPD_BLACK     = const(0x0000)
EPD_WHITE     = const(0xFFFF)

# values for 3-color
EPD_RED       = const(0xF800) # 255,   0,   0
EPD_YELLOW    = const(0xFFE0) # 255, 255,   0 !!no longer same as GxEPD_RED!!
EPD_COLORED   = EPD_RED


class EpdImage(EPD):
        
    def __init__(self):
        EPD.__init__(self)
        self.image = Image(self.WIDTH, self.HEIGHT)
        self.fb = self      # default fb object is black and white buffer
        self.fonts = {}     # fonts loaded
        self.font = None    # font object currently selected
        
        self.foreColor = EPD_BLACK
        self.backColor = EPD_WHITE
        
    def clear(self, bw = EPD_WHITE, rw = EPD_WHITE):
        if bw == EPD_WHITE:
            self.fill(RBW_WHITE)
        else:
            self.fill(RBW_BLACK)

        if rw == EPD_WHITE:
            self.fb_rw.fill(RRW_WHITE)
        else:
            self.fb_rw.fill(RRW_RED)
        
    def drawImage(self, x, y, filename):
        '''Draw image file at (x, y).'''
        self.image.setColor(self.foreColor, self.backColor)
        self.image.load(filename, True)        
        self.image.draw(self.fb, x, y)

    def deepSleep(self, microseconds):
        '''deep sleep for microseconds.'''
        if sys.platform == "linux":
            print("sys deepsleep")
            while(not self.eventProcess()):
                time.sleep(0.01)
        else:
            machine.deepsleep(microseconds)

    def runable(self):
        if sys.platform == "linux":
            runn = self.eventProcess()
            if runn:
                print(f"running {runn}")
            return not runn
        else:
            return False # in hardware, we just refresh ui and do deep sleep
    
    def setColor(self, foreColor, backColor):
        '''Set image/font drawing color, and select internal working Frame Buffer.
        
        Args:
            foreColor: foreground color
            backColor: background color
        '''
        
        if foreColor == EPD_RED or backColor == EPD_RED:
            self.fb = self.fb_rw    # red & white buffer

            # map to panel color
            if foreColor == EPD_RED:
                self.foreColor = RRW_RED
                self.backColor = RRW_WHITE
            else:
                self.foreColor = RRW_WHITE
                self.backColor = RRW_RED
        else:
            self.fb = self          # black & white buffer
            
            # map to panel color
            if foreColor == EPD_BLACK:
                self.foreColor = RBW_BLACK
                self.backColor = RBW_WHITE
            else:
                self.foreColor = RBW_WHITE
                self.backColor = RBW_BLACK
        
        if self.font != None:
            self.font.setRender(self.fb)    # update current font render
            self.font.setColor(self.foreColor, self.backColor)

    def rounded_rect(self, x, y, w, h, r, color):
        self.ellipse(x + r, y + r, r, r, color, False, 2) # left-top
        self.ellipse(x + w - r, y + r, r, r, color, False, 1) # right-top
        self.ellipse(x + r, y + h - r, r, r, color, False, 4) # left-bottom
        self.ellipse(x + w - r, y + h - r, r, r, color, False, 8) # right-bottom
        
        # horizon
        self.hline(x + r, y, w - 2 * r, color)
        self.hline(x + r, y + h, w - 2 * r, color)
        
        # vertical
        self.vline(x, y + r, h - 2 * r, color)
        self.vline(x + w, y + r, h - 2 * r, color)
                    
    def loadFont(self, fonName, size=16):
        '''Load font file from storage.
        
        Args:
            fonName: Font name from font registry
        '''
        
        if fonName in self.fonts:
            fon = self.fonts[f'{fonName}']
            fon.setSize(size)
            return fon  # font loaded before
        
        fon = FT2(ufont.fonts[f'{fonName}'], render=self.fb, mono=True, size=size)
        self.fonts[f'{fonName}'] = fon
        return fon
    
    def selectFont(self, fonName):
        '''Select current font.
        
        Args:
            fonName: Font name to select, which should be in the 'font registry'
            
        Return:
            True if the font selected, False otherwise
        '''
        if fonName in self.fonts:
            self.font = self.fonts[f'{fonName}']
            self.font.setRender(self.fb)    # update current font render
            self.font.setColor(self.foreColor, self.backColor)
            return True
        
        print("failed to load font")
        return False
    
    def drawText(self, x, y, w, h, align, text, size=-1):
        if self.font == None:
            raise RuntimeError("Font not selected")
        
        if size != -1:
            return self.font.drawString(x, y, w, h, align, text, size)
        else:
            return self.font.drawString(x, y, w, h, align, text)

    def text_3c(self, s, x, y, c=1):
        '''
        Write text to the FrameBuffer using the the coordinates as the upper-left corner of the text.         
        The color of the text can be defined by the optional argument but is otherwise a default value of 1.         
        All characters have dimensions of 8x8 pixels and there is currently no way to change the font.
        '''
        self.fb.text(s, x, y, self.convert_color(c))
    
    def dot_hline_3c(self, x1, y1, x2, c):
        x = x1
        while x < x2:
            self.fb.line(x, y1, x + 7, y1, self.convert_color(c))
            x = x + 10
            
    def line_3c(self, x1, y1, x2, y2, c):
        '''
        Draw a line from a set of coordinates using the given color and a thickness of 1 pixel.         
        The line method draws the line up to a second set of coordinates whereas the hline and vline methods 
        draw horizontal and vertical lines respectively up to a given length.
        '''
        self.fb.line(x1, y1, x2, y2, self.convert_color(c))
        
    def fill_3c(self, x1, y1, x2, y2, c):
        '''
        Draw a line from a set of coordinates using the given color and a thickness of 1 pixel.         
        The line method draws the line up to a second set of coordinates whereas the hline and vline methods 
        draw horizontal and vertical lines respectively up to a given length.
        '''
        # def fill_rect(self, *args, **kwargs)
        self.fb.line(x1, y1, x2, y2, self.convert_color(c))
        
    def rect_3c(self, x, y, w, h, c, fill=False):
        '''
        Draw a rectangle at the given location, size and color.
        '''
        self.fb.rect(x, y, w, h, self.convert_color(c), fill)

    def ellipse_3c(self, x, y, xr, yr, c, fill=False):
        '''
        Draw an ellipse at the given location. 
        Radii xr and yr define the geometry; equal values cause a circle to be drawn. 
        The c parameter defines the color.
        '''
        self.fb.ellipse(x, y, xr, yr, self.convert_color(c), fill)

    def convert_color(self, c):
        if c:
            return self.foreColor
        else:
            return self.backColor