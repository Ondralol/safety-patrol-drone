from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from ui.widgets.live_feed_widget import LiveFeedWidget
from ui.widgets.map_widget import MapWidget
from ui.widgets.object_log_widget import ObjectLogWidget
from ui.widgets.status_bar_widget import StatusBarWidget

from communication.dji_api import Drone


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Safety Drone Application")
        self.resize(1920, 1080)

        self.drone = Drone()

        self.buildUI()

    def buildUI(self):

        # The main layout for the whole page
        mainVerticalLayout = QVBoxLayout()

        # Add status bar
        self.statusBar = StatusBarWidget(self, self.drone)
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

    def closeEvent(self, event):
        # TODO: disconnect drone, stop recording
        super().closeEvent(event)
