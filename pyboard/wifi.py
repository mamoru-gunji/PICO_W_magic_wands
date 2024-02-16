import network
import socket
import time
import machine
from machine import Pin
import global_value as g

class wifi:
    def __init__(self):
        print('Wi-Fi connection init')
        self.ssid = 'ssid'
        self.password = 'password'
        self.Pin = Pin(23)
        self.Pin.on()
        self.port = 22
        self.limit = 5000
        self.ip = '0.0.0.0'
        self.wlan = network.WLAN(network.STA_IF)
        self.socket = None
        self.client = None
        self.addr = None
        self.cont = True
        self.connected = False
        self.start_time = time.ticks_ms()
        self.current_time = time.ticks_ms()
        g.data_gen = self.data_gen

    def data_gen(self):
        return 'data'
    
    def disconnect(self):
        try:
            self.client.close()
        except AttributeError:
            pass
        self.wlan.disconnect()
        
        
    def connect(self):
        print(f'Wi-Fi connection start: {self.ssid}')
        self.wlan.active(True)
        try:
            self.wlan.connect(self.ssid, self.password)
        except OSError as error:
            print(f'error is {error}')

        self.start_time = time.ticks_ms()
        print('connecting', end="")
        while not self.wlan.isconnected():
            print(f'.', end="")
            time.sleep_ms(int(self.limit/10))
            self.current_time = time.ticks_ms()
            if time.ticks_diff(self.current_time, self.start_time) >= self.limit:
                print('\nWi-Fi connection timed out')
                self.cont = False
                break

        if self.cont:
            self.connected = True
            self.ip = self.wlan.ifconfig()[0]
            print(f'\nServer connected on {self.ip}:{self.port}')

    def send(self, value=None):
        try:
            if self.client is not None:
                if value == None:
                    value = g.data_gen()
                self.client.send(value.encode())
                print(value)
        except Exception:
            pass

    def server_init(self):
        self.connect()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.ip, self.port))
            self.socket.listen(10)
            self.socket.settimeout(self.limit/10000)
        except Exception as e:
            print(e)
#             self.wlan.disconnect()
    
    def find_client(self):
        if self.cont:
            print(f'Client finding', end="")
            for i in range(50):
                try:
                    print(f'.', end="")
                    self.client, self.addr = self.socket.accept()
                    print('\nClient connected:', self.addr)
                    break
                except Exception:
                    pass
            if self.client is None:            
                print(f'\nClient not found')
                self.cont = False
        
    def server(self):
        while self.cont:
            self.send()
            time.sleep(0.1)
            
    def isconnected(self):
        return self.wlan.isconnected()
    
    def foundclient(self):
        return self.client is not None

    def main(self):
        self.server_init()
        while self.cont:
            g.num = 0
            try:
                self.find_client()
                print('-')
                self.server()
            except Exception as e:
                print(e)
                print('Socket acceptance timed out')
#                 self.wlan.disconnect()
                try:
                    self.client.close()
                except Exception:
                    pass
                break


if __name__ == '__main__':
    Wifi = wifi()
    Wifi.main()
