import bluetooth
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin

# Pin configuration
led_pin = Pin("LED", Pin.OUT)

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_CUSTOM_SERVICE_UUID = bluetooth.UUID(0x181A)
_CUSTOM_CHAR = (bluetooth.UUID(0x2A5A), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
_CUSTOM_SERVICE = (_CUSTOM_SERVICE_UUID, (_CUSTOM_CHAR,),)
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

class BLELEDControl:
    def __init__(self, ble, name="pico_w"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_CUSTOM_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(
            name=name, services=[_CUSTOM_SERVICE_UUID], appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER
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

    def set_led_state(self, led_state, notify=False):
        if led_state == 1:
            led_pin.on()
        else:
            led_pin.off()
        packed_data = struct.pack('i', led_state)
        self._ble.gatts_write(self._handle, packed_data)
        if notify:
            for conn_handle in self._connections:
                self._ble.gatts_notify(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

def main():
    ble = bluetooth.BLE()
    led_control = BLELEDControl(ble)

    while True:
        led_state = led_pin.value()  # Read LED state
        led_control.set_led_state(led_state, notify=True)
        print()

if __name__ == "__main__":
    main()
