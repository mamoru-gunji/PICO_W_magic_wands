from machine import I2C, Pin
import global_value as g
import re
import time
import math

class MPU6050:
    def __init__(self, scl=Pin(17), sda=Pin(16), freq=400000, once=True):
        print('MPU6050 init')
        self.vbus = Pin(18, mode=Pin.OUT)
        g.Pin_scl=scl
        g.Pin_sda=sda
        self.freq = freq
        self.i2c = I2C(0, scl=g.Pin_scl, sda=g.Pin_sda, freq=self.freq)
        self.address = 0x68
        self.scale_a = 16384.0
        self.scale_g = 131.0*100
        self.val = 0
        self.loop = 1
        self.once = once
#         self.accel_data = None
    
    def on(self):
        self.vbus.on()
        
        
    def off(self):
        self.vbus.off()
        
    def twosComplement_hex(self,val):
        if val & (1 << (16 - 1)):
            val -= 1 << 16
        return val

    def read_data(self):
        self.i2c.writeto(self.address, bytes([0x6B, 0x00]))  # MPU6050初期化
        self.accel_data = self.i2c.readfrom_mem(self.address, 0x3B, 14)
        self.accel_x = self.twosComplement_hex((self.accel_data[0] << 8 | self.accel_data[1])) / self.scale_a
        self.accel_y = self.twosComplement_hex((self.accel_data[2] << 8 | self.accel_data[3])) / self.scale_a
        self.accel_z = self.twosComplement_hex((self.accel_data[4] << 8 | self.accel_data[5])) / self.scale_a
        self.gyro_x = self.twosComplement_hex((self.accel_data[8] << 8 | self.accel_data[9])) / self.scale_g
        self.gyro_y = self.twosComplement_hex((self.accel_data[10] << 8 | self.accel_data[11])) / self.scale_g
        self.gyro_z = self.twosComplement_hex((self.accel_data[12] << 8 | self.accel_data[13])) / self.scale_g
        self.val = [self.accel_x, self.accel_y, self.accel_z, self.gyro_x, self.gyro_y, self.gyro_z]
    
    def data(self):
        if self.once:
            self.on()
        if not self.vbus.value():
            self.on()
            time.sleep_ms(10)
            
        for i in range(100):
            try:
                self.read_data()
                if self.val[0] != 0:
                    break
            except Exception as e:
                pass
        if self.once:
            self.off()
        return self.val
    
    def main(self):
        self.data()
        print(self.val)
        
def main():
    MPU = MPU6050(once = False)
    MPU.on()
    try:
        for i in range(100):
            MPU.main()
            time.sleep_ms(1)
    except Exception as e:
        print(e)
    finally:
        MPU.off()
    
if __name__ == '__main__':
    main()