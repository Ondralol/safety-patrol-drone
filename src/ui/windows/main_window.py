from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer

from ui.widgets.live_feed_widget import LiveFeedWidget
from ui.widgets.map_widget import MapWidget
from ui.widgets.object_log_widget import ObjectLogWidget
from ui.widgets.status_bar_widget import StatusBarWidget

from utils.video_worker import VideoWorker, MODEL_TYPE

from communication.dji_api import Drone

POLL_TIME_MS = 2500

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Safety Drone Application")
        self.resize(1920, 1080)

        self.drone = Drone()

        self.buildUI()


        # Timer to fetch drone data
        self.poll_timer = QTimer()
        self.poll_timer.setInterval(POLL_TIME_MS)
        self.poll_timer.timeout.connect(self._poll)
        self.poll_timer.start()


    def buildUI(self):

        # The main layout for the whole page
        mainVerticalLayout = QVBoxLayout()

        # Add status bar
        self.statusBar = StatusBarWidget(
            self,
            self.drone,
            self.startVideo,
            startRecordingCallback=self.startRecording,
            stopRecordingCallback=self.stopRecording,
        )
        mainVerticalLayout.addWidget(self.statusBar)

        # Create horizontal layout
        horizontalLayout = QHBoxLayout()

        # Add live feed
        self.live_feed = LiveFeedWidget()
        horizontalLayout.addWidget(self.live_feed, stretch=2)

        # Create vertical layout for map and log
        verticalLayoutMapAndLog = QVBoxLayout()

        # Add map
        self.map = MapWidget()
        verticalLayoutMapAndLog.addWidget(self.map)
        
        # Add log
        self.object_log = ObjectLogWidget()
        verticalLayoutMapAndLog.addWidget(self.object_log)

        # Add layouts
        horizontalLayout.addLayout(verticalLayoutMapAndLog, stretch=1)
        mainVerticalLayout.addLayout(horizontalLayout)

        root = QWidget()
        root.setLayout(mainVerticalLayout)
        self.setCentralWidget(root)

    def _poll(self):
        """Fetch drone data, such as battery, position, etc."""
        
        battery = self.drone.getBattery()
        if battery is not None:
            self.statusBar.battery.setLevel(battery)
            self.statusBar.activityIndicator.activityDetected()
        
        cur_pos = self.drone.getMissionpadXYZ()
        if cur_pos is not None:
            self.statusBar.droneDebugPopup.current_pos.set_value(f"({cur_pos[0]}, {cur_pos[1]}, {cur_pos[2]})")

        height = self.drone.getHeight()
        if height is not None:
            self.statusBar.droneDebugPopup.current_height.set_value(height, "cm")

        
        temp = self.drone.getTemp()
        if temp is not None:
            self.statusBar.current_temp.set_value(temp, "deg")

        tof = self.drone.getDistanceTof()
        if tof is not None:
            self.statusBar.droneDebugPopup.current_distance_tof.set_value(tof, "cm")

        self.map.update_position(self.drone.position) # TODO more often perhaps? after every move directly emit

        # Send keep alive
        self.drone.keepAlive()

    def startVideo(self):
      self.drone.startStream()
      self.video_worker = VideoWorker(self.drone, MODEL_TYPE.YOLO11_MEDIUM)
      self.video_worker.frame_ready.connect(self.live_feed.updateFrame)
      self.video_worker.target_found.connect(lambda label, pos: self.map.update_targets([pos]))
      self.video_worker.target_found.connect(lambda label, pos: self.object_log.addEntry(label, pos))
      self.video_worker.start()

    def startRecording(self):
        recording_path = self.live_feed.startRecording()
        print(f"Recording started: {recording_path}")

    def stopRecording(self):
        recording_path = self.live_feed.stopRecording()
        print(f"Recording saved: {recording_path}")

    def closeEvent(self, event):
        #  Stop recording and stop the thread
        self.poll_timer.stop()                                                                                                                        
        if hasattr(self, 'video_worker'):                                                                                                             
            self.video_worker.stop()                                                                                                                  
        self.drone.drone.end() 
        super().closeEvent(event)
