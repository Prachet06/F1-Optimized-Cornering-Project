# Code

## Purpose of auto_screenshot.py
Used to automate the process of capturing image data that the CNN trains on.

This is done by detecting each time when I hit the brakes ingame i.e. press or press and hold the L2 button on the PS5 DualSense controller. When this is detected, a screenshot of the monitor (that is specified in the script) which is being used for displaying the game is taken. 

This code is written under the assumption that it will run on a second monitor while data is being recorded. This is why there are lines of coloured string printed after enabling or disabling screenshotting as it allows the user to deduce whether screenshotting is enabled or disabled using the colour visible in their peripheral vision. 
