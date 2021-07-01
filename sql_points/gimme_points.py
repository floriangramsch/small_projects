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

        fbox = qw.QFormLayout()
        self.statistik_mean = qw.QLabel(str(self.statistik_grade[0]))
        fbox.addRow("Statistik:", self.statistik_mean)

        self.db_mean = qw.QLabel(str(self.datenbanken_grade[0]))
        fbox.addRow("Datenbanken:", self.db_mean)

        self.ps_mean = qw.QLabel(str(self.programmiersprachen_grade[0]))
        fbox.addRow("Programmiersprachen:", self.ps_mean)

        self.mfp2_mean = qw.QLabel(str(self.mfp2_grade[0]))
        fbox.addRow("Mathe für Physiker 2:", self.mfp2_mean)

        self.mmr1_mean = qw.QLabel(str(self.mmr1_grade[0]))
        fbox.addRow("Mathematische Modellierung 1:", self.mmr1_mean)

        self.test_mean = qw.QLabel(str(self.test_grade[0]))
        fbox.addRow("Test:", self.test_mean)

        self.points = qw.QLineEdit()
        self.points.setValidator(qg.QDoubleValidator())
        points_fbox = qw.QFormLayout()
        points_fbox.addRow("Punkte:", self.points)
        self.total = qw.QLineEdit()
        self.total.setValidator(qg.QDoubleValidator())
        total_fbox = qw.QFormLayout()
        total_fbox.addRow("Gesamt:", self.total)
        hbox2 = qw.QHBoxLayout()
        hbox2.addLayout(points_fbox)
        hbox2.addLayout(total_fbox)
        
        self.combo = qw.QComboBox()
        self.combo.addItems(["Test", "Statistik", "Datenbanken", "Programmiersprachen", "MfP2", "MMR1"])
        btn = qw.QPushButton("Update Points")
        btn.clicked.connect(lambda: [self.update()])

        btn_test_zero = qw.QPushButton("Test Zero")
        btn_test_zero.clicked.connect(lambda: self.test_zero())

        hbox1 = qw.QHBoxLayout()
        hbox1.addWidget(btn)
        hbox1.addWidget(self.combo)

        layout = qw.QVBoxLayout()
        layout.addLayout(fbox)
        layout.addLayout(hbox2)
        layout.addLayout(hbox1)
        layout.addWidget(btn_test_zero)
        self.setLayout(layout)

    def update(self):
        btn_insert = f"INSERT INTO {self.combo.currentText()} (points, total) VALUES (%s, %s)"
        self.mycursor.execute(btn_insert, (self.points.text(), self.total.text()))
        self.mydb.commit()

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Statistik;")
        self.statistik_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MMR1;")
        self.mmr1_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MfP2;")
        self.mfp2_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Programmiersprachen;")
        self.ps_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Datenbanken;")
        self.db_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Test;")
        self.test_mean.setText(str(self.mycursor.fetchone()[0]))

        print(f"{self.combo.currentText()} Value Updated!")

    def test_zero(self):
        btn_insert = f"INSERT INTO {self.combo.currentText()} (points, total) VALUES (%s, %s)"
        self.mycursor.execute(btn_insert, (self.points.text(), self.total.text()))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Statistik;")
        self.statistik_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MMR1;")
        self.mmr1_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MfP2;")
        self.mfp2_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Programmiersprachen;")
        self.ps_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Datenbanken;")
        self.db_mean.setText(str(self.mycursor.fetchone()[0]))

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Test;")
        self.test_mean.setText(str(self.mycursor.fetchone()[0]))

        print(f"{self.combo.currentText()} Value Updated!")

    def init_db(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="points"
            )
        # self.mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="flo",
        #     password="2406",
        #     database="points"
        #     )
        self.mycursor = self.mydb.cursor()

        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Statistik;")
        self.statistik_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MMR1;")
        self.mmr1_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from MfP2;")
        self.mfp2_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Programmiersprachen;")
        self.programmiersprachen_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Datenbanken;")
        self.datenbanken_grade = self.mycursor.fetchone()
        self.mycursor.execute("SELECT round((sum(points)/sum(total))*100, 2) as Average from Test;")
        self.test_grade = self.mycursor.fetchone()

app = qw.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
