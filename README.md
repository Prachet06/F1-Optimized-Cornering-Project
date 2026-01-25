# F1-Optimized-Cornering-Project
**Track:** Albert Park, Melbourne, Australia
![Controller Button Guide](Data/shiny-app-images/Australia_Circuit.avif)
For this project, in an effort to reduce confounding factors that might have had an impact on the lap time apart from the braking and throttle points, the data recorded is only of Sector 1 of the track (the part highlighted in red). The first sector has 5 turns and usually a pilot does not need to break more than three or even two times as the other corners don't necessarily require the driver to slow down or stop accelerating. This phenomena is more commonly referred to as 'taking a corner flat out' in the sport.


## Shiny App

## Controller Button Guide
![Controller Button Guide](Data/readme-images/button-guide.jpeg)
**Note**: The auto-screenshotting program only works for the PS5 DualSense controller.

### Repository File Structure 

```bash
root
├── Code 
│   ├── Sector Time Extraction Notebook.ipynb
│   └── auto_screenshot.py
├── Data
│   ├── auditory-feedback-data
│   ├── image-data
│   │   ├── session-1
│   │   │   ├── brake 
│   │   │   └── throttle
│   │   ├── session-2
│   │   │   ├── brake 
│   │   │   └── throttle
│   │   ...
│   │   ...
│   │   ...
│   ├── readme-images
│   ├── sector-time-data
│   └── shiny-app-images
├── Shiny App
│   ├── app.py
│   └── styles.css
└── README.md
```
