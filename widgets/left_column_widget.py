from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

class LeftColumnWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(Qt.AlignTop)

        objects_label = QLabel(' Objects')
        font = QFont()
        font.setPointSize(14)
        objects_label.setFont(font)
        objects_label.setContentsMargins(0, 0, 0, 10)
        self.layout.addWidget(objects_label)

        self.left_dropdown = QComboBox()
        self.left_dropdown.addItems(['Structure', 'General', 'Bedroom', 'Bathroom', 'Living', 'Kitchen'])
        self.layout.addWidget(self.left_dropdown)

        self.left_buttons_structure = [
            self.create_button_with_thumbnail('Wall', None),
            self.create_button_with_thumbnail('Door', 'object_textures/door_2x2.png'),
            self.create_button_with_thumbnail('Window', 'object_textures/window_3x1.png'),
            self.create_button_with_thumbnail('Stairs', 'object_textures/stairs_3x8.png')
        ]
        self.left_buttons_general = [
            self.create_button_with_thumbnail('Table', 'object_textures/table_3x2.png'),
            self.create_button_with_thumbnail('Chair', 'object_textures/chair_1x1.png'),
            self.create_button_with_thumbnail('Plant', 'object_textures/plant_2x2.png')
        ]
        self.left_buttons_bedroom = [
            self.create_button_with_thumbnail('Single bed', 'object_textures/single_bed_2x4.png'),
            self.create_button_with_thumbnail('Double bed', 'object_textures/double_bed_3x4.png'),
            self.create_button_with_thumbnail('Closet', 'object_textures/closet_3x2.png')
        ]
        self.left_buttons_bathroom = [
            self.create_button_with_thumbnail('Toilet', 'object_textures/toilet_1x2.png'),
            self.create_button_with_thumbnail('Bathroom sink', 'object_textures/bathroom_sink_2x1.png'),
            self.create_button_with_thumbnail('Bathtub', 'object_textures/bathtub_4x2.png'),
            self.create_button_with_thumbnail('Shower', 'object_textures/shower_2x2.png')
        ]
        self.left_buttons_living = [
            self.create_button_with_thumbnail('Sofa', 'object_textures/sofa_4x2.png'),
            self.create_button_with_thumbnail('Corner sofa', 'object_textures/corner_sofa_6x4.png'),
            self.create_button_with_thumbnail('Armchair', 'object_textures/armchair_2x2.png'),
            self.create_button_with_thumbnail('TV', 'object_textures/tv_3x1.png')
        ]
        self.left_buttons_kitchen = [
            self.create_button_with_thumbnail('Kitchen sink', 'object_textures/kitchen_sink_3x2.png'),
            self.create_button_with_thumbnail('Stove', 'object_textures/stove_2x2.png'),
            self.create_button_with_thumbnail('Cabinet', 'object_textures/cabinet_3x1.png'),
            self.create_button_with_thumbnail('Corner cabinet', 'object_textures/corner_cabinet_2x2.png')
        ]
        for button in (self.left_buttons_structure +
                       self.left_buttons_general +
                       self.left_buttons_bedroom +
                       self.left_buttons_bathroom +
                       self.left_buttons_living +
                       self.left_buttons_kitchen):
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.left_dropdown.currentIndexChanged.connect(self.toggle_left_buttons)
        self.toggle_left_buttons(0)

    def create_button_with_thumbnail(self, label_text, texture_path):
        button = QPushButton()
        button.setFixedSize(90, 90)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        if texture_path:
            pixmap = QPixmap(texture_path).scaled(88, 70, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            thumbnail = QLabel()
            thumbnail.setPixmap(pixmap)
            thumbnail.setContentsMargins(1, 0, 0, 0)
            layout.addWidget(thumbnail)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        button.setLayout(layout)
        button.setProperty('object_name', label_text)
        return button

    def toggle_left_buttons(self, index):
        button_sets = {
            0: self.left_buttons_structure,
            1: self.left_buttons_general,
            2: self.left_buttons_bedroom,
            3: self.left_buttons_bathroom,
            4: self.left_buttons_living,
            5: self.left_buttons_kitchen,
        }
        for key, button_set in button_sets.items():
            if key == index:
                for button in button_set:
                    button.show()
            else:
                for button in button_set:
                    button.hide()

    def connect_buttons(self, set_current_object_callback):
        for button_set in [
            self.left_buttons_structure,
            self.left_buttons_general,
            self.left_buttons_bedroom,
            self.left_buttons_bathroom,
            self.left_buttons_living,
            self.left_buttons_kitchen
        ]:
            for button in button_set:
                button.clicked.connect(lambda checked, b=button: set_current_object_callback(b.property('object_name')))