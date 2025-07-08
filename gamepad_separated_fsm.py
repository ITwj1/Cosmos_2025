# Sample code for interfacing with the USB gamepad
# This is non-blocking
# It separates button and joystick events (to lower the risk of missing a button event when moving a joystick)


# Libraries
from evdev import InputDevice, categorize
import time


# Check if the gamepad is connected
# You need to adjust the event number if the wrong input device is read
#       Method: Unplug the dongle, open a terminal window and list what you see in /dev/input/
#               Now plug in the dongle, and list /dev/input again. You should see an event that
#               was not there before. This is the one you need to use below.
gamepad = InputDevice('/dev/input/event5')
print(gamepad)
print("")



# ------------------------------------------------------------
# Keep track of the state
FSM1State = 0
FSM1NextState = 0

# Keep track of the timing
FSM1LastTime = time.time()

print("Press CTRL+C to end the program.\n")
print ("FSM1: go to state 0 (wait for button A press)")
print ("")

# Main code
try:

        noError = True
        while noError:

            # Check the current time
            currentTime = time.time()

            # Update the state
            FSM1State = FSM1NextState

            
            # Process the gamepad events
            # This implementation is non-blocking
            newbutton = False
            newstick  = False
            try:
                for event in gamepad.read():            # Use this option (and comment out the next line) to react to the latest event only
                    #event = gamepad.read_one()         # Use this option (and comment out the previous line) when you don't want to miss any event
                    eventinfo = categorize(event)
                    if event.type == 1:
                        newbutton = True
                        codebutton  = eventinfo.scancode
                        valuebutton = eventinfo.keystate
                    elif event.type == 3:
                        newstick = True
                        codestick  = eventinfo.event.code
                        valuestick = eventinfo.event.value
            except:
                pass





            # Check the state transitions for FSM 1
            # This is a Mealy FSM
            # State 0:
            if (FSM1State == 0):
                # If button A is pressed
                if (newbutton and codebutton == 305 and valuebutton == 1):                         
                    print (" ** Button A was pressed **\n")
                    FSM1NextState = 1
                    FSM1LastTime = currentTime
                    print ("FSM1: go to state 1 (wait for stick pressed down)")
                    print ("")
                elif (currentTime - FSM1LastTime > 10.0):
                    print (" ** Time out **\n")
                    FSM1NextState = 2
                    FSM1LastTime = currentTime
                    print ("FSM1: go to state 2 (wait for any button press)")
                    print ("")
                else:
                    FSM1NextState = 0


            # State 1: 
            elif (FSM1State == 1):
                # If stick is pressed down
                if (newstick and codestick == 1 and valuestick > 200):                         
                    print (" ** Stick was pressed down **\n")
                    FSM1NextState = 2
                    FSM1LastTime = currentTime
                    print ("FSM1: go to state 2 (wait for any button press)")                
                    print ("")
                elif (currentTime - FSM1LastTime > 10.0):
                    print (" ** Time out **\n")
                    FSM1NextState = 0
                    FSM1LastTime = currentTime
                    print ("FSM1: go to state 0 (wait for button A press)")
                    print ("")
                else:
                    FSM1NextState = 1

                    
            # State 2: 
            elif (FSM1State == 2):
                if (newbutton and valuebutton == 1):
                    print (" ** Random button was pressed **\n")
                    FSM1NextState = 0
                    FSM1LastTime = currentTime
                    print ("FSM1: go to state 0 (wait for button A press)")
                    print ("")
                else:
                    FSM1NextState = 2


            # Unrecognized state
            else:
                print("Error: unrecognized state for FSM1")
                noError = False   


        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        gamepad.close()

        

