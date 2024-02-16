import gc
import machine
import utime

class DFPlayer:
    def __init__(self, uart_port=1, tx_pin=4, rx_pin=5, busy_pin = 3, led_pin="LED", vol=30):
        self.uart = machine.UART(uart_port, baudrate=9600, tx=machine.Pin(tx_pin), rx=machine.Pin(rx_pin))
        self.busy = machine.Pin(busy_pin, machine.Pin.IN)
        self.led = machine.Pin(led_pin, machine.Pin.OUT)

        self.ON  = 0 # LOW
        self.OFF = 1 # HIGH

        self.btn = self.OFF
        self.prev_btn = self.OFF
        self.vol = vol
        self.playing = False
        self.loop = False
        self.timer = None
        self.buff = 200

    def calc_checksum(self, sum_data):
        temp = ~sum_data + 1
        h_byte = (temp & 0xFF00) >> 8
        l_byte = temp & 0x00FF
        return h_byte, l_byte

    def send_data(self, command, param):
        ver      = 0xFF
        d_len    = 0x06
        feedback = 0x00
        param1   = (param & 0xFF00) >> 8
        param2   = param & 0x00FF
        cs1, cs2 = self.calc_checksum(ver + d_len + command + feedback + param1 + param2)
        sdata = bytearray([0x7E, ver, d_len, command, feedback, param1, param2, cs1, cs2, 0xEF])
        self.uart.write(sdata)

    def init_sd(self):
        self.send_data(0x3F, 0x02)

    def set_volume(self, volume):
        self.send_data(0x06, volume)
#         utime.sleep_ms(100)

    def play(self, num, buff=200):
        utime.sleep_ms(min(self.buff, buff))
        while not self.busy.value() and not self.loop:
            utime.sleep_ms(1)
        self.send_data(0x12, num)
        try:
            print("Play {}".format(num))
        except Exception:
            pass
        self.playing = False

    def callback(self,timer):
        if self.loop:
            if self.busy.value():
                self.play(self.num, buff=0)
        else:
            self.timer.deinit()
            self.timer = None
        gc.mem_free()
    
    def play_loop(self, num, limit_ms=1000):
        self.num = num
        self.play(self.num, buff=0)
        self.loop = True
        if not self.timer:
            self.timer = machine.Timer()
            self.timer.init(period=limit_ms, mode=machine.Timer.PERIODIC, callback=self.callback)
    
    def stop(self):
        self.loop = False
