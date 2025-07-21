import network
import socket
import time
import ure
from machine import Pin, PWM, Timer

# Motor control pins and configuration
RIGHT_MOTOR_PIN1 = 0
RIGHT_MOTOR_PIN2 = 1
LEFT_MOTOR_PIN1 = 2
LEFT_MOTOR_PIN2 = 3
DEFAULT_FREQUENCY = 50           # PWM frequency for motors
DEFAULT_DUTY_CYCLE = 65535       # Maximum duty cycle for full speed

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
TRIG_3_T = 13
ECHO_3_T = 12

TRIG_BOTTOM = Pin(TRIG_1_B, Pin.OUT)
ECHO_BOTTOM = Pin(ECHO_1_B, Pin.IN)
TRIG_TOP = Pin(TRIG_2_T, Pin.OUT)
ECHO_TOP = Pin(ECHO_2_T, Pin.IN)
TRIG_COVER = Pin(TRIG_3_T, Pin.OUT)
ECHO_COVER = Pin (ECHO_3_T, Pin.IN)


# Distance thresholds for stopping and turning

DISTANCE_STOP0 = 40              # Distance to stop the vehicle
DISTANCE_STOP1 = 45              # Distance to start turning
DISTANCE_COVER = 20				 # Distance to set ESP32 Interrupt PIN high

# Mute pinouts
MUTE = 8

mute_pin = Pin(MUTE, Pin.OUT)
mute_state = False # Default mute state
auto_mode = False # Default auto mode
forward_mode = False # Default foward mode

# Audio interrupt
AUDIO = 11
audio_interrupt_pin = Pin(AUDIO, Pin.OUT)

# Autonomous and forward mode settings
AUTO_TIMER_PERIOD = 500          # Time interval for autonomous driving
FORWARD_TIMER_PERIOD = 100       # Time interval for checking forward distance
COVER_TIMER_PERIOD = 200         # Time interval for checking distance from cover

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


# change duty cycle for PWM motor

def set_duty(duty):
    EN1.duty_u16(duty)  
    EN2.duty_u16(duty)
# Measure the distance using the ultrasonic sensor
def measure_distance(trig_pin, echo_pin):
    trig_pin.off()
    time.sleep_us(MEASUREMENT_STOP_DELAY)
    trig_pin.on()
    time.sleep_us(MEASUREMENT_START_DELAY)
    trig_pin.off()
    
    while echo_pin.value() == 0:
        pass
    start_time = time.ticks_us()
    
    while echo_pin.value() == 1:
        pass
    end_time = time.ticks_us()
    
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2
    return distance



# Autonomous driving behavior based on distance measurements
def autonomous_drive(timer): 
    global auto_mode, forward_mode
    if auto_mode and not forward_mode:
        distance_front_bottom = measure_distance(TRIG_BOTTOM, ECHO_BOTTOM)
        distance_front_top = measure_distance(TRIG_TOP, ECHO_TOP)
      
        if distance_front_bottom <= DISTANCE_STOP0 or distance_front_top <= DISTANCE_STOP0: 
            stop_all()
            time.sleep(0.1)  
            move_backward()
            time.sleep(0.1)
            stop_all()
            time.sleep(0.1)    

            if distance_front_bottom <= DISTANCE_STOP1 or distance_front_top <= DISTANCE_STOP1:
                turn_right()
                time.sleep(0.1)
            else:
                move_forward()
        else:
            move_forward()
    
            

        
def check_cover_distance(timer):
    distance_cover = measure_distance(TRIG_COVER, ECHO_COVER)
    if distance_cover <= DISTANCE_COVER:
        audio_interrupt_pin.value (1)
    else:
        audio_interrupt_pin.value (0)

def ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    while not ap.active():
        pass
    print(ap.ifconfig()[0])


# Set up the device as a Wi-Fi access point
def http_server():
    global auto_mode, forward_mode
    addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
    s = socket.socket()
    s.bind(addr)  
    s.listen(1)
    # Set up timers for autonomous and forward mode checks
    autonomous_timer = Timer(-1)
    autonomous_timer.init(period=AUTO_TIMER_PERIOD, mode=Timer.PERIODIC, callback=autonomous_drive)
    cover_distance_timer = Timer(-1)
    cover_distance_timer.init(period=COVER_TIMER_PERIOD, mode=Timer.PERIODIC, callback=check_cover_distance)
    while True:
        cl, addr = s.accept()
        
        request = cl.recv(1024).decode()
        print(request)

        match = ure.search("GET (/[^/]+)/", request)
        if match:
            command = match.group(1)
            print(command)
            if (command == "/MOVEFORWARD"):
                move_forward()
                forward_mode = True
            elif (command == "/MOVEBACKWARD"):
                move_backward()
                forward_mode = False
            elif (command == "/TURNLEFT"):
                turn_left()
                forward_mode = False
            elif (command == "/TURNRIGHT"):
                turn_right()
                forward_mode = False
            elif (command == "/STOP"):
                stop_all()
                forward_mode = False
                auto_mode = False
            elif (command == "/AUTO"):
                forward_mode = False
                if auto_mode == False:
                    auto_mode = True
                elif auto_mode == True:
                    auto_mode = False
                    forward_mode = False
                    stop_all()
                    
            elif (command == "/MUTE"):
                global mute_state
                if mute_state == False:
                    mute_pin.value (1)
                    mute_state = True
                elif mute_state == True:
                    mute_pin.value (0)
                    mute_state = False
            elif (command == "/setduty25"):
                duty = int(DEFAULT_DUTY_CYCLE * 0.25)
                set_duty(duty)
            elif (command == "/setduty50"):
                duty = int(DEFAULT_DUTY_CYCLE * 0.50)
                set_duty(duty)
            elif (command == "/setduty75"):
                duty = int(DEFAULT_DUTY_CYCLE * 0.75)
                set_duty(duty)
            elif (command == "/setduty100"):
                duty = int(DEFAULT_DUTY_CYCLE * 1.00)
                set_duty(duty)
        
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
        cl.sendall(response.encode())
        cl.close()
        

# Start the access point mode with given SSID and password
ap_mode('METALUS','123456789')
http_server()







