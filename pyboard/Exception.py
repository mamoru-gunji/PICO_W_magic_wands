import time

class CustomError(Exception):
    pass

class MyClass:
    def some_method(self):
        try:
            time.sleep(2)
            raise CustomError("This is a custom error.")
        except CustomError as e:
            # クラス外に例外を渡す
            raise e

try:
    instance = MyClass()
    instance.some_method()
except CustomError as e:
    # メインルーチンで例外をキャッチ
    print(f"Caught an exception: {e}")