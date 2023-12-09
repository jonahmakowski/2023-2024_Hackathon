from microbit import *
import radio

RADIO_GROUP = 10
ID = 1

radio.config(group=RADIO_GROUP, power=7)
radio.on()

def get_serial():
    if uart.any():
        received_data = uart.read()
        
        return received_data
    return False

def send_serial(data):
    print(data)

while True:
    radio_receive = radio.receive()
    if radio_receive:
        send_serial(radio_receive)
    recived = get_serial()
    if not recived is False:
        radio.send(str(recived))
