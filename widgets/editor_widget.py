from PySide6.QtGui import QColor, QBrush, QPainter, QUndoStack
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem

from objects.placeable_object_command import PlaceableObjectCommand
from objects.placeable_object import PlaceableObject


class EditorWidget(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.grid_size = 30
        self.grid_width = 54
        self.grid_height = 34
        self.setRenderHint(QPainter.RenderHint.Antialiasing)    # Grid lines look bad without this when zoomed out
        self.draw_grid()
        self.current_object_size = (2, 3)  # TODO schimba asta cu marimea coresp. obiectului selectat
        self.object_stack = QUndoStack(self)

    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                grid_item = GridItem(x * self.grid_size, y * self.grid_size, self.grid_size)
                self.scene.addItem(grid_item)

    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.grid_size) * self.grid_size
        y = int(pos.y() // self.grid_size) * self.grid_size
        width = self.current_object_size[0] * self.grid_size
        height = self.current_object_size[1] * self.grid_size
        placeable_object = PlaceableObject(x, y, width, height)
        object_command = PlaceableObjectCommand(self.scene, placeable_object)
        self.object_stack.push(object_command)

class GridItem(QGraphicsRectItem):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.default_color = QColor(255, 255, 255)
        self.hover_color = QColor(200, 200, 200)
        self.setBrush(QBrush(self.default_color))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(self.hover_color))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(self.default_color))
        super().hoverLeaveEvent(event)