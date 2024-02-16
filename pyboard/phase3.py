import sys
import re
import time
from machine import Timer, Pin, lightsleep
from l_chika import l_chika
import global_value as g
import phase

g.num = 0
g.tim = Timer()
led = Pin("LED", Pin.OUT)

class timer:
    def __init__(self):
        self.tim = Timer()
    
    
    
class phase_0:
    def __init__(self):
        g.phase_old = int(re.sub(r"\D", "", type(self).__name__))
        pass
    
    def mycallback(self,t):
        try:
            print('---call back!---')
            l_chika(blink=0.01,duty=0.01)
            g.phase_new = g.phase_old/(g.phase_old == g.phase_new)
        except ZeroDivisionError:
            l_chika(cycle=4,blink=0.5,duty=0.02)
            print('**change phase!**')
            g.phase_old = g.phase_new
            g.num -= 1
            
            try: 
                exec(f'g.PHASE = phase_{g.phase_new}()')
                self.process()
            except NameError:
                sys.exit()
            
        except KeyboardInterrupt:
            g.tim.init()
        pass

    def process(self):
        g.tim.init(mode=Timer.PERIODIC, freq=1, callback=self.mycallback)

    def main(self):
        try:
            g.phase_new = g.num
            print('phase',g.phase_old,'-> phase', g.phase_new)
            g.num += 1
            self.process()
            print('---slep now!---')
            l_chika()
            time.sleep(0.3)
            print('---wake  up !---')
            l_chika()
            time.sleep(0.3)
            g.tim.init()
        except Exception as e:
            print(e)
            g.tim.init()
            pass

class phase_1(phase_0):
    def __init__(self):
        super().__init__()
        
        
def main():
    try:
        g.PHASE.main()
    except Exception as e:
        print('phase init')
        g.PHASE = phase_0()

if __name__ == '__main__':
    g.phase_old = g.num
    num = 5
    while num:
        main()
        num -= 1

