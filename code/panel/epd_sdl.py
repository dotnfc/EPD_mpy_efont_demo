#-*- coding:utf-8 -*-
# epd sdl simulator base class
# by dotnfc, 2023/09/11

# https://wiki.libsdl.org/SDL_CreateRenderer

import time
import array
from usdl2 import *
from micropython import const

# import os
# os.chdir('/home/dotnfc/mpy_home')

# color in 0xAARRGGBB format
SDL_RED    = const(0xffcc0000)
SDL_BLACK  = const(0xff363636)
SDL_WHITE  = const(0xfff2f2f2)
SDL_YELLOW = const(0xfff2f2f2)

SDL_WINDOW_SHOWN = const(0x00000004)
SDL_WINDOW_ALLOW_HIGHDPI = const(0x00002000)
SDL_RENDERER_SOFTWARE = const(0x00000001)       # The renderer is a software fallback
SDL_RENDERER_ACCELERATED = const(0x00000002)    # The renderer uses hardware acceleration
SDL_RENDERER_PRESENTVSYNC = const(0x00000004)   # Present is synchronized with the refresh rate
SDL_RENDERER_TARGETTEXTURE = const(0x00000008)  # The renderer supports
NULL = None

class EpdSDLBase():
    def __init__(self, width, height, zoom):
        self._w = width
        self._h = height
        self._pitch = width * 4
        self._pixel = array.array("I", [0] * width*height)
        self._buf_size_byte = width*height // 8
        
        self.setRamUpdateArea(0, 0, width, height)
        pos_center = SDL_WINDOWPOS_CENTERED
        flags = SDL_WINDOW_SHOWN | SDL_WINDOW_ALLOW_HIGHDPI
        self._window = SDL_CreateWindow("EFORE Simulator Window", pos_center, pos_center, width * zoom, height * zoom, flags)
        self._renderer = SDL_CreateRenderer(self._window, -1, SDL_RENDERER_ACCELERATED)
        self._texture = SDL_CreateTexture(self._renderer, SDL_PIXELFORMAT_ARGB8888, SDL_TEXTUREACCESS_STREAMING, self._w, self._h)

    async def async_refresh(self):
        ref_evt = array.array("P", [0])
        
        while True:
            await self.refresh_event.wait()
            result = SDL_PollEvent(ref_evt)
            if result:
                event = ref_evt[0]
                # if event.type 
            self.refresh_event.clear()
            
    def __del__(self):
        SDL_DestroyTexture(self._texture)
        SDL_DestroyRenderer(self._renderer)
        SDL_DestroyWindow(self._window)
        SDL_Quit()
        pass
        
    def setScale(self, scale):
        refw = array.array("P", [0])
        refh = array.array("P", [0])
        SDL_GetWindowSize(self._window, refw, refh)
        w = refw[0] * scale
        h = refh[0] * scale
        SDL_SetWindowSize(self._window, w, h)
        
    def setRamUpdateArea(self, px, py, pw, ph):
        self._px = px
        self._py = py
        self._pw = pw
        self._ph = ph
        
    def display(self):
        SDL_RenderPresent(self._render)
    
    def clearDisplay(self):
        SDL_SetRenderDrawColor(self._renderer, 0, 0, 0, 255)
        SDL_RenderClear(self._renderer)
        
    def fillBWRam(self, color):
        ARGB = SDL_BLACK     # default black, in 0xAARRGGBB format
        if color != 0:
            ARGB = SDL_WHITE # white

        bufLen = len(self._pixel)
        for i in range(bufLen):
            self._pixel[i] = ARGB
    
    def fillRWRam(self, color):
        ARGB = SDL_RED       # default red, in 0xAARRGGBB format
        if color != 0:
            ARGB = SDL_WHITE # white
    
        bufLen = len(self._pixel)
        for i in range(bufLen):
            self._pixel[i] = ARGB
    
    def updateScreen(self, full=True):
        SDL_UpdateTexture(self._texture, NULL, self._pixel, self._pitch)
        SDL_RenderCopy(self._renderer, self._texture, NULL, NULL)
        SDL_RenderPresent(self._renderer)
        SDL_UpdateWindowSurface(self._window)
        if full:
            time.sleep(0.8)
        else:
            time.sleep(0.3)

    def updateSubWindowBW(self, buffer, px, py, pw, ph):
        color = 0
        _wb = pw // 8  # Integer division in Python

        for i in range(ph):
            y_ = i
            for j in range(_wb):
                x_ = j * 8
                idx = i * _wb + j
                c_bw = buffer[idx]
                # preview colors: https://www.w3schools.com/colors/colors_picker.asp
                for shift in range(8):
                    color = SDL_BLACK  # default black, in 0xAARRGGBB format
                    if c_bw & 0x80:
                        color = SDL_WHITE  # white
                    c_bw <<= 1
                    self._pixel[self._w * (py + y_) + (px + x_)] = color
                    x_ += 1

    def updateSubWindowRW(self, buffer, px, py, pw, ph):
        color = 0
        _wb = pw // 8  # Integer division in Python

        for i in range(ph):
            y_ = i
            for j in range(_wb):
                x_ = j * 8
                idx = i * _wb + j
                c_rw = buffer[idx]
                # preview colors: https://www.w3schools.com/colors/colors_picker.asp
                for shift in range(8):
                    color = SDL_RED  # default black, in 0xAARRGGBB format
                    if c_rw & 0x80:
                        color = SDL_WHITE  # white
                    c_rw <<= 1
                    self._pixel[self._w * (py + y_) + (px + x_)] = color
                    x_ += 1
     
    def updateSubWindow3Color(self, bwBuf, rwBuf, px, py, pw, ph):
        color = 0
        _wb = pw // 8  # Integer division in Python

        for i in range(ph):
            y_ = i
            for j in range(_wb):
                x_ = j * 8
                idx = i * _wb + j
                c_bw = bwBuf[idx]
                c_rw = rwBuf[idx]
                
                # preview colors: https://www.w3schools.com/colors/colors_picker.asp
                for shift in range(8):
                    color = SDL_WHITE  # default white, in 0xAARRGGBB format
                    if c_bw & 0x80:
                        color = SDL_BLACK # black
                    elif c_rw & 0x80:
                        color = SDL_RED   # red
                    else:
                        color = SDL_WHITE # white
                        
                    c_bw <<= 1
                    c_rw <<= 1
                    
                    self._pixel[self._w * (py + y_) + (px + x_)] = color
                    x_ += 1
                    
    def eventProcess(self) -> bool:        
        return SDL_Poll()

    