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

#currently this gets user inputs in the place of actual information from anchors since we are limited by not having hardware
#main information we will need from the anchors would be the distance to the ball since achors will be at fixed locations on the field
#we would need to break down the field into an xy plane, a simple way to do this would be to treat the values for calculation as
#the yardage values
loc = 0 
def calculate():
    P=lx.Project(mode='2D',solver='LSE') 
    a_x = input("A x value = ")
    a_y = input("A x value = ")
    b_x = input("B x value = ")
    b_y = input("B y value = ")
    a_dist= input("A to point = ")
    b_dist = input("B to points = ")
    
    a_x = int(a_x)
    a_y = int(a_y)
    b_x = int(b_x)
    b_y = int(b_y)
    a_dist = int(a_dist)
    b_dist = int(b_dist)

    P.add_anchor('anchore_A',(a_x,a_y))
    P.add_anchor('anchore_B',(b_x,b_y))
    #P.add_anchor('anchore_C',(100,0))

    t,label=P.add_target()

    t.add_measure('anchore_A',a_dist)
    t.add_measure('anchore_B',b_dist)
    #t.add_measure('anchore_C',50)

    P.solve()

# Then the target location is:

    print(t.loc)
    loc = t.loc

#calls to functions, can also connect to a BLE device for demo in pre-alpha

#asyncio.run(connect(address))
#asyncio.run(find())
calculate()