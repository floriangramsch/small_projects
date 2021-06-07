from dataclasses import dataclass, field
from typing import List

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import math

@dataclass
class Fluid:
    size: int
    scale: int
    iter: int
    dt: float
    diff: float
    visc: float

    def __post_init__(self):
        self.s = [0 for i in range(self.size * self.size)]
        self.density = [0 for i in range(self.size * self.size)]
        self.Vx = [0 for i in range(self.size * self.size)]
        self.Vy = [0 for i in range(self.size * self.size)]
        self.Vx0 = [0 for i in range(self.size * self.size)]
        self.Vy0 = [0 for i in range(self.size * self.size)]

    def addDensity(self, x, y, amount):
        index = self.IX(x, y)
        self.density[index] += amount

    def addVelocity(self, x, y, amountx, amounty):
        index = self.IX(x, y)
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

        self.diffuse(1, Vx0, Vx, visc, dt)
        self.diffuse(2, Vy0, Vy, visc, dt)

        self.project(Vx0, Vy0, Vx, Vy)

        self.advect(1, Vx, Vx0, Vx0, Vy0, dt)
        self.advect(2, Vy, Vy0, Vx0, Vy0, dt)

        self.project(Vx, Vy, Vx0, Vy0)

        self.diffuse(0, s, density, diff, dt)
        self.advect(0, density, s, Vx, Vy, dt)

    def renderD(self, ebene, painter, brush):
        ebene.fill(Qt.transparent)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        color = QtGui.QColor(Qt.blue)
        for i in range(self.size):
            for j in range(self.size):
                d = self.density[self.IX(i, j)]
                # print(d, self.IX(i, j))
                color.setAlpha(255 - d%255)
                brush.setColor(color)
                painter.setBrush(brush)
                x = i * self.scale
                y = j * self.scale
                painter.drawRect(x, y, self.scale, self.scale)

    def renderV(self, ebene, painter, brush):
        ebene.fill(Qt.transparent)
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        color = QtGui.QColor(Qt.black)
        for i in range(self.size):
            for j in range(self.size):
                x = i * self.scale;
                y = j * self.scale;
                vx = self.Vx[self.IX(i, j)];
                vy = self.Vy[self.IX(i, j)];
                # color.setAlpha(d%255)
                # self.canvas.stroke(0);
                brush.setColor(color)
                painter.setBrush(brush)

                if not (abs(vx) < 0.1 and abs(vy) <= 0.1):
                    painter.drawLine(x, y, x + vx * self.scale, y + vy * self.scale)


    def IX(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return x + y * self.size
        return 0

    def lin_solve(self, b, x, x0, a, c):
        cRecip = 1.0 / c
        for k in range(self.iter):
            for j in range(self.size):
                for i in range(self.size):
                    x[self.IX(i, j)] = (x0[self.IX(i, j)] + a *(x[self.IX(i + 1, j)] + x[self.IX(i - 1, j)] + x[self.IX(i, j + 1)] + x[self.IX(i, j - 1)])) * cRecip
        self.set_bnd(b, x)

    def diffuse(self, b, x, x0, diff, dt):
        a = dt * diff * (self.size - 2) * (self.size - 2)
        self.lin_solve(b, x, x0, a, 1 + 6 * a) 

    def project(self, velocX, velocY, p, div):
        for j in range(self.size):
            for i in range(self.size):
                div[self.IX(i, j)] = (-0.5 *
                    (velocX[self.IX(i + 1, j)] -
                        velocX[self.IX(i - 1, j)] +
                        velocY[self.IX(i, j + 1)] -
                        velocY[self.IX(i, j - 1)])) / self.size
                p[self.IX(i, j)] = 0

        self.set_bnd(0, div)
        self.set_bnd(0, p)
        self.lin_solve(0, p, div, 1, 6)

        for j in range(self.size):
            for i in range(self.size):
                velocX[self.IX(i, j)] -= 0.5 * (p[self.IX(i + 1, j)] - p[self.IX(i - 1, j)]) * self.size
                velocY[self.IX(i, j)] -= 0.5 * (p[self.IX(i, j + 1)] - p[self.IX(i, j - 1)]) * self.size

        self.set_bnd(1, velocX)
        self.set_bnd(2, velocY)

    def advect(self, b, d, d0, velocX, velocY, dt):
        dtx = dt * (self.size - 2)
        dty = dt * (self.size - 2)

        Nfloat = self.size - 2

        for j, jfloat in zip(range(self.size), range(self.size)): 
            for i, ifloat in zip(range(self.size), range(self.size)):
                tmp1 = dtx * velocX[self.IX(i, j)]
                tmp2 = dty * velocY[self.IX(i, j)]
                x = ifloat - tmp1
                y = jfloat - tmp2

                if x < 0.5: x = 0.5
                if (x > Nfloat + 0.5): x = Nfloat + 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0
                if (y < 0.5): y = 0.5
                if (y > Nfloat + 0.5): y = Nfloat + 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0 
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                d[self.IX(i, j)] = s0 * (t0 * d0[self.IX(i0i, j0i)] + t1 * d0[self.IX(i0i, j1i)]) + s1 * (t0 * d0[self.IX(i1i, j0i)] + t1 * d0[self.IX(i1i, j1i)])

        self.set_bnd(b, d)

    def set_bnd(self, b, x):
        for i in range(self.size):
            x[self.IX(i, 0)] = b == 2 if -x[self.IX(i, 1)] else x[self.IX(i, 1)]
            x[self.IX(i, self.size - 1)] = b == 2 if -x[self.IX(i, self.size - 2)] else x[self.IX(i, self.size - 2)]

        for j in range(self.size):
            x[self.IX(0, j)] = b == 1 if -x[self.IX(1, j)] else x[self.IX(1, j)]
            x[self.IX(self.size - 1, j)] = b == 1 if -x[self.IX(self.size - 2, j)] else x[self.IX(self.size - 2, j)]


        x[self.IX(0, 0)] = 0.5 * (x[self.IX(1, 0)] + x[self.IX(0, 1)])
        x[self.IX(0, self.size - 1)] = 0.5 * (x[self.IX(1, self.size - 1)] + x[self.IX(0, self.size - 2)])
        x[self.IX(self.size - 1, 0)] = 0.5 * (x[self.IX(self.size - 2, 0)] + x[self.IX(self.size - 1, 1)])
        x[self.IX(self.size - 1, self.size - 1)] = 0.5 * (x[self.IX(self.size - 2, self.size - 1)] + x[self.IX(self.size - 1, self.size - 2)])

