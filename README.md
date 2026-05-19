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
sudo ufw allow 8890/udp                                                                                                                           
sudo ufw allow 11111/udp



# TODO
Create button to reset the movement