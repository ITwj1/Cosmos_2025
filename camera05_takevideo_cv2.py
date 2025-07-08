# This program illustrates how to capture frames in a video stream and how to do further processing on them
# It uses numpy to do the calculations and OpenCV to display the frames

import picamera
import picamera.array                           # This needs to be imported explicitly
import time
import cv2
import numpy as np                              



# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = False                            # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create a data structure to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))

print("Press CTRL+C to end the program.")

try:
    
        # Allow the camera to warm up
        time.sleep(0.1)
  
        # Continuously capture frames from the camera
        # Note that the format is BGR instead of RGB because we want to use openCV later on and it only supports BGR
        for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
            
            # Create a numpy array representing the image
            img_np = frame.array

            #-----------------------------------------------------
            # We will use numpy to do all our image manipulations
            #-----------------------------------------------------

            # Make a copy of the image
            img_np1 = img_np.copy()

            # Modify the copy of the image 
            img_np1.setflags(write=1)                                   # Making the array mutable                                                                                                      
            w,h,d = img_np1.shape
            img_np1[w//4:3*w//4 , h//4:3*h//4 , :] = 255 - img_np1[w//4:3*w//4 , h//4:3*h//4 , :]


            # Show the frames
            # Note that OpenCV assumes BRG color representation
            # The waitKey command is needed to force openCV to show the image
            cv2.imshow("Orignal frame", img_np)
            cv2.imshow("Modified frame", img_np1)
            cv2.waitKey(1)

            # Clear the rawframe in preparation for the next frame
            rawframe.truncate(0)


# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
            # Clean up the resources
            cv2.destroyAllWindows()
            camera.close() 
