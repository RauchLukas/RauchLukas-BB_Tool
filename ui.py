from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import random

import listwidget as lw
import tabwidget as tw
import graphicswidget as gw


class bbToolUi(QWidget):
    '''bbTool's View (GUI)'''
    def __init__(self, *args, **kwargs):
        super(bbToolUi, self).__init__(*args, **kwargs)

        self.supports = [[0,0], [30,0]]
        self.nodes = []

        self.geo_model = dict()
        
        # # Set Up the main Layout
        self.frame = QHBoxLayout()
        self.layoutLeft = QVBoxLayout()
        self.layoutRight = QVBoxLayout()
        self._centralWidget = QWidget(self)
        # Set the central widget for the main window
        self._centralWidget.setLayout(self.frame)
        # self.setCentralWidget(self._centralWidget)

        # Import the GUI modula
        self._createLoadWidget()


        self.listwidget = lw.ListWidget(self.nodes, self.supports)

        self.listwidget._createGeograpyWidget()
        self.listwidget.placeWidget(self.layoutLeft)

        self.stackwidget = tw.TabWidget()
        self.stackwidget._createStackWidget()
        self.stackwidget.placeWidget(self.layoutLeft)
        # self.stackwidget.tab_1.button.pressed.connect(print)

        self._paint = gw.Graphics(self.supports)     # retunrs a widget
        _butten = QPushButton("random")

        # Signals
        _butten.pressed.connect(self._trigger_refresh_add)
        self.listwidget.clickedAddButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_item)
        self.listwidget.clickedlistItem.connect(self._trigger_refresh_item)

        self.stackwidget.tab_1.geometryChanged.connect(self._trigger_refresh_geo)

        self.layoutRight.addWidget(self._paint)
        self.layoutRight.addWidget(_butten)

        self.frame.addLayout(self.layoutLeft)
        self.frame.addLayout(self.layoutRight)

        self.setLayout(self.frame)

        
    def _trigger_refresh_geo(self):     # TODO Hier gehts weiter
        
        self.geo_model = self.stackwidget.tab_1.getModel()

        self._paint.crosssec._triger_refresh_model(self.geo_model)

    def _trigger_refresh_add(self):

        try:
            self.nodes[0]
            self._paint._triger_refresh(nodes=self.nodes)
        except: 
            return
    
    def _trigger_refresh_item(self):

        index = self.listwidget.geo_list.currentRow()
        if index == -1:
            self.selected_node = [None, None]
            self._paint._triger_refresh(nodes=self.nodes, selection=self.selected_node)
        else:
            self.selected_node = self.nodes[index]
            self._paint._triger_refresh(nodes=self.nodes, selection=self.selected_node)

    def _createLoadWidget(self):
        '''Creates the load input widget.'''
        group = QGroupBox("Lasteingabe")

        self.mlc_class = QComboBox()
        self.mlc_class.addItems(["MLC20", "MLC30", "MLC40", "MLC50", "MLC60", "MLC70", "MLC80"])
        self.lm1_class = QCheckBox(" LM1 (Zivil)")
        label = QLabel("Bemessungslastklassen: ")

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.mlc_class)
        layout.addWidget(self.lm1_class)
        layout.addStretch(1)

        group.setLayout(layout)
        self.layoutLeft.addWidget(group)

    def _createGraphicWidget(self):
        self.graphic_dummy = QLabel("Graphic Widget Dummy.")

        self.layoutRight.addWidget(self.graphic_dummy)

    def sPrint(self, s):
        print(s)
    # def addListObject(self, s):
    #     self.geo_list.addItem(s)


    # def _createGeograpyWidget(self):
    #     '''Creates the input widget for the global geography.'''

    #     group = QGroupBox("Geländeeingabe")
    #     layout = QVBoxLayout()
    #     row1 = QHBoxLayout()
    #     row2 = QHBoxLayout()

    #     self.geo_list = QListWidget()
    #     self.geo_list.setAlternatingRowColors(True)
    #     x_label = QLabel("x: [m] ")
    #     y_label = QLabel("y: [m] ")
    #     self.geo_x = QLineEdit()
    #     self.geo_x.setPlaceholderText("0.0 m")
    #     self.geo_y = QLineEdit()
    #     self.geo_y.setPlaceholderText("1.0 m")
    #     self.geo_add = QPushButton("Hinzufügen")
    #     self.geo_add.setFixedWidth(70)
    #     self.geo_del = QPushButton("Löschen")
    #     self.geo_del.setFixedWidth(70)

    #     row1.addStretch(1)
    #     row1.addWidget(QLabel("x: [m] "))
    #     row1.addWidget(self.geo_x)
    #     row1.addWidget(self.geo_add)
    #     row2.addStretch(1)
    #     row2.addWidget(QLabel("y: [m] "))
    #     row2.addWidget(self.geo_y)
    #     row2.addWidget(self.geo_del)

    #     layout.addWidget(self.geo_list)
    #     layout.addLayout(row1)
    #     layout.addLayout(row2)

    #     group.setLayout(layout)

    #     self.layoutLeft.addWidget(group)




    # def _createStackWidget(self):
    #     self.stack = QTabWidget()

    #     self.tab_1 = QWidget()
    #     self.tab_1.layout = QVBoxLayout()
    #     self.tab_1.setLayout(self.tab_1.layout)

    #     self.tab_2 = QWidget()
    #     self.tab_2.layout = QVBoxLayout()
    #     self.tab_2.setLayout(self.tab_2.layout)
    #     self.tab_3 = QWidget()
    #     self.tab_3.layout = QVBoxLayout()
    #     self.tab_3.setLayout(self.tab_3.layout)

    #     self._createMaterialWidget()
    #     self._createGeometryTopWidget()
    #     self._createGeometryBotWidget()
    #     self._createFoundationWidget()

    #     self.stack.addTab(self.tab_1, "Überbau")
    #     self.stack.addTab(self.tab_2, "Unterbau")
    #     self.stack.addTab(self.tab_3, "Gründung")

    #     self.layoutLeft.addWidget(self.stack)

    # def _createMaterialWidget(self):
    #     # Create dummy material widget
    #     self.tab_1.layout.addWidget(QLabel("Material Dummy Widget"))
    #     self.tab_2.layout.addWidget(QLabel("Material Dummy Widget"))

    # def _createGeometryTopWidget(self):
    #     # Create dummy Überbau widget
    #     self.tab_1.layout.addWidget(QLabel("Geomertrie Überbau Dummy Widget"))

    # def _createGeometryBotWidget(self):
    #     # Create dummy Unterbau widget
    #     self.tab_2.layout.addWidget(QLabel("Geomertrie Unterbau Dummy Widget"))

    # def _createFoundationWidget(self):
    #     # Create dummy Unterbau widget
    #     self.tab_3.layout.addWidget(QLabel(" Grüngung Dummy Widget"))
