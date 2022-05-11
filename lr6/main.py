import sys
from widget import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    qt_app = app.exec()
    sys.exit(qt_app)
