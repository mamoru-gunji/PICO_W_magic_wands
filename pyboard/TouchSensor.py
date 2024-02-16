from machine import Pin, Timer
import time
from memory_usage import free

class TouchSensor:
    def __init__(self, power_pin=2, output_pin=1):
        self.power_pin = Pin(power_pin, Pin.OUT)
        self.outputpin_num = output_pin
        self.output_pin_init(self.outputpin_num)
        self.OFF()
        self.limit_ms = 0
        self.timer = None
        
    def output_pin_init(self,output_pin):
        self.output_pin = Pin(output_pin, Pin.IN)

    def is_touched(self):
        return self.output_pin.value() == 1
    
    def ON(self):
        self.power_pin.value(1)
        if self.limit_ms:
            self.Pin_IRQ()

            
        
    def OFF(self):
        self.power_pin.value(0)
        
    def TOGGLE(self):
        self.power_pin.value(not self.power_pin.value())
        
    def timer_callback(self,timer):
        self.output_pin_init(self.outputpin_num)
        print("Timer triggered!")
        self.OFF()
        self.timer.deinit()
        self.timer = None
        free()
    
    def Timer(self, limit_ms):
        if not self.timer:
            self.timer = Timer()
            self.timer.init(period=limit_ms, mode=Timer.ONE_SHOT, callback=self.timer_callback)
        
    def pin_callback(self, pin):
        self.output_pin_init(self.outputpin_num)
        if pin.value():
            self.Timer(self.limit_ms)
            print('pin change', pin)
        free()
    
    def Pin_IRQ(self):
        self.output_pin.irq(trigger=Pin.IRQ_RISING, handler=self.pin_callback)
        
def main():
    touch_sensor = TouchSensor()
    touch_sensor.limit_ms = 2000
    touch_sensor.ON()

    while True:
        if touch_sensor.is_touched():
            print("Touch detected!")
        else:
            print("....")
            touch_sensor.ON()
            free(True)
        time.sleep(0.4)
        

if __name__ == "__main__":
    main()