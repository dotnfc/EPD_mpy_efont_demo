"""
    BLE 协程，配置设备指令处理。需与 flutter app 配合[.NFC 2023/12/18]
"""
import sys
sys.path.extend(["/ex10d2", ""])

import deflate, io, machine
from micropython import const
import uasyncio as asyncio
import aioble, bluetooth
from wlan_helper import wifiHelper
import json, devinfo, settings

BLE_CMD_RESET = const(0x10)     # 复位设备
BLE_CMD_LIST_WIFI = const(0x11) # 列举 WIFI 热点
BLE_CMD_CONFIG = const(0x12)    # 获取/设置 配置
BLE_CMD_DEV_INFO = const(0x15)    # 获取设备信息

# BLE packet length
MAX_BLE_APDU        = 20 - 3 + 128 * (20 -1)
MAX_BLE_PACK_LEN    = 20

# eForecast Frame Tag
EFC_CMD_PING  = 0x81
EFC_CMD_KEEP  = 0x82
EFC_CMD_MSG   = 0x83
EFC_CMD_ERROR = 0xBF

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000

class bleFramer(object):
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.recv_data = None
        self.recv_frame_length = 0
        self.recv_done = False

    def start(self):
        # Register GATT server.
        self.uart_service = aioble.Service(_UART_UUID)
        self.uart_tx_characteristic = aioble.Characteristic(
            self.uart_service, _UART_TX, notify=True
        )
        self.uart_rx_characteristic = aioble.Characteristic(
            self.uart_service, _UART_RX, write=True
        )

        aioble.register_services(self.uart_service)
        
    def decompress(data, *args):
        '''decompress data
        sdat = decompress(zip, deflate.RAW)
        '''
        buf = io.BytesIO(data)
        with deflate.DeflateIO(buf, *args) as g:
            return g.read()

    def compress(data, *args):
        '''compress data
        sdat = 'hello world hello world '
        zip = compress(sdat, deflate.RAW)
        s = ', '.join(f'{byte}' for byte in zip)
        '''
        b = io.BytesIO()
        with deflate.DeflateIO(b, *args) as g:
            g.write(data)
        return b.getvalue()

    def recvFrame(self, data: bytearray):
        if self.recv_data == None:
            if data[0] == EFC_CMD_MSG:
                self.recv_frame_length = data[1] * 256 + data[2]
                self.recv_data = data[3:]
        else:
            # skip the seq
            self.recv_data = data[1:]
        
        if self.recv_data != None:
            if len(self.recv_data) >= self.recv_frame_length:
                self.recv_done = True

    def sendBlock (self, connection, seq, data, offset, length):
        buf = []
        slen = 0

        if (seq < 0):       # first block
            slen = MAX_BLE_PACK_LEN
            if (slen > length):
                slen = length
            buf = data[offset:(offset + slen)]
        else:               # partial block
            buf.append(seq)
            if length > (MAX_BLE_PACK_LEN - 1):
                slen = MAX_BLE_PACK_LEN - 1
            else:
                slen = length
            buf += data[offset:offset + slen]
        # print(f"{len(buf):02d}: {buf}")
        self.uart_tx_characteristic.notify(connection, bytearray(buf))        
        return slen
    
    def sendResponseSW(self, connection, apdu, sw):
        if isinstance(apdu,str):
            apdu = list(apdu.encode('utf-8')) # str -> bytes -> list

        apdu.append(sw >> 8)
        apdu.append(sw & 0xff)
        self.sendResponse(connection, apdu)
    
    def sendResponse(self, connection, apdu):
        tpdu = []
        self.reset()
        seq = -1
        offset = 0
        slen = len(apdu)
        
        tpdu.append(EFC_CMD_MSG)
        tpdu.append((slen >> 8) & 0xFF)
        tpdu.append((slen >> 0) & 0xFF)
        tpdu += list(apdu)
        tpduLen = len(tpdu)    
        
        while (tpduLen > 0):
            tsLen = self.sendBlock (connection, seq, tpdu, offset, tpduLen)
            offset  += tsLen
            tpduLen -= tsLen
            seq += 1
    
    def getDevName(self):
        mac = bluetooth.BLE().config('mac') # (addr_type, addr)
        sid = ''.join(['{:02X}'.format(b) for b in mac[1]])
        return f"eFore-{sid}"

    def processListWifi(self, connection):
        listAP = wifiHelper.listAP()
        strAPs = json.dumps(listAP)
        self.sendResponseSW(connection, strAPs, 0x9000)
        
    def processConfig(self, connection):
        lc = cmd = self.recv_data[4]
        if lc == 0:
            listCfg = settings.cfgGet()
            sCfg = json.dumps(listCfg)
            print(f"cfg =>\n{sCfg}")
            self.sendResponseSW(connection, sCfg, 0x9000)
        else:
            self.sendResponse(connection, [0x69, 0x82])
        
    def processDevInfo(self, connection):
        dev_info = devinfo.DeviceInfo()
        strAPs = json.dumps(dev_info)
        self.sendResponseSW(connection, strAPs, 0x9000)

    async def delayResetMcu(self):
        await asyncio.sleep_ms(300)
        if sys.platform == 'esp32':
            machine.reset()
        else:
            print('sys reset')
            
    def processEFCommand(self, connection):
        cmd = self.recv_data[1]
        capdu = ''.join(['{:02X}'.format(b) for b in self.recv_data])
        print(f"apdu: {capdu}")
        
        if cmd == BLE_CMD_RESET:
            print("reset")
            resp = [0x90, 0x00]
            self.sendResponse(connection, resp)
            asyncio.run(self.delayResetMcu())
            
        elif cmd == BLE_CMD_LIST_WIFI:
            self.processListWifi(connection)
        elif cmd == BLE_CMD_CONFIG:
            self.processConfig(connection)
        elif cmd == BLE_CMD_DEV_INFO:
            self.processDevInfo(connection)
        else:
            self.sendResponse(connection, [0x6D, 0x00])
        
    async def communication_task(self, connection):
        try:
            with connection.timeout(None):
                while True:
                    print("Waiting for write")
                    await self.uart_rx_characteristic.written()
                    msg = self.uart_rx_characteristic.read()
                    print('[d] one frame 1')
                    
                    if len(msg) < 3:
                        continue
                    
                    self.recvFrame(msg)
                    print('[d] one frame 2')
                    if self.recv_done:
                        print('[d] process command')
                        self.processEFCommand(connection)

        except aioble.DeviceDisconnectedError:
            print('disconnected')

    async def peripheral_task(self):
        while True:
            connection = await aioble.advertise(
                _ADV_INTERVAL_MS,
                name = self.getDevName(),
                services=[_UART_UUID]
            )
            print("Connection from", connection.device)

            await self.communication_task(connection)
            await connection.disconnected()
            print('Connection closed')

# Run both tasks.
async def ble_app():
    bleEF = bleFramer()
    bleEF.start()
    await bleEF.peripheral_task()

if __name__ == '__main__':
    asyncio.run(ble_app())


