from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QLabel, QWidget
from PyQt5.QtGui import QBrush, QImage, QKeyEvent, QPainter, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(900, 900)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.label = QLabel("JASDL:")
        # self.centralWidget = QWidget(self)
        self.setCentralWidget(self.label)

        self.draw()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_Q or a0.key() == Qt.Key_Escape:
            self.close()

    def draw(self):
        self.canvas = QImage(900, 900, QImage.Format_RGBA8888)
        self.painter = QPainter(self.canvas)
        self.brush = QBrush()

        self.painter.fillRect(0, 0, 100, 100, Qt.black)
        self.label.setPixmap(QPixmap.fromImage(self.canvas))