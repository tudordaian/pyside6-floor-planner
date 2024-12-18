from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap


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
            self.create_button_with_thumbnail('Undo', 'tool_icons/undo.png'),
            self.create_button_with_thumbnail('Redo', 'tool_icons/redo.png'),
            self.create_button_with_thumbnail('Erase', 'tool_icons/eraser.png'),
            self.create_button_with_thumbnail('New floor', 'tool_icons/plus-sign.png'),
            self.create_button_with_thumbnail('Go up', 'tool_icons/up-arrow.png'),
            self.create_button_with_thumbnail('Go down', 'tool_icons/down-arrow.png'),
        ]
        for button in self.right_buttons:
            button.setFixedSize(75, 75)
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.right_buttons[2].clicked.connect(self.toggle_eraser_mode)

    def create_button_with_thumbnail(self, label_text, icon_path):
        button = QPushButton()
        button.setFixedSize(75, 75)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        if icon_path:
            pixmap = QPixmap(icon_path).scaled(73, 55, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            thumbnail = QLabel()
            thumbnail.setPixmap(pixmap)
            thumbnail.setContentsMargins(1, 0, 0, 0)
            layout.addWidget(thumbnail)

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        button.setLayout(layout)
        button.setProperty('label_text', label_text)
        button.setProperty('icon_path', icon_path)
        return button

    def toggle_eraser_mode(self):
        self.editor.eraser_mode = not self.editor.eraser_mode
        thumbnail_label = self.right_buttons[2].layout().itemAt(0).widget()
        text_label = self.right_buttons[2].layout().itemAt(1).widget()

        if isinstance(thumbnail_label, QLabel) and isinstance(text_label, QLabel):
            if self.editor.eraser_mode:
                thumbnail_label.setPixmap(
                    QPixmap('tool_icons/pencil.png').scaled(73, 55, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                text_label.setText('Draw')
            else:
                thumbnail_label.setPixmap(
                    QPixmap('tool_icons/eraser.png').scaled(73, 55, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
                text_label.setText('Erase')

        self.editor.set_preview_visibility(not self.editor.eraser_mode)