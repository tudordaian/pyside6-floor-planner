import os
import sys
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QAction, QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QToolBar, QStatusBar, \
    QApplication, QLabel

from widgets.editor_widget import EditorWidget
from widgets.left_column_widget import LeftColumnWidget
from widgets.right_column_widget import RightColumnWidget


class FloorCreatorWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle('Floor Plan Creator')
        self.setMinimumSize(950, 650)

        # Menubar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: #4D4D4D;")

        # File menu
        file_menu = menu_bar.addMenu('File')
        save_action = file_menu.addAction('Save')
        save_action.triggered.connect(self.save)
        quit_action = file_menu.addAction('Quit')
        quit_action.triggered.connect(self.quit)

        # View menu
        view_menu = menu_bar.addMenu('View')
        self.fullscreen_action = view_menu.addAction('Fullscreen')
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)

        # Toolbar
        toolbar = QToolBar("Toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.setStyleSheet("background-color: #4D4D4D;")

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)

        # Left column
        self.left_column = LeftColumnWidget()
        self.left_column.connect_buttons(self.set_current_object)
        central_layout.addWidget(self.left_column)

        # Bottom statusbar
        status_bar = QStatusBar(self)
        status_bar.setStyleSheet("background-color: #5B5B5B;")
        self.setStatusBar(status_bar)
        font = QFont()
        font.setPointSize(12)
        self.zoom_label = QLabel(f'Zoom level: 1')
        self.zoom_label.setFont(font)
        self.zoom_label.setContentsMargins(10, 0, 0, 10)
        status_bar.addWidget(self.zoom_label)
        self.selected_object_label = QLabel('Selected object: Wall')
        self.selected_object_label.setFont(font)
        self.selected_object_label.setContentsMargins(10, 0, 0, 10)
        status_bar.addWidget(self.selected_object_label)

        # Center
        self.editor = EditorWidget(self.zoom_label)
        central_layout.addWidget(self.editor)

        # Toolbar actions
        zoom_in_button = QAction('+ Zoom In', self)
        zoom_in_button.triggered.connect(self.editor.zoom_in)
        toolbar.addAction(zoom_in_button)
        zoom_out_button = QAction('- Zoom Out', self)
        zoom_out_button.triggered.connect(self.editor.zoom_out)
        toolbar.addAction(zoom_out_button)

        # Right column
        self.right_column = RightColumnWidget(self.editor)
        self.right_column.right_buttons[0].clicked.connect(self.editor.object_stack.undo)
        self.right_column.right_buttons[1].clicked.connect(self.editor.object_stack.redo)
        central_layout.addWidget(self.right_column)

        self.center_window()
        self.show()

    def center_window(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def quit(self):
        self.app.quit()

    def save(self):
        save_dir = 'saved_projects'
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y_%m_%d_%H:%M')
        file_path = os.path.join(save_dir, f'floor_plan_{timestamp}.png')
        self.editor.save(file_path)

    def set_current_object(self, object_name):
        self.editor.set_current_object(object_name)
        self.selected_object_label.setText(f'Selected object: {object_name}')

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_action.setText('Fullscreen')
        else:
            self.showFullScreen()
            self.fullscreen_action.setText('Exit fullscreen')

