
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel

from ui.elements.generic_button import GenericButton
from ui.elements.generic_label import GenericLabel
from ui.elements.record_button import RecordButton
from ui.elements.debug_widget import DebugWidget

from ui.widgets.activity_indicator_widget import ActivityIndicatorWidget
from ui.widgets.battery_widget import BatteryWidget

from ui.windows.popup_window_drone_controls import PopupWindowDroneControls
from ui.windows.popup_window_drone_debug import PopupWindowDroneDebug

from communication.dji_api import Drone

MAIN_STATUS_BAR_WIDGET_WIDTH = 1920
MAIN_STATUS_BAR_WIDGET_HEIGHT = 75

class StatusBarWidget(QFrame):
    """Status bar widget for the main window.
    
    Contains the connect button, drone connectivity indicator, battery status, wifi status
    and buttons to open popup windows for debug and controls."""

    def __init__(self, parent, drone: Drone, startVideoCallback):
        super().__init__(parent)

        self.drone = drone

        # Create horizontal layout and set spacing/margins
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setContentsMargins(10, 10, 10, 10)
        horizontalLayout.setSpacing(10)

        # Add connect to drone button
        self.buttonDroneConnect = GenericButton(self, "Connect to the Drone")
        self.buttonDroneConnect.clicked.connect(self.DroneConnectButtonClicked)
        horizontalLayout.addWidget(self.buttonDroneConnect)

        # Add activity dot
        horizontalLayout.addWidget(GenericLabel(self, "Drone"))   
        self.activityIndicator = ActivityIndicatorWidget(self, 3000)                                                                                                                           
        horizontalLayout.addWidget(self.activityIndicator)

        # Drone controls button to open popup window - to control drone
        self.buttonDroneControls = GenericButton(self, "Drone Controls")
        self.buttonDroneControls.clicked.connect(self.droneControlsButtonClicked)
        horizontalLayout.addWidget(self.buttonDroneControls)

        self.droneControlsPopup = PopupWindowDroneControls(self, drone)

        # Drone debug button to open popup window - to debug the drone
        self.buttonDroneDebug = GenericButton(self, "Drone Debug")
        self.buttonDroneDebug.clicked.connect(self.droneDebugButtonClicked)
        horizontalLayout.addWidget(self.buttonDroneDebug)

        self.droneDebugPopup = PopupWindowDroneDebug(self, drone)

        # Add start stream video
        self.buttonDroneStartStream = GenericButton(self, "Start Stream")
        self.buttonDroneStartStream.clicked.connect(startVideoCallback)
        horizontalLayout.addWidget(self.buttonDroneStartStream)

        # Add record button
        horizontalLayout.addWidget(RecordButton(self))

        # Add temperature
        # Current temp
        self.current_temp = DebugWidget(self, "Temp")
        horizontalLayout.addWidget(self.current_temp)

        # Add battery indicator
        self.battery = BatteryWidget(self)
        horizontalLayout.addWidget(self.battery)

        self.setLayout(horizontalLayout)
        
        self.setMaximumHeight(MAIN_STATUS_BAR_WIDGET_HEIGHT)

    # Default size
    def sizeHint(self) -> QSize:
        return QSize(MAIN_STATUS_BAR_WIDGET_WIDTH, MAIN_STATUS_BAR_WIDGET_HEIGHT)

    def droneControlsButtonClicked(self):
        self.droneControlsPopup.show()

    def droneDebugButtonClicked(self):
        self.droneDebugPopup.show()

    def DroneConnectButtonClicked(self):
        self.drone.connect()
        print("Connecting to the drone")
