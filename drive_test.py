from evdev import InputDevice, categorize
import RPi.GPIO as GPIO
import time

# === GPIO Pin Setup ===
GPIO.setmode(GPIO.BCM)

# Motor A Pins
GPIO_Ain1 = 17
GPIO_Ain2 = 27
GPIO_Apwm = 22

# Motor B Pins
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

# PWM Setup
pwm_frequency = 500
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)
pwmA.start(0)
pwmB.start(0)

# === Gamepad Setup ===
gamepad = InputDevice('/dev/input/event0')  # Change if needed
print(gamepad)

# === D-pad Tracking (instead of joystick) ===
dpad = [0, 0]  # [x, y] where x = HAT0X, y = HAT0Y

# === Button Tracking ===
buttons = [0] * 10

# Indexes for button meanings
BLUE = 0      # A
RED = 1       # B
YELLOW = 2    # X
GREEN = 3     # Y
LT = 4
RT = 5
SELECT = 8
START = 9

enabled = True  # FSM-like toggle

# === Shutdown Handler ===
def stop_execution():
    print("Stopping")
    gamepad.close()
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    time.sleep(1)

# === Input Handler ===
def handle_input():
    global enabled
    if newbutton:
        buttons[codebutton - 304] = valuebutton

    if buttons[SELECT]:
        enabled = not enabled
        print("enabled" if enabled else "disabled")
        time.sleep(0.2)  # debounce

# === Motor Control Function ===
def drive_motors(left, right):
    GPIO.output(GPIO_Ain1, left > 0)
    GPIO.output(GPIO_Ain2, left < 0)
    GPIO.output(GPIO_Bin1, right > 0)
    GPIO.output(GPIO_Bin2, right < 0)
    pwmA.ChangeDutyCycle(abs(left))
    pwmB.ChangeDutyCycle(abs(right))

# === D-pad Based Driving Logic ===
def drive():
    x = dpad[0]
    y = dpad[1]

    if x == 0 and y == -1:        # UP
        drive_motors(100, 100)
    elif x == 0 and y == 1:       # DOWN
        drive_motors(-100, -100)
    elif x == -1 and y == 0:      # LEFT
        drive_motors(-100, 100)
    elif x == 1 and y == 0:       # RIGHT
        drive_motors(100, -100)
    elif x == -1 and y == -1:     # UP + LEFT
        drive_motors(40, 100)
    elif x == 1 and y == -1:      # UP + RIGHT
        drive_motors(100, 40)
    else:                         # No input
        drive_motors(0, 0)

# === Idle State ===
def idle():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

# === MAIN LOOP ===
try:
    noError = True
    while noError:
        newbutton = False

        try:
            for event in gamepad.read():
                eventinfo = categorize(event)

                if event.type == 1:  # Button press/release
                    newbutton = True
                    codebutton = eventinfo.scancode
                    valuebutton = eventinfo.keystate

                elif event.type == 3:  # ABS event → D-pad
                    if eventinfo.event.code == 16:  # HAT0X (left/right)
                        dpad[0] = eventinfo.event.value
                    elif eventinfo.event.code == 17:  # HAT0Y (up/down)
                        dpad[1] = eventinfo.event.value

        except:
            pass

        handle_input()

        if enabled:
            drive()
        else:
            idle()

except KeyboardInterrupt:
    stop_execution()
