from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QPushButton, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QToolBar, QStatusBar, \
    QApplication


class FloorCreatorWindow (QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Floor Plan Creator')
        self.setMinimumSize(950, 650)

        # Top toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setFixedHeight(25)
        self.addToolBar(toolbar)

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
        center_editor = QWidget()
        center_editor.setStyleSheet("background-color: white;")

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
        central_layout.addWidget(center_editor)
        central_layout.addLayout(right_column)

        # Bottom statusbar
        self.setStatusBar(QStatusBar(self))

        self.center_window()
        self.show()

    def center_window(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

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