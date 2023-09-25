from machine import Pin, ADC
import time

# ADCピンを設定
adc_pin = ADC(Pin(26))

# シリアル通信を初期化
uart = machine.UART(0, baudrate=9600)

raw = 0.0

while True:
    raw += (adc_pin.read_u16() - raw) * 0.1
    print(str(raw) + '\n')
    time.sleep_ms(10)
