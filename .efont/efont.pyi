__author__ = 'dotnfc'


ALIGN_LEFT = 0    # Left alignment
ALIGN_RIGHT = 1   # Right alignment
ALIGN_CENTER = 2  # Center alignment

class FT2(object):
    """
    A FreeType2 Wrapper class
    """
    mono = False   # monochrome drawing for EPD
    bold = False   # bold style when drawing
    italic = False # italic style when drawing
    
    def __init__(self, file: str,
             render: framebuf.FrameBuffer,
             size: int = 16,
             mono: bool = False,
             bold: bool = False,
             italic: bool = False):
        """Load font from file(.ttf, .pcf).
        
        Args:
            file: file path to load.
            render: an instance of framebuf.FrameBuffer which pixel() method will be called when drawString().
            size: default size to draw text
            mono: true for loading as mono font for EPD
            bold: bold style to draw text
            italic: italic style to draw text
            
        Returns:
            return True if font was loaded
        
        Raises:
            Error - raises an exception
        """
        pass
    
    def unload(self):
        '''Unload font and free resources.
        '''
        pass
    
    def drawString(self,
               x: int,
               y: int,
               w: int = -1,
               h: int = -1,
               align: int = 0,
               text: str = "",
               size: int = 16) -> int:
        '''Draw text string.
        
        Args:
            x: x coordinate of text drawing box
            y: y coordinate of text drawing box
            w: width of text drawing box
            h: height of text drawing box
            align: alignment of text, ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT
            text: text to draw
            size: optional size to draw text
            
        Return:
            next x coordinate after drawing
        '''
        pass
    
    def getStringWidth(self, text : str) -> int:
        '''Get text width when drawing.
        
        Args:
            text: text for measurement
        
        Return:
            text width
        '''
        pass
    
    def setSize(self, size: int):
        '''Set font size to draw.
        
        Args:
            Size, to modify
        '''
        pass
    
    def setColor(self, fg: int, bg: int):
        '''Set the foreground and background color when monochrome mode
        '''
        pass
    
    def setRender(self, render: FrameBuffer):
        '''Set font new render
        
        Args:
            render, new render to use
        '''
        pass

class Image(object):
    """PNG, JPG Wrapper Class
    """
    
    def __init__(self, width: int, height: int):
        '''
        Args:
            width, height: container width and height when drawing
        '''
        pass

    def load(self, file : str, 
            mono : bool = False):
        '''Load image from file(.png, .jpg).
        
        Args:
            file: file path to load
            mono: load as mono image for EPD
        
        Return:
            loaded image (width, height)
        '''
        pass
    
    def draw(self, 
            render:framebuf.FrameBuffer, 
            x : int = 0, 
            y : int = 0, 
            unload : bool = True):
        '''Render image at(render, x, y).
        
        Args:
            render: the container to rend, must be a FrameBuffer (derived) instance
            x, y: left-top position to draw
            unload: free image resources after drawing automatically.
        '''
        pass
    
    def setColor(self, fg: int, bg: int):
        '''Set the foreground and background color when monochrome mode
        '''
        pass
    
    def unload(self):
        '''Unload image, free image resource.
        '''
        pass

