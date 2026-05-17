from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget

from ui.elements.title import Title

from datetime import datetime
import os
import pandas as pd

# Class for buffering sensor data to a CSV file - Buffer size is set to 50 by default
class Buffer:
    def __init__(self, fileName, bufferSize=50):
        if not os.path.exists(os.path.dirname(fileName)):
            os.makedirs(os.path.dirname(fileName))

        self.buffer = []
        self.bufferSize = bufferSize
        self.fileName = fileName

    def __del__(self):
        # Save remaining data to CSV if any
        self.flush()

    # Adds row
    def addData(self, row):
        self.buffer.append(row)

        # If buffer is full, save to CSV
        if len(self.buffer) >= self.bufferSize:
            df = pd.DataFrame(self.buffer)
            df.to_csv(self.fileName, mode="a", header=False, index=False)
            self.buffer = []

    # Saves the remaining data to CSV
    def flush(self):
        if self.buffer:
            df = pd.DataFrame(self.buffer)
            df.to_csv(self.fileName, mode="a", header=False, index=False)
            self.buffer = []


class ObjectLogWidget(QWidget):
    """Scrollable log of detected objects with timestamps."""

    def __init__(self, parent=None):
        super().__init__(parent)

        timestamp = datetime.now().strftime("%H_%S_%f")[:-3]
        self.buffer = Buffer(f"logs/object_log{timestamp}")
        row = []
        row.append("timestamp")
        row.append("object")
        row.append("position")
        self.buffer.addData(row)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = Title(self, "Detected objects")
        layout.addWidget(title)

        self.log = QListWidget()
        layout.addWidget(self.log)

    def addEntry(self, label, pos):
        timestamp = datetime.now().strftime("%H_%S_%f")[:-3]
        self.log.addItem(f"[{timestamp}] - Found {label} at coords: ({pos[0]:.3f}, {pos[1]:.3f})")

        row = []
        row.append(timestamp)
        row.append(label)
        row.append(pos)
        self.buffer.addData(row)

