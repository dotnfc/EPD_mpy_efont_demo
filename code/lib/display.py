#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# monochrome epd with image support, based on frameBuffer
#
# by dotnfc, 2023/09/22
#

import sys
if sys.platform == 'linux':
    # from panel.epd_sdl_420bw import *
    from panel.epd_sdl_460bw import *
else:
    # from panel.epd_0426T8 import *
    from panel.epd_z96 import *
    # from panel.epd_z98 import *
    # from panel.epd_cz11 import *
    # from panel.epd_075a01 import *
    # from panel.epd_102a012c import *
    
from efont import *
import ufont
import machine
import time

EPD_BLACK     = const(0)
EPD_WHITE     = const(1)

class EpdImage(EPD):
        
    def __init__(self):
        EPD.__init__(self)
        self.image = Image(self.WIDTH, self.HEIGHT)
        
        self.fonts = {}     # fonts loaded
        self.font = None    # font object currently selected
        
        self.foreColor = EPD_BLACK
        self.backColor = EPD_WHITE
        
    def clear(self, fg = EPD_WHITE):
        self.fill(fg)
            
    def drawImage(self, x, y, filename):
        '''Draw image file at (x, y).'''
        self.image.setColor(self.foreColor, self.backColor)
        self.image.load(filename, True)
        self.image.draw(self, x, y)

    def deepSleep(self, microseconds):
        '''deep sleep for microseconds'''
        if sys.platform == "linux":
            print("sys deep sleep")
            while(not self.eventProcess()):
                time.sleep(0.01)
        else:
            machine.deepsleep(microseconds)
            
    def setColor(self, foreColor, backColor):
        '''Set image/font drawing color, and select internal working Frame Buffer.
        
        Args:
            foreColor: foreground color
            backColor: background color
        '''          
        
        self.foreColor = foreColor
        self.backColor = backColor
        
        if self.font != None:
            self.font.setRender(self)    # update current font render
            self.font.setColor(self.foreColor, self.backColor)
            
    def loadFont(self, fonName, size=16):
        '''Load font file from storage.
        
        Args:
            fonName: Font name from font registry
        '''
        
        if fonName in self.fonts:
            fon = self.fonts[f'{fonName}']
            fon.setSize(size)
            return fon  # font loaded before
        
        fon = FT2(ufont.fonts[f'{fonName}'], render=self, mono=True, size=size)
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
            self.font.setRender(self)    # update current font render
            self.font.setColor(self.foreColor, self.backColor) # fore back reverted
            return True
               
        return False
    
    def setFontSize(self, size):
        if self.font == None:
            raise RuntimeError("Font not selected")
        
        self.font.setSize(size)
        
    def drawText(self, x, y, w, h, align, text, size=-1):
        if self.font == None:
            raise RuntimeError("Font not selected")
        
        if size != -1:
            return self.font.drawString(x, y, w, h, align, text, size)
        else:
            return self.font.drawString(x, y, w, h, align, text)
