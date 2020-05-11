from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import random

import listwidget as lw
import tabwidget as tw
import graphicswidget as gw
import model

class bbToolUi(QWidget):
    '''bbTool's View (GUI)'''
    def __init__(self, *args, **kwargs):
        super(bbToolUi, self).__init__(*args, **kwargs)

        self.model = model.Model()

        self.supports = [[0,0], [30,0]]
        self.model.support = self.supports
        
        self.nodes = []

        self.geo_model = dict()
        self.load_model = dict()
        
        # Set Up the main Layout
        self.frame = QHBoxLayout()
        self.layoutLeft = QVBoxLayout()
        self.layoutRight = QVBoxLayout()
        self.statusbar = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self._centralWidget.setLayout(self.frame)
        self._indicator = IndicatorWidget()
        self._controll_unit = QHBoxLayout()

        self.statusbar.addWidget(self._indicator)

        self.save_button = QPushButton('Speichern')
        self.print_button = QPushButton('Drucken')
        self.random_button = QPushButton('Random')

        self._controll_unit.addWidget(self.save_button)
        self._controll_unit.addWidget(self.print_button)
        self._controll_unit.addWidget(self.random_button)

        # Import the GUI modula
        self._createLoadWidget()

        self.listwidget = lw.ListWidget(self.nodes, self.supports)

        self.listwidget._createGeograpyWidget()
        self.listwidget.placeWidget(self.layoutLeft)

        self.stackwidget = tw.TabWidget()
        self.stackwidget._createStackWidget()
        self.stackwidget.placeWidget(self.layoutLeft)

        self._graphic = gw.Graphics(self.model)     # retunrs a widget

        # Signals

        self.random_button.pressed.connect(self._indicator._triger_refresh)

        self.mlc_class.currentTextChanged.connect(self._triger_refresh_load)
        self.lm1_class.stateChanged.connect(self._triger_refresh_load)

        self.listwidget.clickedAddButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_item)
        self.listwidget.clickedlistItem.connect(self._trigger_refresh_item)

        self.stackwidget.tab_1.elementLengthChanged.connect(self._triger_refresh_system)
        self.stackwidget.tab_1.elementDistChanged.connect(self._triger_refresh_system_dist)
        self.stackwidget.tab_1.geometryChanged.connect(self._trigger_refresh_geo)

        self.layoutRight.addWidget(self._graphic)
        self.layoutRight.addLayout(self._controll_unit)

        self.frame.addLayout(self.layoutLeft)
        self.frame.addLayout(self.layoutRight)
        self.frame.addLayout(self.statusbar)

        self.setLayout(self.frame)

    def _triger_refresh_system(self):
        self.model.spacing = float(self.stackwidget.tab_1.com_lt_l.currentText())
        self.model._triger_refresh()

        self._graphic.model = self.model
        self._graphic.system._triger_refresh()
    
    def _triger_refresh_system_dist(self, s):
        self.model.dist = s
        self.model._triger_refresh()

        self._graphic.model = self.model
        self._graphic.system._triger_refresh()

    def _triger_refresh_load(self):
        self.load_model['mlc'] = self.mlc_class.currentText()
        self.load_model['lm1'] = self.lm1_class.checkState()
        
    def _trigger_refresh_geo(self):
        
        self.geo_model = self.stackwidget.tab_1.getModel()

        self._graphic.crosssec._triger_refresh_model(self.geo_model)
        self.model._triger_refresh()

    def _trigger_refresh_add(self):

        try:
            self.nodes[0]
            nodes = self.model.makeNodes(self.nodes)
            self._graphic._triger_refresh(nodes=nodes)
            self.model._triger_refresh()
        except: 
            return
    
    def _trigger_refresh_item(self):

        index = self.listwidget.geo_list.currentRow()
        if index == -1:
            self.selected_node = [None, None]
            nodes = self.model.makeNodes(self.nodes)
            self._graphic._triger_refresh(nodes=nodes, selection=self.selected_node)
        else:
            self.selected_node = self.nodes[index]
            nodes = self.model.makeNodes(self.nodes)
            self._graphic._triger_refresh(nodes=nodes, selection=self.selected_node)

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


class IndicatorWidget(QWidget):
 
    def __init__(self, *args, **kwargs):
        super(IndicatorWidget,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.MinimumExpanding,
        )     

        self.color = ['green','red']  

        self.h = 300
        self.b = 100

        self.status = True

    def sizeHint(self):
        return QSize(self.b,self.h)

    def _triger_refresh(self):
        self.status = random.getrandbits(1)

        self.update()

    def paintEvent(self, event):
        '''Painter function within the GUI loop. Calls all the necessary draw functions.'''

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(self.color[self.status]))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)


        self.painter.end()


