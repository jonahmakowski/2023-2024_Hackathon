import threading
import serial
import time
from flask import Flask, render_template_string
task1 = False
task2 = False
app = Flask(__name__)
@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="csslearn.css"> 
<title>not among us at all but education</title>
</head>
<body>

<h1 class="title">not among us at all but education</h1>

<p>

<span style="float: right;" class=".endGameButton">
<form action="/end" method="POST">
    <button class="endGameButton"> End Game </button>
</form>
</span>
</p>

<p>Active MicroBits <br>
   MicroBit1 ->

        <form action="/blink1" method="POST">
            <button class="button"> Blink </button>
        </form>
        <form action="/setImposter1" method="POST">
            <button class="button"> Imposter </button>
        </form>
        <form action="/taskDone1" method="POST">
            <button class="button"> Do Task </button>
        </form>
        <form action="/kick1" method="POST">
            <button class="button"> Kick </button>
        </form>
        <text> </text> <br>

   MicroBit2 ->
        <form action="/blink2" method="POST">
            <button class="button"> Blink </button>
        </form>
        <form action="/setImposter2" method="POST">
            <button class="button"> Imposter </button>
        </form>
        <form action="/taskDone2" method="POST">
            <button class="button"> Do Task </button>
        </form>
        <form action="/kick2" method="POST">
            <button class="button"> Kick </button>
        </form>
</p>
</body>
<style>
    body {
  background-color: lightblue;
}

.title {
  font-family: impact;
  border-weight: 2px;
  font-size: 60px
  color: red;
  text-align: center;
}

p {
  font-family: arial;
  font-size: 20px;
}

.button {
  background-color: #04AA6D;
  border-weight: 4px;
  color: white;
  padding: 5px;
  font-family: arial;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  white-space: nowrap;
}
</style>
</html>""")
@app.route('/blink1', methods=['POST'])
def blink1():
    send('{}:blink_light'.format(3))
    return ('', 204)
@app.route('/blink2', methods=['POST'])
def blink2():
    send('{}:blink_light'.format(2))
    return ('', 204)
@app.route('/taskDone1', methods=['POST'])
def taskDone1():
    global task1
    task1 = True
    return ('', 204)
@app.route('/taskDone2', methods=['POST'])
def taskDone2():
    global task2
    task2 = True
    return ('', 204)
@app.route('/kick1', methods=['POST'])
def kick1():
    send('{}:dead'.format(3))
    return ('', 204)
@app.route('/kick2', methods=['POST'])
def kick2():
    send('{}:dead'.format(2))
    return ('', 204)

@app.route('/setImposter1', methods=['POST'])
def imposter1():
    global imposter_ID
    imposter_ID = 3
    send('{}:imposter'.format(3))
    return ('', 204)
@app.route('/setImposter2', methods=['POST'])
def imposter2():
    global imposter_ID
    imposter_ID = 2
    send('{}:imposter'.format(2))
    return ('', 204)

@app.route('/end', methods=['POST'])
def end():
    send('{}:dead'.format(3))
    send('{}:dead'.format(2))
    return ('', 204)

def run_server(host):
    app.run(host=host)
app_thread = threading.Thread(target=run_server, args=('0.0.0.0',))
app_thread.start()

ser = serial.Serial('COM3', 115200)
time.sleep(2)
reciver_input = [['', ''], False]
imposter_ID = 2
kill_mode = 0

def send(dataee):
    data_to_send = dataee
    ser.write(data_to_send.encode('utf-8'))


def reciver():
    global reciver_input
    while True:
        data = ser.readline().decode('utf-8').rstrip()
        if data is not None:
            print(str(data))
            temp = data.split(':')
            reciver_input = [temp, False]
            print(reciver_input)

receiver_thread = threading.Thread(target=reciver)
receiver_thread.start()
while True:
    if reciver_input == [[str(imposter_ID), 'b'], False] and task1 and task2:
        reciver_input[1] = True
        kill_mode = 1
        start_time = time.time()
        print('Kill Mode 1')
    if (reciver_input[0][1] == 'b' and not reciver_input[1]) and (kill_mode == 1 and reciver_input[0][0] != str(imposter_ID)):
        kill_mode = 0
        reciver_input[1] = True
        send('{}:dead'.format(reciver_input[0][0]))
    if kill_mode == 1 and time.time() - start_time > 5:
        kill_mode = 0
        print('Time Up')

    if reciver_input[0][1] == 'a' and not reciver_input[1]:
        reciver_input[1] = True
        send('meet')
