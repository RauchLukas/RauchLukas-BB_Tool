from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import Qt

import sys
import ui
import graphicswidget as gw


class Main(QtWidgets.QMainWindow):

    def __init__(self, ):
        super().__init__()

        # # Rename the Main Window
        self.setWindowTitle('Behelfsbrücken Tool')

        layout = QVBoxLayout()

        window = ui.bbToolUi()
        layout.addWidget(window)

        w = QtWidgets.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.show()



if __name__ == '__main__':
    # Main()
    print("Hello UI. Init start sequence.")
    app = QApplication([])
    mainwindow = Main()

    app.exec_()
