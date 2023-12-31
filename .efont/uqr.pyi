__author__ = 'dotnfc'

ECC_LOW = 0
ECC_MEDIUM = 1
ECC_QUARTILE = 2
ECC_HIGH = 3
Mode_NUMERIC = 1
Mode_ALPHANUMERIC = 2
Mode_BYTE = 4
VERSION_MIN = 1
VERSION_MAX = 40
  
class uqr(object):
    """mpy-qr producing QR codes"""
        
    def load(self, message : str, min_version:int=1, max_version:int=10, 
             encoding:int=0, mask:int=-1, ecl=ECC_LOW):
        '''Create a QR code.
        
        Args:
            message: Binary or text to be put into the QR code. Can be bytes or unicode string.
            encoding: Default is auto detect, but you can force encoding to be bytes, alphanumeric (ie. 0—9A—Z $%*+-./:") or numeric (0—9).
            mask: default is -1 for auto select best mask, otherwise a number from 0..7
            min_version: minimum QR version code (ie. size)
            max_version: maximum QR version code. size). Supports up to 40, but default is lower to conserve memory in typical cases.
            ecl: error correcting level. If it can use a better error correcting level, without making the QR larger (version) it will always do that, so best to leave as LOW.
        
        Return:
            Returns a RenderedQR object, with these methods:
                __str__: renders as a QR code (mostly for fun)
                                
        Note:
            Using invalid parameters, such as asking for lower case to be encoded in alphanumeric will raise a RuntimeError with the line number of qrcodegen.c where you hit the assertion.
            To control the QR version number and therefore fix it's graphic size, set max and min version to the same number.
        '''
        pass
    
    def width(self) ->int:
        '''Get the number of pixels in the QR code (be sure to add some whitespace around that)'''
        pass
    
    def get(self, x, y) ->int:
        '''return pixel value at that location.
        
        Args:
            x, y: the location to retrieve the pixel value
        '''
        pass
    
    def packed(self) ->int:
        '''returns a 3-tuple with (width, height, pixel_data).
        
        Note:
            Pixel data is 8-bit packed, and padded so that each row is byte-aligned. 
            The padding is at the right side of the image and will be: 0 < (width-height) < 8
        '''
        pass
    
    def draw(self, 
            render:framebuf.FrameBuffer, 
            x : int = 0, 
            y : int = 0, 
            scale : int = 1,
            c: int =0):
        '''draw qrcode.
        
        Args:
            x, y: the location to draw
            scale: enlarge scale
            color: forecolor to draw
        '''
