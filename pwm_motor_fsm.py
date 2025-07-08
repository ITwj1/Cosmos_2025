# This program demonstrates how to control DC motors
# connected via a motor driver.
# The PWM signal to the motor driver is generated
# by the PCA9685 PWM driver.

# Libraries
import RPi.GPIO as GPIO
import time

from adafruit_pca9685 import PCA9685
import busio
import board

 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO Pins
GPIO_Ain1 = 17
GPIO_Ain2 = 27
GPIO_Bin1 = 5
GPIO_Bin2 = 6

# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)

# Both motors are stopped 
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)

# Configure the PWM driver for the motors
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
# However, if we are using ServoKit (for servos),
# this will automatically be overwritten to 50.
pca.frequency = 1000        

motor_pwmA = pca.channels[4]
motor_pwmB = pca.channels[5]

# Helper function
def duty(speed):
    return int(speed * 65535)

# Set the initial speed of the motors
speed = 0.5
motor_pwmA.duty_cycle = duty(speed)
motor_pwmB.duty_cycle = duty(speed)



# Keep track of the state
FSM1State = 0
FSM1NextState = 0

# Keep track of the timing
FSM1LastTime = 0

print("Press CTRL+C to end the program.")

# Main program
try:
        
        noError = True
        while noError:

            # Check the current time
            currentTime = time.time()

            # Update the state
            FSM1State = FSM1NextState


            # Check the state transitions for FSM 1
            if (FSM1State == 0):
                if (currentTime - FSM1LastTime > 1):
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    speed = 0.5
                    motor_pwmA.duty_cycle = duty(speed)
                    print ("Forward half speed")
                
                    FSM1NextState = 1
                else:
                    FSM1NextState = 0

            elif (FSM1State == 1):
                if (currentTime - FSM1LastTime > 1):
                    GPIO.output(GPIO_Ain1, True)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, True)
                    GPIO.output(GPIO_Bin2, False)
                    speed = 1.0
                    motor_pwmA.duty_cycle = duty(speed)
                    print ("Forward full speed")
                    
                    FSM1NextState = 2
                else:
                    FSM1NextState = 1

            elif (FSM1State == 2):
                if (currentTime - FSM1LastTime > 1):
                    GPIO.output(GPIO_Ain1, False)
                    GPIO.output(GPIO_Ain2, True)
                    GPIO.output(GPIO_Bin1, False)
                    GPIO.output(GPIO_Bin2, True)
                    speed = 0.33
                    motor_pwmA.duty_cycle = duty(speed)
                    print ("Backward third speed")
                                    
                    FSM1NextState = 3
                else:
                    FSM1NextState = 2

            elif (FSM1State == 3):
                if (currentTime - FSM1LastTime > 1):
                    GPIO.output(GPIO_Ain1, False)
                    GPIO.output(GPIO_Ain2, False)
                    GPIO.output(GPIO_Bin1, False)
                    GPIO.output(GPIO_Bin2, False)
                    print ("Stop")
                
                    FSM1NextState = 0
                else:
                    FSM1NextState = 3

            else:
                print("Error: unrecognized state for FSM1")
                noError = False   

            # If there is a state change, record the time    
            if (FSM1State != FSM1NextState):
                FSM1LastTime = currentTime
                
                                
        # Clean up GPIO if there was an error
        GPIO.cleanup()

            

# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        GPIO.cleanup()
