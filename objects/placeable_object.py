from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsRectItem

class PlaceableObject(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setBrush(QBrush(QColor(139, 69, 19)))  # Brown color
        self.setAcceptHoverEvents(False)