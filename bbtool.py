from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import MainWindow

app = QtWidgets.QApplication([])

mainwindow = MainWindow()
mainwindow.show()
app.exec_()