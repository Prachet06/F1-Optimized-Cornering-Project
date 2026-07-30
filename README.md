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

## 2.6. Collected Dataset Summary

Data was recorded across **25 separate driving sessions**, producing a collated dataset of **255 laps**.

The complete collection contains:

| Data component | Amount collected |
|---|---:|
| Recording sessions | 25 |
| Laps with a recorded Sector 1 time | 255 |
| Braking screenshots | 460 |
| Throttle screenshots | 459 |
| Total screenshots | 919 |

Each lap-level record contains:

- its overall recorded lap number;
- its Sector 1 time;
- any recorded incident label;
- the file paths of its braking screenshots;
- the file paths of its throttle screenshots; and
- any available brake–throttle delta measurements.

Brake–throttle delta recording was introduced after the first five sessions. Sessions 1–5 therefore contain Sector 1 times and screenshots but do not contain delta measurements.

This section describes the complete collected dataset before any eligibility filtering. The following section explains which laps were retained for modelling and how their performance labels were assigned.

# 3. Lap Eligibility and Labelling Rules

Not every recorded lap was suitable for training and evaluating the final models. Before assigning performance labels, a set of eligibility rules was applied to remove incident laps, unusually slow sectors and laps with incomplete or inconsistent screenshot sequences.

The full filtering and labelling process is documented in [`data_analysis.ipynb`](Code/notebooks/data_analysis.ipynb).

## 3.1. Original Five-Class Objective

The original aim of the project was to classify laps into five categories:

1. **Optimal**
2. **Standard**
3. **Sub-standard**
4. **Crash-causing**
5. **Track-limits-violating**

The collection script was designed with this objective in mind. After completing a lap, controller inputs could be used to mark its most recent braking and throttle screenshots as having contributed to either a crash or a track-limits violation.

However, the five-class objective proved too ambitious for the amount and structure of the data collected. Of the 255 recorded laps, only:

- **13 laps** were labelled as involving a crash; and
- **39 laps** were labelled as involving a track-limits violation.

These classes were substantially smaller than the ordinary-lap dataset. Their screenshots were also recorded differently: when an incident was marked, the script retained only the final braking and throttle inputs believed to have contributed to the incident rather than a complete two-brake and two-throttle sequence.

Training crash and track-limits classifiers using these small and structurally different groups would have produced unreliable comparisons. The final modelling objective was therefore narrowed to three performance classes:

- **Optimal**
- **Standard**
- **Sub-standard**

Crash and track-limits laps were retained in the raw dataset as records of the collection process but excluded from model training and evaluation.

## 3.2. Eligibility Rules

A recorded lap was considered eligible for performance labelling only when it satisfied all four of the following conditions:

1. **No recorded incident**  
   The lap could not be labelled as involving a crash or track-limits violation.

2. **Sector 1 time below 30,000 ms**  
   Laps with Sector-1 taking 30 seconds or longer were treated as unusually slow observations that were not representative of an ordinary Sector 1 attempt.

3. **Exactly two braking screenshots**  
   Each eligible lap had to contain the same number of braking images.

4. **Exactly two throttle screenshots**  
   Each eligible lap also had to contain the same number of throttle images.

The image-count requirements created a consistent four-image structure for every eligible lap:

- two braking screenshots; and
- two throttle screenshots.

These rules are specific to the dataset and collection method used in this project. They do not imply that every valid lap of Albert Park must contain exactly two braking or throttle applications. Instead, they remove laps affected by missed captures, additional trigger presses or incident-specific recording behaviour.

## 3.3. Filtering Outcome

The eligibility rules reduced the dataset from **255 recorded laps to 197 eligible laps**.

The table below shows the filtering process in the order in which the rules were applied:

| Filtering stage | Laps removed at this stage | Laps remaining |
|---|---:|---:|
| Initial recorded dataset | — | 255 |
| Remove crashes and track-limits violations | 52 | 203 |
| Remove Sector 1 times of 30,000 ms or longer | 1 | 202 |
| Require exactly two braking screenshots | 2 | 200 |
| Require exactly two throttle screenshots | 3 | 197 |

Because the rules were applied sequentially, each excluded lap is counted at the first rule it failed. A lap that failed more than one condition is therefore not counted multiple times in the table.

The final 197 eligible laps contain **788 modelling images**, consisting of two braking and two throttle screenshots per lap.

Of these 197 laps:

- **169 laps** contain two complete brake–throttle delta measurements; and
- **28 laps** do not contain delta data because they were recorded during Sessions 1–5.

All 197 laps could be used by the image model, while only the 169 laps with complete delta measurements could be used by the delta model and the final fused pipeline.

## 3.4. Quantile-Based Performance Labels

The three performance classes were defined using the distribution of Sector 1 times among the **197 eligible laps**.

The first and third quartiles were:

- **First quartile (Q1): 28,103 ms**
- **Third quartile (Q3): 28,569 ms**

The following rules were then applied:

| Performance class | Sector 1 time rule | Number of laps |
|---|---|---:|
| **Optimal** | `Sector 1 time <= 28,103 ms` | 50 |
| **Standard** | `28,103 ms < Sector 1 time < 28,569 ms` | 97 |
| **Sub-standard** | `Sector 1 time >= 28,569 ms` | 50 |

This assigns approximately:

- the fastest quarter of eligible laps to the **Optimal** class;
- the middle half to the **Standard** class; and
- the slowest quarter to the **Sub-standard** class.

Using quartiles avoided selecting arbitrary time boundaries and produced two equally sized extreme-performance classes, with the larger standard class representing the centre of the observed performance distribution.

## 3.5. Interpretation of the Labels

The labels describe performance **relative to the dataset collected for this project**.

An **Optimal** label means that a lap belongs to the fastest quarter of the eligible recorded observations. It does not mean that the lap represents a theoretically perfect racing line, a professional Formula 1 lap or the fastest possible Sector 1 time at Albert Park.

Similarly, **Sub-standard** refers to the slowest quarter of this dataset rather than an objectively poor lap under every possible driving condition.

The labels are derived from Sector 1 time, which is the outcome the models attempt to predict from braking screenshots, throttle screenshots and brake–throttle delta measurements. These recorded inputs are expected to contain useful information about performance, but they do not capture every factor that may affect the sector time, such as steering input, racing line or corner-entry speed.

# 4 Models

will def need to add a latex cnn diagram like my capstone here

Should also add plots across the readme, like the sector 1 times across the board etc.

## CNN

## Delta Logistic Regression Model

## Fusion Model

# 5 Results

# 6 Limitations
- SESSION 20 onwards, the sponsors on the wall are from qatar airways not louis vuitton, so there is a stark difference in colour but that is the extent of the difference.
- All sessions do not have the same amount of laps.
- All sessions do not have all classes of laps.
- The difference between the sub-standard and standard lap may be more than the difference between an optimal and a standard lap.
- Sample size is not large enough due to the nature of data collection.
- There might be other reasons as to why the sector times were not fast consistent which do not rely on braking, acceleration, and the time between the both. One of them could be related to the movement of the steering wheel.
- Perhaps mention that not all kinds of telemetry data was avalaible to be extracted, otherwise geospatial lap data might have been more useful than visual data. Also the extent at which the pedals are pressed could have been useful.

# 7 Reproducibility

# 8 Miscellaneous

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
