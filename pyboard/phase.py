from machine import Timer
import re
import time
import global_value as g
from l_chika import l_chika
from machine import Pin
import global_value as g

g.sw = Pin(2, Pin.IN)
g.init = True


tim = Timer()
led = Pin("LED", Pin.OUT)


def pin_change(p):
    while g.init:
        print('pin change', p)
        g.init = False
    g.init = True


class phase_0():
    def __init__(self):
        g.phase = re.sub(r"\D", "", type(self).__name__)
        g.next_phase = g.phase
        g.tim = Timer()
        self.print_phase()
        self.tim_start()
    
    def print_phase(self):
        print(type(self).__name__)
        
    def tim_start(self):
        g.tim.init(mode=Timer.PERIODIC, freq=1000, callback=self.callback)

    def callback(self,t):
        l_chika(cycle=1,blink=0.1)
        print('***')
        if g.sw.value():
            g.tim.init()
        if g.next_phase != g.phase:
            try:
                exec(f'next_phase = phase_{g.next_phase}()')
                exec('next_phase.main()')
            except Exception as e:
                print('please set a new phase!')
    
    def process(self):
        time.sleep(0.1)
        print('--')
        pass
    
    def main(self):
        self.process()
        pass


class phase_1(phase_0):
    def __init__(self):
        super().__init__()
        
    def process(self):
        time.sleep(10)
        
        
def main():
    g.PHASE = phase_0()
    g.PHASE.main()
    time.sleep(1)
    print('main process')
    time.sleep(1)
    g.next_phase = 1
    time.sleep(3)
    g.next_phase = 0
    
    
if __name__ == '__main__':
    main()

