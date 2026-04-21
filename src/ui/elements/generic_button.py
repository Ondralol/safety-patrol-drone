from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtWidgets import QPushButton, QSizePolicy

BUTTON_WIDTH = 145
BUTTON_HEIGHT = 25

STYLE_SHEET_BUTTON = """
    QPushButton {
        background-color: #2196F3;  /* Blue */
        color: white;
        font-size: 15px;
        font-weight: bold;
        border-radius: 8px;
        padding: 8px 16px;
        border: 2px solid #1976D2;  /* Darker Blue for border */
    }

    QPushButton:hover {
        background-color: #1976D2;  /* Darker Blue */
        border-color: #1565C0;
    }

    QPushButton:pressed {
        background-color: #1565C0;  /* Even darker Blue */
        border-color: #0D47A1;
    }

    QPushButton:disabled {
        background-color: #BDBDBD;  /* Gray */
        color: #9E9E9E;
        border-color: #9E9E9E;
    }
"""


class GenericButton(QPushButton):
    """Generic Button"""
    def __init__(self, parent, name) -> None:
        super().__init__(parent)

        self.setText(name)

        self.setStyleSheet(STYLE_SHEET_BUTTON)

        # Disable ability to use keyboard to accidentally trigger buttons
        self.setFocusPolicy(Qt.NoFocus)

        # Sizing policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMaximumHeight(90)
        self.setMaximumWidth(200)

    @Slot(bool)
    def handleClick(self):
        # Pass to parent
        pass

    # Default size
    def sizeHint(self) -> QSize:
        return QSize(BUTTON_WIDTH, BUTTON_HEIGHT)