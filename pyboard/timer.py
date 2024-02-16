from machine import Timer, Pin
import time
from l_chika import l_chika
import global_value as g

class timer:
    def __init__(self):
        self.freq = 100
        self.interval = 3
        g.tim = Timer()
        g.led = Pin("LED", Pin.OUT)
        g.prt = False
        g.ago = time.ticks_ms()/1000
        g.now = g.ago
        g.prt = None
        

    def mycallback(self,t):
        try:
            if g.now - g.ago > self.interval:
                self.stop()

            else:
                self.process()
                if self.prt:
                    print(g.now)
                l_chika(duty=0.0001,blink = 0.01)
                g.now = time.ticks_ms()/1000
        except Exception as e:
            self.stop()
    
    def start(self):
        try:
            g.tim.init(mode=Timer.PERIODIC, freq=self.freq, callback=self.mycallback)
        except Exception:
            raise Exception('2')

    def stop(self):
        g.tim.deinit()
        
    def restart(self):
        self.stop()
        self.start()

        
    def process(self):
        pass
        
    def main(self):
        self.start()


if __name__ == '__main__':
    try:
        print('sleep now !')
        l_chika(cycle=4,duty=0.4)
        tim = timer()
        tim.main()
        time.sleep(3)
        
    except Exception as e:
        print('wake up !')
        l_chika(cycle=4,duty=0.4)
        pass

    finally:
        pass
