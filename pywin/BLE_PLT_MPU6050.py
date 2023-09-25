import numpy as np
import matplotlib.pyplot as plt
import asyncio
from bleak import BleakClient
import struct
import time

address = "XX:XX:XX:XX:XX:XX"
UUID = "00002a5a-0000-1000-8000-00805f9b34fb"
buffer = 1

T = []
t = []
xt = []
yt = []
zt = []
rollt = []
pitcht = []
yawt = []

fig, ax = plt.subplots()


async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))
        while True:
            now = time.time()
            y = await client.read_gatt_char(UUID)
            # print("Received data:", y)
            process_received_data(
                # y, printer = "Visible", ploter = "Visible"
                y,
                ploter="Visible",
            )  # Call a function to process and interpret the data
            # await asyncio.sleep(0.01)
            print(time.time() - now)


def process_received_data(data, printer=None, ploter=None, timer="off"):
    format_string = "<" + "h" * (1 + 6 * buffer)
    data_size = struct.calcsize(format_string)

    if len(data) == data_size:
        unpacked_data = struct.unpack(format_string, data)
        x, y, z, roll, pitch, yaw = [], [], [], [], [], []
        index = unpacked_data[0]
        for i in range(buffer):
            x = unpacked_data[6 * i + 1] / 1000
            y = unpacked_data[6 * i + 2] / 1000
            z = unpacked_data[6 * i + 3] / 1000
            roll = unpacked_data[6 * i + 4] / 1000
            pitch = unpacked_data[6 * i + 5] / 1000
            yaw = unpacked_data[6 * i + 6] / 1000

            if not printer == None:
                print(
                    index,
                    "Acceleration: X:",
                    x,
                    " Y:",
                    y,
                    " Z:",
                    z,
                    " ROLL:",
                    roll,
                    " PITCH:",
                    pitch,
                    " YAW:",
                    yaw,
                )

            if not ploter == None:
                T.append(time.time())
                t.append(time.time() - T[0])
                xt.append(x)
                yt.append(y)
                zt.append(z)
                rollt.append(roll / 30)
                pitcht.append(pitch / 30)
                yawt.append(yaw / 30)

                ax.plot(t, xt, color="C0")
                ax.plot(t, yt, color="C1")
                ax.plot(t, zt, color="C2")
                ax.plot(t, rollt, color="C3")
                ax.plot(t, pitcht, color="C4")
                ax.plot(t, yawt, color="C5")

                ax.set_xlabel("Time")
                ax.set_ylabel("Values")
                plt.legend(["ax", "ay", "az", "gx", "gy", "gz"])
                plt.pause(0.00001)
    else:
        print("Invalid data size:", len(data))


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
