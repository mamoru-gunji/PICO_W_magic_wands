import re
import global_value as g
import time
from timer import timer


def change_phase():
    print(f'phase{g.phase_num} <- phase{g.phase_next.num}')
    exec(f'g.phase_next = phase_{g.phase_num}()')
    exec(f'g.phase_next.main()')

    
class phase_0:
    def __init__(self):
        self.num = g.phase_num = int(re.sub(r"\D", "", type(self).__name__))
        g.phase_next = self
        
    def process(self):
        print('-')
        g.phase_num += 1
        g.timer.restart()
        
    def main(self):
        self.process()
        
        if self.num != g.phase_num:
            try:
                change_phase()
            except Exception as e:
                g.timer.stop()
                print('main',e)
                pass


class phase_1(phase_0):
    def __init__(self):
        super().__init__()
    
    def process(self):
        print('--')
        time.sleep(1)
        g.phase_num = 2

class phase_2(phase_0):
    def __init__(self):
        super().__init__()
        
class phase_3(phase_0):
    def __init__(self):
        super().__init__()
        
        
def process():
    try:
        if g.phase_next.num != int(g.phase_num) or not g.phase_num:
            change_phase()
    except Exception as e:
        g.timer.stop()
        print(e)
        print('pro')
        raise Exception
#         g.loop = False
        pass

def main():
    g.timer = timer()
    g.timer.interval = 5
    g.timer.freq = 10
    g.timer.process = process
    g.timer.main()
    g.phase_num = 0
    g.phase_next = phase_0()
    g.loop = True
#     while g.loop:
    try:
        print('main')
        process()
    except Exception as e:
        g.timer.stop()
        print(e)
#         break
        pass
 
 
  
if __name__ == '__main__':
    main()