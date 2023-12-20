import os
import sys
import time
from logging import getLogger

logger = getLogger(__name__)

_PORTS_CACHE = []
_PORTS_CACHE_TIME = 0


def get_serial_port_label(p) -> str:
    # On Windows, port is given also in description
    if p.product:
        desc = p.product
    elif p.interface:
        desc = p.interface
    else:
        desc = p.description.replace(f" ({p.device})", "")

    if desc == "USB Serial Device":
        # Try finding something less generic
        if p.product:
            desc = p.product
        elif p.interface:
            desc = p.interface

    return f"{desc} @ {p.device}"


def list_serial_ports(max_cache_age: float = 0.5, skip_logging: bool = False):
    global _PORTS_CACHE, _PORTS_CACHE_TIME

    cur_time = time.time()
    if cur_time - _PORTS_CACHE_TIME > max_cache_age:
        _PORTS_CACHE = _list_serial_ports_uncached(skip_logging=skip_logging)
        _PORTS_CACHE_TIME = cur_time

    return _PORTS_CACHE


def _list_serial_ports_uncached(skip_logging: bool = False):
    if not skip_logging:
        logger.info("Listing serial ports")
    # serial.tools.list_ports.comports() can be too slow
    # because os.path.islink can be too slow (https://github.com/pyserial/pyserial/pull/303)
    # Workarond: temporally patch os.path.islink
    old_islink = os.path.islink
    try:
        if sys.platform == "win32":
            os.path.islink = lambda _: False

        if sys.platform == "win32":
            try:
                from adafruit_board_toolkit._list_ports_windows import comports
            except ImportError:
                logger.info("Falling back to serial.tools.list_ports.comports")
                from serial.tools.list_ports import comports
        elif sys.platform == "darwin":
            try:
                from adafruit_board_toolkit._list_ports_osx import comports
            except ImportError:
                logger.info("Falling back to serial.tools.list_ports.comports")
                from serial.tools.list_ports import comports
        else:
            from serial.tools.list_ports import comports

        irrelevant = ["/dev/cu.Bluetooth-Incoming-Port", "/dev/cu.iPhone-WirelessiAP"]
        result = []
        for p in comports():
            if p.device not in irrelevant:
                result.append(p)

        return result
    finally:
        os.path.islink = old_islink


def port_exists(device):
    for port in list_serial_ports():
        if port.device == device:
            return True

    return False


def get_uart_adapter_vids_pids():
    # https://github.com/per1234/zzInoVIDPID
    # https://github.com/per1234/zzInoVIDPID/blob/master/zzInoVIDPID/boards.txt
    # http://esp32.net/usb-uart/
    # https://www.usb.org/developers
    # https://github.com/espressif/usb-pids
    return {
        (0x1A86, 0x7523),  # CH340 (HL-340?)
        (0x1A86, 0x5523),  # CH341
        (0x1A86, 0x55D4),  # CH9102F, seen at Adafruit Feather ESP32 V2, M5 stamp C3
        (0x10C4, 0xEA60),  # CP210x,
        (0x0403, 0x6001),  # FT232/FT245 (XinaBox CW01, CW02)
        (0x0403, 0x6010),  # FT2232C/D/L/HL/Q (ESP-WROVER-KIT)
        (0x0403, 0x6011),  # FT4232
        (0x0403, 0x6014),  # FT232H
        (0x0403, 0x6015),  # FT X-Series (Sparkfun ESP32)
        (0x0403, 0x601C),  # FT4222H
        (0x303A, 0x1001),  # Espressif's built-in USB-to-Serial, seen at QtPy C3
    }


def get_port_info(port):
    for info in list_serial_ports():
        if info.device == port:
            return info
    raise RuntimeError("Port %s not found" % port)


if __name__ == "__main__":
    ports = list_serial_ports()
    print("Ports: %s" % ports)
    