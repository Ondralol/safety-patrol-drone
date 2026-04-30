from PySide6.QtCore import QThread, Signal                                                                                                                                                                                                                                                                          
from enum import StrEnum
import numpy as np


class MODEL_TYPE(StrEnum):
    YOLO11_NANO = "yolo11n-pretrained.pt"
    YOLO11_SMALL = "yolo11s-pretrained.pt"
    YOLO11_MEDIUM = "yolo11m-pretrained.pt"
    RT_DETR_LARGE = "rtdetrl-pretrained.pt"


MODEL_PATH_PREFIX = "models/"             

INFERENCE_EVERY_N = 1 # Only run inference every nth frame
CONFIRM_INFERENCE_M = 3 # Only confirm inference after n consetutive inferences 
BOX_EXPIRE_FRAMES = 3 # Old boxes expire after this number of frames
CONFIDENCE_RATE = 0.45

class VideoWorker(QThread):                                                                                                                                            
    frame_ready = Signal(np.ndarray)
    
    target_found = Signal() # TODO improve target localization, more granual steps
                                                                                                                                                                        
    def __init__(self, drone, model_type: MODEL_TYPE):
        super().__init__()                                                                                                                                               
        self.drone = drone      
        self.model_type = model_type                                                                                                                                       
        self.model_loaded = False
        self.running = True

        # If there is currently running inspection
        self.currently_running_inspection = False
    
    def _loadModel(self):
        from ultralytics import YOLO  
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
        
        last_boxes = None
        last_inference_frame = 0
        consecutive_count = 0
        frame_count = 0

        while self.running:                                                                                                                                              
            frame = frame_read.frame                                                                                                                                   
            if frame is None:
                continue

            if frame_count % INFERENCE_EVERY_N == 0:
                results = self.model(frame, verbose=False, conf=CONFIDENCE_RATE)                                                                                                                   
                last_boxes = results[0]
                last_inference_frame = frame_count

                # TODO Consecutive detection here

                # TODO Call inspection
                if len(results[0].boxes) > 0:                                                                                                                 
                    self.on_detection(results[0])

                    # TODO properly track where the target is on the map
                    self.target_found.emit()

            if last_boxes is not None and (frame_count - last_inference_frame) < BOX_EXPIRE_FRAMES:
                try:
                    display_frame = last_boxes.plot(img=frame.copy())
                except:
                    display_frame = frame
            else:
                display_frame = frame

            self.frame_ready.emit(display_frame)    
            # Might neeed to add like a time sleep or something since
            # this runs in the loop and might poll the same frame multiple times
            # idk if that's an issue (probably not)      

            frame_count += 1 
                                                                                                                               
    
    def on_detection(self, result):
        # If there isn't currently running inspection
        if not self.currently_running_inspection:
            self.currently_running_inspection = True
            self.drone.inspectObject(on_done = self._on_inspection_done)

    def _on_inspection_done(self):
      self.currently_running_inspection = False 

    def stop(self):                                                                                                                                                      
        self.running = False                                                                                                                                           
        if not self.wait(2000):
            self.terminate()
            self.wait()
