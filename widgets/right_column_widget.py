from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class RightColumnWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setAlignment(Qt.AlignTop)

        tools_label = QLabel('   Tools')
        font = QFont()
        font.setPointSize(14)
        tools_label.setFont(font)
        tools_label.setContentsMargins(0, 0, 0, 10)
        self.layout.addWidget(tools_label)

        self.right_buttons = [
            QPushButton('Undo'),
            QPushButton('Redo'),
            QPushButton('Eraser'),
            QPushButton('New floor'),
            QPushButton('Go up'),
            QPushButton('Go down'),
        ]
        for button in self.right_buttons:
            button.setFixedSize(75, 75)
            self.layout.addWidget(button)

        self.setLayout(self.layout)