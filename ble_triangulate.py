import asyncio
import numpy as np
import localization as lx
from bleak import BleakScanner
from bleak import BleakClient

#Goals of this script
# 1. Find and connect to the ESP32 through BLE
# 2. Gather and display positional data gathered from the modules

#Sources - https://github.com/hbldh/bleak examples from README file
# https://github.com/kamalshadi/Localization - localization dependency
# https://shapely.readthedocs.io/en/stable/  - Dependency needed for locatization

# Future tasks to develop - 
# Programming the ESP32 with DWM3000 for transmitting data to each other
# Calculation for determining postions

async def find():  #example for finding devices, useful for testing and finding given address
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

address = "AA:AA:AA:AA:AA:AA"  #find address of our modules, this is just a filler for now from an example
MODEL_NBR_UUID = "2A24"

async def connect(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

# asyncio.run(connect(address))

def calculate():
    P=lx.Project(mode='2D',solver='LSE') 
    

    P.add_anchor('anchore_A',(0,100))
    P.add_anchor('anchore_B',(100,100))
    P.add_anchor('anchore_C',(100,0))

    t,label=P.add_target()

    t.add_measure('anchore_A',50)
    t.add_measure('anchore_B',50)
    t.add_measure('anchore_C',50)

    P.solve()

# Then the target location is:

    print(t.loc)

asyncio.run(find())
calculate()