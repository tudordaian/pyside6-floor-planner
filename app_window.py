from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QAction, QFont
from PySide6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QToolBar, QStatusBar, \
    QApplication, QLabel, QComboBox

from widgets.editor import Editor


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
        left_column = QVBoxLayout()
        left_column.setSpacing(2)
        left_column.setContentsMargins(5, 5, 5, 5)
        left_column.setAlignment(Qt.AlignTop)

        objects_label = QLabel(' Objects')
        font = QFont()
        font.setPointSize(14)
        objects_label.setFont(font)
        objects_label.setContentsMargins(0, 0, 0, 10)
        left_column.addWidget(objects_label)

        self.left_dropdown = QComboBox()
        self.left_dropdown.addItems(['Structure', 'General', 'Bedroom', 'Bathroom', 'Living', 'Kitchen'])
        self.left_dropdown.currentIndexChanged.connect(self.toggle_left_buttons)
        left_column.addWidget(self.left_dropdown)
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
            left_column.addWidget(button)
        # TODO paseaza o lambda ca sa poti pasa numele butonului ca param si fa o singura functie de press btn cu un switch
        self.left_buttons_structure[0].clicked.connect(self.button_wall_clicked)
        self.left_buttons_structure[1].clicked.connect(self.button_door_clicked)
        self.left_buttons_structure[2].clicked.connect(self.button_window_clicked)

        # Center
        self.editor = Editor()

        # Right column
        right_column = QVBoxLayout()
        right_column.setSpacing(2)
        right_column.setContentsMargins(5, 5, 5, 5)
        right_column.setAlignment(Qt.AlignTop)

        tools_label = QLabel('   Tools')
        font = QFont()
        font.setPointSize(14)
        tools_label.setFont(font)
        tools_label.setContentsMargins(0, 0, 0, 10)
        right_column.addWidget(tools_label)

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
            right_column.addWidget(button)
        self.right_buttons[0].clicked.connect(self.button_floor_clicked)
        self.right_buttons[1].clicked.connect(self.button_roof_clicked)
        self.right_buttons[2].clicked.connect(self.button_furniture_clicked)

        central_layout.addLayout(left_column)
        central_layout.addWidget(self.editor)
        central_layout.addLayout(right_column)

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