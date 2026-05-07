import math

from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QPainterPath
from PySide6.QtWidgets import QSizePolicy, QVBoxLayout, QWidget

from ui.elements.title import Title
from utils.position import Position

WIDTH_CM = 200  # 2x2 meters

class MapCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.position = Position(0.0, 0.0, 0.0, 0)
        self.targets = []
        self.setMinimumSize(480, 360)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def update_position(self, position: Position):
        self.position = position
        self.update()

    def draw_targets(self, painter):
        """Draws targets."""

        w, h = self.width(), self.height()
        size = min(w, h) - 20
        
        # Offsets
        ox = (w - size) / 2
        oy = (h - size) / 2
        cx, cy = ox + size / 2, oy + size / 2
        # Drone position in screen coords
        scale = size / WIDTH_CM

        for x, y in self.targets:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QColor("#ff0000")))
            px = cx + y * scale
            py = cy - x * scale
            px = max(ox, min(ox + size, px))
            py = max(oy, min(oy + size, py))
            painter.drawEllipse(QPointF(px, py), 3, 3)



    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        size = min(w, h) - 20
        # Offsets
        ox = (w - size) / 2
        oy = (h - size) / 2

        painter.fillRect(0, 0, w, h, QColor("#1a1a2e"))

        # Area border
        painter.setPen(QPen(QColor("#444466"), 2))
        painter.drawRect(int(ox), int(oy), size, size)

        # Grid 4x4 cells, each 0.5x0.5 m in real life
        painter.setPen(QPen(QColor("#2a2a4a"), 1))
        for i in [0.25, 0.5, 0.75]:
            gx = ox + size * i
            gy = oy + size * i
            painter.drawLine(int(gx), int(oy), int(gx), int(oy + size))
            painter.drawLine(int(ox), int(gy), int(ox + size), int(gy))

        # Center cross
        painter.setPen(QPen(QColor("#444466"), 1, Qt.PenStyle.DashLine))
        cx, cy = ox + size / 2, oy + size / 2
        painter.drawLine(int(cx), int(oy), int(cx), int(oy + size))
        painter.drawLine(int(ox), int(cy), int(ox + size), int(cy))


        # Draw targets
        self.draw_targets(painter)

        # Drone position in screen coords
        scale = size / WIDTH_CM
        px = cx + self.position.y * scale
        py = cy - self.position.x * scale
        # Clamp
        px = max(ox, min(ox + size, px))
        py = max(oy, min(oy + size, py))
        

        # Displays sorta triangle arrow thing where the drone is looking
        a = math.radians(self.position.angle)
        # Arrow length
        cone_len = 28
        cone_half = math.radians(25)

        # The corners of the arrow
        left_x  = px + math.sin(a - cone_half) * cone_len
        left_y  = py - math.cos(a - cone_half) * cone_len
        right_x = px + math.sin(a + cone_half) * cone_len
        right_y = py - math.cos(a + cone_half) * cone_len

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor("#00d4ff")))

        # Actually draws the arrow by connecting all the points
        cone = QPainterPath()
        cone.moveTo(QPointF(px, py)) # Current positon
        cone.lineTo(QPointF(left_x, left_y)) # far left
        cone.lineTo(QPointF(right_x, right_y)) # far right
        cone.closeSubpath() # Connect back to the starting point and fill the inside area
        painter.drawPath(cone)

        # Display dot at drones position
        painter.drawEllipse(QPointF(px, py), 6, 6)


class MapWidget(QWidget):
    """Map showing drone position and heading in the 2x2m flight area."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        title = Title(self, "Drone position map")
        layout.addWidget(title)

        self.canvas = MapCanvas()
        layout.addWidget(self.canvas)

    def update_position(self, position: Position):
        self.canvas.update_position(position)

    def update_targets(self, new_targets):
        for xy in new_targets:
            self.canvas.targets.append(xy)
        self.canvas.update()