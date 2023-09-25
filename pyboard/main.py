import machine
import utime

pin_btn = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
uart = machine.UART(1, baudrate=9600, tx=machine.Pin(4), rx=machine.Pin(5))
led = machine.Pin("LED", machine.Pin.OUT)

ON  = 0 # LOW
OFF = 1 # HIGH

btn = OFF
prev_btn = OFF

# DFPlayer シリアル通信データフォーマット (以下、各1byte)
#  1. スタートバイト (0x7E固定)
#  2. バージョン情報 (0xFF固定で良い)
#  3. データ長 (スタートバイト、チェックサム(上位、下位)、エンドバイトを除くので、ほぼ0x06固定)
#  4. コマンド (よく使うものは、0x06:ボリューム指定(0〜30)、0x12: "mp3"フォルダ内の曲番号指定再生、0x0E:曲停止)
#  5. フィードバック (0x00:フィードバック不要、0x01:フィードバック必要)
#  6. パラメータ１ (2byteの上位)
#  7. パラメータ２ (2byteの下位)
#  8. チェックサム1 (2byteの上位)
#  9. チェックサム2 (2byteの下位)
# 10. エンドバイト (0xEF固定)
# ※ 8,9のチェックサムは、0 - (2.〜7.の和)で算出されるマイナス値の2byteの2の補数表現
# 例) [7E, FF, 06, 09, 00, 00, 04, FE, EE, EF]のとき、チェックサムの[FE, EE]の部分は以下のように計算される。
#     [FF, 06, 09, 00, 00, 04]の合算値が274なので、チェックサムの値は 0 - 274 = -274。
#     274は2進数表現だと 0000 0001 0001 0010 なので、反転させると 1111 1110 1110 1101 (=1の補数)
#     2の補数はこれに1を加えるので 1111 1110 1110 1110 = 0xFEEE となる。

def calc_checksum(sum_data):
    temp = ~sum_data + 1 # 2の補数の計算(ビットを反転させて1を足す)
    h_byte = (temp & 0xFF00) >> 8
    l_byte = temp & 0x00FF
    return h_byte, l_byte

def send_data(command, param):
    ver      = 0xFF
    d_len    = 0x06
    feedback = 0x00
    param1  = (param & 0xFF00) >> 8
    param2  = param & 0x00FF
    cs1, cs2 = calc_checksum(ver + d_len + command + feedback + param1 + param2)
    sdata = bytearray([0x7E, ver, d_len, command, feedback, param1, param2, cs1, cs2, 0xEF])
    uart.write(sdata)
    #print(sdata)

def init_sd():
    send_data(0x3F, 0x02) # 0x02でSDカードのみ有効化
    utime.sleep_ms(1000)

def set_volume(volume):
    send_data(0x06, volume)
    utime.sleep_ms(500)

def play_sound(num):
    # "mp3"という名称のフォルダ内に保存された、"0001.mp3"のような名称のファイルを再生
    print("Play {}".format(num))
    send_data(0x12, num)
    utime.sleep_ms(500)

###################################

init_sd()
print("Ready.")
set_volume(30)

num= 0

while True:
    btn = pin_btn.value()

    if prev_btn == OFF and btn == ON:
        num += 1
        if num >= 3:
            num = 1
        play_sound(num)

    prev_btn = btn
    led.on()
    utime.sleep_ms(1)
    led.off()
