# 1 F1-Optimized-Cornering-Project
The aim of this project is to combine visual and numerical inputs to model corner-taking decisions and their impact on lap-time performance in Formula 1. The scope of this project is limited to sector-1 of the Australian track: Albert Park, but with enough time and data this project could also cover the whole track and other tracks on the Formula 1 calendar as well.

# 2 Data Collection
The dataset used in this project was collected specifically for this investigation rather than obtained from an existing public dataset. Data was recorded using the video game *EA SPORTS F1 25* at the Albert Park Circuit in Melbourne, Australia.

*F1 25* includes five circuits recreated using full-track LiDAR scans: Bahrain, Miami, Melbourne, Suzuka and Imola. EA states that millions of scanned data points were used to reproduce features such as surface bumps and elevation changes. This made the LiDAR-scanned Albert Park circuit a suitable virtual environment for collecting spatially meaningful braking- and throttle-point screenshots.

Further information about the LiDAR-scanned circuits is available on the [official EA F1 25 circuits page](https://www.ea.com/games/f1/f1-25/features/circuits). A more detailed description of how LiDAR data can be transformed into in-game track geometry is provided in [The Future 3D's overview of F1 25 circuit scanning](https://www.thefuture3d.com/blog/f1-25-game-lidar-stadium-track-scanning/).

The collection process produced three main types of data:

1. Screenshots showing the car's position when the brakes were applied.
2. Screenshots showing the car's position when the throttle was applied.
3. Numerical information, including the number of times the brakes and throttles were applied in sector 1, Sector 1 times, and the elapsed time between selected braking and throttle inputs.

Recording the data myself allowed the images, controller inputs and lap-performance measurements to be associated at the individual-lap level.


## 2.1 Track: Albert Park, Melbourne, Australia
![Albert Park Circuit with Sector 1 highlighted](Data/readme-images/Australia_Circuit.avif)

To reduce variation caused by parts of the circuit unrelated to the braking and throttle points being studied, the project focuses exclusively on **Sector 1**, highlighted in red above.

Sector 1 contains five turns but generally requires only two or three major braking events. Some of its corners can be taken without heavy braking, depending on the driver's speed and racing line. This made the sector suitable for the project: it is short enough to produce a relatively controlled dataset while still containing meaningful differences in braking position, throttle application and overall sector performance.

Restricting the analysis to one sector also helped reduce the influence of factors such as mistakes made elsewhere in the lap, and differences in performance across unrelated corner types.

## 2.2. Controlled Recording Conditions

To make the recording sessions as comparable as possible, all controllable in-game settings were kept consistent throughout data collection. The same track and environmental conditions were used for every session, while vehicle damage and tyre degradation were disabled.

Disabling these systems prevented later laps from being affected by accumulated tyre wear or damage from earlier mistakes. Keeping the remaining conditions fixed also reduced variation caused by factors unrelated to the braking and throttle behaviour being investigated.

**These controls do not remove all variation between laps**, since sector performance still depends on factors such as steering inputs, racing line, braking position and throttle application. However, they reduce the likelihood that differences in Sector 1 time were primarily caused by changing weather, track conditions, vehicle damage or tyre degradation.

## 2.3 Screenshot and Brake–Throttle Delta Collection
I created `collect_screenshots_and_deltas.py` to automate the collection of gameplay screenshots and controller-input timing data.

During each recorded lap, the script:

- captures a screenshot when the brake trigger is pressed;
- captures a screenshot when the throttle trigger is pressed;
- counts the brake and throttle inputs made during the lap;
- measures the elapsed time between a braking input and the following throttle input;
- associates every screenshot with its recording session, lap number and input number;
- allows invalid laps to be deleted or marked as involving a crash or track-limits violation; and
- writes the recorded brake–throttle timing information to a session-specific CSV file.

The elapsed time between a braking input and the associated throttle input is referred to throughout this project as the **brake–throttle delta**. A shorter or longer delta may reflect differences in how the driver approaches, rotates through and exits a corner.

The script automatically creates a new session directory each time data collection begins, preventing previously recorded screenshots from being overwritten. Screenshots are stored separately in `brake` and `throttle` directories for each session.

## 2.4 Controller Button Guide
![Controller Button Guide](Data/readme-images/button-guide.jpeg)

The data-collection script responds to the following PS5 DualSense controller inputs:

| Input | Function |
|---|---|
| **Triangle** | Enables or disables recording for the current lap |
| **L2** | Captures a braking-point screenshot and records the braking time |
| **R2** | Captures a throttle-point screenshot and calculates the brake–throttle delta when applicable |
| **D-pad Up** | Deletes the most recently recorded lap |
| **D-pad Left** | Marks the previous lap as involving a crash |
| **D-pad Right** | Marks the previous lap as involving a track-limits violation |
| **Share** | Stops the program and saves the session's delta data |

The script also displays large coloured terminal messages when recording is enabled or disabled. It was designed to run on a second monitor, allowing the recording state to be recognised through peripheral vision while driving.

> **Note:** The collection script currently depends on the `pydualsense` library and was designed specifically for a PS5 DualSense controller.

## 2.5. Sector-Time Extraction and Data Association

The screenshot-collection script does not directly obtain official sector times from the game. Instead, I used the [Pits n' Giggles F1 Telemetry Companion](https://github.com/ashwin-nat/pits-n-giggles) to export lap-history telemetry from *F1 25*.

The exported JSON files contain the Sector 1 time for each completed lap. These times were later associated with:

- the lap's braking screenshots;
- the lap's throttle screenshots;
- any recorded brake–throttle deltas; and
- incident information such as crashes or track-limits violations.

The `data_collate.py` script combines these sources into a single lap-level dataset while retaining the file paths of all screenshots associated with each lap.

Brake–throttle delta recording was introduced after the first five sessions. Consequently, sessions 1–5 contain screenshots and sector-time information but do not contain delta measurements.

# 3 Lap Eligibility and Labelling Rules

608 total references
- 103 incident images
- 13 images from irregular 2+2 input laps
- 4 images from the lap exceeding 30 seconds

= 488 CNN images

# Limitations
- SESSION 20 onwards, the sponsors on the wall are from qatar airways not louis vuitton, so there is a stark difference in colour but that is the extent of the difference.
- All sessions do not have the same amount of laps.
- All sessions do not have all classes of laps.
- The difference between the sub-standard and standard lap may be more than the difference between an optimal and a standard lap.
- Sample size is not large enough due to the nature of data collection.
- There might be other reasons as to why the sector times were not fast consistent which do not rely on braking, acceleration, and the time between the both. One of them could be related to the movement of the steering wheel.


# Miscellaneous

## Repository File Structure 

```bash
root
├── Code 
│   ├── notebooks
│   │   ├── data_analysis.ipynb
│   │   ├── final_modelling.ipynb
│   │   ├── rebuild_manifests_and_splits.ipynb
│   │   └── sector_time_extraction.ipynb
│   ├── scripts
│   │   ├── collect_screenshots_and_deltas.py
│   │   └── collate_session_data.py
│   └── README.md
├── Data
│   ├── brake-throttle-delta-data
│   ├── collated-data
│   ├── image-data
│   │   ├── session-1
│   │   │   ├── brake 
│   │   │   └── throttle
│   │   ├── session-2
│   │   │   ├── brake 
│   │   │   └── throttle
│   │   ...
│   │   ...
│   ├── manifests
│   │   ├── image-manifest.csv
│   │   ├── lap-manifest.csv
│   │   ├── image-manifest-with-split.csv
│   │   └── lap-manifest-with-split.csv
│   ├── readme-images
│   ├── results
│   │   ├── loso
│   │   ├── test
│   │   ├── validation
│   ├── sector-time-data
│   └── README.md
├── Models
└── README.md
```
