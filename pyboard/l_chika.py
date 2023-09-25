import machine, utime
led = machine.Pin("LED", machine.Pin.OUT)
while True:
    led.on()
    utime.sleep(0.5)
    led.off()
    utime.sleep(0.5)
    