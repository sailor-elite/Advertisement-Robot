import network
import socket
from machine import Pin, PWM, Timer
import time

# Motor control pins and configuration
RIGHT_MOTOR_PIN1 = 0
RIGHT_MOTOR_PIN2 = 1
LEFT_MOTOR_PIN1 = 2
LEFT_MOTOR_PIN2 = 3
DEFAULT_FREQUENCY = 50           # PWM frequency for motors
DEFAULT_DUTY_CYCLE = 65535		 # Maximum duty cycle for full speed

RIGHT_MOTOR_CONTROL_PIN_OUTPUT = 6
LEFT_MOTOR_CONTROL_PIN_OUTPUT = 7

# Initialize motor pins
IN1 = Pin(RIGHT_MOTOR_PIN1, Pin.OUT)
IN2 = Pin(RIGHT_MOTOR_PIN2, Pin.OUT)
IN3 = Pin(LEFT_MOTOR_PIN1, Pin.OUT)
IN4 = Pin(LEFT_MOTOR_PIN2, Pin.OUT)

# Set up PWM for motor speed control
EN1 = PWM(Pin(RIGHT_MOTOR_CONTROL_PIN_OUTPUT))
EN2 = PWM(Pin(LEFT_MOTOR_CONTROL_PIN_OUTPUT))
EN1.freq(DEFAULT_FREQUENCY)
EN2.freq(DEFAULT_FREQUENCY)
EN1.duty_u16(DEFAULT_DUTY_CYCLE)  
EN2.duty_u16(DEFAULT_DUTY_CYCLE)



# Ultrasonic sensor configuration
TRIG_1_B = 26
ECHO_1_B = 27
TRIG_2_T = 14
ECHO_2_T = 15
TRIG_BOTTOM = Pin(TRIG_1_B, Pin.OUT)
ECHO_BOTTOM = Pin(ECHO_1_B, Pin.IN)
TRIG_TOP = Pin(TRIG_2_T, Pin.OUT)
ECHO_TOP = Pin(ECHO_2_T, Pin.IN)

# Distance thresholds for stopping and turning

DISTANCE_STOP0 = 40              # Distance to stop the vehicle
DISTANCE_STOP1 = 45              # Distance to start turning

# Mute pinouts
MUTE = 8

mute_pin = Pin(MUTE, Pin.OUT)
mute_state = False # Default mute state

# Autonomous and forward mode settings
AUTO_TIMER_PERIOD = 500          # Time interval for autonomous driving
FORWARD_TIMER_PERIOD = 100       # Time interval for checking forward distance

# Ultrasonic sensor parameters
MEASUREMENT_STOP_DELAY = 2
MEASUREMENT_START_DELAY = 10

# Function to move the vehicle forward
def move_forward():
    motor1_forward()
    motor2_forward()
    
# Function to move the vehicle backward
def move_backward():
    motor1_backward()
    motor2_backward()

# Function to turn the vehicle left
def turn_left():
    motor2_backward()
    motor1_forward()

# Function to turn the vehicle right
def turn_right():
    motor2_forward()
    motor1_backward()

# Motor control functions for specific directions
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

# Function to stop all motors
def stop_all():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()

# Measure the distance using the ultrasonic sensor
def measure_distance_bottom():
    TRIG_BOTTOM.off()
    time.sleep_us(MEASUREMENT_STOP_DELAY)
    TRIG_BOTTOM.on()
    time.sleep_us(MEASUREMENT_START_DELAY)
    TRIG_BOTTOM.off()
    
    while ECHO_BOTTOM.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while ECHO_BOTTOM.value() == 1:
        pass
    end_time = time.ticks_us()
    
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    return distance


def measure_distance_top():
    TRIG_TOP.off()
    time.sleep_us(2)
    TRIG_TOP.on()
    time.sleep_us(10)
    TRIG_TOP.off()
    
    while ECHO_TOP.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while ECHO_TOP.value() == 1:
        pass
    end_time = time.ticks_us()
    
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    return distance

auto_mode = False
forward_mode = False

# Autonomous driving behavior based on distance measurements
def autonomous_drive(timer):
    global auto_mode, forward_mode
    if auto_mode:
        distance_front_bottom = measure_distance_bottom()
        distance_front_top = measure_distance_top()
        print("Distance front bottom:", distance_front_bottom, "cm")
        print("Distance front top:", distance_front_top, "cm")
        
        if distance_front_bottom <= DISTANCE_STOP0 or distance_front_top <= DISTANCE_STOP0: 
            stop_all()
            time.sleep(0.5)
            move_backward()
            time.sleep(0.5)
            stop_all()
            time.sleep(0.5)    
            while measure_distance_bottom() <= DISTANCE_STOP1:
                turn_right()
                time.sleep(0.5)
            while measure_distance_top() <= DISTANCE_STOP1:
                turn_right()
                time.sleep(0.5)
        else:
            move_forward()
            

# Check distance in forward mode and stop if an obstacle is detected
def check_forward_distance(timer):
    global forward_mode
    if forward_mode:
        distance_front_bottom = measure_distance_bottom()
        distance_front_top = measure_distance_top()
        if distance_front_bottom <= DISTANCE_STOP0 or distance_front_top <=DISTANCE_STOP0:  # Próg odległości w cm
            stop_all()
            forward_mode = False

# Generate a web page for controlling the vehicle
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
            <button onclick="sendCommand('auto')" class="btn">AUTO</button>
            <button onclick="toggleMute()" class="btn">MUTE</button>
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
         function toggleMute() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "/mute", true);
            xhr.send();
            }

    </script>
</body>
</html>
"""
    return html

# Set up the device as a Wi-Fi access point
def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        pass

    print('AP Mode Is Active, You can Now Connect')
    print('IP Address To Connect to: ' + ap.ifconfig()[0])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))  # Powiązanie gniazda z adresem IP punktu dostępowego
    s.listen(5)
    print("Socket listening on port 80")

    while True:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024).decode()
        print('Content = %s' % str(request))
        
        # Parse and execute commands from the web interface
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
            EN1.duty_u16(duty)
            EN2.duty_u16(duty)
        
        elif '/move' in request:
            command = request.split('command=')[1].split(' ')[0]
            if command == 'forward':
                move_forward()
                global forward_mode
                forward_mode = True
            elif command == 'backward':
                move_backward()
                forward_mode = False
            elif command == 'left':
                turn_left()
                forward_mode = False
            elif command == 'right':
                turn_right()
                forward_mode = False
            elif command == 'stop':
                stop_all()
                forward_mode = False
            elif command == 'auto':
                global auto_mode
                auto_mode = not auto_mode
                forward_mode = False
            elif '/mute' in request:
                if mute_state == False:
                    mute_pin.value (1)
                    mute_state = True
                
                elif mute_state == True:
                    mute_pin.value (0)
                    mute_state = False

        # Send the web page as a response
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page()
        conn.sendall(response.encode())
        conn.close()

# Set up timers for autonomous and forward mode checks
autonomous_timer = Timer(-1)
autonomous_timer.init(period=AUTO_TIMER_PERIOD, mode=Timer.PERIODIC, callback=autonomous_drive)

# Start the access point mode with given SSID and password
forward_timer = Timer(-1)
forward_timer.init(period=FORWARD_TIMER_PERIOD, mode=Timer.PERIODIC, callback=check_forward_distance)

ap_mode('mm', '123456789')



