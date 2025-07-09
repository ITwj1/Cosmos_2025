from evdev import InputDevice, categorize
import RPi.GPIO as GPIO
import time

# Pin setup
GPIO.setmode(GPIO.BCM)

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

# Gamepad setup
gamepad = InputDevice('/dev/input/event0')
print(gamepad)

joystick = [128, 128]
buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

X = 0
Y = 1

BLUE = 0
RED = 1
YELLOW = 2
GREEN = 3
LT = 4
RT = 5
SELECT = 8
START = 9

enabled = True


def stop_execution():
    print("Stopping")
    gamepad.close()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    time.sleep(1)


def handle_input():
    global enabled
    
    if newbutton:
        buttons[codebutton - 304] = valuebutton

    elif newstick:
        joystick[codestick] = valuestick

    if buttons[SELECT]:
        enabled = not enabled
        print("enabled" if enabled else "disabled")
        time.sleep(0.2)


def drive_motors(left, right):
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


def drive():
    if joystick[X] == 128 and joystick[Y] == 0:  		# forward
        drive_motors(100, 100)

    elif joystick[X] == 128 and joystick[Y] == 255:  	# backwards
        drive_motors(-100, -100)

    elif joystick[X] == 0 and joystick[Y] == 128:  		# ccw
        drive_motors(-100, 100)

    elif joystick[X] == 255 and joystick[Y] == 128:  	# cw
        drive_motors(100, -100)

    elif joystick[X] == 0 and joystick[Y] == 0:  		# left
        drive_motors(40, 100)

    elif joystick[X] == 255 and joystick[Y] == 0:  		# right
        drive_motors(100, 40)

    elif joystick[X] == 128 and joystick[Y] == 128:  	# idle
        drive_motors(0, 0)


def idle():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)


try:

    noError = True
    while noError:

        newbutton = False
        newstick = False
        try:
            for event in gamepad.read():
                eventinfo = categorize(event)

                if event.type == 1:
                    newbutton = True
                    codebutton = eventinfo.scancode
                    valuebutton = eventinfo.keystate

                elif event.type == 3:
                    newstick = True
                    codestick = eventinfo.event.code
                    valuestick = eventinfo.event.value
        except:
            pass

        handle_input()

        if enabled:
            drive()

        else:
            idle()

except KeyboardInterrupt:
    stop_execution()


