from time import sleep
import _thread
import machine
import global_value as g

led = machine.Pin("LED", machine.Pin.OUT)
def process0(num=1):
    sleep(g.sleep_0)
    with g.lock():
        g.dammy_data += num
    print('core0', g.dammy_data)


def process1(num=-0.00001):
    sleep(g.sleep_1)
    with g.lock():
        g.dammy_data -= num
    print('core1', g.dammy_data)

            
class ThreadManager:
    def __init__(self):
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.state = False
        g.dammy_data = 0
        g.lock = _thread.allocate_lock
        g.process0 = process0
        g.process1 = process1
        g.sleep_1 = 0.1
        g.sleep_0 = 1
        g.prt = False
        

    def core1_thread(self):
        self.state = True
        self.led.on()
        g.process1()
        self.led.off()
        with g.lock():
            self.state = False
            _thread.exit()

    def multi_thread(self):
        try:
            if not self.state:
                with g.lock():
                    _thread.start_new_thread(self.core1_thread, ())
            else:
                if g.prt:
                    print('skip')
            g.process0()
        except Exception as e:
            raise Exception(e)
        

    def main(self):
        while True:
            self.multi_thread()


if __name__ == '__main__':
    manager = ThreadManager()
    manager.main()