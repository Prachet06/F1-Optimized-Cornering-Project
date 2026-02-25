# Code

## Purpose of auto_screenshot.py
Used to automate the process of capturing image data that the CNN trains on.

This is done by detecting each time when I hit the brakes ingame i.e. press or press and hold the L2 button on the PS5 DualSense controller. When this is detected, a screenshot of the monitor (that is specified in the script) which is being used for displaying the game is taken. 

write about r2

write about dpadup and how you avoided the issue to delete the second most recent lap's data incorrectly.

This code is written under the assumption that it will run on a second monitor while data is being recorded. This is why there are lines of coloured string printed after enabling or disabling screenshotting as it allows the user to deduce whether screenshotting is enabled or disabled using the colour visible in their peripheral vision. 

## Purpose of CNN.py

## Purpose of data_collate.py
This script is supposed to collate all numerical along with the addresses of all the images associated with each lap into one file. It is designed to run after all the data has been recorded.

## Purpose of Sector Time Extraction Notebook.ipynb

This notebook is a detailed walkthrough of my thinking when I first extracted the lap sector-1 times from the json files that the Pits n Giggles app produces. It also was a chance for me to practice literate programming.