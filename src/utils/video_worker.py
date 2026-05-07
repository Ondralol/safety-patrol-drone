from PySide6.QtCore import QThread, Signal
from enum import StrEnum
import numpy as np
import math


class MODEL_TYPE(StrEnum):
    YOLO11_NANO = "yolo11n-pretrained.pt"
    YOLO11_SMALL = "yolo11s-pretrained.pt"
    YOLO11_MEDIUM = "yolo11m-pretrained.pt"
    RT_DETR_LARGE = "rtdetrl-pretrained.pt"


MODEL_PATH_PREFIX = "models/"             

INFERENCE_EVERY_N = 1 # Only run inference every nth frame
CONFIRM_INFERENCE_M = 3 # Only confirm inference after n consetutive inferences 
BOX_EXPIRE_FRAMES = 4 # Old boxes expire after this number of frames
CONFIDENCE_RATE = 0.40

class VideoWorker(QThread):                                                                                                                                            
    frame_ready = Signal(np.ndarray)
    
    target_found = Signal(str, tuple)
                                                                                                                                                                        
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

    def _estimate_target_position(self, box, frame_shape):
        # Get box position
        x1, y1, x2, y2 = box.xyxy[0].tolist()

        # Get frame dimensions
        frame_height, frame_width = frame_shape[0], frame_shape[1]
        if frame_width <= 0 or frame_height <= 0:
            return None

        # Horizontal bearing
        center_x = (x1 + x2) * 0.5
        h_offset = (center_x - frame_width * 0.5) / frame_width
        bearing_offset_deg = h_offset * 82.6  # horizontal FOV of the tello edu camera
        bearing_rad = math.radians(self.drone.position.angle + bearing_offset_deg)

        # Distance from elevation angle + drone height
        center_y = (y1 + y2) * 0.5
        v_offset = (center_y - frame_height * 0.5) / frame_height  # positive = below center
        depression_rad = math.radians(v_offset * 66.5) # vertical FOV

        if depression_rad <= 0:
            return None  # object at or above horizon, can't estimate ground distance

        ground_distance = self.drone.position.z / math.tan(depression_rad)

        # Project x, y in world space
        obj_x = self.drone.position.x + ground_distance * math.cos(bearing_rad)
        obj_y = self.drone.position.y + ground_distance * math.sin(bearing_rad)

        return (obj_x, obj_y)

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
                results = self.model(frame, verbose=False, conf=CONFIDENCE_RATE,
                                     classes=list(self.model.names.keys()))
                last_boxes = results[0]
                last_inference_frame = frame_count

                if len(results[0].boxes) > 0:
                    consecutive_count += 1
                else:
                    consecutive_count = 0

                # TODO: Only confirm inference after its been on M consecutive frames
                if consecutive_count >= CONFIRM_INFERENCE_M:

                    # TODO: Automatic inspection
                    # self.on_detection(results[0])
                    
                    # Get more precise target position
                    for box in results[0].boxes:
                        label = results[0].names[int(box.cls[0])]
                        target_position = self._estimate_target_position(box, frame.shape)
                        if target_position is not None:
                            self.target_found.emit(label, target_position)

            if last_boxes is not None and (frame_count - last_inference_frame) < BOX_EXPIRE_FRAMES:
                try:
                    display_frame = last_boxes.plot(img=frame.copy())
                except Exception as e:
                    print(f"plot() failed: {type(e).__name__}: {e}")
                    import traceback; traceback.print_exc()
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
