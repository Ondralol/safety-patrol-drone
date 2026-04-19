# Safety Drone Applicaiton

A Python application using PySide6 for GUI and YOLO for object detection to find and map dangerous object in warehouses

# Prerequisites

Make sure you have the following installed:

- Python >= 3.10  
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

## Run the main app
```
uv run src/main.py
```

## Run jupyter notebooks
Install kernel
```
uv run python -m ipykernel install --user --name safety-drone-app --display-name "safety-drone-app"
```
Run notebook
```
uv run jupyter notebook
```
and select the "safety-drone-app" kernel

## Google colab setup
On google drive create folder
`deep-learning-cnn` and inside three subfolders: `data` and `models`. Inside the data folder, paste in the dataset (download it as YOLOv8 Pytorch from Roboflow). 


