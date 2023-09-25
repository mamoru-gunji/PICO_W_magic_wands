import example  # ビルドしたCモジュールをインポート

def run_c_code():
    example.c_function()  # Cコードの関数を呼び出す
    print("Back to MicroPython prompt!")

run_c_code()  # Cコードを実行してMicroPythonのプロンプトに戻る
