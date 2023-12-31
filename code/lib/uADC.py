#-*- coding:utf-8 -*-
# machine.ADC stub for unix port
# by dotnfc, 2023/09/20
#
# for ESP32, 
# Note that the absolute maximum voltage rating for input pins is 3.6V. 
# Going near to this boundary risks damage to the IC!
# 
class ADC:
    """
    Access the ADC associated with a source identified by *id*.  This
    *id* may be an integer (usually specifying a channel number), a
    :ref:`Pin <machine.Pin>` object, or other value supported by the
    underlying machine.

    If additional keyword-arguments are given then they will configure
    various aspects of the ADC.  If not given, these settings will take
    previous or default values.  The settings are:

      - *atten* specifies the input attenuation.
    """
    WIDTH_9BIT = const(9) 
    WIDTH_10BIT = const(10)
    WIDTH_11BIT = const(11)
    WIDTH_12BIT = const(12)    

    ATTN_0DB = const(10)   # No attenuation (100mV - 950mV)
    ATTN_2_5DB = const(11) # 2.5dB attenuation (100mV - 1250mV)
    ATTN_6DB = const(12)   # 6dB attenuation (150mV - 1750mV)
    ATTN_11DB = const(13)  # 11dB attenuation (150mV - 2450mV)

    def read_u16(self) -> int:
        """
        Take an analog reading and return an integer in the range 0-65535.
        The return value represents the raw reading taken by the ADC, scaled
        such that the minimum value is 0 and the maximum value is 65535.
        """
        return 32225
    
    def init(self, *, atten):
        """
        Apply the given settings to the ADC.  Only those arguments that are
        specified will be changed.  See the ADC constructor above for what the
        arguments are.
        """
        return self

    def read_uv(self) -> int:
        """
        Take an analog reading and return an integer value with units of
        microvolts.  It is up to the particular port whether or not this value
        is calibrated, and how calibration is done.
        """
        return 32225
    
    def width(self, *args, **kwargs):
        ...
        
    def read(self, *args, **kwargs):
        ...

    def block(self):
        """
        Return the :ref:`ADCBlock <machine.ADCBlock>` instance associated with
        this ADC object.

        This method only exists if the port supports the
        :ref:`ADCBlock <machine.ADCBlock>` class.
        """
        return self

