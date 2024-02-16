import time
import global_value as g
from key_triger import input_with_timeout as input

class Phase_0:
    def process(self):
        print("Base class for all phases.")


class Phase1(Phase_0):
    def process(self):
        print("フェーズ1の処理を実行します。")


class Phase2(Phase_0):
    def process(self):
        print("フェーズ2の処理を実行します。")


class Phase3(Phase_0):
    def process(self):
        print("フェーズ3の処理を実行します.")


class StateMachine:
    def __init__(self):
        self.phase_objects = {
            1: Phase1(),
            2: Phase2(),
            3: Phase3(),
        }
        self.current_phase = 1

    def get_key(self):
        key = input(0.1)
        return key
        

    def change_phase(self, number):
        if 1 <= number <= 3:
            self.current_phase = number
            print("フェーズが変更されました:", self.current_phase)
        else:
            print("無効な数字です。1から3の範囲で入力してください。")

    def main_loop(self):
        while True:
            print("現在のフェーズ:", self.current_phase)

            key = self.get_key()

            if key.isdigit():
                number = int(key)
                self.change_phase(number)

            # 現在のフェーズに対応する処理を実行
            self.phase_objects[self.current_phase].process()

            # 一時的な待機時間（実際にはセンサーの読み取りや処理を行う部分が入ります）
            time.sleep(0.1)


if __name__ == "__main__":
    state_machine = StateMachine()
    state_machine.main_loop()