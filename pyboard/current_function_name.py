import sys

def current_function_name():
    # スタックトレースから関数名を取得する
    # スタックトレースはタプルのリストとして返される
    stack = sys.exc_info()[2]
    # 現在の関数がスタックの一番上にある
    frame = stack.tb_frame.f_back
    return frame.f_code.co_name

def foo():
    print("Current function:", current_function_name())

def bar():
    foo()

bar()  # テスト用