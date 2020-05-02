from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout

import sys
import ui
import graphicswidget as gw
#
#
# class Window(QtWidgets.QMainWindow):

#     def __init__(self, ):
#         super().__init__()

#         layout = QtWidgets.QVBoxLayout()

#         volume = ui.bbToolUi()
#         layout.addWidget(volume)

#         # paint = gw.Graphics()
#         # layout.addWidget(paint)

#         w = QtWidgets.QWidget()
#         w.setLayout(layout)
#         self.setCentralWidget(w)
#         self.show()

# app = QtWidgets.QApplication([])
# window = Window()
# app.exec_()


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


app = QApplication([])
mainwindow = Main()

app.exec_()

    
#
# if __name__ == '__main__':
#     Main()
