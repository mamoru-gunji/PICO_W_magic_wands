import machine
import time

# ADCピンを設定
adc_pin = machine.ADC(machine.Pin(26))
num_samples = 30000
samples_sum = 0

Vref = 3.3  # マイクロコントローラの参照電圧（3.3Vなど）
Rref = 10000  # 参照抵抗の抵抗値（オーム）

while True:
    samples_sum = 0
    for _ in range(num_samples):
        samples_sum += adc_pin.read_u16()
    adc_value = samples_sum / num_samples
    voltage = adc_value / 65535 * Vref  # ピンにかかる電圧を計算
    resistance = ((3.3-voltage)*Rref)/(-3.3+2*voltage)  # 抵抗値を計算
    print(resistance)
    time.sleep_ms(100)
