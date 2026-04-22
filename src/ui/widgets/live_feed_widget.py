from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap

import numpy as np

from ui.elements.title import Title

class LiveFeedWidget(QWidget):
    """Live video feed with object detection overlay."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = Title(self, "Live video feed with object detection")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.feed_label = QLabel("No feed")
        self.feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feed_label.setMinimumSize(960, 720)
        self.feed_label.setStyleSheet("background: black; color: white;")
        self.feed_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.feed_label)
    
    def updateFrame(self, frame: np.ndarray):
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.feed_label.setPixmap(
            QPixmap.fromImage(img).scaled(
                self.feed_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
