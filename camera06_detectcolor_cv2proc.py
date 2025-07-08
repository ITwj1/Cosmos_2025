# This program illustrates how to capture frames in a video stream and
# and how to do extract pixels of a specific color
# It uses openCV

import picamera
import picamera.array                                   # This needs to be imported explicitly
import cv2
import time
import numpy as np                                      



# Define the range colors to filter; these numbers represent HSV
lowerColorThreshold = np.array([0, 30, 60])
upperColorThreshold = np.array([20, 150, 255])


# Initialize the camera and grab a reference to the frame
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = False                            # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))


print("Press CTRL+C to end the program.")

try:

        # Allow the camera to warm up
        time.sleep(0.1)
        
        # Continuously capture frames from the camera
        # Note that the format is BGR instead of RGB because we want to use openCV later on and it only supports BGR
        for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
                        
            # Create a numpy array representing the image
            image = frame.array     

            #-----------------------------------------------------
            # We will use numpy and OpenCV for image manipulations
            #-----------------------------------------------------

            # Convert for BGR to HSV color space, using openCV
            # The reason is that it is easier to extract colors in the HSV space
            # Note: the fact that we are using openCV is why the format for the camera.capture was chosen to be BGR
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            # Threshold the HSV image to get only colors in a range
            # The colors in range are set to white (255), while the colors not in range are set to black (0)
            ourmask = cv2.inRange(image_hsv, lowerColorThreshold, upperColorThreshold)

            # Count the number of white pixels in the mask
            numpixels = cv2.countNonZero(ourmask)
            print("Number of pixels in the color range:", numpixels)
       
            # Get the size of the array (the mask is of type 'numpy')
            # This should be 640 x 480 as defined earlier
            numx, numy = ourmask.shape

            # Select a part of the image and count the number of white pixels
            ourmask_center = ourmask[ numx//4 : 3*numx//4 , numy//4 : 3*numy//4 ]
            numpixels_center = cv2.countNonZero(ourmask_center)
            print("Number of pixels in the color range in the center part of the image:", numpixels_center)
           
            # Bitwise AND of the mask and the original image
            image_masked = cv2.bitwise_and(image, image, mask = ourmask)


            # Show the frames
            # The waitKey command is needed to force openCV to show the image
            cv2.imshow("Frame in BGR", image)
            cv2.imshow("Frame in HSV", image_hsv)
            cv2.imshow("Mask", ourmask)
            cv2.imshow("Masked image", image_masked)  
            cv2.waitKey(1)

            # Clear the stream in preparation for the next frame
            rawframe.truncate(0)            
            
  
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        # Clean up the resources
        cv2.destroyAllWindows()
        camera.close() 
