from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


DEBUG_WIDGET_STYLE_SHEET = """
DebugWidget {
    background-color: transparent;
    border-radius: 1px;
    border: 1px solid #374151;
}

DebugWidget QLabel#nameLabel {
    color: #D1D5DB;
    font-weight: 600;
    font-size: 11.5px;
    background-color: #374151;
    border-radius: 3px;
    min-width: 250px;
    min-height: 21px;
}

DebugWidget QLabel#valueLabel {
    color: #FACC15;
    font-weight: 700;
    font-size: 13.6px;
    background-color: #111827;
    border-radius: 3px;
    min-width:250px;
    min-height: 21px;
}
"""


class DebugWidget(QWidget):
    def __init__(self, parent, name: str):
        super().__init__(parent)

        # Create labels
        self.name_label = QLabel(name.upper())
        self.value_label = QLabel("-")

        # Set object names for styling
        self.name_label.setObjectName("nameLabel")
        self.value_label.setObjectName("valueLabel")

        # Alignment
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)

    
        self.setStyleSheet(DEBUG_WIDGET_STYLE_SHEET)
        #self.setFixedSize(250, 60)
        layout.setContentsMargins(1, 1, 1, 1)
        layout.setSpacing(1)
        self.setMaximumWidth(450)

        self.setLayout(layout)
       
    def set_value(self, value, suffix: str = ""):
        """Update the displayed value"""
        self.value_label.setText(f"{value} {suffix}".strip())