
from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class ListWidget(QWidget):

    clickedAddButten = QtCore.pyqtSignal(int)
    clickedDelButten = QtCore.pyqtSignal(int)
    clickedlistItem = QtCore.pyqtSignal(int)

    def __init__(self, nodes, supports):
        super().__init__()

        self.nodes = nodes
        self.supports = supports

    def _createGeograpyWidget(self):
        '''Creates the input widget for the global geography.'''

        self.group_listwidget = QGroupBox("Geländeeingabe")
        layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()

        self.geo_list = QListWidget()
        self.geo_list.setAlternatingRowColors(True)
        self.geo_list.currentRowChanged.connect(self.clickedlistItem.emit)
        x_label = QLabel("x: [m] ")
        y_label = QLabel("y: [m] ")
        self.geo_x = QLineEdit()
        self.geo_x.setPlaceholderText("0.0 m")
        self.geo_y = QLineEdit()
        self.geo_y.setPlaceholderText("1.0 m")
        self.geo_add = QPushButton("Hinzufügen")
        self.geo_add.pressed.connect(self.addListObject)
        self.geo_add.setFixedWidth(70)
        self.geo_del = QPushButton("Löschen")
        self.geo_del.setFixedWidth(70)
        self.geo_del.pressed.connect(self.delListObject)

        row1.addStretch(1)
        row1.addWidget(QLabel("x: [m] "))
        row1.addWidget(self.geo_x)
        row1.addWidget(self.geo_del)
        row2.addStretch(1)
        row2.addWidget(QLabel("y: [m] "))
        row2.addWidget(self.geo_y)
        row2.addWidget(self.geo_add)

        layout.addWidget(self.geo_list)
        layout.addLayout(row1)
        layout.addLayout(row2)

        self.group_listwidget.setLayout(layout)

    def placeWidget(self, layout):

        layout.addWidget(self.group_listwidget)

    def addListObject(self):

        # TDOO cover case: input is str()

        x = self.geo_x.text()
        y = self.geo_y.text()



        if str(x):
            x = self.convertStr(x)
        if str(y):
            y = self.convertStr(y)

        try:
            if float(x) and float(y):
                x = float(x)
                y = float(y)

                if not self.supports[0][0] <= x <=  self.supports[-1][0]:

                    self.geo_x.settext('')
                    self.geo_y.settext('')
                    return

                self.nodes.append([x, y])
                s = (f"GeoPunkt x = {x:.2f} [m], y = {y:.2f} [m]")
                self.geo_list.addItem(s)
        except:
            pass

        self.geo_x.setText('')
        self.geo_y.setText('')

        self.update()
        self.clickedAddButten.emit(0)



    def convertStr(self, s):
        try:
            s.replace(',', '.')
        except:
            pass

        return s


    def delListObject(self):

        row = self.geo_list.currentRow()
        item = self.geo_list.item(row)

        if item is None:
            return
        
        item = self.geo_list.takeItem(row)

        del self.nodes[row]
        del item

        self.update()
        self.clickedDelButten.emit(1)

    def getListItems(self):

        items = []

        for i in range(self.geo_list.count()):
            items.append(self.geo_list.item(i).text())

        return items

