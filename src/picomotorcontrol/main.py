import network
import socket
from machine import Pin, PWM

RIGHT_MOTOR_PIN1 = 0
RIGHT_MOTOR_PIN2 = 1
LEFT_MOTOR_PIN1 = 2
LEFT_MOTOR_PIN2 = 3
DEFAULT_FREQUENCY = 50
DEFAULT_DUTY_CYCLE = 25535

RIGHT_MOTOR_CONTROL_PIN_OUTPUT = 6
LEFT_MOTOR_CONTROL_PIN_OUTPUT = 7

# Konfiguracja GPIO dla L298N
IN1 = Pin(RIGHT_MOTOR_PIN1, Pin.OUT)
IN2 = Pin(RIGHT_MOTOR_PIN2, Pin.OUT)
IN3 = Pin(LEFT_MOTOR_PIN1, Pin.OUT)
IN4 = Pin(LEFT_MOTOR_PIN2, Pin.OUT)

EN1 = PWM(Pin(RIGHT_MOTOR_CONTROL_PIN_OUTPUT))
EN2 = PWM(Pin(LEFT_MOTOR_CONTROL_PIN_OUTPUT))

EN1.freq(DEFAULT_FREQUENCY)
EN2.freq(DEFAULT_FREQUENCY)
EN1.duty_u16(DEFAULT_DUTY_CYCLE)  
EN2.duty_u16(DEFAULT_DUTY_CYCLE)

# Steering motor functions
def move_forward():
    motor1_forward()
    motor2_forward()

def move_backward():
    motor1_backward()
    motor2_backward()

def turn_left():
    motor1_backward()
    motor2_forward()

def turn_right():
    motor1_forward()
    motor2_backward()

def motor1_forward():
    IN1.on()
    IN2.off()

def motor1_backward():
    IN1.off()
    IN2.on()

def motor2_forward():
    IN3.on()
    IN4.off()

def motor2_backward():
    IN3.off()
    IN4.on()

def stop_all():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()

# Strona HTML z formularzem
def web_page():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>MOTOR STEERING</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            background-color: #f0f0f0;
            margin: 0;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .controller {
            text-align: center;
            max-width: 90%;
            margin: 0 auto;
        }
        .controller button {
            width: 10vw;
            height: 10vw;
            margin: 5px;
            font-size: 1.5vw;
        }
        .stop-button {
            margin: 10px 0;
            width: 12.5vw;
            height: 12.5vw;
            font-size: 1.5vw;
        }
        .row {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .col {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .speed-controls {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .speed-controls button {
            width: 7.5vw;
            height: 5vw;
            margin: 2px;
            font-size: 1.5vw;
        }
        @media (max-width: 600px) {
            .controller button {
                width: 22.5vw;
                height: 22.5vw;
                font-size: 3vw;
            }
            .stop-button {
                width: 17.5vw;
                height: 17.5vw;
                font-size: 3vw;
            }
             .speed-controls button {
                width: 14vw;
                height: 10vw;
                margin: 2px;
                font-size: 2.5vw;
            }
        }
        @media (max-width: 400px) {
            .controller button {
                width: 20vw;
                height: 20vw;
                font-size: 3vw;
            }
            .stop-button {
                width: 22.5vw;
                height: 22.5vw;
                font-size: 3vw;
            }
            .speed-controls button {
                width: 14vw;
                height: 10vw;
                margin: 2px;
                font-size: 2.5vw;
            }
        }
             @media (max-width: 300px) {
            .controller button {
                width: 20vw;
                height: 20vw;
                font-size: 2vw;
            }
            .stop-button {
                width: 15vw;
                height: 15vw;
                font-size: 2vw;
            }
            .speed-controls button {
                width: 14vw;
                height: 10vw;
                margin: 2px;
                font-size: 2.5vw;
            }
        }
    </style>
</head>
<body>
    <div class="controller">
        <div class="row">
            <button onclick="sendCommand('forward')" class="btn">MOVE FORWARD</button>
        </div>
        <div class="row">
            <div class="col">
                <button onclick="sendCommand('left')" class="btn">TURN LEFT</button>
            </div>
            <div class="col">
                <button onclick="sendCommand('stop')" class="btn stop-button">STOP ALL</button>
            </div>
            <div class="col">
                <button onclick="sendCommand('right')" class="btn">TURN RIGHT</button>
            </div>
        </div>
        <div class="row">
            <button onclick="sendCommand('backward')" class="btn">MOVE BACKWARD</button>
        </div>
        <div class="row speed-controls">
            <button onclick="setDuty('25')" class="btn">25%</button>
            <button onclick="setDuty('50')" class="btn">50%</button>
            <button onclick="setDuty('75')" class="btn">75%</button>
            <button onclick="setDuty('100')" class="btn">100%</button>
            <button onclick="" class="btn">AUTO</button>
        </div>
    </div>
    <script>
        function setDuty(percentage) {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/set_duty?value=" + percentage, true);
            xhr.send();
        }

        function sendCommand(command) {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/move?command=" + command, true);
            xhr.send();
        }
    </script>
</body>
</html>


"""
    return html

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        pass

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to: ' + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))  
    s.listen(5)
    print("Socket listening on port 80")

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode()
        print('Content = %s' % str(request))
        
        if '/set_duty' in request:
            value = request.split('value=')[1].split(' ')[0]
            if value == '25':
                duty = int(65535 * 0.25)
            elif value == '50':
                duty = int(65535 * 0.50)
            elif value == '75':
                duty = int(65535 * 0.75)
            elif value == '100':
                duty = int(65535 * 1.0)
            elif value == '10':
                duty = int(65535 * 0.1)
            EN1.duty_u16(duty)
            EN2.duty_u16(duty)
        
        elif '/move' in request:
            command = request.split('command=')[1].split(' ')[0]
            if command == 'forward':
                move_forward()
            elif command == 'backward':
                move_backward()
            elif command == 'left':
                turn_left()
            elif command == 'right':
                turn_right()
            elif command == 'stop':
                stop_all()

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page()
        conn.sendall(response.encode())
        conn.close()

ap_mode('SSID', 'PASSWORD')

