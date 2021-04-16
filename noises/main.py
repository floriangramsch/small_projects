from PyQt5.QtWidgets import QApplication

import sys

from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec_())