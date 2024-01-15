"""
    BLE 协程，供 Win/Unix 使用
"""

import asyncio

class bleFramer(object):
    def start(self):
        ...
        
    async def peripheral_task(self):
        while True:
            await asyncio.sleep_ms(100)
            ...
    
    
def getBleDevName():
    sid = "023178205809"
    return f"eFore-{sid}"

async def ble_app():
    bleEF = bleFramer()
    bleEF.start()
    await bleEF.peripheral_task()
    