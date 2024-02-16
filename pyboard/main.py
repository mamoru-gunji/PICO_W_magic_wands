import global_value as g
from DFPlayer import DFPlayer

g.dfplayer = DFPlayer()
g.dfplayer.vol = 20
g.dfplayer.buff = 0
g.dfplayer.play(9999)


import gc
import time
import utime
import ntptime
from time import sleep
import machine
from memory_usage import free
from key_triger import input_with_timeout as input
from TouchSensor import TouchSensor
from wifi import wifi
from MPU6050 import MPU6050
from ulab import numpy as np
from LSTM_np import LSTM
from l_chika import l_chika
from multi_thread import ThreadManager
from DataManager import DataManager

g.dfplayer.play(9998)


class Phase:
    def __init__(self):
        try:
            g.spcial_mode
        except AttributeError:
            g.spcial_mode = False
        print(self.__class__.__name__, "init")
        gc.mem_free()

    def process(self):
        print("Base class for all Phases.")


class Phase1(Phase):
    def __init__(self):
        g.spcial_mode = False
        super().__init__()
        g.TouchSensor.ON()

    def process(self):
        pass


class Phase2(Phase):
    def __init__(self):
        super().__init__()
        self.use_special_mode(8000)
        pass

    def process(self):
        print("Phase2 processing")
        while g.TouchSensor.is_touched():
            print("..")
            time.sleep(0.1)

        g.next_Phase = 3

    def use_special_mode(self, limit_ms=20000):
        try:
            g.start_time
            g.spcial_mode
        except AttributeError:
            g.start_time = utime.ticks_ms()
            g.spcial_mode = True
            print("********Special mode start!********")
        self.limit_ms = limit_ms
        try:
            if not g.timer:
                self.init_timer()
        except AttributeError:
            self.init_timer()

    def init_timer(self):  # timerの初期化を行うメソッドを追加
        g.timer = machine.Timer()
        g.timer.init(
            mode=machine.Timer.ONE_SHOT,
            period=self.limit_ms,
            callback=self.timer_handler,
        )

    def timer_handler(self, timer):
        print("********Special mode finished!********")
        g.spcial_mode = False
        g.timer = None


class Phase3(Phase):
    def __init__(self):
        super().__init__()
        g.TouchSensor.OFF()

    def process(self):
        print("Phase3の処理を実行します.")
        time.sleep(2)
        g.play_day.play_day()
        g.next_Phase = 1


class StateMachine:
    def __init__(self):
        self.Phase_objects = {
            1: Phase1,
            2: Phase2,
            3: Phase3,
        }
        g.current_Phase = 1
        g.switch_prev = machine.Pin(1).value()
        g.switch = g.switch_prev
        g.TouchSensor = TouchSensor()
        g.TouchSensor.limit_ms = 2000

    def get_key(self):
        key = input(0.01)
        return key

    def change_Phase(self, next_Phase):
        if 1 <= next_Phase <= 3:
            print("Phaseが変更されました:", next_Phase)
            g.current_Phase = next_Phase
        else:
            print("無効な数字です。1から3の範囲で入力してください。")

    def run(self):
        print("initial Phase:", g.current_Phase)
        while True:
            key = self.get_key()
            if key.isdigit():
                g.next_Phase = int(key)
            if g.TouchSensor.is_touched():
                g.next_Phase = 2

            try:
                if g.next_Phase != g.current_Phase:
                    self.change_Phase(g.next_Phase)
            except Exception:
                pass

            # 現在のPhaseに対応する処理を実行
            current_Phase = self.Phase_objects[g.current_Phase]()
            current_Phase.process()


class play_day:
    def __init__(self, train=True):
        g.rtc = machine.RTC()
        self.time_init()

    def play_day(self):
        for i in range(4):
            if i > 1:
                j = i + 2
            else:
                j = i + 1
            g.dfplayer.play(100 * (3 - i) + g.rtc.datetime()[j])

    def time_init(self):
        now = ntptime.get_now()
        if now:
            value_to_move = now[6]
            new_tuple = now[:6] + now[7:]
            new_tuple = new_tuple[:3] + (value_to_move,) + new_tuple[3:]
            g.rtc.datetime(new_tuple)

    def date_time(self):
        return machine.RTC().datetime()


class Main:
    def __init__(self, train=True):
        self.train = train
        self.state_machine = StateMachine()
        g.dfplayer = DFPlayer()
        g.dfplayer.vol = 30
        g.wifi = wifi()
        g.wifi.ssid = "your ssid"
        g.wifi.password = "your password"

        g.wifi.port = 1205
        g.wifi.server_init()
        if g.wifi.connected == True:
            g.dfplayer.play(1000)
        else:
            g.dfplayer.play(9900)
            time.sleep(4)
            machine.reset()
        g.play_day = play_day()

        if self.train:
            g.wifi.find_client()
        l_chika(blink=0.01)
        self.data_manager = DataManager(train=True)

        pass

    def run(self):
        if self.train:
            self.state_machine.run()


#             g.wifi.disconnect()
#             time.sleep(2)
#
#

#             g.wifi.find_client()
#             g.wifi.send(str(ntptime.time()))

if __name__ == "__main__":
    l_chika(blink=0.01)
    main = Main()
    main.run()
