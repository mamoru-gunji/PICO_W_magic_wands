import _thread
import time

def trigger_exception():
    # ここで例外を発生させる
    raise Exception("Custom exception!")

def thread_function():
    try:
        trigger_exception()
    except Exception as e:
        print(f"Caught exception: {e}")

# 新しいスレッドを開始し、そこで例外を発生させる
_thread.start_new_thread(thread_function, ())

# メインスレッドでは通常の処理を行う
print("Entering main thread")
time.sleep(3)
print("Exiting main thread")
