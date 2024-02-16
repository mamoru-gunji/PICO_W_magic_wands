import machine
import utime

class DFPlayer:
    def __init__(self, uart_port=1, tx_pin=4, rx_pin=5, pin_btn=16, led_pin="LED"):
        self.uart = machine.UART(uart_port, baudrate=9600, tx=machine.Pin(tx_pin), rx=machine.Pin(rx_pin))
        self.pin_btn = machine.Pin(pin_btn, machine.Pin.IN, machine.Pin.PULL_UP)
        self.led = machine.Pin(led_pin, machine.Pin.OUT)

        self.ON  = 0 # LOW
        self.OFF = 1 # HIGH

        self.btn = self.OFF
        self.prev_btn = self.OFF

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
        utime.sleep_ms(1000)

    def set_volume(self, volume):
        self.send_data(0x06, volume)
        utime.sleep_ms(500)

    def play_sound(self, num, vol=30):
        self.set_volume(vol)
        print("Play {}".format(num))
        self.send_data(0x12, num)
        utime.sleep_ms(500)

    def run(self):
        self.init_sd()
        print("Ready.")

        num = 0
        while True:
            self.btn = self.pin_btn.value()

            if self.prev_btn == self.OFF and self.btn == self.ON:
                num += 1
                if num >= 3:
                    num = 1
                self.play_sound(num)

            self.prev_btn = self.btn
            self.led.on()
            utime.sleep_ms(1)
            self.led.off()

if __name__ == "__main__":
    dfplayer = DFPlayer()
    dfplayer.run()
