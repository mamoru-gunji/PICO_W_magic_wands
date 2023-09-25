import bluetooth
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin, I2C

led = Pin("LED", Pin.OUT)
button = Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN)  # Assuming there's a BUTTON pin

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)
MMA8452Q_ADDR = 0x1D
MMA8452_G_SCALE = 2.0

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
_ACCEL_CHAR = (bluetooth.UUID(0x2A5A), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
_ENV_SENSE_SERVICE = (_ENV_SENSE_UUID, (_ACCEL_CHAR,),)
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

class BLEAccelerometer:
    def __init__(self, ble, name="pico_w"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_ENV_SENSE_UUID], appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
        )
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()

    def set_acceleration(self, accel_data, notify=False):
        packed_data = struct.pack('<hhh', *accel_data)
        self._ble.gatts_write(self._handle, packed_data)
        if notify:
            for conn_handle in self._connections:
                self._ble.gatts_notify(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

def init_mma8452q():
    i2c.writeto_mem(MMA8452Q_ADDR, 0x2A, bytes([0x01]))  # Active mode

def trimmed_mean(data, trim_percent):
    data.sort()
    trim_size = int(len(data) * trim_percent)
    trimmed_data = data[trim_size:-trim_size]
    return sum(trimmed_data) / max(len(trimmed_data),1)

def read_acceleration(samples=1, trim_percent=0.1):
    x_data, y_data, z_data = [], [], []
    for _ in range(samples):
        data = i2c.readfrom_mem(MMA8452Q_ADDR, 0x01, 6)
        x_data.append(
            -(float((int((data[0] << 8) | data[1]) >> 4)) / ((1 << 11) / MMA8452_G_SCALE))
        )
        y_data.append(
            -(float((int((data[2] << 8) | data[3]) >> 4)) / ((1 << 11) / MMA8452_G_SCALE))
        )
        z_data.append(
            -(float((int((data[4] << 8) | data[5]) >> 4)) / ((1 << 11) / MMA8452_G_SCALE))
        )

    x_avg = trimmed_mean(x_data, trim_percent)
    y_avg = trimmed_mean(y_data, trim_percent)
    z_avg = trimmed_mean(z_data, trim_percent)
    return x_avg, y_avg, z_avg

def is_button_pressed():
    return button.value() == 0  # Button is active low

def main_accel():
    led.on()
    ble = bluetooth.BLE()
    accel = BLEAccelerometer(ble)

    init_mma8452q()
#     x_offset, y_offset, z_offset = read_acceleration(10)

    while is_button_pressed():
        x, y, z = read_acceleration(samples=10)

        accel_data = (int(x * 1000), int(y * 1000), int(z * 1000))  # Scaling to fit into 16-bit integers

        accel.set_acceleration(accel_data, notify=True)
        print("Acceleration: X:", x, " Y:", y, " Z:", z)
        led.off()
    else:
        main_communicate()
            

def main_communicate():
    led.on()
    ble = bluetooth.BLE()
    ble.active(True)
    ((handle,),) = ble.gatts_register_services(((_ENV_SENSE_SERVICE[0],),))
    connections = set()
    payload = advertising_payload(
        name="pico_w",
        services=[_ENV_SENSE_UUID],
        appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
    )

    while True:
        if is_button_pressed():
            ble.gap_advertise(500000, adv_data=payload)
            main_accel()
        else:
            ble.gap_advertise(500000, adv_data=b'')
            time.sleep(1)
            led.off()
            

if __name__ == "__main__":
    if is_button_pressed():
        main_accel()
    else:
        main_communicate()

