import machine, time

# ピンの設定
pin = machine.Pin(2, machine.Pin.IN)

# 割り込みハンドラの定義
def pin_change_handler(pin):
    print("Pin changed!")

# ピンの割り込み設定
pin.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=pin_change_handler)

print('good night!')
machine.Pin('LED', machine.Pin.OUT).on()
time.sleep(1)
machine.Pin('LED', machine.Pin.OUT).off()
machine.deepsleep(3000)  # 3秒間のディープスリープ
machine.Pin('LED', machine.Pin.OUT).on()
print('hello!')