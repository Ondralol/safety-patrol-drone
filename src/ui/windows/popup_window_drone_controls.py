from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout

from communication.dji_api import Drone, DIRECTION, ROTATION_DIRECTION, SPEED
from ui.elements.title import Title
from ui.elements.generic_button import GenericButton
from ui.elements.dropdown import Dropdown
from ui.elements.spinbox import Spinbox


POPUP_WIDTH = 1000
POPUP_HEIGHT = 900

STYLE_SHEET_POPUP_DIALOG = """
    QDialog {
        background-color: #1e1e1e;
        border: 2px solid #444444;
        border-radius: 10px;
    }
"""


class PopupWindowDroneControls(QDialog):
    def __init__(self, parent, drone: Drone):
        super().__init__(parent)

        self.parent = parent
        self.drone = drone

        self.setWindowTitle("Drone controls")
        self.setStyleSheet(STYLE_SHEET_POPUP_DIALOG)
        self.setMinimumSize(QSize(POPUP_WIDTH, POPUP_HEIGHT))

        # Remove window frame for cleaner look
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # Allow non blocking behaviour
        self.setModal(False)

        # Main layout with proper margins
        self.mainLayoutVertical = QVBoxLayout()
        self.mainLayoutVertical.setContentsMargins(50, 50, 50, 50)
        self.mainLayoutVertical.setSpacing(10)
        
        self.mainLayoutVertical.addWidget(Title(self, "Main Controls"))
        self._buildMainControls()
        self.mainLayoutVertical.addWidget(Title(self, "Advanced Controls"))
        self._buildAdvancedControls()

        self.setLayout(self.mainLayoutVertical)

    def _buildMainControls(self):
        horizotalLayout = QHBoxLayout()
        
        # Takeoff
        self.buttonTakeoff = GenericButton(self, "Takeoff")
        self.buttonTakeoff.clicked.connect(self.drone.takeoff)
        horizotalLayout.addWidget(self.buttonTakeoff)

        # Land
        self.buttonLand = GenericButton(self, "Land")
        self.buttonLand.clicked.connect(self.drone.land)
        horizotalLayout.addWidget(self.buttonLand)

        # Emrgency
        self.buttonEmergency = GenericButton(self, "Emergency")
        self.buttonEmergency.clicked.connect(self.drone.emergency)
        horizotalLayout.addWidget(self.buttonEmergency)

        # Start Stream
        #self.buttonStartStream = GenericButton(self, "Start Stream")
        #self.buttonStartStream.clicked.connect(self.parent.parent.startVideo)
        #horizotalLayout.addWidget(self.buttonStartStream)

        # Automatic Sequence
        self.buttonAutomaticSequence = GenericButton(self, "Automatic Sequence")
        self.buttonAutomaticSequence.clicked.connect(self.drone.startSequence)
        horizotalLayout.addWidget(self.buttonAutomaticSequence)

        self.mainLayoutVertical.addLayout(horizotalLayout)

    def _buildAdvancedControls(self):
        self.mainLayoutVertical.addLayout(self._buildButtonPad())
        self.mainLayoutVertical.addLayout(self._buildMove())
        self.mainLayoutVertical.addLayout(self._buildRotate())
        self.mainLayoutVertical.addLayout(self.__buildMoveToXYZRelativeToCurrentPosition())
        self.mainLayoutVertical.addLayout(self._buildCircle())
        

    def _buildButtonPad(self):
        horizontalLayout = QHBoxLayout()
        self.buttonPad = GenericButton(self, "Enable mission pads")
        self.buttonPad.clicked.connect(self.drone.enableMissionPads)
        horizontalLayout.addWidget(self.buttonPad)
        horizontalLayout.addStretch(0)
        return horizontalLayout

    def _buildMove(self):
        horizontalLayout = QHBoxLayout()
        self.dropdownMove = Dropdown(self, "Direction", DIRECTION)
        self.spinboxMove = Spinbox(self, "Distance", " cm", 10, 500, 10, 1, 0)
        self.buttonMove = GenericButton(self, "Move")
        self.buttonMove.clicked.connect(lambda: self.drone.move(self.dropdownMove.getCurrentEnum(), self.spinboxMove.getValue()))

        horizontalLayout.addWidget(self.buttonMove)
        horizontalLayout.addWidget(self.dropdownMove)
        horizontalLayout.addWidget(self.spinboxMove)
        return horizontalLayout
    
    def _buildRotate(self):
        horizontalLayout = QHBoxLayout()
        self.dropdownRotate = Dropdown(self, "Direction", ROTATION_DIRECTION)
        self.spinboxRotate = Spinbox(self, "Angle", " deg", 10, 500, 10, 1, 0)
        self.buttonRotate = GenericButton(self, "Rotate")
        self.buttonRotate.clicked.connect(lambda: self.drone.rotate(self.dropdownRotate.getCurrentEnum(),
                                                                    self.spinboxRotate.getValue()))
        horizontalLayout.addWidget(self.buttonRotate)
        horizontalLayout.addWidget(self.dropdownRotate)
        horizontalLayout.addWidget(self.spinboxRotate)
        return horizontalLayout
    
    def __buildMoveToXYZRelativeToCurrentPosition(self):
        horizontalLayout = QHBoxLayout()
        self.dropdownMoveToXYZRelative = Dropdown(self, "Speed", SPEED)
        self.spinboxMoveToXYZRelative_X = Spinbox(self, "X", "", 10, 500, 10, 1, 0)
        self.spinboxMoveToXYZRelative_Y = Spinbox(self, "Y", "", 10, 500, 10, 1, 0)
        self.spinboxMoveToXYZRelative_Z = Spinbox(self, "Z", "", 10, 500, 10, 1, 0)
        self.buttonMoveToXYZRelative = GenericButton(self, "Move To XYZ Relative")
        self.buttonMoveToXYZRelative.clicked.connect(lambda: self.drone.moveToXYZRelativeToCurrentPosition(self.spinboxMoveToXYZRelative_X.getValue(),
                                                                                              self.spinboxMoveToXYZRelative_Y.getValue(),
                                                                                              self.spinboxMoveToXYZRelative_Z.getValue(),
                                                                                              self.dropdownMoveToXYZRelative.getCurrentEnum()))
        horizontalLayout.addWidget(self.buttonMoveToXYZRelative)
        horizontalLayout.addWidget(self.spinboxMoveToXYZRelative_X)
        horizontalLayout.addWidget(self.spinboxMoveToXYZRelative_Y)
        horizontalLayout.addWidget(self.spinboxMoveToXYZRelative_Z)
        horizontalLayout.addWidget(self.dropdownMoveToXYZRelative)

        return horizontalLayout

    def _buildCircle(self):
        horizontalLayout = QHBoxLayout()
        self.dropdownCircle = Dropdown(self, "Speed", SPEED)
        self.spinboxCircleRadius= Spinbox(self, "Radius in cm", "", 10, 500, 10, 1, 0)
        self.spinboxCircleSteps = Spinbox(self, "Steps", "", 0, 100, 5, 1, 0)
        self.buttonCircle = GenericButton(self, "Circle")
        self.buttonCircle.clicked.connect(lambda: self.drone.circleObject(self.spinboxCircleRadius.getValue(),
                                                                                        self.dropdownCircle.getCurrentEnum(),
                                                                                        self.spinboxCircleSteps.getValue()))
        horizontalLayout.addWidget(self.buttonCircle)
        horizontalLayout.addWidget(self.spinboxCircleRadius)
        horizontalLayout.addWidget(self.spinboxCircleSteps)
        horizontalLayout.addWidget(self.dropdownCircle)

        return horizontalLayout


    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(10, self.center_on_screen)

    def show(self):
        """Override show to reliably bring window to front"""
        # Hide first if visible (forces a proper show)
        if self.isVisible():
            self.hide()

        # Small delay to ensure hide is processed
        QTimer.singleShot(10, self._do_show)

    def _do_show(self):
        """Actually show the window"""
        super().show()
        self.raise_()
        self.activateWindow()

    def center_on_screen(self):
        from PySide6.QtWidgets import QApplication

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2 + screen.x()
        y = (screen.height() - self.height()) // 2 + screen.y()
        self.move(x, y)