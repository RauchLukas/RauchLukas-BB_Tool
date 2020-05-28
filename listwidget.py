
from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class ListWidget(QWidget):

    clickedAddButten = QtCore.pyqtSignal(int)
    clickedDelButten = QtCore.pyqtSignal(int)
    clickedlistItem = QtCore.pyqtSignal(int)

    def __init__(self, model):
        super().__init__()

        self.model = model
        # self.nodes = nodes
        # self.support = support

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
        self.geo_add.setMinimumWidth(70)
        self.geo_del = QPushButton("Löschen")
        self.geo_del.setMinimumWidth(70)
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

        nodelist = self.model.nodes.keys()
        
        nodecount = 1
        self.model.nodecount += 1
        
        flag = True

        while flag:
            if nodecount in nodelist:
                nodecount += 1
            else:
            
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

                        if not self.model.supports[0][0] <= x <  self.model.supports[-1][0] or not 0 <= y <= 9:

                            self.geo_x.settext('')
                            self.geo_y.settext('')
                            return

                        self.model.nodes[nodecount]  = [x, y]
                        s = QListWidgetItem()
                        # s.setValue(self.model.nodecount)
                        s.setText(f"GeoPunkt x = {x:.2f} [m], y = {y:.2f} [m]")
                        s.id = nodecount
                        self.geo_list.addItem(s)            # TODO Fix give fix index
                except:
                    pass
                break

        # print('added: ', self.model.nodes)

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
        
        id = item.id
        item = self.geo_list.takeItem(row)

        del self.model.nodes[id]
        del item

        self.model.nodecount -= 1

        # print('delet: ', self.model.nodes)

        # self.geo_list.setCurrentItem=False

        self.update()
        self.clickedDelButten.emit(1)

    def getListItems(self):

        items = []

        for i in range(self.geo_list.count()):
            items.append(self.geo_list.item(i).text())

        return items

