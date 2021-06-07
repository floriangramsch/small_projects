#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_pushButton_clicked()
{
    QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL");
    db.setHostName("127.0.0.1");
    db.setUserName("root");
    db.setPassword("2406");
    db.setDatabaseName("qt6");

    if (db.open()) {
        QMessageBox::information(this, "Connection", "Database Connected Successfully");
    } else {
        QSqlError error = db.lastError();
        QMessageBox::information(this, "Not Connected", "Database is not connected");
    }
}
