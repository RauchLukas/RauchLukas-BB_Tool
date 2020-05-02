
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Graphics(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = model

        self.layout = QVBoxLayout()

        self.gradient = GGradient(self.model)
        self.crosssection = GCrosssection()
        self.system = GSystem()

        self.layout.addWidget(self.gradient)
        self.layout.addWidget(self.crosssection)
        self.layout.addWidget(self.system)

    def _triger_refresher(self):
        self.update()
        self.gradient._triger_refresher()


class GGradient(QWidget):

    def __init__(self, model):
        super().__init__()

        self.model = model

        self.nodes = [[0,0]]
        self.nodes.extend(model.coordinates)
        self.nodes.append([self.model.span, 0])
        # Sort nodes by x-value
        self.nodes = sorted(self.nodes, key=lambda x: x[0])

        self.w = 600
        self.h = 300

        self.pad = 20
        self.l = self.w - 2 * self.pad
        self.nn = 50 # self.h / 2

        self.fac = self.l / self.model.span
        
        self.color = 'black'


    def sizeHint(self):
        return QSize(self.w,self.h)

    def paintEvent(self, e):

        painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        pen = painter.pen()
        pen.setColor(QColor('gray'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Latin')#
        font.setPointSize(10)
        painter.setFont(font)

        rect = QRect(0, 0, painter.device().width(),
                          painter.device().height())

        painter.fillRect(rect, brush)
        painter.drawText(5, 20, "Geländegradiente")

        pen.setWidth(2)
        pen.setColor(QColor('red'))
        painter.setPen(pen)

        self.drawGradient(painter)

        painter.end()

    def _triger_refresher(self):
        self.update()

    def drawGradient(self, painter):
        nodes = self.nodes

        pen = painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor('green'))
        painter.setPen(pen)

        for i in range(len(nodes)-1):
            painter.drawLine(
                QPoint(int(nodes[i][0] * self.fac + self.pad),
                       int(nodes[i][1] * self.fac + self.nn)),
                QPoint(int(nodes[i+1][0] * self.fac + self.pad),
                       int(nodes[i+1][1] * self.fac + self.nn)))

        pen.setWidth(5)
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        
        for i, co in enumerate(nodes):
            painter.drawPoint(co[0] * self.fac + self.pad,
                              self.nn + co[1] * self.fac)

        pen.setWidth(1)
        pen.setColor(QColor('gray'))
        painter.setPen(pen)
        painter.drawLine(
            QPoint(int(nodes[0][0] * self.fac + self.pad),
                    int(nodes[0][1] * self.fac + self.nn)),
            QPoint(int(nodes[-1][0] * self.fac + self.pad),
                    int(nodes[-1][1] * self.fac + self.nn))
        )


class GCrosssection(QWidget):

    def __init__(self):
        super().__init__()

        self.w = 600
        self.h = 300

        self.color = 'black'


    def sizeHint(self):
        return QSize(self.w,self.h)

    def paintEvent(self, e):

        painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        pen = painter.pen()
        pen.setColor(QColor('gray'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Latin')#
        font.setPointSize(10)
        painter.setFont(font)

        rect = QRect(0, 0, painter.device().width(),
                          painter.device().height())

        painter.fillRect(rect, brush)
        painter.drawText(5, 20, "Überbau Querschnitt")
        painter.end()

    def _triger_refresher(self):
        self.update()


class GSystem(QWidget):

    def __init__(self):
        super().__init__()

        self.w = 600
        self.h = 300

        self.color = 'black'


    def sizeHint(self):
        return QSize(self.w,self.h)

    def paintEvent(self, e):

        painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        pen = painter.pen()
        pen.setColor(QColor('gray'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Latin')#
        font.setPointSize(10)
        painter.setFont(font)

        rect = QRect(0, 0, painter.device().width(),
                          painter.device().height())

        painter.fillRect(rect, brush)
        painter.drawText(5, 20, "System Längsschnitt")
        painter.end()

    def _triger_refresher(self):
        self.update()