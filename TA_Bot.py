#this is the code to control the TA bot
from evdev import InputDevice, categorize
# Libraries
import time

# This library uses BCM numbering!!!!
from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #it is important to use BCM numbering for the PWA board

# Initialize ServoKit for the PWA board.
kit = ServoKit(channels=16)


#Constants
enabled = True

#DC motors setup (in BCM):
GPIO_Ain1 = 17
GPIO_Ain2 = 27
GPIO_Apwm = 22
GPIO_Bin1 = 5
GPIO_Bin2 = 6
GPIO_Bpwm = 13

GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)

GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Motor Driver setup
pwm_frequency = 500

pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)

pwmA.start(0)
pwmB.start(0)

# Servo setup

# Specify the channels you are using on the PWM driver
#Note: you can include the DC motors on the pwm driver later
channel_servo1 = 0
channel_servo2 = 1
# To set the servo range to 180 degrees for the standard servos
# You can adjust the values if needed
kit.servo[channel_servo1].set_pulse_width_range(400,2300)
kit.servo[channel_servo2].set_pulse_width_range(400,2300)



# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
#       Method: Unplug the dongle, open a terminal window and list what you see in /dev/input/
#               Now plug in the dongle, and list /dev/input again. You should see an event that
#               was not there before. This is the one you need to use below.
gamepad = InputDevice('/dev/input/event5')
print(gamepad)
print("")

arrows = [128,128] #this is the equilibrium
Horizontal = 0
Vertical = 1
newArrow = False

buttons = [0,0,0,0,0,0,0,0] #this is the equilibrium
Blue = 0
Red = 1
Yellow = 2
Green = 3
LT = 4
RT = 5
Select = 6
Start = 7
newButton = False

#Functions:

def stop_execution():
    print("Stopping")
    gamepad.close()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    time.sleep(1)

def take_action():
    global arrows, buttons, pwmA, pwmB, enabled

    if newButton:
        buttons[codebutton - 304] = valuebutton

    elif newArrow:
        arrows[codeArrow] = valueArrow
    
    if buttons[Select]:
        enabled = not enabled
        if enabled:
            print("Enabled")
        else:
            print("Disabled")
        time.sleep(0.5) #to avoid multiple presses


def drive_motors(left, right): #positive inputs = forward, negative inputs = backwards
    if left > 0:
        GPIO.output(GPIO_Ain1, True)
        GPIO.output(GPIO_Ain2, False)

    else:
        GPIO.output(GPIO_Ain1, False)
        GPIO.output(GPIO_Ain2, True)

    if right > 0:
        GPIO.output(GPIO_Bin1, True)
        GPIO.output(GPIO_Bin2, False)

    else:
        GPIO.output(GPIO_Bin1, False)
        GPIO.output(GPIO_Bin2, True)

    pwmA.ChangeDutyCycle(abs(left))
    pwmB.ChangeDutyCycle(abs(right))


def drive(): # This function will drive the motors based on the Arrows Input
    if arrows[Horizontal] == 128 and arrows[Vertical] == 0:  		# forward
        drive_motors(100, 100)

    elif arrows[Horizontal] == 128 and arrows[Vertical] == 255:  	# backwards
        drive_motors(-100, -100)

    elif arrows[Horizontal] == 0 and arrows[Vertical] == 128:  		# ccw
        drive_motors(-100, 100)

    elif arrows[Horizontal] == 255 and arrows[Vertical] == 128:  	# cw
        drive_motors(100, -100)

    elif arrows[Horizontal] == 0 and arrows[Vertical] == 0:  		# left
        drive_motors(40, 100)

    elif arrows[Horizontal] == 255 and arrows[Vertical] == 0:  		# right
        drive_motors(100, 40)

    elif arrows[Horizontal] == 128 and arrows[Vertical] == 128:  	# idle
        drive_motors(0, 0)


def attack():
    """
    Executes a servo movement sequence to simulate an attack.
    This moves servo1 and servo2 through a series of angles.
    You can call this function whenever you're in the ATTACKING state.
    """
    print("Attacking!")
    kit.servo[channel_servo1].angle = 0
    kit.servo[channel_servo2].angle = 180
    time.sleep(0.3)

    kit.servo[channel_servo1].angle = 90
    kit.servo[channel_servo2].angle = 90
    time.sleep(0.3)

    kit.servo[channel_servo1].angle = 180
    kit.servo[channel_servo2].angle = 0
    time.sleep(0.3)

    # Reset
    kit.servo[channel_servo1].angle = 90
    kit.servo[channel_servo2].angle = 90


print("Press CTRL+C to end the program.")


# FSM States
STATE_DRIVING = 0
STATE_ATTACKING = 1
STATE_IDLE = 2

FSM1State = STATE_IDLE
FSM1NextState = STATE_IDLE

try:
    while True:
        # Read input events
        newArrow = False
        newButton = False
        try:
            for event in gamepad.read():
                eventinfo = categorize(event)

                if event.type == 1:
                    newButton = True
                    codebutton = eventinfo.scancode
                    valuebutton = eventinfo.keystate

                elif event.type == 3:
                    newArrow = True
                    codeArrow = eventinfo.event.code
                    valueArrow = eventinfo.event.value
        except:
            pass

        take_action()

        FSM1State = FSM1NextState  # update FSM state

        # FSM Logic
        if FSM1State == STATE_DRIVING:
            if buttons[Red]:  # Go to attacking
                FSM1NextState = STATE_ATTACKING
                print("-> Switching to ATTACK")
            elif buttons[Select]:  # Go to idle
                FSM1NextState = STATE_IDLE
                print("-> Switching to IDLE")
            else:
                drive()

                if buttons[LT]:
                    print("Manual Attack with LT")
                    kit.servo[channel_servo1].angle = 0
                    time.sleep(0.1)
                    kit.servo[channel_servo1].angle = 90
                if buttons[RT]:
                    print("Manual Attack with RT")
                    kit.servo[channel_servo2].angle = 180
                    time.sleep(0.1)
                    kit.servo[channel_servo2].angle = 90

        elif FSM1State == STATE_ATTACKING:
            attack()  # Perform attack sequence
            FSM1NextState = STATE_IDLE  # Always go to idle after attack

        elif FSM1State == STATE_IDLE:
            idle()
            if buttons[Green]:  # Resume driving
                FSM1NextState = STATE_DRIVING
                print("-> Switching to DRIVE")
            elif buttons[Red]:  # Go to attack directly
                FSM1NextState = STATE_ATTACKING
                print("-> Switching to ATTACK")

        else:
            print("Error: unrecognized FSM state")
            break  # stop the loop on error

except KeyboardInterrupt:
    stop_execution()
