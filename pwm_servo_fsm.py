# This program demonstrates the use of the PCA9685 PWM driver
# This is useful to effectively control multiple servos
# In this example, there is a standard servo on channel 0.

# Libraries
import time

# This library uses BCM numbering!!!!
from adafruit_servokit import ServoKit

# Initialize ServoKit for the PWA board.
kit = ServoKit(channels=16)

# Specify the channels you are using on the PWM driver
channel_servo1 = 0

# To set the servo range to 180 degrees for the standard servos
# You can adjust the values if needed
kit.servo[channel_servo1].set_pulse_width_range(400,2300)
    

print("Press CTRL+C to end the program.")


# Keep track of the state
FSM1State = 0
FSM1NextState = 0

# Keep track of the timing
FSM1LastTime = 0
duration = 2

# Main program 
try:
        
    noError = True
    while noError:

        # Check the current time
        currentTime = time.time()

        # Update the state
        FSM1State = FSM1NextState


        # Check the state transitions for FSM 1
        # This is a Mealy FSM
        # State 0: angle of 0 on channel 0 or on the way there
        if (FSM1State == 0):        

            if (currentTime - FSM1LastTime > duration):
                
                channel = channel_servo1
                angle = 0
                kit.servo[channel].angle = angle
                print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                FSM1NextState = 1
            else:
                FSM1NextState = 0

        # State 1: angle of 45 on channel 0 or on the way there
        elif (FSM1State == 1):      

            if (currentTime - FSM1LastTime > duration):
                
                channel = channel_servo1
                angle = 180
                kit.servo[channel].angle = angle
                print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                FSM1NextState = 2
            else:
                FSM1NextState = 1

        # State 2: angle of 90 on channel 1 or on the way there
        elif (FSM1State == 2):      

            if (currentTime - FSM1LastTime > duration):

                channel = channel_servo1
                angle = 90
                kit.servo[channel].angle = angle
                print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                FSM1NextState = 3
            else:
                FSM1NextState = 2

        # State 3: angle of 135 on channel 0 or on the way there
        elif (FSM1State == 3):      

            if (currentTime - FSM1LastTime > duration):
                
                channel = channel_servo1
                angle = 135
                kit.servo[channel].angle = angle
                print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                FSM1NextState = 4
            else:
                FSM1NextState = 3

        # State 4: angle of 180  on channel 1 or on the way there
        elif (FSM1State == 4):      

            if (currentTime - FSM1LastTime > duration):
                
                channel = channel_servo1
                angle = 60
                kit.servo[channel].angle = angle
                print ('angle: {0} \t channel: {1}'.format(angle,channel))
                
                FSM1NextState = 0

            else:
                FSM1NextState = 4
                
        # State ??
        else:
            print("Error: unrecognized state for FSM1")
            
        # If there is a state change, record the time    
        if (FSM1State != FSM1NextState):
            FSM1LastTime = currentTime
 
            
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        pass		# do nothing
