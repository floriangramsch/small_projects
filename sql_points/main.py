import mysql.connector

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

import string
import sys

class MainWindow(qw.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.init_db()

        # self.figure, self.axis = plt.subplots()
        # self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        fbox = qw.QFormLayout()
        fbox.addRow("Statistik:", qw.QLabel(str(self.statistik_grade[0])))
        fbox.addRow("Datenbanken:", qw.QLabel(str(self.datenbanken_grade[0])))
        fbox.addRow("Programmiersprachen:", qw.QLabel(str(self.programmiersprachen_grade[0])))
        fbox.addRow("Mathe für Physiker 2:", qw.QLabel(str(self.mfp2_grade[0])))
        fbox.addRow("Mathematische Modellierung 1:", qw.QLabel(str(self.mmr1_grade[0])))
        fbox.addRow("Test:", qw.QLabel(str(self.test_grade[0])))

        points = qw.QLineEdit()
        points.setValidator(qg.QIntValidator())
        points_fbox = qw.QFormLayout()
        points_fbox.addRow("Punkte:", points)
        total = qw.QLineEdit()
        total.setValidator(qg.QIntValidator())
        total_fbox = qw.QFormLayout()
        total_fbox.addRow("Gesamt:", total)
        hbox2 = qw.QHBoxLayout()
        hbox2.addLayout(points_fbox)
        hbox2.addLayout(total_fbox)
        
        combo = qw.QComboBox()
        combo.addItems(["Test", "Statistik", "Datenbanken", "Programmiersprachen", "MfP2", "MMR1"])
        btn = qw.QPushButton("Update Points")
        btn_insert = f"INSERT INTO {combo.currentText()} (points, total) VALUES (%s, %s)"
        btn.clicked.connect(lambda: [self.mycursor.execute(btn_insert, (points.text(), total.text())), self.mydb.commit(), print("Value Updated!")])
        hbox1 = qw.QHBoxLayout()
        hbox1.addWidget(btn)
        hbox1.addWidget(combo)

        layout = qw.QVBoxLayout()
        layout.addLayout(fbox)
        layout.addLayout(hbox2)
        layout.addLayout(hbox1)
        self.setLayout(layout)

    def init_db(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="points"
            )
        self.mycursor = self.mydb.cursor()

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Statistik;")
        self.statistik_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from mmr1;")
        self.mmr1_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from mfp2;")
        self.mfp2_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from programmiersprachen;")
        self.programmiersprachen_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from datenbanken;")
        self.datenbanken_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Test;")
        self.test_grade = self.mycursor.fetchone()

    def plot(self):
        pass

        # Zeichnen und Anzeige
        # self.axis.plot(x, y, label='Funktion')
        # self.axis.legend()

        # Achtung: keine plt.show!
        # (Neu-)Zeichnen des Canva
        # self.canvas.draw()

if __name__ == '__main__':
    app = qw.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
