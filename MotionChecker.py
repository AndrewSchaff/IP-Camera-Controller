#Look for motion

#Python Libraries
import cv2
import numpy as np
import time

import Camera #Camera script (needed for images)

#Setup Pygame (used for the sound effects)
import pygame
pygame.init()
pygame.mixer.music.load("Alert.wav") #Load up the sound effect

timeOfLastSound = 0 #When was the last sound effect played?
timeOfLastFlash = 0 #What was the banner last flashed?
showBanner = True #Are we showing the banner right now?

#Duplicate of the Arduino map function (borrowed from StackExchange)
def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

#Reset the background subtractor
def getResetBG():
    global fgbg
    global lastReset
    
    fgbg  = cv2.BackgroundSubtractorMOG()
    lastReset = time.time()

#Get a mask representing what's changed in the frame
def processDifference(frame, warningThreshold = 35000, wantMask=True):
    global timeOfLastFlash, timeOfLastSound
    global showBanner

    #Reset the background subtractor every 60s
    if time.time() - lastReset >= 60:
        getResetBG()

    #Run the background subtractor on the current frame
    fgmask = fgbg.apply(frame)

    #Clean up the mask to reduce noise
    kernel = np.ones((10,10), np.uint8)
    erosion = cv2.erode(fgmask, kernel, iterations = 2)
    
    differenceScore = int(sum(sum(fgmask))/255) #Get the number of white pixels in the frame

    if wantMask: frame = fgmask #If the user wants it, show them the mask

    #Draw the motion reading indicator
    cv2.putText(frame, "Motion Reading: " + str(differenceScore), (0, len(frame) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

    #If 'warningThreshold' has been exceeded, display a warning
    if differenceScore > warningThreshold:

        #Play a sound effect every 3 seconds
        if time.time() - timeOfLastSound > 3:
            pygame.mixer.music.play()
            timeOfLastSound = time.time()

        #Show the banner, if we're supposed to
        if showBanner:
            cv2.rectangle(frame, (0,0), (320, 30), (0,0,255), -1)
            cv2.putText(frame, "Movement Detected", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        #Activate/Deactivate the banner every 0.5 seconds
        if time.time() - timeOfLastFlash > 0.5: #"""map(differenceScore, warningThreshold, warningThreshold * 2, 2, 1)"""
            showBanner = not showBanner

            timeOfLastFlash = time.time()

    return frame

getResetBG() #Setup the background subtractor

#Some test code, only to be run when this isn't being used as a library
if __name__ == "__main__":
        while True:
            #ret, frame = cap.read()
            frame = Camera.getIMG()
            fgmask = fgbg.apply(frame)
            #res = cv2.bitwise_and(frame, frame, mask = fgmask)
            res = processDifference(frame)
            cv2.imshow('img', res)

            if cv2.waitKey(20) == 27:
                break
        cv2.destroyAllWindows()
