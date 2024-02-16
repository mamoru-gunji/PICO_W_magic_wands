# ov7670.py
import time
from machine import Pin, I2C

class OV7670:
    def __init__(self, scl_pin=21, sda_pin=20, address=0x21):
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))  # Adjust the I2C bus number if needed
        self.address = address

    def read_reg(self, reg):
        return self.i2c.readfrom_mem(self.address, reg, 1)[0]

    def write_reg(self, reg, value):
        self.i2c.writeto_mem(self.address, reg, bytes([value]))

    def reset(self):
        self.write_reg(0x12, 0x80)
        time.sleep_ms(100)

    def init(self):
        self.reset()
        
        # OV7670 initialization steps
        self.write_reg(0x3a, 0x04)  # TSLB: UV format
        self.write_reg(0x67, 0x80)  # TSLB: enable scaling
        # ... Add more initialization steps based on the datasheet

    def capture_frame(self):
        # Capture a single frame
        self.write_reg(0x0e, 0x06)  # COM7: Set bit 2 to enable QCIF format
        self.write_reg(0x12, 0x01)  # COM7: Set bit 0 to enable QCIF format
        self.write_reg(0x1a, 0x7a)  # HREF: Set HSTART to 0x7a
        self.write_reg(0x32, 0x80)  # HREF: Set HSTOP to 0x80
        self.write_reg(0x17, 0x16)  # HSTART: Set HSTART to 0x16
        self.write_reg(0x18, 0x04)  # HSTOP: Set HSTOP to 0x04
        
        # Trigger a single frame capture
        self.write_reg(0x0d, self.read_reg(0x0d) | 0x04)  # COM7: Set bit 2 to start capture

        while not (self.read_reg(0x0d) & 0x04):  # Wait for the capture to complete
            time.sleep_ms(10)

        # Read the captured frame data
        frame_data = self.i2c.readfrom_mem(self.address, 0x00, frame_size)
        
        return frame_data

# Example usage:
# ov7670 = OV7670()
# ov7670.init()
# frame = ov7670.capture_frame()
# print("Frame captured:", frame)
