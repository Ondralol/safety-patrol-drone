from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout

from communication.dji_api import Drone

POPUP_WIDTH = 1600
POPUP_HEIGHT = 900

STYLE_SHEET_POPUP_DIALOG = """
    QDialog {
        background-color: #1e1e1e;
        border: 2px solid #444444;
        border-radius: 10px;
    }
"""


class PopupWindowDroneDebug(QDialog):
    def __init__(self, parent, drone: Drone):
        super().__init__(parent)

        self.parent = parent
        self.drone = drone

        self.setWindowTitle("Drone debug")
        self.setStyleSheet(STYLE_SHEET_POPUP_DIALOG)
        self.setMinimumSize(QSize(POPUP_WIDTH, POPUP_HEIGHT))

        # Remove window frame for cleaner look
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # Allow non blocking behaviour
        self.setModal(False)

        # Main layout with proper margins
        mainLayoutVertical = QVBoxLayout()
        mainLayoutVertical.setContentsMargins(50, 50, 50, 50)
        mainLayoutVertical.setSpacing(10)

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