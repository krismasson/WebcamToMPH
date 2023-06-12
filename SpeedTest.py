import cv2
import numpy as np
import mss
from PIL import Image
import keyboard
import time

#loading the picture we compare to current video frame 
background = cv2.imread("captured_frame.png")
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background,(21,21), 0)


video_capture = mss.mss()

#this is the area of the desktop we capture
capture_area = {
    "left": 5,
    "top": 750,
    "width": 1380,
    "height": 330
}

objartime = time.time()
object_present = False
objentime = None
OBJDISPLAY = False
ContourThreshold = 16000  #threshold for object size
CameraDistance = 39.575  #feet visible in camera

cv2.namedWindow("Captured Video", cv2.WINDOW_NORMAL) #make window resizeable
cv2.resizeWindow("Captured Video", 500, 500)  # Adjust the window size here

while True:
    screenshot = video_capture.grab(capture_area)
    image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    frame = np.array(image)  #Capture Desktop frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21), 0)
    
    diff = cv2.absdiff(background,gray)
    thresh = cv2.threshold(diff,30,255,cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations = 2)
    
    motion = False  
    
    cnts,res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if OBJDISPLAY:
        time_diff = ((time.time()) - objentime)  #compare current time to time object left
        the_diff = (objentime - objartime)  #Calculate time elapsed
        obj_diff = CameraDistance / the_diff  #Calculate Speed
        
        if (time_diff < 5):   # show speed for 5 seconds then quit.
            cv2.putText(frame, f"Speed: {obj_diff:.2f}Mph", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        if (time_diff > 5):   # if its been 5 seconds we good.
            OBJDISPLAY = False
            print("Speed " + str(obj_diff) + " Mph" + "  Time difference: " + str(the_diff))
             #print the speed/time difference into the console
    
    #F1 captures a new screenshot to compare the current frame with
    if keyboard.is_pressed('F1'):
        cv2.imwrite("captured_frame.png", frame)
        print("Frame saved as captured_frame.png")
        background = cv2.imread("captured_frame.png")
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background,(21,21), 0)
        
    for contour in cnts:   #motion detect
        if cv2.contourArea(contour) < ContourThreshold :
            continue
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
        motion = True
        if not object_present:
            object_present = True
            objartime = time.time()   #set object Arival time
            

    if object_present and not motion:   #detect motion stopping
        object_present = False
        objentime = time.time()     #set object end time
        OBJDISPLAY = True          #allow the object speed to be displayed
    
    cv2.imshow("Captured Video", frame)
    #cv2.imshow("Captured Video", gray)
    

        
       
    if cv2.waitKey(1) & 0xFF == ord("q") or keyboard.is_pressed('ESC'):
        break

cv2.destroyAllWindows()
