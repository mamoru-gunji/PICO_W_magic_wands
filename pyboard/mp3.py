from dfplayermini import Player
from machine import Pin, SPI
from time import sleep

music = Player(pin_TX=4, pin_RX=5)
print("set volume")
music.volume(25)

print("start play")
music.play(1)
sleep(5)

print("stop play with fadeout")
music.fadeout(3000)

music.play(2)
sleep(1)

music.pause()
sleep(3)

music.loop()
while True:
    music.play(1)
    sleep(1)

# sleep(2)
# music.volume(15)
# music.play(1)
# music.module_sleep()
# music.module_wake()
# print("start play")
# music.play(1)