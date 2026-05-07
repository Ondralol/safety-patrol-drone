from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget

from ui.elements.title import Title

from datetime import datetime

class ObjectLogWidget(QWidget):
    """Scrollable log of detected objects with timestamps."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = Title(self, "Detected objects")
        layout.addWidget(title)

        self.log = QListWidget()
        layout.addWidget(self.log)

    def addEntry(self, message: str):
        timestamp = datetime.now().strftime("%H_%S_%f")[:-3]
        self.log.addItem(f"[{timestamp}] - {message}")
