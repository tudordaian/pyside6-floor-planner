from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class RightColumnWidget(QWidget):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
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
            QPushButton('Erase'),
            QPushButton('New floor'),
            QPushButton('Go up'),
            QPushButton('Go down'),
        ]
        for button in self.right_buttons:
            button.setFixedSize(75, 75)
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.right_buttons[2].clicked.connect(self.toggle_eraser_mode)

    # TODO vezi ce vrea chatu ca i prajit
    def toggle_eraser_mode(self):
        self.editor.eraser_mode = not self.editor.eraser_mode
        self.right_buttons[2].setText('Draw' if self.editor.eraser_mode else 'Erase')
