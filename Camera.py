#Python Libraries
import cv2
import numpy as np
import urllib
from time import sleep

#More of my code
import GamepadInterface as GP
import MotionChecker

#Camera details (IP address and login details)
ip_address = "### Insert Camera IP Here ###" #IP Address of the Camera
username = "admin"
password = ""

#Movement Codes
UP = 0
UP_STOP = 1
DOWN = 2
DOWN_STOP = 3
LEFT = 4
LEFT_STOP = 5
RIGHT = 6
RIGHT_STOP = 7
LEFT_UP = 90
LEFT_DOWN = 92
RIGHT_UP = 91
RIGHT_DOWN = 93
STOP = 1

#Command library (makes programming movements easier)
commands = {"up" : 0, "down" : 2, "left" : 4, "right" : 6, "left up" : 90, "left down" : 92, "right up" : 91, "right down" : 93, "stop" : 1}

#Run a command
def runCommand(command):
    if command == "iroff": #Turn IR LEDs on
        urllib.urlopen("http://" + ip_address + ":81/camera_control.cgi?loginuse=" + username + "&loginpas=" + password + "&param=14")

    elif command == "iron": #Turn IR LEDs off
        urllib.urlopen("http://" + ip_address + ":81/camera_control.cgi?loginuse=" + username + "&loginpas=" + password + "&param=14")

    elif command == "goto 720": #Switch to 720p resolution
        urllib.urlopen("http://" + ip_address + ":81/camera_control.cgi?loginuse=" + username + "&loginpas=" + password + "&param=0&value=3")

    elif command == "goto 320": #Switch to a 320 x 240 window
        urllib.urlopen("http://" + ip_address + ":81/camera_control.cgi?loginuse=" + username + "&loginpas=" + password + "&param=0&value=1")
        
    elif command in commands: #Lookup command in 'commands'
        urllib.urlopen("http://" + ip_address + ":81/decoder_control.cgi?loginuse=" + username + "&loginpas=" + password + "&command=" + str(commands[command]) + "&onestep=0&14204158294030.3511137398587523&_=1420415829403")

#Figure out what to do with the joystick data
def interpretJoystickData(axes):
    axes = axes[0] #X/Y, U/D

    #Pretty self-explanatory
    if axes[0] == -1 and axes[1] == 0:
        runCommand('left')
        
    elif axes[0] == 1 and axes[1] == 0:
        runCommand('right')
        
    elif axes[1] == 1 and axes[0] == 0:
        runCommand('up')
        
    elif axes[1] == -1 and axes[0] == 0:
        runCommand('down')

    elif axes[0] == -1 and axes[1] == -1:
        runCommand('left down')
        
    elif axes[0] == 1 and axes[1] == -1:
        runCommand('right down')
        
    elif axes[0] == -1 and axes[1] == 1:
        runCommand('left up')
        
    elif axes[0] == 1 and axes[1] == 1:
        runCommand('right up')

    else:
        runCommand('stop')

#Get an image from the camera
def getIMG():
    url = "http://" + ip_address + ":81/snapshot.cgi?user=" + username + "&pwd=" + password

    #This code borrowed from StackOverflow (http://stackoverflow.com/questions/21061814/how-can-i-read-an-image-from-an-internet-url-in-python-cv2-scikit-image-and-ma)
    req = urllib.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr,-1) # 'load it as it is'

    return img

#Basically turns a joystick into a hat switch
def filterAxisData(axes):
    corrected_axes = []

    for axis in axes:
        axis = float(axis)
        if abs(axis) <= 0.05: #Cut out noise
            corrected_axes.append(0)

        else:
            #Ceiling round anything above -0.05 or 0.05 to -1 or 1
            if axis < 0:
                corrected_axes.append(-1)

            else:
                corrected_axes.append(1)
        
    #Bundle the joystick data into a list of tuples for processing
    joysticks = [(corrected_axes[0], -1 * corrected_axes[1]),(corrected_axes[2], -1 * corrected_axes[3])]
    return joysticks


showFeed = True #Display the feed?
ignoreHide = False #Prevent the hide option from causing unstable windows when the button is held down
wantMask = False #Show the image or movement mask
moving = False #Is the camera moving? (Used to disable motion detection)
LEDs_on = None #Are the IR LEDs on? (Set to None at the start because they may have turned on automatically)

if __name__ == "__main__":
    while True:
        #Get the state of the gamepad
        axes, hat, buttons = GP.getState()
        axes = filterAxisData(axes)

        #Button 1
        if buttons[0] == 1:
            print "Activating IR LEDs"
            runCommand('iron')
            LEDs_on = True

        #Button 2
        if buttons[1] == 1:
            print "Shutting off IR LEDs"
            runCommand('iroff')
            LEDs_on = False

        #Button 4
        if buttons[2] == 1:
            runCommand('goto 720') #Switch to 720p resolution (REALLY SLOW!)

        #Button 3
        if buttons[3] == 1:
            runCommand('goto 320') #Switch to 320 x 240 (much better!)

        #Start Button
        if buttons[9] == 1:
            runCommand('stop') #Stop all movement before exiting the program
            break

        #LB Button (This option works as a hold, rather than a toggle (one must hold down LB to see the mask))
        if buttons[4] == 1:
            wantMask = True #Show the user the movement mask
        else:
            wantMask = False #Show the user the image

        #LT Button (push this to reset the motion detection system & silence alarms)
        if buttons[6] == 1:
            MotionChecker.getResetBG()

        #Back button (If this button has been pressed, hide the window and set it to 320p)
        if buttons[8] == 1 and not ignoreHide:

            if showFeed: #If we're showing the feed, hide it
                showFeed = False #Hide feed if desired
                cv2.destroyAllWindows()
                runCommand('goto 320')
            
            else: #If we're not showing the feed, show it
                showFeed = True

            ignoreHide = True #We've pushed this button once, so ignore it from now on

        elif buttons[8] == 0:
            ignoreHide = False #Since we're not pushing the button, there's no need to debounce

        
        
        #print axes
        interpretJoystickData(axes)

        #Only display the feed if we asked to
        if showFeed:
            img = getIMG() #Get an image from the camera
            if not moving:
                img = MotionChecker.processDifference(img, wantMask = wantMask)
                
            else:
                #Disable the motion reading when the camera is moving
                cv2.putText(img, "Motion Reading: (Camera Moving)", (0, len(img) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            #Tell the user that the LEDs are on
            if LEDs_on == True:
                cv2.putText(img, "IR LEDs - ON", (0, len(img) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

            #Tell the user that the LEDs are off
            elif LEDs_on == False:
                cv2.putText(img, "IR LEDs - OFF", (0, len(img) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
                
            cv2.imshow('Camera Feed', img) #Show the image

        #If this sum is more than 0, the camera is moving (it takes the sum of the absolute value of the joystick data)
        #This has to go after the bit where we show images, because of the movement of the camera (it shakes a little when it stops)
        if sum([sum([abs(y) for y in x]) for x in axes]) > 0:
            moving = True

        elif moving == True:
            moving = False
            sleep(0.5) #Wait a bit before resetting the background
            MotionChecker.getResetBG()
            
        #Find out if we've pressed ESC
        if cv2.waitKey(20) == 27:
            break

    cv2.destroyAllWindows() #Get rid of all windows
