import asyncio
from bleak import BleakClient
import struct

address = "XX:XX:XX:XX:XX:XX"
UUID = "00002a5a-0000-1000-8000-00805f9b34fb"
buffer = 40


async def run(address, loop):
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))
        while True:
            y = await client.read_gatt_char(UUID)
            # print("Received data:", y)
            process_received_data(
                y
            )  # Call a function to process and interpret the data
            # await asyncio.sleep(0.01)


def process_received_data(data):
    format_string = "<" + "h" * (1 + 6 * buffer)
    data_size = struct.calcsize(format_string)

    if len(data) == data_size:
        unpacked_data = struct.unpack(format_string, data)
        x, y, z, roll, pitch, yaw = [], [], [], [], [], []
        index = unpacked_data[0]
        if index != -1:
            for i in range(buffer):
                x.append(unpacked_data[6 * i + 1] / 1000)
                y.append(unpacked_data[6 * i + 2] / 1000)
                z.append(unpacked_data[6 * i + 3] / 1000)
                roll.append(unpacked_data[6 * i + 4] / 1000)
                pitch.append(unpacked_data[6 * i + 5] / 1000)
                yaw.append(unpacked_data[6 * i + 6] / 1000)
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
        else:
            print("stop")
    else:
        print("Invalid data size:", len(data))


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
