# Safety Drone Application

Autonomous drone patrol system for warehouses and factories. It flies a work area on a set path, spots hazards like spills and misplaced tools with a live YOLO model, drops a pin on a map for each one, and logs the class, time, and coordinates so they can be cleaned up before the next shift.



## Demo

**Path sequence** - the drone autonomously sweeps the work area, detecting hazards as it flies.




https://github.com/user-attachments/assets/9a0be8c9-c1d0-40e0-9abf-f79a63bfcee9


**Inspection sequence** - once something is detected, the drone circles it for a closer, more reliable look.

https://github.com/user-attachments/assets/0e33fec8-c347-420e-bb87-77b9c19626bb



## How it works

Two automated flight sequences drive the drone: a path sequence that covers the entire work area, and an inspection sequence that flies an arc around a detected object to confirm it from multiple angles. Since the Tello EDU has no GPS, position is tracked with dead reckoning from every command sent to the drone.

For detection, we trained and compared 6 models across two architectures on a custom dataset of 10,504 images built from Objects365 and a spill-detection dataset, covering 6 hazard classes: hammer, screwdriver, knife, tape, scissors, and spill. RT-DETR Large came out on top for accuracy, but YOLO11 Medium is what actually runs on the drone, since inference needed to run in real time without a GPU.

| Model | Train mAP50 | Val mAP50 | Test mAP50 |
|---|---|---|---|
| YOLOv5 Nano (Transfer) | 0.74 | 0.33 | 0.36 |
| YOLO11 Nano | 0.53 | 0.26 | 0.26 |
| YOLO11 Nano (Transfer) | 0.73 | 0.35 | 0.37 |
| YOLO11 Small (Transfer) | 0.71 | 0.37 | 0.39 |
| YOLO11 Medium (Transfer) | 0.70 | 0.38 | 0.42 |
| RT-DETR Large (Transfer) | 0.88 | 0.40 | 0.45 |

## Features

- Autonomous patrol and inspection flight sequences, launchable with a single button
- Live object detection overlaid on the video feed
- Map of the drone's position and every detected hazard
- Structured hazard log: class, timestamp, coordinates
- Manual flight controls and a debug panel for live telemetry
- Custom, publicly available dataset (10K+ images, 6 classes)

Full report: [resources/report.pdf](resources/report.pdf)

# Project structure
- Application source code can be found in `src/` folder
- Jupyter notebooks containing training can be found in `/notebooks` folder

# Prerequisites

Make sure you have the following installed:

- Python >= 3.11
- Pip  
- UV (recommended package manager)

## Install UV

```
pip install uv
```

## Install dependencies
```
uv sync
```

## Install models
Install the models from huggingface and move them into the `models` folder
```
https://huggingface.co/ondralol/deep-learning-cnn/tree/main
```

## Run the main app
```
uv run src/main.py
```

## Run jupyter notebooks
Run 
```
uv sync
```
Install kernel
```
uv run python -m ipykernel install --user --name safety-drone-app --display-name "safety-drone-app"
```
Run the notebook
```
uv run jupyter notebook
```
and select the "safety-drone-app" kernel \
Note: If running inside sagemaker, you need to copy `pyproject.toml` first

# Streaming
```
sudo ufw allow 8890/udp
sudo ufw allow 11111/udp
```


Built by [Hector Freard Ruiz](https://github.com/Hectorfr), [Florian Thollot](https://github.com/Flo822), and [Ondrej Duba](https://github.com/Ondralol).
