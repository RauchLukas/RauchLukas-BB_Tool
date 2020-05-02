from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import tabbox
import graphics

class Model(QAbstractListModel):

    def __init__(self, gradient=None, *args, **kwargs):
        super(Model, self).__init__(*args, **kwargs)

        self.gradients = gradient or []
        self.coordinates = []

        # self.coordsToList([0,1.0012])
        self.addNode(10,5)
        self.addNode(20,5)

    def addNode(self, x, y):
        # Adds a new node to the database
        self.coordsToList([x,y])

    def coordsToList(self, node):
        
        id = len(self.gradients)+1
        self.coordinates.append(node)
        self.gradients.append((True,"Punkt %d:   %s" % (id, str(node))))

        print(self.coordinates)

    def data(self, index, role):

        if role == Qt.DisplayRole:
            id, node = self.gradients[index.row()]

            # Return the Coordinates x, y only
            return node

    def rowCount(self, index):

        # Return the number of given Points
        return len(self.gradients)


class NodeListWidget(QWidget):

    def __init__(self, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        model = model
        
        self.nodelist = QListView()
        # self.nodelist = QStandardItemModel()
        self.nodelist.setModel(model)

        layout = QVBoxLayout()

        self.xIn = QLineEdit()
        self.xIn.setPlaceholderText("0.0")
        self.yIn = QLineEdit()     
        self.yIn.setPlaceholderText("5.0")
        self.addButten = QPushButton("Punkt hinzufügen")
        self.delButten = QPushButton("Punkt löschen")


        gradient_buttens = QGridLayout()
        gradient_buttens.addWidget(QLabel("x [m]"), 1, 0)
        gradient_buttens.addWidget(self.xIn, 1, 1)
        gradient_buttens.addWidget(QLabel("y [m]"), 2, 0)
        gradient_buttens.addWidget(self.yIn, 2, 1)
        gradient_buttens.addWidget(self.addButten, 1, 2)
        gradient_buttens.addWidget(self.delButten, 2, 2)
        buttens = QHBoxLayout()
        buttens.addStretch(1)
        buttens.addLayout(gradient_buttens)

        layout.addWidget(self.nodelist)
        layout.addLayout(buttens)

        self.setLayout(layout)

        self.addButten.pressed.connect(self.add)
        self.delButten.pressed.connect(self.delete)

    def add(self):
        # TDOO cover case: input is str()

        x = self.xIn.text()
        y = self.yIn.text()

        if str(x):
            x = self.convertStr(x)
        if str(y):
            y = self.convertStr(y)

        try:
            if float(x) and float(y):
                self.model.addNode(float(x),float(y))
                self.model.layoutChanged.emit()
                self.xIn.setText("")
                self.yIn.setText("")
        except:
            pass
        
        self.update()
        # self.grafic._triger_refresher()       # TODO fix Update

    def delete(self):
        indexes = self.nodelist.selectedIndexes()
        if indexes:
            index = indexes[0]

            del self.model.gradients[index.row()]
            del self.model.coordinates[index.row()]

            self.model.layoutChanged.emit()
            self.nodelist.clearSelection()
        
        self.update()
        # self.grafic._triger_refresher() # TODO fix Update


    def convertStr(self, s):
        try:
            s.replace(',', '.')
        except:
            pass

        return s




class MainWindow(QMainWindow):

    valueChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Behelfsbrückentool")

        self.model = Model()
        
        self.model.span = 30

        # Load grapics
        self.grafic = graphics.Graphics(self.model)
        # load tabbox widget
        tab_widget = tabbox.TabStack()

        main_layout = QHBoxLayout()

        list_view = NodeListWidget(self.model)


        l_span = 5
        n_laengs = 5

        spann_label = QLabel("Elementspannweite")
        spann_input = QLineEdit()
        spann_input.setPlaceholderText("5.0 m")

        mlc_combo = QComboBox()
        mlc_combo.addItems(["MLC20", "MLC30", "MLC40", "MLC50", "MLC60", "MLC70", "MLC80"])
        lm1_combo = QCheckBox("LM1")
        load_layout = QHBoxLayout()
        load_layout.addWidget(spann_label)
        load_layout.addWidget(spann_input)
        load_layout.addWidget(mlc_combo)
        load_layout.addWidget(lm1_combo)
        load_layout.addStretch(1)
        group1 = QGroupBox("Auswahl der Lastklassen")
        group1.setLayout(load_layout)



        left_layout = QGridLayout()
        right_layout = self.grafic.layout


        left_layout.addWidget(group1, 1, 1)
        left_layout.addWidget(list_view, 2, 1)

        left_layout.addWidget(tab_widget, 3, 0, 1, 2)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        w = QWidget()
        w.setLayout(main_layout)

        self.setCentralWidget(w)
        self.show()










    def _triger_refresh(self):
        self.update()


