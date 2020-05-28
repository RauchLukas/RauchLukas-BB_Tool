from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import random
import copy

import listwidget as lw
import tabwidget as tw
import graphicswidget as gw
from model import Model
from core import Core

class bbToolUi(QWidget):
    '''bbTool's View (GUI)'''
    def __init__(self, *args, **kwargs):
        super(bbToolUi, self).__init__(*args, **kwargs)

        self.model = Model()
        self.core = Core(model=self.model)

        self.support = [[0,0], [30,0]]
        self.model.support = self.support
        
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
        self._indicator = IndicatorWidget(self.model)
        self._controll_unit = QHBoxLayout()

        self.statusbar.addWidget(self._indicator)

        self.save_button = QPushButton('Speichern')
        self.print_button = QPushButton('Drucken')
        self.calc_button = QPushButton('Berechnen')

        self._controll_unit.addWidget(self.save_button)
        self._controll_unit.addWidget(self.print_button)
        self._controll_unit.addWidget(self.calc_button)

        # Import the GUI modula
        self._createLoadWidget()

        self.listwidget = lw.ListWidget(self.model)

        self.listwidget._createGeograpyWidget()
        self.listwidget.placeWidget(self.layoutLeft)

        self.stackwidget = tw.TabWidget(self.model)
        self.stackwidget._createStackWidget()
        self.stackwidget.placeWidget(self.layoutLeft)

        self._graphic = gw.Graphics(self.model)     # retunrs a widget

        # Signals

        self.calc_button.pressed.connect(self._triger_refresh_status)

        self.mlc_class.currentTextChanged.connect(self._triger_refresh_load)
        self.lm1_class.stateChanged.connect(self._triger_refresh_load)

        self.listwidget.clickedAddButten.connect(self._trigger_refresh_add)
        self.listwidget.clickedDelButten.connect(self._trigger_refresh_del)
        # self.listwidget.clickedAddButten.connect(self._trigger_refresh_item)
        # self.listwidget.clickedDelButten.connect(self._trigger_refresh_item)
        self.listwidget.clickedlistItem.connect(self._trigger_refresh_item)

        self.stackwidget.tab_1.elementLengthChanged.connect(self._triger_refresh_system)
        self.stackwidget.tab_1.elementDistChanged.connect(self._triger_refresh_system_dist)
        self.stackwidget.tab_1.geometryChanged.connect(self._trigger_refresh_geo)
        self.stackwidget.tab_1.modelChanged.connect(self._triger_refresh_model)

        self.layoutRight.addWidget(self._graphic)
        self.layoutRight.addLayout(self._controll_unit)

        self.frame.addLayout(self.layoutLeft)
        self.frame.addLayout(self.layoutRight)
        self.frame.addLayout(self.statusbar)

        self.setLayout(self.frame)

    def _triger_refresh_model(self):
        self._triger_refresh_status()

        self._trigger_refresh_geo()
        self.update()


    def _triger_refresh_status(self):
        geo_model = self.stackwidget.tab_1.getModel()

        status = self.core.design()
        self._indicator._triger_refresh(status=status)

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

        self.model._triger_refresh()
        self._graphic.crosssec._triger_refresh_model()

    def _trigger_refresh_del(self):

        self.model._triger_refresh()
        selected_node = [None, None]
        # self._graphic.gradient._triger_refresh(nodes=True, selection=selected_node)
        nodes = self.model.makeNodes(self.model.nodes)
        self._graphic._triger_refresh(nodes=nodes)

    def _trigger_refresh_add(self):

        try:
            self.model.nodes[1]
            nodes = self.model.makeNodes(self.model.nodes)
            self._graphic._triger_refresh(nodes=nodes)
            self.model._triger_refresh()
        except: 
            return
    
    def _trigger_refresh_item(self):

        row = self.listwidget.geo_list.currentRow()

        if row == -1:
            pass
        else:
            item = self.listwidget.geo_list.item(row)
        
            selected_node = self.model.nodes[item.id]
            self._graphic.gradient._triger_refresh(nodes=False, selection=selected_node)

        # # print('id ', item.id)
        #     self.selected_node = [None, None]
        #     nodes = self.model.makeNodes(self.model.nodes)
        #     self._graphic._triger_refresh(nodes=nodes, selection=self.selected_node)
        # else:
        #     # self.selected_node = self.model.nodes[index+1]
        #     # # nodes = self.model.makeNodes(self.model.nodes)
        #     self._graphic._triger_refresh()

    def _createLoadWidget(self):
        '''Creates the load input widget.'''
        group = QGroupBox("Lasteingabe")

        self.mlc_class = QComboBox()
        self.mlc_class.addItems(["MLC20", "MLC30", "MLC40", "MLC50", "MLC60", "MLC70", "MLC80"])
        self.lm1_class = QCheckBox(" LM1 (Zivil)")
        label = QLabel("Bemessungslastklassen: ")

        length_label = QLabel("Überbaulänge")
        self.length = QLineEdit()
        self.length.setPlaceholderText("30.0 m")

        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.mlc_class)
        layout.addWidget(self.lm1_class)
        layout.addWidget(length_label)
        layout.addWidget(self.length)
        layout.addStretch(1)

        group.setLayout(layout)
        self.layoutLeft.addWidget(group)

        self.length.editingFinished.connect(self._length_changed)

        self.mlc_class.currentTextChanged.connect(self.loadClassChanged)
        self.lm1_class.stateChanged.connect(self.loadClassChanged)

        self.load_model['mlc'] = self.mlc_class.currentText()
        self.load_model['lm1'] = self.lm1_class.checkState()

    def _length_changed(self):
        self.update_span()

    def update_span(self):

        try:
            nx = float(self.length.text())
        except:
            self.length.clear()
            
        try: 
            if 0 < nx <= 40:

                self.model.span = nx
                self._update_nodes(nx)
                
            if nx > 40:
                self.length.setText('40.0')
                self._update_nodes(40.0)
            if nx <= 0:
                self.length.setText('1.0')
                self._update_nodes(1.0)
                  
        except:
            pass

    def _update_nodes(self, span):

        if self.model.nodes[-1]:

            del self.model.nodes[-1]

            nodelist = list(self.model.nodes.items())

            for node_id, node in nodelist:

                if node[0] >= span or node[0] >= self.model.support[1][0]:

                    for item_id in range(self.listwidget.geo_list.count()):
                        item = self.listwidget.geo_list.item(item_id)       # 
                        row = self.listwidget.geo_list.row(item)
                        if item.id == node_id:

                            dump.append(row)
                            item = self.listwidget.geo_list.takeItem(row)
                            del item
                            break

                    del self.model.nodes[node_id]

        self.listwidget.geo_list.update()

        self.model.nodes[-1]  = [span, 0]
        self.model.supports = [[0,0], [span, 0]]

        self._triger_refresh_model()
        self._trigger_refresh_add()

    def loadClassChanged(self):
        self.model.setmlc(self.mlc_class.currentText())
        self.model.lm1 = self.lm1_class.checkState()

        self._triger_refresh_model()

    def sPrint(self, s):
        print(s)

class IndicatorWidget(QWidget):
 
    def __init__(self, model, *args, **kwargs):
        super(IndicatorWidget,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.MinimumExpanding,
        )     

        self.color = ['green','red']  

        self.status = False

        self.h = 300
        self.b = 70

        self.model = model
        self.status = True

    def sizeHint(self):
        return QSize(self.b,self.h)

    def _triger_refresh(self,status):
        
        if status <= 1: 
            self.status = 0
        else: 
            self.status = 1

        # self.update()

    def paintEvent(self, event):
        '''Painter function within the GUI loop. Calls all the necessary draw functions.'''

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(self.color[self.status]))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)

        self.painter.end()


