import sys

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
        self.zoom_level = 1

        # Menubar
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu('File')
        save_action = file_menu.addAction('Save')
        #TODO save_action.triggered.connect(self.save)
        quit_action = file_menu.addAction('Quit')
        quit_action.triggered.connect(self.quit)

        # View menu
        view_menu = menu_bar.addMenu('View')
        self.fullscreen_action = view_menu.addAction('Fullscreen')
        self.fullscreen_action.triggered.connect(self.toggle_fullscreen)

        # Toolbar
        toolbar = QToolBar("Toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        zoom_in_button = QAction('+ Zoom In', self)
        zoom_in_button.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_button)
        zoom_out_button = QAction('- Zoom Out', self)
        zoom_out_button.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_button)

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)

        # Left column
        self.left_column = LeftColumnWidget()   # TODO fa ca mai jos cu self ca argument
        self.left_column.left_dropdown.currentIndexChanged.connect(self.toggle_left_buttons)
        self.left_column.left_buttons_structure[0].clicked.connect(self.button_wall_clicked)
        self.left_column.left_buttons_structure[1].clicked.connect(self.button_door_clicked)
        self.left_column.left_buttons_structure[2].clicked.connect(self.button_window_clicked)
        central_layout.addWidget(self.left_column)

        # Center
        self.editor = EditorWidget()
        central_layout.addWidget(self.editor)

        # Right column
        self.right_column = RightColumnWidget(self.editor)
        self.right_column.right_buttons[0].clicked.connect(self.editor.object_stack.undo)
        self.right_column.right_buttons[1].clicked.connect(self.editor.object_stack.redo)
        central_layout.addWidget(self.right_column)

        # Bottom statusbar
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        font = QFont()
        font.setPointSize(12)
        self.zoom_label = QLabel(f'Zoom level: {self.zoom_level}')
        self.zoom_label.setFont(font)
        self.zoom_label.setContentsMargins(10, 0, 0, 10)
        status_bar.addWidget(self.zoom_label)
        #TODO show current selected item in the statusbar

        self.center_window()
        self.show()
        self.toggle_left_buttons(0)

    def toggle_left_buttons(self, index):
        button_sets = {
            0: self.left_column.left_buttons_structure,
            1: self.left_column.left_buttons_general,
            2: self.left_column.left_buttons_bedroom,
            3: self.left_column.left_buttons_bathroom,
            4: self.left_column.left_buttons_living,
            5: self.left_column.left_buttons_kitchen,
        }
        for key, button_set in button_sets.items():
            if key == index:
                for button in button_set:
                    button.show()
            else:
                for button in button_set:
                    button.hide()

    def center_window(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def quit(self):
        self.app.quit()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
            self.fullscreen_action.setText('Fullscreen')
        else:
            self.showFullScreen()
            self.fullscreen_action.setText('Exit fullscreen')

    def zoom_in(self):
        if self.zoom_level < 5:
            zoom_factor = 1.2
            self.editor.scale(zoom_factor, zoom_factor)
            self.zoom_level += 1
            self.zoom_label.setText(f'Zoom level: {self.zoom_level}')

    def zoom_out(self):
        if self.zoom_level > 0:
            zoom_factor = 1.2
            self.editor.scale(1 / zoom_factor, 1 / zoom_factor)
            self.zoom_level -= 1
            self.zoom_label.setText(f'Zoom level: {self.zoom_level}')

    def button_wall_clicked(self):
        print('Wall button clicked')

    def button_door_clicked(self):
        print('Door button clicked')

    def button_window_clicked(self):
        print('Window button clicked')

    def button_floor_clicked(self):
        print('Floor button clicked')

    def button_roof_clicked(self):
        print('Roof button clicked')

    def button_furniture_clicked(self):
        print('Furniture button clicked')

    def button_bed_clicked(self):
        self.editor.current_object_size = (2, 3)
        print('Bed button clicked')




app = QApplication(sys.argv)
window = FloorCreatorWindow(app)
sys.exit(app.exec())