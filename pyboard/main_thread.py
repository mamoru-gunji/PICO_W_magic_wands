import machine
import time
now = time.ticks_ms()
# import _thread
try:
    import numpy as np
except ImportError:
    from ulab import numpy as np
    pass
from multi_thread import ThreadManager
import global_value as g
from LSTM_np import LSTM
from memory_usage import free

manager = ThreadManager()
AI = LSTM()

def process2(num=0):
    try:
        g.y_hat = np.concatenate((g.y_hat, AI.main()))
    except Exception as e:
        g.y_hat = AI.main()
        
    print(g.y_hat)
    with g.lock():
        g.counter *= num
    print('core1')

        
def main():
    g.counter = 0
    g.process1 = process2
    g.val1 = 0.5
    g.y_hat = []
    X_test = np.array(AI.generate_random_matrix(500, AI.input_dim))


    while True:
            g.X_test = np.array(AI.generate_random_matrix(AI.seq_length, AI.input_dim))
            manager.multi_thread()
            time.sleep(1)
            g.mem(True)

if __name__ == '__main__':
    g.mem = free
    print((time.ticks_ms()-now)/1000)
    main()