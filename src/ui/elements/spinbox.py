from PySide6.QtCore import QEvent, QSize, Qt
from PySide6.QtWidgets import QDoubleSpinBox, QSizePolicy, QVBoxLayout, QWidget, QLabel

SPINBOX_WIDGET_WIDTH = 80
SPINBOX_WIDGET_HEIGHT = 40

class Spinbox(QWidget):
    def __init__(self, parent, name, suffix, minVal, maxVal, setVal, stepSize, decimals):
        super().__init__(parent)

        self.parent = parent

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(2, 2, 2, 2)

        layout.addWidget(QLabel(f"{name}"))

        self.durationSpin = QDoubleSpinBox()
        self.durationSpin.setRange(minVal, maxVal)
        self.durationSpin.setValue(setVal)
        self.durationSpin.setDecimals(decimals)
        self.durationSpin.setSingleStep(stepSize)
        self.durationSpin.setSuffix(suffix)

        layout.addWidget(self.durationSpin)

        layout.addStretch(1)

        self.setLayout(layout)

        # Set sizing policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set no focus
        self.durationSpin.setFocusPolicy(Qt.ClickFocus)

        # Get the top window
        top_window = self.window()
        if top_window and top_window != self:
            top_window.installEventFilter(self)
        
        self.setMaximumHeight(90)
        self.setMaximumWidth(150)

    # Default size
    def sizeHint(self) -> QSize:
        return QSize(SPINBOX_WIDGET_WIDTH, SPINBOX_WIDGET_HEIGHT)

    # Removes cursor from spinbox if mouse clicked anywhere else
    def eventFilter(self, watched, event):
        # Check if the event type is MouseButtonPress
        if event.type() == QEvent.MouseButtonPress:
            # If the clicked area is not inside a QSpinBox, clear focus
            if not isinstance(watched, QDoubleSpinBox):
                focus_widget = self.window().focusWidget()
                if focus_widget and isinstance(focus_widget, QDoubleSpinBox):
                    focus_widget.clearFocus()  # Clear focus from spinbox if clicked outside

        # Continue processing the event
        return super().eventFilter(watched, event)

    def keyPressEvent(self, event):
        # Exit spinbox on ENTER
        if event.key() == Qt.Key_Return:
            self.durationSpin.clearFocus()

        # Escape spinbox on ESC
        if event.key() == Qt.Key_Escape:
            self.durationSpin.clearFocus()

        return super().keyPressEvent(event)

    def getValue(self):
        return int(self.durationSpin.value())