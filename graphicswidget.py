
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import random


class Graphics(QWidget):

    def __init__(self, nodes, *args, **kwargs):
        super(Graphics,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )       

        self.nodes = nodes

        layout = QVBoxLayout()
        
        self.gradient = GGradient(self.nodes)
        self.crosssec = GCrosssection(self.nodes)

        layout.addWidget(self.gradient)
        layout.addWidget(self.crosssec)

        self.setLayout(layout)
        

    def _triger_refresh(self, nodes=None, selection=None):

        if nodes:
            self.nodes = nodes
        if selection:
            self.selected_node = selection

        self.update()

        self.gradient._triger_refresh(nodes, selection)
        self.crosssec._triger_refresh(nodes, selection)


class GGradient(QWidget):
    
    def __init__(self, nodes, *args, **kwargs):
        super(GGradient,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )       

        self.support = nodes
        self.nodes = []

        self.b = 600
        self.h = 250

        self.x = 200
        self.y = 200

        self.selected_node = [None, None]


    def _triger_refresh(self, nodes, selection):

        if nodes:
            self.nodes = nodes
        if selection:
            self.selected_node = selection

        self.update()
    
    def sizeHint(self):
        return QSize(self.b,self.h)

    def paintEvent(self, event):

        self.b = self.width()
        self.h = self.height()

        self.pad = 20

        nodes = self.makeNodes(self.nodes)
        self.span = self.support[-1][0] - self.support[0][0]
        
        self.l = self.b - 2 * self.pad
        self.fact = self.l / self.span
        self.nn = self.h * 0.25

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('black'))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)


        if self.selected_node[0]:

            pen = QPen()
            pen.setWidth(10)
            pen.setColor(QColor('yellow'))
            self.painter.setPen(pen)
            self.painter.drawPoint(QPoint(
                            self.selected_node[0] * self.fact + self.pad,
                            self.nn + self.selected_node[1] * self.fact))


        pen = self.painter.pen()
        pen.setWidth(3)
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        self.painter.drawLine(
            QPoint(
            nodes[0][0] * self.fact + self.pad,
            nodes[0][1] * self.fact + self.nn),
            QPoint(
            nodes[-1][0] * self.fact + self.pad,
            nodes[-1][1] * self.fact + self.nn)
        )

        pen = self.painter.pen()
        pen.setWidth(5)
        pen.setColor(QColor('red'))
        self.painter.setPen(pen)

        for i, co in enumerate(nodes): 
            self.painter.drawPoint(QPoint(
                            co[0] * self.fact + self.pad,
                            self.nn + co[1] * self.fact))

        pen = self.painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(QColor('dark green')))
        self.painter.setPen(pen)

        for i in range(len(nodes)-1):
            self.painter.drawLine(
                QPoint(int(nodes[i][0] * self.fact + self.pad),
                    int(nodes[i][1] * self.fact + self.nn)),
                QPoint(int(nodes[i+1][0] * self.fact + self.pad),
                    int(nodes[i+1][1] * self.fact + self.nn)))

        self.painter.end()

    def makeNodes(self, nodelist):

        out = [self.support[0]]
        end = self.support[-1]

        if nodelist == []:
            nodelist = out

        if nodelist == [[]]:
            nodelist = out

        if nodelist[0][0] != 0: 
            out.extend(nodelist)

        if out[-1][0] != end[0]: 
            out.append(end)

        out = sorted(out, key=lambda x: x[0] )

        return out

    def placeWidget(self, layout):
        layout.addWidget(self.group_grapfic)


    def labelWidget(self):

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(10)
        self.painter.setFont(font)

        self.painter.drawText(5, 20, "TESTName.")


#
#
#
class GCrosssection(QWidget):

    def __init__(self, nodes, *args, **kwargs):
        super(GCrosssection, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )       

        self.support = nodes
        self.nodes = []

        self.x = 200
        self.y = 200

        self.h = 250
        self.b = 600
        self.pad = 20
        self.span = 30

        self.l = self.b - 2 * self.pad
        self.fact = self.l / self.span

        self.nn = self.h * 0.1


    def _triger_refresh(self, nodes, selection):

        if nodes:
            self.nodes = nodes
        if selection:
            self.selected_node = selection

        self.update()
    
    def sizeHint(self):
        return QSize(self.b,self.h)

    def paintEvent(self, event):

        self.b = self.width()
        self.h = self.height()

        self.pad = 20

        nodes = self.makeNodes(self.nodes)
        self.span = nodes[-1][0] - nodes[0][0]
        
        self.l = self.b - 2 * self.pad
        self.fact = self.l / self.span
        self.nn = self.h * 0.25

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('black'))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)

        pen = self.painter.pen()
        pen.setWidth(5)
        pen.setColor(QColor('red'))
        self.painter.setPen(pen)

        for i, co in enumerate(nodes): 
            self.painter.drawPoint(QPoint(
                            co[0] * self.fact + self.pad,
                            + self.h - self.nn - co[1] * self.fact))

        pen = self.painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(QColor('dark green')))
        self.painter.setPen(pen)

        for i in range(len(nodes)-1):
            self.painter.drawLine(
                QPoint(int(nodes[i][0] * self.fact + self.pad),
                    int(-nodes[i][1] * self.fact + + self.h - self.nn)),
                QPoint(int(nodes[i+1][0] * self.fact + self.pad),
                    int(-nodes[i+1][1] * self.fact + self.h - self.nn)))

        self.painter.end()

    def makeNodes(self, nodelist):

        out = [self.support[0]]
        end = self.support[-1]

        if nodelist == []:
            nodelist = out

        if nodelist == [[]]:
            nodelist = out

        if nodelist[0][0] != 0: 
            out.extend(nodelist)

        if out[-1][0] != end[0]: 
            out.append(end)

        out = sorted(out, key=lambda x: x[0] )

        return out

    def placeWidget(self, layout):
        layout.addWidget(self.group_grapfic)


    def labelWidget(self):

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(10)
        self.painter.setFont(font)

        self.painter.drawText(5, 20, "TESTName.")
#
#
# class GSystem(QWidget):
#
#     def __init__(self):
#         super().__init__()
#
#         self.w = 600
#         self.h = 300
#
#         self.color = 'black'
#
#
#     def sizeHint(self):
#         return QSize(self.w,self.h)
#
#     def paintEvent(self, e):
#
#         self.painter = QPainter(self)
#
#         brush = QBrush()
#         brush.setColor(QColor(self.color))
#         brush.setStyle(Qt.SolidPattern)
#
#         pen = self.painter.pen()
#         pen.setColor(QColor('gray'))
#         self.painter.setPen(pen)
#
#         font = self.painter.font()
#         font.setFamily('Latin')#
#         font.setPointSize(10)
#         self.painter.setFont(font)
#
#         rect = QRect(0, 0, self.painter.device().width(),
#                           self.painter.device().height())
#
#         self.painter.fillRect(rect, brush)
#         self.painter.drawText(5, 20, "System Längsschnitt")
#         self.painter.end()
#
#     def _triger_refresher(self):
#         self.update()