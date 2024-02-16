from machine import Timer

# タイマー1のコールバック関数
def timer1_callback(timer):
    print("Timer 1 callback!")

# タイマー2のコールバック関数
def timer2_callback(timer):
    print("Timer 2 callback!")

# タイマー1のインスタンスを作成し、1秒ごとにコールバックを実行
timer1 = Timer(-1)
timer1.init(period=1000, mode=Timer.PERIODIC, callback=timer1_callback)

# タイマー2のインスタンスを作成し、2秒ごとにコールバックを実行
timer2 = Timer()
timer2.init(period=2000, mode=Timer.PERIODIC, callback=timer2_callback)