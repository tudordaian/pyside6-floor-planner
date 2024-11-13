from PySide6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class LeftColumnWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
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
            QPushButton('Wall'),
            QPushButton('Door'),
            QPushButton('Window'),
            QPushButton('Stairs')
        ]
        self.left_buttons_general = [
            QPushButton('Table'),
            QPushButton('Corner table'),
            QPushButton('Chair'),
            QPushButton('Shelf'),
            QPushButton('Plant')
        ]
        self.left_buttons_bedroom = [
            QPushButton('Bed'),
            QPushButton('Closet'),
        ]
        self.left_buttons_bathroom = [
            QPushButton('Toilet'),
            QPushButton('Sink'),
            QPushButton('Bathtub'),
        ]
        self.left_buttons_living = [
            QPushButton('Sofa'),
            QPushButton('Corner sofa'),
            QPushButton('Armchair'),
            QPushButton('TV'),
        ]
        self.left_buttons_kitchen = [
            QPushButton('Kitchen sink'),
            QPushButton('Stove'),
            QPushButton('Cabinet'),
            QPushButton('Corner cabinet')
        ]
        for button in (self.left_buttons_structure +
                       self.left_buttons_general +
                       self.left_buttons_bedroom +
                       self.left_buttons_bathroom +
                       self.left_buttons_living +
                       self.left_buttons_kitchen):
            button.setFixedSize(75, 75)
            self.layout.addWidget(button)

        self.setLayout(self.layout)