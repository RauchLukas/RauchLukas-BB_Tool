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
        self.load_model = dict()
        
        # Set Up the main Layout
        self.frame = QHBoxLayout()
        self.layoutLeft = QVBoxLayout()
        self.layoutRight = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.frame)

        # Import the GUI modula
        self._createLoadWidget()


        self.listwidget = lw.ListWidget(self.nodes, self.supports)

        self.listwidget._createGeograpyWidget()
        self.listwidget.placeWidget(self.layoutLeft)

        self.stackwidget = tw.TabWidget()
        self.stackwidget._createStackWidget()
        self.stackwidget.placeWidget(self.layoutLeft)

        self._graphic = gw.Graphics(self.supports)     # retunrs a widget
        _butten = QPushButton("random")

        # Signals

        self.mlc_class.currentTextChanged.connect(self._triger_refresh_load)
        self.lm1_class.stateChanged.connect(self._triger_refresh_load)

        self.listwidget.clickedAddButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_item)
        self.listwidget.clickedlistItem.connect(self._trigger_refresh_item)

        self.stackwidget.tab_1.geometryChanged.connect(self._trigger_refresh_geo)

        self.layoutRight.addWidget(self._graphic)
        self.layoutRight.addWidget(_butten)

        self.frame.addLayout(self.layoutLeft)
        self.frame.addLayout(self.layoutRight)

        self.setLayout(self.frame)

    def _triger_refresh_load(self):
        self.load_model['mlc'] = self.mlc_class.currentText()
        self.load_model['lm1'] = self.lm1_class.checkState()
        
    def _trigger_refresh_geo(self):     # TODO Hier gehts weiter
        
        self.geo_model = self.stackwidget.tab_1.getModel()

        self._graphic.crosssec._triger_refresh_model(self.geo_model)

    def _trigger_refresh_add(self):

        try:
            self.nodes[0]
            self._graphic._triger_refresh(nodes=self.nodes)
        except: 
            return
    
    def _trigger_refresh_item(self):

        index = self.listwidget.geo_list.currentRow()
        if index == -1:
            self.selected_node = [None, None]
            self._graphic._triger_refresh(nodes=self.nodes, selection=self.selected_node)
        else:
            self.selected_node = self.nodes[index]
            self._graphic._triger_refresh(nodes=self.nodes, selection=self.selected_node)

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

        self.load_model['mlc'] = self.mlc_class.currentText()
        self.load_model['lm1'] = self.lm1_class.checkState()

        
    def sPrint(self, s):
        print(s)



