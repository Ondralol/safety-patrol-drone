from enum import Enum


from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QWidget,
    QVBoxLayout,
    QSizePolicy
)

class Dropdown(QWidget):
    def __init__(self, parent, str, enum):
        super().__init__()
        self.parent = parent

        verticalLayout = QVBoxLayout()
        verticalLayout.setSpacing(0)
        verticalLayout.setContentsMargins(2, 2, 2, 2)

        # Dropdown from Enum
        self.dropdown = QComboBox()
        for option in enum:
            self.dropdown.addItem(option.name, option)

        verticalLayout.addWidget(QLabel(f"Select {str}:"))
        verticalLayout.addWidget(self.dropdown)
        self.setLayout(verticalLayout)
        self.setMaximumHeight(90)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)     

    def getCurrentEnum(self):
        index = self.dropdown.currentIndex()
        return self.dropdown.itemData(index)