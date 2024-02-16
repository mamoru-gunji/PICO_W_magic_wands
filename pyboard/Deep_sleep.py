import machine
import utime

# スイッチ入力、Wi-Fi通信チップ、電源ピンのピン番号
switch_pin = 0         # 任意のピン番号を指定してください
wifi_chip_pin = 23     # Wi-Fi通信チップのピン番号
switch_power_pin = 2   # スイッチ用電源ピンのピン番号
led_pin = "LED"

# スリープまでの待機時間（秒）
sleep_time = 3

def enter_deepsleep():
    # Wi-Fi通信チップのピンをlowに設定
    machine.Pin(wifi_chip_pin, machine.Pin.OUT).value(0)
    machine.Pin(led_pin, machine.Pin.OUT).value(0)
    print("Deep Sleepモードに移行します。")
    machine.deepsleep()

def awaken_state_operations():
    # アウェイク中はWi-Fi通信チップのピンをhighに設定
    machine.Pin(wifi_chip_pin, machine.Pin.OUT).value(1)
    machine.Pin(led_pin, machine.Pin.OUT).value(1)
    print("アウェイク状態の操作を実行します。")

# 電源ピンをON
machine.Pin(switch_power_pin, machine.Pin.OUT, value=1)

# メインループ
while True:
    # スリープ時間内にスイッチが押された場合
    awake_start_time = utime.ticks_ms()
    awaken_state_operations()
    while True:
        utime.sleep_ms(100)
        switch_state = machine.Pin(switch_pin, machine.Pin.IN).value()
        if switch_state == 1:
            print("スイッチが押されました。アウェイク状態に移行します。")
            break
        elif utime.ticks_diff(utime.ticks_ms(), awake_start_time) >= sleep_time * 1000:
            print("スリープ時間が経過しました。")
            enter_deepsleep()
