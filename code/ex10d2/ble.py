"""
    BLE 协程，配置设备指令处理。需与 flutter app 配合[.NFC 2023/12/18]
"""
import sys
sys.path.extend(["/ex10d2", ""])

import gc
import deflate, io, machine
from micropython import const
import uasyncio as asyncio
import aioble, bluetooth
from qw_api import test_api
from wlan_helper import wifiHelper
import json, devinfo, settings

BLE_CMD_RESET = const(0x10)     # 复位设备
BLE_CMD_LIST_WIFI = const(0x11) # 列举 WIFI 热点 (数据压缩)
BLE_CMD_CONFIG = const(0x12)    # 获取/设置 配置
BLE_CMD_DEV_INFO = const(0x15)    # 获取设备信息
BLE_CMD_DEV_TEST = const(0x16)    # 测试功能

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
        self.recv_seq = 0

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
        
    def decompress(self, data):
        '''decompress data
        sdat = decompress(zip)
        '''
        buf = io.BytesIO(data)
        with deflate.DeflateIO(buf, deflate.RAW) as g:
            return g.read()

    def compress(self, data):
        '''compress data
        sdat = 'hello world hello world '
        zip = compress(sdat)
        s = ', '.join(f'{byte}' for byte in zip)
        '''
        b = io.BytesIO()
        with deflate.DeflateIO(b, deflate.RAW) as g:
            g.write(data)
        return b.getvalue()

    def recvFrame(self, data: bytearray):
        if data[0] == EFC_CMD_MSG:
            self.recv_frame_length = data[1] * 256 + data[2]
            self.recv_data = data[3:]
            self.recv_seq = 0
            #print(f"drcv 1 {data}")
        elif data[0] > 0x80:
            print(f"rcv error: {data}")
        else:
            if data[0] != self.recv_seq:
                return
            self.recv_seq = self.recv_seq + 1
            if self.recv_seq > 0x80:
                self.recv_seq = 0
            
            if self.recv_data is not None:
                self.recv_data = self.recv_data + data[1:]
            else:
                print(f"xrcv 2 {data}")
        
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
        gc.collect()
        # print(f"[f] {gc.mem_free()}")
        self.uart_tx_characteristic.notify(connection, bytearray(buf))
        return slen
    
    def sendResponseSW(self, connection, apdu, sw):
        if isinstance(apdu, str):
            apdu = list(apdu.encode('utf-8')) # str -> bytes -> list
        if isinstance(apdu, bytes):
            apdu = bytearray(apdu)
            
        apdu.append(sw >> 8)
        apdu.append(sw & 0xff)
        self.sendResponse(connection, apdu)
    
    def sendResponse(self, connection, apdu):
        gc.collect()
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
        
        #print(f"[f] {gc.mem_free()}")
        
        while (tpduLen > 0):
            tsLen = self.sendBlock (connection, seq, tpdu, offset, tpduLen)
            offset  += tsLen
            tpduLen -= tsLen
            seq += 1
            #print(f"[f] {gc.mem_free()}")
            #await asyncio.sleep_ms(10)

    def processListWifi(self, connection):
        '''扫热点命令处理'''
        print('[cmd] list wifi')
        listAP = wifiHelper.listAP()
        strAPs = json.dumps(listAP)
        # print(f"ap =>\n{strAPs}")
        
        self.sendResponseSW(connection, self.compress(strAPs), 0x9000)
        
    def processConfig(self, connection):
        '''配置功能命令处理'''
        print('[cmd] config')
        lc = self.recv_data[4]
        if lc == 0:
            listCfg = settings.cfgGet()
            sCfg = json.dumps(listCfg)
            # print(f"cfg =>\n{sCfg}")
            self.sendResponseSW(connection, self.compress(sCfg), 0x9000)
        else:
            try:
                cdat = self.decompress(self.recv_data[5:])
                sjson = cdat.decode('utf-8')
                params = json.loads(sjson)
                print(f"cfg =>\n{params}")
                if settings.cfgSet(params):
                    self.sendResponse(connection, [0x90, 0x00])
                else:
                    self.sendResponse(connection, [0x6A, 0x81])
            except Exception as e:
                self.sendResponse(connection, [0x6A, 0x80]) # wrong data
            
    def processDevTest(self, connection):
        '''测试连接命令处理'''
        print('[cmd] test')
        p1 = cmd = self.recv_data[2]
        lc = cmd = self.recv_data[4]
        if lc == 0:
            self.sendResponse(connection, [0x67, 0x00]) # wrong length
            return
        if not (p1 == 1 or p1 == 2):
            self.sendResponse(connection, [0x6A, 0x86]) # wrong P1P2
            return
        
        # data to json
        try:
            sjson = self.recv_data[5:].decode('utf-8')
            params = json.loads(sjson)
            sw = [0x94, 0x85]
            if p1 == 1:
                # test wifi connecton
                print(f"wifi {params['ssid']} {params['password']}")
                if wifiHelper.test_connect(params['ssid'], params['password'], False):
                    sw = [0x90, 0x00]
            elif p1 == 2:
                # test qweather api
                print(f"qwapi {params['key']} {params['city']}")
                
                if not wifiHelper.isconnected():
                    sw = [0x94, 0x86]
                elif test_api(params['key'], params['city']):
                    sw = [0x90, 0x00]               

            self.sendResponse(connection, sw) # wrong P1P2            
        except Exception as e:
            print(e)
            self.sendResponse(connection, [0x6A, 0x80]) # wrong data

    def processDevInfo(self, connection):
        '''获取设备命令处理'''
        print('[cmd] devinfo')
        dev_info = devinfo.DeviceInfo()
        strInfo = json.dumps(dev_info)
        self.sendResponseSW(connection, self.compress(strInfo), 0x9000)

    async def delayResetMcu(self):
        '''延迟重启设备命令支持'''
        await asyncio.sleep_ms(300)
        if sys.platform == 'esp32':
            machine.reset()
        else:
            print('sys reset')
            
    def processEFCommand(self, connection):
        cmd = self.recv_data[1]
        capdu = ''.join(['{:02X}'.format(b) for b in self.recv_data])
        # print(f"apdu: {capdu}")
        
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
        elif cmd == BLE_CMD_DEV_TEST:
            self.processDevTest(connection)
        else:
            self.sendResponse(connection, [0x6D, 0x00])
        
    async def communication_task(self, connection):
        try:
            with connection.timeout(None):
                while True:
                    #print("Waiting for write")
                    await self.uart_rx_characteristic.written()
                    msg = self.uart_rx_characteristic.read()
                                        
                    if len(msg) < 3:
                        continue
                    
                    self.recvFrame(msg)
                    
                    if self.recv_done:
                        print('[d] process command')
                        self.recv_done = False
                        self.processEFCommand(connection)

        except aioble.DeviceDisconnectedError:
            print('disconnected')

    async def peripheral_task(self, bleName):
        while True:
            connection = await aioble.advertise(
                _ADV_INTERVAL_MS,
                name = bleName,
                services=[_UART_UUID]
            )
            print("Connection from", connection.device)
            self.reset()
            await self.communication_task(connection)
            await connection.disconnected()
            print('Connection closed')

_ble_name = ""
def getBleDevName():
    global _ble_name
    if _ble_name == "":
        ble = bluetooth.BLE()
        ble.active(True)
        mac = ble.config('mac') # (addr_type, addr)
        ble.active(False)
    
        sid = ''.join(['{:02X}'.format(b) for b in mac[1]])
        _ble_name = f"eFore-{sid}"
    return _ble_name

# Run both tasks.
async def ble_app():
    bleEF = bleFramer()
    bleEF.start()
    await bleEF.peripheral_task(_ble_name)

if __name__ == '__main__':
    asyncio.run(ble_app())


