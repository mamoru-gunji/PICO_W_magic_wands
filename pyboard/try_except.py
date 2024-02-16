from machine import Timer
import time
import global_value as g


tim = Timer()
def raise_e(t):
    try:
        raise Exception
    except Exception:
        pass
#     try:
#         raise ValueError("error!")
#     except ValueError as e:
#         print(e)


tim.init(mode=Timer.ONE_SHOT, period=1000, callback=raise_e)


try:
    while True:
#         time.sleep(float('inf'))
        time.sleep(1)
        print('\n')
except Exception as e:
    print('e')
    pass