from time import sleep
import _thread

# Lockオブジェクトを作成
lock = _thread.allocate_lock()
counter = 0
state = False
sleep_time = 1

def core1_thread():
    global counter, state
    state = True
    with lock:
        counter += 0.1
    print('core1', counter)
    sleep(sleep_time)
    with lock:
        state = False
        _thread.exit()
        
def core0_thread():
    global counter, state
    while True:
        with lock:
            counter += 1
        print('core0', counter)
        while state:
            sleep(0)
        with lock:
            _thread.start_new_thread(core1_thread, ())  # Core1スレッド再起動
        sleep(sleep_time)
# スレッドを開始
core0_thread()