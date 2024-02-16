from machine import Pin
import global_value as g
import time
from memory_usage import free

p2 = Pin(1, Pin.IN)
p1 = Pin(2, Pin.OUT)
print(p1.value(1))
g.init = True


def callback(p):
    while g.init:
        print('pin change', p)
        g.init = False
    g.init = True
    
# p0.irq(trigger=Pin.IRQ_FALLING, handler=callback)
p2.irq(trigger=Pin.IRQ_RISING, handler=callback)
print('good night!')
time.sleep(5)
print('good morning!')