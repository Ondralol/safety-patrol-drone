# Safety Drone Applicaiton

A Python application using PySide6 for GUI and YOLO for object detection to find and map dangerous object in warehouses

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
Install the models from huggingface and move them into  the `models` folder
```
https://huggingface.co/ondralol/deep-learning-cnn/tree/main
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

