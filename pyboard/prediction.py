from LSTM_np import LSTM
try:
    import numpy as np
except ImportError:
    from ulab import numpy as np
    pass

PRED = LSTM()
PRED.X_test = np.ones((30,7))
PRED.y_hat = PRED.main()
print(PRED.y_hat)
def prediction():
    
    PRED.y_hat = PRED.main()
    
    with lock:
        y_hat = PRED.y_hat
        return y_hat