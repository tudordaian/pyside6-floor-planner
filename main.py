from PySide6.QtWidgets import QApplication
from app_window import FloorCreatorWindow

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FloorCreatorWindow()
    sys.exit(app.exec())