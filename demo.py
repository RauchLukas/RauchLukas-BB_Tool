from PyQt5 import QtCore, QtGui, QtWidgets
from tabbox import TabStack

app = QtWidgets.QApplication([])

stack = TabStack()
stack.show()
app.exec_()