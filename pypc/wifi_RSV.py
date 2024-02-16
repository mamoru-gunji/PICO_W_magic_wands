import socket
from data_to_csv import save_data
import time


def connect(device_ip, device_port):
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"Connecting to {device_ip}:{device_port}")
            server_socket.connect((device_ip, device_port))
            print("Server connected")
            return server_socket

        except OSError as e:
            print(e)
            server_socket.close()
            time.sleep(1)
            pass


data_index = 3

# Pico-WデバイスのIPアドレスとポート
device_ip = "your ip"
device_port = 1205  # Pico-Wデバイスで設定したポート番号

# サーバーソケットを作成

server_socket = connect(device_ip, device_port)


data = ""
print(f"data_index = {data_index}\n start ...")
while True:
    try:

        received_data = server_socket.recv(1024).decode()

        if not received_data:
            # データがまだ到着していない場合はループを再開
            continue

        data += received_data
        try:
            print(received_data)
        except SyntaxError:
            pass

        if "]]" in data:
            end_index = data.find("]]") + 2
            save_data(data[0:end_index], data_index)
            data = data[end_index:]
        # "ACK"応答を送信
        # server_socket.send("ACK".encode())
    except (KeyboardInterrupt, ConnectionResetError) as e:
        print(e)
        save_data(data, data_index)
        server_socket.close()
    except (SyntaxError, OSError) as e:
        print(e)
        data = ""
        received_data = None
        pass
