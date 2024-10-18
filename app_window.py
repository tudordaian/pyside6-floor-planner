from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QScreen, QPen, QPainter
from PySide6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QToolBar, QStatusBar, \
    QApplication, QGraphicsScene, QGraphicsRectItem, QGraphicsView

from widgets.editor import Editor


class FloorCreatorWindow (QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle('Floor Plan Creator')
        self.setMinimumSize(950, 650)

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
        zoom_in_action = view_menu.addAction('+ Zoom In')
        #TODO zoom_in_action.triggered.connect(self.zoom_in)
        zoom_out_action = view_menu.addAction('- Zoom Out')
        #TODO zoom_out_action.triggered.connect(self.zoom_out)

        # Central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_layout = QHBoxLayout()
        central_widget.setLayout(central_layout)

        # Left column
        left_column = QVBoxLayout()
        button_wall = QPushButton('Wall')
        button_door = QPushButton('Door')
        button_window = QPushButton('Window')
        button_wall.setFixedSize(75, 75)
        button_door.setFixedSize(75, 75)
        button_window.setFixedSize(75, 75)
        button_wall.clicked.connect(self.button_wall_clicked)
        button_door.clicked.connect(self.button_door_clicked)
        button_window.clicked.connect(self.button_window_clicked)
        left_column.addWidget(button_wall)
        left_column.addWidget(button_door)
        left_column.addWidget(button_window)

        # Center
        self.editor = Editor()

        # Right column
        right_column = QVBoxLayout()
        button_floor = QPushButton('Floor')
        button_roof = QPushButton('Roof')
        button_furniture = QPushButton('Furniture')
        button_floor.setFixedSize(75, 75)
        button_roof.setFixedSize(75, 75)
        button_furniture.setFixedSize(75, 75)
        button_floor.clicked.connect(self.button_floor_clicked)
        button_roof.clicked.connect(self.button_roof_clicked)
        button_furniture.clicked.connect(self.button_furniture_clicked)
        right_column.addWidget(button_floor)
        right_column.addWidget(button_roof)
        right_column.addWidget(button_furniture)

        central_layout.addLayout(left_column)
        central_layout.addWidget(self.editor)
        central_layout.addLayout(right_column)

        # Bottom statusbar
        self.setStatusBar(QStatusBar(self))

        self.center_window()
        self.show()

    def center_window(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def quit(self):
        self.app.quit()

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