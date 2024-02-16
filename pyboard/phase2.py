from machine import Timer, Pin, lightsleep
import time
import sys
from l_chika import l_chika
import global_value as g
import phase

g.num = 0
g.tim = Timer()
led = Pin("LED", Pin.OUT)

class phase_0():
    def __init__(self):
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
        g.tim.init(mode=Timer.PERIODIC, freq=2, callback=self.mycallback)

    def main(self):
        try:
            g.phase_new = g.num
            print('phase',g.phase_old,'-> phase', g.phase_new)
            g.num += 1
            self.process()
            print('---slep now!---')
            l_chika()
            time.sleep(2)
            print('---wake  up !---')
            l_chika()
            time.sleep(2)
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
        g.PHASE = phase_0()
        g.PHASE.main()

if __name__ == '__main__':
    g.phase_old = g.num
    while 1:
        main()
