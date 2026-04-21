from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget

STYLE_GREEN = "QProgressBar::chunk { background-color: #2ecc71; }"
STYLE_YELLOW = "QProgressBar::chunk { background-color: #f39c12; }"
STYLE_RED = "QProgressBar::chunk { background-color: #e74c3c; }"

STYLE_BAR = """
    QProgressBar {
        border: 2px solid #555;
        border-radius: 4px;
        background-color: #2a2a2a;
        text-align: center;
    }
"""


class BatteryWidget(QWidget):
    """Horizontal battery bar with percentage label."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.label = QLabel("Battery")
        layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet(STYLE_BAR + STYLE_GREEN)
        layout.addWidget(self.bar)

        self.percent_label = QLabel("100%")
        self.percent_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.percent_label)

        self.setLevel(0)

    def setLevel(self, percent: int):
        percent = max(0, min(100, percent))
        self.bar.setValue(percent)
        self.percent_label.setText(f"{percent}%")

        if percent > 50:
            chunk_style = STYLE_GREEN
        elif percent > 20:
            chunk_style = STYLE_YELLOW
        else:
            chunk_style = STYLE_RED

        self.bar.setStyleSheet(STYLE_BAR + chunk_style)
