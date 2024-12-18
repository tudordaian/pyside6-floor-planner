from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QPixmap, QPen
from PySide6.QtWidgets import QGraphicsRectItem

class PlaceableObject(QGraphicsRectItem):
    def __init__(self, x, y, width, height, texture_path=None):
        super().__init__(0, 0, width, height)
        self.setPos(x, y)
        if texture_path:
            pixmap = QPixmap(texture_path).scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            brush = QBrush(pixmap)
            self.setBrush(brush)
        else:
            self.setBrush(QBrush(QColor(0, 0, 0)))  # Brown color
        self.setPen(QPen(Qt.NoPen))
        self.setAcceptHoverEvents(False)
