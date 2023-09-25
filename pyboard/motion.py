from machine import Pin, I2C
import time

# I2Cに使うピンの設定です
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)

# デバイスのアドレス
MMA8452Q_ADDR = 0x1D

# スケールの設定（±2gの場合）
MMA8452_G_SCALE = 2.0

# 加速度センサの設定を初期化します
def init_mma8452q():
    i2c.writeto_mem(MMA8452Q_ADDR, 0x2A, bytes([0x01]))  # Active mode
    # 他の設定も必要に応じて行います
    # 例えば、データレートや動作モードなど

def trimmed_mean(data, trim_percent):
    data.sort()
    trim_size = int(len(data) * trim_percent)
    trimmed_data = data[trim_size:-trim_size]
    return sum(trimmed_data) / len(trimmed_data)

# 加速度データを取得します
def read_acceleration(samples=1, trim_percent=0.2):
    x_data, y_data, z_data = [], [], []
    for _ in range(samples):
        data = i2c.readfrom_mem(MMA8452Q_ADDR, 0x01, 6)
        x_data.append(-(float((int((data[0] << 8) | data[1]) >> 4))/((1 << 11) / MMA8452_G_SCALE)))
        y_data.append(-(float((int((data[2] << 8) | data[3]) >> 4))/((1 << 11) / MMA8452_G_SCALE)))
        z_data.append(-(float((int((data[4] << 8) | data[5]) >> 4))/((1 << 11) / MMA8452_G_SCALE)))
        
    x_avg = trimmed_mean(x_data, trim_percent)
    y_avg = trimmed_mean(y_data, trim_percent)
    z_avg = trimmed_mean(z_data, trim_percent)
    return x_avg, y_avg, z_avg

init_mma8452q()

while True:
    x_offset, y_offset, z_offset = read_acceleration(samples=200)
    x, y, z = read_acceleration(samples=50)  # 100サンプルの平均を取得
    print("X:", x-x_offset, "Y:", y-y_offset, "Z:", z-z_offset)
    time.sleep_ms(100)

