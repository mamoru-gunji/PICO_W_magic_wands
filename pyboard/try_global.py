from machine import Timer
import time
import global_value as g

g.value = 0
tim = Timer()

def wake(t):
    g.value = 1

tim.init(mode=Timer.ONE_SHOT, period=3000, callback=wake)


try:
    while True:
        print(g.value)
        time.sleep(1)
        pass
    
except g.value == 1:
    print('wake up!')
    pass
