from time import sleep
from machine import Pin


led = Pin("LED", Pin.OUT)

def l_chika(cycle=1, blink=1, duty=0.5):
    for i in range(cycle):
        led.on()
        sleep((blink * duty)/cycle)
        led.off()
        sleep((blink * (1 - duty))/cycle)