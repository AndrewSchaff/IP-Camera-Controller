inputs = [] #Somewhere to store the current status (not really necessary)

pygame = None

buttonIDs = {0 : "1",
	     1 : "2",
             2 : "3",
             3 : "4",
             4 : "LB",
             5 : "RB",
             6 : "LT",
             7 : "RT",
             8 : "Back",
             9 : "Start",
             10 : "L Joystick",
             11 : "R Joystick",
             }

"""
Axis Configuration
0 - Left Stick L/R (-1 to +1)
1 - Left Stick U/D (-1 to +1)
2 - Right Stick L/R (-1 to +1)
3 - Right Stick U/D (-1 to +1)

Hat Configuration
(X/Y (-1 to +1), U/D (-1 to +1))
"""

#Start up pygame if necessary
def startPygame():
    global pygame
    import pygame

    #Initialize all libraries and the joystick
    try:
        pygame.init()
        pygame.joystick.init()
        
    except:
        print "Error: PyGame failed to intialize!"

#Stop pygame if necessary
def stopPygame():
    pygame.quit()
    
#Start the joystick
def startJoystick():
    print "Initializing gamepad..."
    global joystick
    
    try:
        joystick = pygame.joystick.Joystick(0)

    except:
        print "Error: Joystick not found!"

    try:
        joystick.init()
        print "Gamepad ready!"
        
    except:
        print "Error: Joystick failed to initialize!"

    
#Duplicate of the Arduino map function (borrowed from here: https://mail.python.org/pipermail/tutor/2013-August/097291.html)
def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
#Convert joystick value to a hex value (-1 to 1 mapped to 0 to F)
def toHex(num):
        mapped = int(map(float(num), -1.0, 1.0, 0, 15)) #Map value between 0 and 15
        return ["0", "1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"][mapped] #Convert to hex

#Get the state of all buttons/hats/sticks on the gamepad
def getState():
    global inputs
    z = pygame.event.get()
    
    #axes = [toHex(joystick.get_axis(0)), toHex(joystick.get_axis(1)), toHex(joystick.get_axis(2)), toHex(joystick.get_axis(3)), toHex(joystick.get_hat(0)[0]), toHex(joystick.get_hat(0)[1])]
    axes = [joystick.get_axis(0), joystick.get_axis(1), joystick.get_axis(2), joystick.get_axis(3)]
    hat = joystick.get_hat(0)
    buttons = [joystick.get_button(button) for button in range(12)]
        
    return axes, hat, buttons

#Automatically start the necessary functions (so the user doesn't have to)
startPygame()
startJoystick()
"""
while True:
    pygame.event.get()
    print "".join([str(joystick.get_button(x)) for x in range(12)])
"""
