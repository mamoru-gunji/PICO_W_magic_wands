import os
import csv
import struct
import asyncio
import OpenEXR
import numpy as np
from bleak import BleakClient


address = "28:CD:C1:0E:39:C3"
UUID = "00002a5a-0000-1000-8000-00805f9b34fb"
buffer = 40
initial = True
index = -1

directory_path = os.path.join(os.getcwd(), "data-folder")
log_file_path = os.path.join(directory_path, "data_log.csv")


if not os.path.exists(directory_path):
    # If it doesn't exist, create the directory
    os.makedirs(directory_path)


def read_counter():
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as file:
            return int(file.read())
    else:
        return 0


def write_counter(count):
    with open(log_file_path, "w") as file:
        file.write(str(count))


def increment_counter():
    count = read_counter()
    count += 1
    write_counter(count)
    return count


def save_array_as_exr(array, file_path):
    # OpenEXRファイルを作成
    header = OpenEXR.Header(array.shape[1], array.shape[0])
    exr_file = OpenEXR.OutputFile(file_path, header)

    # RGBチャンネルのデータを書き込む
    rgb_data = {
        "R": array[..., 0].tobytes(),
        "G": array[..., 1].tobytes(),
        "B": array[..., 2].tobytes(),
    }
    exr_file.writePixels(rgb_data)


if not os.path.exists(log_file_path):
    with open(log_file_path, mode="w", newline="") as log_file:
        writer = csv.writer(log_file)
        num_samples = 0
        new_data = [num_samples]
        with open(log_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(new_data)
else:
    with open(log_file_path, "r", newline="") as log_file:
        for row in log_file:
            num_samples = int(row)

if not "num_samples" in locals() and not "num_samples" in globals():
    num_samples = 0

print(num_samples)

# CSVファイルのヘッダーを定義
header = ["X", "Y", "Z", "ROLL", "PITCH", "YAW"]


# CSVファイルにデータを書き込むための関数
def write_data_to_csv(filename, data_point):
    with open(filename, "a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data_point)


def convert_to_float(fixed_point_array):
    # 0~1の固定小数点数を32ビット整数に変換
    integer_array = ((2 ** (32 * fixed_point_array)) - 1).astype(np.uint32)
    return integer_array


async def run(address, loop):
    global label_type
    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        print("Connected: {0}".format(x))
        label_type = int(input("変身:0|♡:1|✾:2|⚡:3|\n input number: "))
        while True:
            try:
                y = await client.read_gatt_char(UUID)
                # print("Received data:", y)
                process_received_data(
                    y
                )  # Call a function to process and interpret the data
                # await asyncio.sleep(0.01)

            except KeyboardInterrupt:
                new_data = [num_samples]
                with open(log_file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(new_data)
                print("Program stopped.")


def process_received_data(data):
    global initial, index, num_samples, label_type
    format_string = "<" + "h" * (1 + 6 * buffer)
    data_size = struct.calcsize(format_string)

    if len(data) == data_size:
        unpacked_data = struct.unpack(format_string, data)

        if unpacked_data[0] != -1:
            if index != unpacked_data[0]:
                index = unpacked_data[0]

                for i in range(buffer):
                    x = unpacked_data[6 * i + 1] / 1000
                    y = unpacked_data[6 * i + 2] / 1000
                    z = unpacked_data[6 * i + 3] / 1000
                    roll = unpacked_data[6 * i + 4] / 100000
                    pitch = unpacked_data[6 * i + 5] / 100000
                    yaw = unpacked_data[6 * i + 6] / 100000

                    data_point = [x, y, z, roll, pitch, yaw]

                    if initial == True:
                        print(f"{num_samples:04d}.csv")
                        initial = False

                    filename = os.path.join(directory_path, f"{num_samples:04d}.csv")

                    if not os.path.exists(filename):
                        with open(filename, "w", newline="") as file:
                            csv_writer = csv.writer(file)
                            csv_writer.writerow(header)
                    write_data_to_csv(filename, data_point)

                print(index)
        else:
            if initial == False:
                initial = True
                data_file = os.path.join(directory_path, "data.csv")

                data = [{"label": label_type, "data": f"{num_samples:04d}.csv"}]

                if not os.path.exists(data_file):
                    # File doesn't exist, create a new file and write the header
                    with open(data_file, mode="w", newline="") as data_files:
                        fieldnames = ["label", "data"]
                        writer = csv.DictWriter(data_files, fieldnames=fieldnames)

                        # Write the CSV header
                        writer.writeheader()

                # Append new data
                with open(data_file, mode="a", newline="") as data_files:
                    fieldnames = ["label", "data"]
                    writer = csv.DictWriter(data_files, fieldnames=fieldnames)
                    for row in data:
                        writer.writerow(row)

                num_samples += 1
                with open(log_file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([num_samples])
                data = []
                # label_type = int(input("変身:0|♡:1|✾:2|⚡:3|\n input number: "))

            print("stop")

    else:
        print("Invalid data size:", len(data))


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address, loop))
