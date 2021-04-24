from dataclasses import dataclass, field
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import math
from fluid_utils import *

@dataclass
class Fluid:
    size: int
    dt: float
    diff: float
    visc: float

    def __post_init__(self):
        self.s = [0 for i in range(N*N)]
        self.density = [0 for i in range(N*N)]
        self.Vx = [0 for i in range(N*N)]
        self.Vy = [0 for i in range(N*N)]
        self.Vx0 = [0 for i in range(N*N)]
        self.Vy0 = [0 for i in range(N*N)]

    def addDensity(self, x, y, amount):
        index = IX(x, y)
        self.density[index] += amount

    def addVelocity(self, x, y, amountx, amounty):
        index = IX(x, y)
        self.Vx[index] += amountx
        self.Vy[index] += amounty

    def step(self):
        visc = self.visc
        diff = self.diff
        dt = self.dt
        Vx = self.Vx
        Vy = self.Vy
        Vx0 = self.Vx0
        Vy0 = self.Vy0
        s = self.s
        density = self.density

        diffuse(1, Vx0, Vx, visc, dt)
        diffuse(2, Vy0, Vy, visc, dt)

        project(Vx0, Vy0, Vx, Vy)

        advect(1, Vx, Vx0, Vx0, Vy0, dt)
        advect(2, Vy, Vy0, Vx0, Vy0, dt)

        project(Vx, Vy, Vx0, Vy0)

        diffuse(0, s, density, diff, dt)
        advect(0, density, s, Vx, Vy, dt)

    def renderD(self, ebene, painter, brush):
        ebene.fill(Qt.transparent)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        color = QtGui.QColor(Qt.black)
        for i in range(N):
            for j in range(N):
                d = self.density[IX(i, j)]
                # print(d, IX(i, j))
                color.setAlpha(d%255)
                brush.setColor(color)
                painter.setBrush(brush)
                x = i * SCALE
                y = j * SCALE
                painter.drawRect(x, y, SCALE, SCALE)

    def renderV(self, ebene, painter, brush):
        ebene.fill(Qt.transparent)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        color = QtGui.QColor(Qt.black)
        for i in range(N):
            for j in range(N):
                x = i * SCALE;
                y = j * SCALE;
                vx = self.Vx[IX(i, j)];
                vy = self.Vy[IX(i, j)];
                # color.setAlpha(d%255)
                # self.canvas.stroke(0);
                brush.setColor(color)
                painter.setBrush(brush)

                if not (abs(vx) < 0.1 and abs(vy) <= 0.1):
                    painter.drawLine(x, y, x + vx * SCALE, y + vy * SCALE)