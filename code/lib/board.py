#-*- coding:utf-8 -*-
#----------------------------------------------------------------
#
# board config
#
# by dotnfc, 2023/09/22
#
from micropython import const
try:
    from machine import Pin
except ImportError:
    from usdl2_pin import Pin

# led
LED_BLUE     = Pin(4)

# buzzer
BUZZER       = Pin(10)

# epd io
EPD_PIN_CS   = Pin(13)
EPD_PIN_SCK  = Pin(12)
EPD_PIN_SDA  = Pin(11)

EPD_PIN_CS2  = Pin(48)

EPD_PIN_DC   = Pin(14)
EPD_PIN_RST  = Pin(21)
EPD_PIN_BUSY = Pin(47)

# button
KEY_IO0      = Pin(0)
KEY_USER     = Pin(9)

#
USB_PWR_SENSE= Pin(8)
NFC_PWR_SENSE= Pin(18)

# battery
BATTERY_ADC  = Pin(1)
BATTERY_ADC_EN= Pin(2)

# temperature sensor
SENSOR_EN   = Pin(5)  # -> IO5
SENSOR_SCL  = Pin(39)
SENSOR_SDA  = Pin(38)

# nfc tag
NFC_TAG_NSS = Pin(17)
NFC_TAG_IRQ = Pin(6)
NFC_TAG_SCL = Pin(16)
NFC_TAG_SDA = Pin(15)

# sd mmc one data line
SD_MMC_CLK = Pin(41)
SD_MMC_CMD = Pin(40)
SD_MMC_D0  = Pin(42)
