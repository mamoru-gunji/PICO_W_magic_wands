import machine
import time

# メインループが実行中かどうかを示す変数
main_loop_running = True

# タイマーが経過したときに呼び出されるコールバック関数
def timer_callback(timer):
    global main_loop_running
    main_loop_running = False

# タイマーのインスタンスを作成
# 第1引数: タイマーが呼び出される間隔（ミリ秒）
# 第2引数: タイマーが呼び出される関数（コールバック）
timer = machine.Timer()
timer.init(period=5000, mode=machine.Timer.PERIODIC, callback=timer_callback)

# メインループ
while main_loop_running:
    # メインの処理を実行
#     print("Main loop running...")
    time.sleep(1)

# メインループが終了した後の処理
print("Main loop exited.")
timer.init()
