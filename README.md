# IP Camera Controller
A program that can be used to interface with a Kaicong IP Camera, allowing the user to watch the feed, operate the camera, and check for motion.  I wrote this program to enable me to watch for deliveries from the comfort of another room.  As such, it is equipped with a number of features of questionable necessity but undeniable 'fun-ness'.

## Quick Start
### How to use this program
1. Download and unzip the entirety of this repo to a directory of your choosing
2. Connect a game controller
3. Enter your login details in the fields in `Camera.py`
2. Run `Camera.py`
3. Set the camera window to stay on top of windows using something like [this](http://www.labnol.org/software/tutorials/keep-window-always-on-top/5213/)
4. Profit!

### Controls
 - Left Analog Stick - Look around
 - Left Trigger button - Reset background subtractor/silence motion alarms
 - Left Shoulder Button - Hold this down to see the motion in the frame
 - Button 1/Square - Turn on IR LEDs
 - Button 2/X - Turn off IR LEDs
 - Button 3/Cross - Go to 720p resolution (SLOW)
 - Button 4/Triangle - Go to 320 x 240 resolution (FASTER)
 - Back Button - Toggle window visibility
 - Start Button - Close the program

## Watching the feed
This program makes use of the camera's built-in web server to retrieve images.  It contacts the camera on Port 81, logs in with the provided details, and retrieves the latest image from `snapshot.cgi`.  It then converts these images to a format that `OpenCV` can use before displaying them.  By default, the program gets 320 x 240 images, but this can be changed to 720p if you want a closer look.

## Controlling the camera
The program uses the same control system as the camera's web interface, giving you near full control over the motion of the camera.  Pan and tilt are controlled by the joystick or hat switch of a game controller, with other features (controlling IR LEDs, etc.) controlled by the controller's buttons.  The controller/program interface uses `PyGame` and an interface script originally written for [this project] (https://github.com/QuickRecon/ScotchOARKit).

### What you can control
 - Camera Pan and Tilt
 - Activate/Deactivate IR LEDs
 - Change resolution

## Motion Detection
This program also uses `OpenCV`'s background subtractor to provide a motion alarm.  When a significant change is detected in the frame, a red banner with the words 'Movement Detected' will flash at the top of the screen while an audible tone is played.  This works based on a 'difference score': after the background subtractor mask is created, the number of white pixels counted.  More white pixels = more change.  This feature is still a little sensitive to small movements, so try to avoid pointing the camera at trees if you can.

There are a few basic controls for `MotionChecker.py`:
 - Left Shoulder Button: Hold this to show the motion mask (B/W image of all motion in frame)
 - Left Trigger Button: Reset background subtractor/silence alarms

## Program features
Every now and then, you may want to hide the camera feed window.  Toggling window visibility is down with the BACK button.  Push once to hide the window, and another time to show the window.

Alt-H2 Sources
 - Camera: https://www.amazon.com/Network-Infrared-Wireless-Camera-Detection/dp/B01E8QITFY/ref=sr_1_10?ie=UTF8&qid=1468330513
 - Alert Sound Effect: http://soundbible.com/1599-Store-Door-Chime.html
