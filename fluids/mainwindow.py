from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QMainWindow, QMenuBar, QSlider, QSplitter, QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QDialog, QPushButton, QFormLayout, QDesktopWidget, QAction
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor

import random

from Fluid import Fluid
from globals import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluids!")
        self.size = N
        self.window_width = self.size * SCALE
        self.window_height = self.size * SCALE
        self.resize(self.window_width, self.window_height)
        self.pmousex = 0
        self.pmousey = 0
        
        self.initialize_ui()
        self.init()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.fluid.addDensity(a0.x()//SCALE, a0.y()//SCALE, 100)
        amtx = a0.x() - self.pmousex
        amty = a0.y() - self.pmousey
        self.pmousex = a0.x()
        self.pmousey = a0.y()

        self.fluid.addVelocity(a0.x()//SCALE, a0.y()//SCALE, amtx, amty)

    def initialize_ui(self):
        ## Setting up the Window
        # self.centralWidget = QWidget(self)

        self.label = QLabel()
        self.label.resize(self.window_width, self.window_height)
        self.label.setStyleSheet("border: 5px solid black;")
        self.setCentralWidget(self.label)

        self.canvas = QImage(self.window_width, self.window_height, QImage.Format_RGBA8888)
        self.background = QImage(self.window_width, self.window_height, QImage.Format_RGBA8888)

        ## Timer
        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        ## Painter & Brush
        self.painter_canvas = QPainter(self.canvas)
        self.painter_background = QPainter(self.background)
        
        self.brush = QBrush()

    def init(self):
        self.fluid = Fluid(self.size, 0.01, 0, 0)  

    def update(self):
        self.fluid.step()
        self.render()

    def draw_canvas(self):
        self.painter_canvas.fillRect(0, 0, self.window_width, self.window_height, Qt.white)

    def draw_background(self):
        self.fluid.renderD(self.background, self.painter_background, self.brush)
        # self.fluid.renderV(self.background, self.painter_background, self.brush)

    def render(self):
        self.draw_canvas()
        self.draw_background()

        self.painter_canvas.drawImage(0, 0, self.background)
        self.label.setPixmap(QPixmap.fromImage(self.canvas)) 
