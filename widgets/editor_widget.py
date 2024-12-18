from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QBrush, QPainter, QUndoStack, QPen, QTransform, QPixmap
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem

from objects.object_command import ObjectCommand
from objects.placeable_object import PlaceableObject


class EditorWidget(QGraphicsView):
    def __init__(self, zoom_label):
        super().__init__()
        # Scena pe care se deseneaza obiectele
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        # Dimensiunile grid ului
        self.grid_size = 30
        self.grid_width = 90
        self.grid_height = 70
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.draw_grid()
        # Obiectul curent ce urmeaza a fi plasat
        self.current_object_size = (1, 1)
        self.current_texture_path = None
        self.current_rotation = 0
        self.object_stack = QUndoStack(self)
        self.eraser_mode = False
        # Pentru preview la obiect inainte de plasare
        self.preview_object = None
        self.init_preview_object()
        # Date despre zoom
        self.zoom_level = 1
        self.zoom_factors = [0.6, 0.8, 0.95, 1.15, 1.35, 1.5]
        self.zoom_label = zoom_label
        self.apply_zoom()
        # Variabile pentru plasare obiecte si panning
        self.is_placing = False
        self.is_panning = False
        self.pan_start_x = 0
        self.pan_start_y = 0
        # Centrez viewport ul la start
        self.centerOn(self.grid_width * self.grid_size / 2, self.grid_height * self.grid_size / 2)

    # Functie pentru a initializa grid ul
    def draw_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                grid_item = GridItem(x * self.grid_size, y * self.grid_size, self.grid_size)
                self.scene.addItem(grid_item)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_placing = True
            self.place_object(event)
        elif event.button() == Qt.MiddleButton:
            self.is_panning = True
            self.pan_start_x = event.x()
            self.pan_start_y = event.y()
            self.setCursor(Qt.ClosedHandCursor)
        elif event.button() == Qt.RightButton:
            self.rotate_preview_object()

    def mouseMoveEvent(self, event):
        pos = self.mapToScene(event.pos())
        x = int(pos.x() // self.grid_size) * self.grid_size
        y = int(pos.y() // self.grid_size) * self.grid_size
        self.preview_object.setPos(x, y)
        if self.is_placing:
            self.place_object(event)
        elif self.is_panning:
            # Mapez coordonatele mouse event ului ca sa controlez scroll bar urile
            delta_x = event.x() - self.pan_start_x
            delta_y = event.y() - self.pan_start_y
            self.pan_start_x = event.x()
            self.pan_start_y = event.y()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta_x)
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_placing = False
        elif event.button() == Qt.MiddleButton:
            self.is_panning = False
            self.setCursor(Qt.ArrowCursor)

    def place_object(self, event):
        pos = self.mapToScene(event.pos())
        if self.eraser_mode:
            item = self.scene.itemAt(pos, self.transform())
            if isinstance(item, PlaceableObject):
                self.object_stack.push(ObjectCommand(self.scene, item, remove=True))
        else:
            x = int(pos.x() // self.grid_size) * self.grid_size
            y = int(pos.y() // self.grid_size) * self.grid_size
            width = self.current_object_size[0] * self.grid_size
            height = self.current_object_size[1] * self.grid_size

            # Creez un obiect temporar pentru a verifica daca exista coliziuni
            temp_object = PlaceableObject(x, y, width, height, self.current_texture_path)
            temp_object.setRotation(self.current_rotation)
            bounding_rect = temp_object.mapRectToScene(temp_object.boundingRect())

            # Verific daca exista deja un obiect la pozitia respectiva
            items = self.scene.items(bounding_rect)
            if any(isinstance(item, PlaceableObject) for item in items):
                return

            placeable_object = PlaceableObject(x, y, width, height, self.current_texture_path)
            placeable_object.setRotation(self.current_rotation)
            self.object_stack.push(ObjectCommand(self.scene, placeable_object))

    def set_current_object(self, object_name):
        object_properties = {
            'Wall': ((1, 1), None),
            'Door': ((2, 2), 'object_textures/door_2x2.png'),
            'Window': ((3, 1), 'object_textures/window_3x1.png'),
            'Stairs': ((3, 8), 'object_textures/stairs_3x8.png'),
            'Table': ((3, 2), 'object_textures/table_3x2.png'),
            'Chair': ((1, 1), 'object_textures/chair_1x1.png'),
            'Plant': ((2, 2), 'object_textures/plant_2x2.png'),
            'Single bed': ((2, 4), 'object_textures/single_bed_2x4.png'),
            'Double bed': ((3, 4), 'object_textures/double_bed_3x4.png'),
            'Closet': ((3, 2), 'object_textures/closet_3x2.png'),
            'Toilet': ((1, 2), 'object_textures/toilet_1x2.png'),
            'Bathroom sink': ((2, 1), 'object_textures/bathroom_sink_2x1.png'),
            'Bathtub': ((4, 2), 'object_textures/bathtub_4x2.png'),
            'Shower': ((2, 2), 'object_textures/shower_2x2.png'),
            'Sofa': ((4, 2), 'object_textures/sofa_4x2.png'),
            'Corner sofa': ((6, 4), 'object_textures/corner_sofa_6x4.png'),
            'Armchair': ((2, 2), 'object_textures/armchair_2x2.png'),
            'TV': ((3, 1), 'object_textures/tv_3x1.png'),
            'Kitchen sink': ((3, 2), 'object_textures/kitchen_sink_3x2.png'),
            'Stove': ((2, 2), 'object_textures/stove_2x2.png'),
            'Cabinet': ((3, 1), 'object_textures/cabinet_3x1.png'),
            'Corner cabinet': ((2, 2), 'object_textures/corner_cabinet_2x2.png')
        }
        if object_name in object_properties:
            self.current_object_size, self.current_texture_path = object_properties[object_name]
        else:
            self.current_object_size, self.current_texture_path = (1, 1), None
        self.update_preview_object()

    def init_preview_object(self):
        self.preview_object = QGraphicsRectItem(0, 0, self.current_object_size[0] * self.grid_size,
                                                self.current_object_size[1] * self.grid_size)
        self.preview_object.setPen(Qt.NoPen)
        self.update_preview_object()
        self.scene.addItem(self.preview_object)

    def update_preview_object(self):
        self.preview_object.setRect(0, 0, self.current_object_size[0] * self.grid_size,
                                    self.current_object_size[1] * self.grid_size)
        if self.current_texture_path:
            pixmap = QPixmap(self.current_texture_path).scaled(self.current_object_size[0] * self.grid_size,
                                                               self.current_object_size[1] * self.grid_size,
                                                               Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            transparent_pixmap = QPixmap(pixmap.size())
            transparent_pixmap.fill(Qt.transparent)
            painter = QPainter(transparent_pixmap)
            painter.setOpacity(0.5)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            brush = QBrush(transparent_pixmap)
        else:
            brush = QBrush(QColor(0, 0, 0, 100))
        self.preview_object.setBrush(brush)

    def rotate_preview_object(self):
        self.current_rotation = (self.current_rotation + 90) % 360
        self.preview_object.setRotation(self.current_rotation)

    def set_preview_visibility(self, visible):
        self.preview_object.setVisible(visible)

    def zoom_in(self):
        if self.zoom_level < 5:
            self.zoom_level += 1
            self.apply_zoom()

    def zoom_out(self):
        if self.zoom_level > 0:
            self.zoom_level -= 1
            self.apply_zoom()

    def apply_zoom(self):
        self.setTransform(QTransform().scale(self.zoom_factors[self.zoom_level], self.zoom_factors[self.zoom_level]))
        self.zoom_label.setText(f'Zoom level: {self.zoom_level}')

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def save(self, file_path):
        image = QPixmap(self.scene.sceneRect().size().toSize())
        image.fill(Qt.transparent)
        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()
        image.save(file_path)



class GridItem(QGraphicsRectItem):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        self.default_color = QColor(255, 255, 255)
        self.hover_color = QColor(200, 200, 200)
        self.setBrush(QBrush(self.default_color))
        self.setAcceptHoverEvents(True)
        pen = QPen(QColor(225, 225, 225))   # Grid line color
        pen.setWidth(1)                     # Grid line thickness
        self.setPen(pen)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(self.hover_color))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(self.default_color))
        super().hoverLeaveEvent(event)