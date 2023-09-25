import machine
 
import time


uart = machine.UART(1,baudrate=9600,tx = machine.Pin(4),rx = machine.Pin(5))

 
#タクトスィッチ
# green_button = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
# yellow_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
# red_button = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
# blue_button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)



# LEDー光らせてみました、それだけ
led = machine.Pin("LED", machine.Pin.OUT)
 
# スィッチ１回だけ反応するためのフラグ
B = 0

# トグルスィッチ（赤）用のフラグ
T = 0

# def chk_buttonState():
#     #global pressed_button
#     pressed_button = -1
#     
#     green_b = green_button.value()
#     yellow_b = yellow_button.value()
#     red_b = red_button.value()
#     blue_b = blue_button.value()
#     
#     if not green_b:
#         pressed_button = 10
#     
#     if not yellow_b:
#         pressed_button = 14
# 
#     if not red_b:
#         pressed_button = 17
# 
#     if not blue_b:
#         pressed_button = 21
# 
#     return pressed_button
# 

def calc_checksum(sum_data):
    temp = ~sum_data + 1
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

def play_sound(num):
    global T
    T = 0
     
    send_data(0x12, num)
    #utime.sleep_ms(500)
    

def pause_and_play():
    global T
    
    if T == 0:
        send_data(0x0E, 0)
        T = 1
    elif T == 1:
        send_data(0x0D, 0)
        T = 0
    
    #utime.sleep_ms(500)

def next_sound():
    global T
    T = 0
    
    send_data(0x01, 0)
    
    
def prev_sound():
    global T
    T = 0
    
    send_data(0x02, 0)
    

while True:
    try:

        btnState = 10

        if btnState != -1:
            led.value(0)
            B = B + 1
        else:
            led.value(0)
            B = 0

        if B == 1:
            print(btnState)
            #when any button pressed , do job just once
            if btnState == 10:
                #green
                play_sound(1)
                
                
            elif btnState == 14:
                #Yellow
                prev_sound()
                
            elif btnState == 17:
                #Red
                pause_and_play()
                
                
            elif btnState == 21:
                #Blue
                next_sound()
                
                
            else:
                pass
            
        time.sleep(3)# wait
        led.value(0)
    except KeyboardInterrupt:
        break