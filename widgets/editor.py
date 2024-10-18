from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem


class Editor(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.grid_size = 30
        self.grid_width = 50
        self.grid_height = 40
        self.draw_grid()

    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                grid_item = GridItem(x * self.grid_size, y * self.grid_size, self.grid_size)
                self.scene.addItem(grid_item)


class GridItem(QGraphicsRectItem):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.default_color = QColor(255, 255, 255)  # Default color
        self.hover_color = QColor(200, 200, 200)    # Hover color
        self.setBrush(QBrush(self.default_color))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(self.hover_color))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(self.default_color))
        super().hoverLeaveEvent(event)