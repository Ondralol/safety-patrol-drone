from PySide6.QtCore import QThread, Signal                                                                                                                               
from ultralytics import YOLO                                                                                                                                             
from enum import StrEnum
import numpy as np


class MODEL_TYPE(StrEnum):
    YOLO11_NANO = "yolo11n-pretrained.pt"
    YOLO11_SMALL = "yolo11s-pretrained.pt"
    YOLO11_MEDIUM = "yolo11m-pretrained.pt"
    RT_DETR_LARGE = "rtdetrl-pretrained.pt"


MODEL_PATH_PREFIX = "models/"             


class VideoWorker(QThread):                                                                                                                                            
    frame_ready = Signal(np.ndarray)
                                                                                                                                                                        
    def __init__(self, drone, model_type: MODEL_TYPE):
        super().__init__()                                                                                                                                               
        self.drone = drone      
        self.model_type = model_type                                                                                                                                       
        self.model_loaded = False
        self.running = True
    
    def _loadModel(self):
        path = MODEL_PATH_PREFIX + self.model_type
        print(path)
        self.model = YOLO(path)
        self.model_loaded = True

    def run(self):
        """Read frame and let yolo process it."""
        
        if not self.model_loaded:
            self._loadModel()
        
        try:
            frame_read = self.drone.drone.get_frame_read()
        except:
            return
        
        while self.running:                                                                                                                                              
            frame = frame_read.frame                                                                                                                                   
            if frame is None:
                continue
            results = self.model(frame, verbose=False)                                                                                                                   
            annotated = results[0].plot()  # draws boxes + labels
            self.frame_ready.emit(annotated)    
            # Might neeed to add like a time sleep or something since
            # this runs in the loop and might poll the same frame multiple times
            # idk if that's an issue (probably not)                                                                                                                         
                                                                                                                                                                        
    def stop(self):                                                                                                                                                      
        self.running = False                                                                                                                                           
        self.wait()
