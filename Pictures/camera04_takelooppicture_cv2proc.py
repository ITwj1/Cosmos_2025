# This program illustrates how to capture a single image and how to do further processing on it
# The image capture is part of a loop
# It uses openCV

import picamera
import picamera.array                           # This needs to be imported explicitly
import time
import cv2



# Initialize the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.vflip = False                            # Flip upside down or not
camera.hflip = True                             # Flip left-right or not


# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size = (640, 480))



try:
        
        # Allow the camera to warm up
        time.sleep(1)
        print("Starting the main program")
        
        counter = 0
        
        # Loop
        # Capture an individual frame and put it in an array for processing
        print("Showing 5 images consecutively. Press CTRL+C to interrupt.")
        while (counter < 5):

            print("Loop %d" % counter)

            # Capture a single frame and store it in the array we created before
            # Note that we chose the BGR format, since we will be passing this on to openCV
            camera.capture(rawframe, format = 'bgr')

            # Clear the rawframe in preparation for the next frame
            # This way, you can use the same rawframe for the next image capture if you need to
            # You need this if you want to place the camera.capture in a loop
            rawframe.truncate(0)

            
            # Create a numpy array representing the image   
            img_np = rawframe.array


            #-----------------------------------------------------
            # We will use numpy and OpenCV for image manipulations
            #-----------------------------------------------------

            # Convert for BGR to HSV color space, using openCV
            # The reason is that it is easier to extract colors in the HSV space
            # Note: this transformation is also why the format for the camera.capture was chosen to be BGR     
            img_hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)


            # Show the images
            # The waitKey command is needed to force openCV to show the image; if the image does not show up, you can increase the number of ms (the argument of waitKey)
            cv2.imshow("Image in BGR", img_np)
            cv2.imshow("Image in HSV", img_hsv)
            cv2.waitKey(250)
           
           
            # Save the first image to file
            if counter == 0:
                  filename = 'image_modified.jpg'
                  cv2.imwrite(filename, img_hsv)
                  print("  Image written to file " + filename)
                
                  
            # Update the loop counter
            counter = counter + 1
            time.sleep(1)


        # After the while loop, clean up the resources
        cv2.destroyAllWindows()
        camera.close()
        
        
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
        # Clean up the resources
        cv2.destroyAllWindows()
        camera.close()                
        
