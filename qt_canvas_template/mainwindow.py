from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QMenuBar, QSlider, QSplitter, QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QDialog, QPushButton, QFormLayout, QDesktopWidget, QAction
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor

import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width = 900
        self.window_height = 900
        self.resize(self.window_width, self.window_height)
        
        self.initialize()

    def initialize(self):
        ## Setting up the Window
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.label = QLabel()
        self.label.resize(self.window_width, self.window_height)
        self.label.setStyleSheet("border: 5px solid black;")

        self.hbox = QHBoxLayout(self.centralWidget)
        self.hbox.addWidget(self.label)

        self.centralWidget.setLayout(self.hbox)

        self.canvas = QImage(self.window_width, self.window_height, QImage.Format_RGBA8888)
        self.background = QImage(self.window_width, self.window_height, QImage.Format_RGBA8888)

        ## Timer
        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.update)
        self.timer.start(300)

        ## Painter & Brush
        self.painter_canvas = QPainter(self.canvas)
        self.painter_background = QPainter(self.background)
        
        self.brush = QBrush()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
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

    def update(self):
        self.render()

    def draw_canvas(self):
        self.painter_canvas.fillRect(0, 0, self.window_width, self.window_height, Qt.white)
        
    def draw_background(self):
        self.background.fill(Qt.transparent)
        color = QColor(Qt.green)
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(color)
        self.painter_background.setBrush(self.brush)
        self.painter_background.drawRoundedRect(QRect(200, 200, 70, 80), 2, 2)

    def render(self):
        self.draw_canvas()
        self.draw_background()

        self.painter_canvas.drawImage(0, 0, self.background)
        self.label.setPixmap(QPixmap.fromImage(self.canvas)) 
