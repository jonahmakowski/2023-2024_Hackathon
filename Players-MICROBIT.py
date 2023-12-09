from microbit import *
import radio

ID = 2
RADIO_GROUP = 10
radio.config(group=RADIO_GROUP, power=7)
radio.on()

def fill_screen():
    for x in range(0, 5):
        for y in range(0, 5):
            display.set_pixel(x, y, 9)

while True:
    receiver = radio.receive()
    if button_a.was_pressed():
        radio.send('{}:a'.format(ID))
    elif button_b.was_pressed():
        radio.send('{}:b'.format(ID))
    if receiver:
        if receiver == "b'meet'":
            while not button_a.was_pressed() and not button_b.was_pressed():
                fill_screen()
                sleep(100)
                display.clear()
                sleep(100)
        elif receiver == "b'" + str(ID) + ":dead'":
            display.scroll('DEAD')
            fill_screen()
            radio.off()
            while True:
                pass
        elif receiver == "b'" + str(ID) + ":blink_light'":
            while not button_a.was_pressed() and not button_b.was_pressed():
                display.set_pixel(2, 2, 9)
                sleep(100)
                display.clear()
                sleep(100)
        elif receiver == "b'" + str(ID) + ":imposter'":
            display.scroll('You Imposter!')
