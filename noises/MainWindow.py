from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QLabel
from PyQt5.QtGui import QBrush, QColor, QImage, QKeyEvent, QPainter, QPixmap

import random

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

        self.init_mal_zeug()

        # self.draw_random_color()
        self.draw_random_blacks()
        self.label.setPixmap(QPixmap.fromImage(self.canvas))

    def init_mal_zeug(self):
        self.canvas = QImage(900, 900, QImage.Format_RGBA8888)
        self.painter = QPainter(self.canvas)
        self.brush = QBrush()
        self.brush.setStyle(Qt.SolidPattern)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_Q or a0.key() == Qt.Key_Escape:
            self.close()

    def random_color(self):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        a = 255
        r, g, b, a = hex(r)[2:], hex(g)[2:], hex(b)[2:], hex(a)[2:]
        if len(r) == 1:
            r = '0' + r
        if len(g) == 1:
            g = '0' + g
        if len(b) == 1:
            b = '0' + b
        if len(a) == 1:
            a = '0' + a
        hex_code =  '#' + r + g + b

        return hex_code

    def draw_random_color(self):
        for i in range(90):
            for j in range(90):
                color = QColor(self.random_color())
                self.brush.setColor(color)
                self.painter.setBrush(self.brush)
                self.painter.drawRect(i*10, j*10, 10, 10)
                # self.painter.drawPoint(i, j)

    def draw_random_blacks(self):
        for i in range(90):
            for j in range(90):
                color = QColor(Qt.black)
                color.setAlpha(random.randint(0, 255))
                self.brush.setColor(color)
                self.painter.setBrush(self.brush)
                self.painter.drawRect(i*10, j*10, 10, 10)
                # self.painter.drawPoint(i, j)