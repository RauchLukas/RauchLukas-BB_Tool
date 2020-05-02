
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class Graphics(QWidget):

    def __init__(self, *args, **kwargs):
        super(Graphics, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )

        self.setup = dict()
        self.setup = {
            'w' : 600,
            'h' : 250,
            'pad' : 20,
            'span' : 30,
        }
        self.setup['l'] = self.setup['w'] - 2 * self.setup['pad']
        self.setup['fact'] = self.setup['l'] / self.setup['span']

        print("Factor: %f" % self.setup['fact'])
        
        self.group_grapfic = QGroupBox("")
        
        self.nodes = [[5,3], [15,5], [22,4]]
        nodelist = self.makeNodes(self.nodes)
        self.bridge = [nodelist[0], nodelist[-1]]

        self.gradient = GGradient(self.setup)

    def sizeHint(self):
        return QSize(20,400)
    
    def _triger_refresher(self):
        self.update()

    def paintEvent(self, qtEvent):
        
        layout = QVBoxLayout()

        self.g_pixmap = self.makeCanvas("Gradiente")
        q_pixmap = self.makeCanvas("Überbau Querschnitt")
        l_pixmap = self.makeCanvas("System Längssschnitt")

        # self.makeWidget(nodelist)

        layout.addWidget(self.g_pixmap)
        layout.addWidget(q_pixmap)
        layout.addWidget(l_pixmap)
        self.group_grapfic.setLayout(layout)


        self.makeWidget(self.nodes)
        # self.gradient.drawLines(self.g_pixmap, self.bridge, 'brown')
        # self.gradient.drawLines(self.g_pixmap, nodelist, 'green')
        # self.gradient.drawPoints(self.g_pixmap, nodelist)

        # self.g_pixmap.repaint()
        # layout.update()
        self.group_grapfic.setLayout(layout)
    
    def makeWidget(self, nodes):
        self.nodes = nodes
        nodelist = self.makeNodes(self.nodes)
        self.g_pixmap = self.makeCanvas("Gradiente")
        self.gradient.drawLines(self.g_pixmap, self.bridge, 'brown')
        self.gradient.drawLines(self.g_pixmap, nodelist, 'green')
        self.gradient.drawPoints(self.g_pixmap, nodelist)
    



    def placeWidget(self, layout):
        layout.addWidget(self.group_grapfic)

    def makeCanvas(self, label):

        pixmap = QLabel()
        # pixmap.setUpdatesEnabled(True)
        canvas = QPixmap(self.setup['w'], self.setup['h'])
        canvas.fill(QColor("black"))
        pixmap.setPixmap(canvas)

        pixmap = self.labelWidget(pixmap, label)

        return pixmap

    def labelWidget(self, pixmap, label):

        painter = QPainter(pixmap.pixmap())
        pen = painter.pen()
        pen.setColor(QColor('gray'))
        painter.setPen(pen)

        font = painter.font()
        font.setFamily('Latin')
        font.setPointSize(10)
        painter.setFont(font)

        painter.drawText(5, 20, label)
        painter.end()

        return pixmap

    def makeNodes(self, nodelist):

        nodelist = sorted(nodelist, key=lambda x: x[0] )

        out = [[0,0]]
        end = [self.setup['span'], 0]

        if nodelist[0][0] != 0: 
            out.extend(nodelist)
        else:
            out = nodelist
        
        if nodelist[-1][0] != self.setup['span']: 
            out.append(end)
        
        print(out)

        return out

class GGradient(QWidget):

    def __init__(self, setup):
        super().__init__()

        self.setup = setup

        self.nn = self.setup['h'] * 0.33

   
    def drawPoints(self, pixmap, nodes):

        painter = QPainter(pixmap.pixmap())
        pen = painter.pen()
        pen.setWidth(5)
        pen.setColor(QColor('red'))
        painter.setPen(pen)

        for i, co in enumerate(nodes): 
            painter.drawPoint(QPoint(
                            co[0] * self.setup['fact'] + self.setup['pad'],
                            self.nn + co[1] * self.setup['fact']))

        painter.end()

    def drawLines(self,pixmap, nodes, *color): 

        painter = QPainter(pixmap.pixmap())
        
        pen = painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(QColor(*color)))
        painter.setPen(pen)

        for i in range(len(nodes)-1):
            painter.drawLine(
                QPoint(int(nodes[i][0] * self.setup['fact'] + self.setup['pad']),
                    int(nodes[i][1] * self.setup['fact'] + self.nn)),
                QPoint(int(nodes[i+1][0] * self.setup['fact'] + self.setup['pad']),
                    int(nodes[i+1][1] * self.setup['fact'] + self.nn)))

        painter.end()



    # def sizeHint(self):
    #     return QSize(self.w,self.h)

    # def paintEvent(self, e):

    #     self.painter = QPainter(self)

    #     brush = QBrush()
    #     brush.setColor(QColor(self.color))
    #     brush.setStyle(Qt.SolidPattern)

    #     pen = self.painter.pen()
    #     pen.setColor(QColor('gray'))
    #     self.painter.setPen(pen)

    #     font = self.painter.font()
    #     font.setFamily('Latin')#
    #     font.setPointSize(10)
    #     self.painter.setFont(font)

    #     rect = QRect(0, 0, self.painter.device().width(),
    #                       self.painter.device().height())

    #     self.painter.fillRect(rect, brush)
    #     self.painter.drawText(5, 20, "Geländegradiente")

    #     pen.setWidth(2)
    #     pen.setColor(QColor('red'))
    #     self.painter.setPen(pen)

    #     self.painter.end()

    # def drawGradient(self, nodes):

    #     painter = QPainter()

    #     fact = 0.5
    
    #     pen = painter.pen()
    #     pen.setWidth(2)
    #     pen.setColor(QColor('green'))
    #     painter.setPen(pen)

    
    #     for i in range(len(nodes)-1):
    #         painter.drawLin
    #             QPoint(int(nodes[i][0] * fact + self.pad),
    #                    int(nodes[i][1] * fact + self.n),
    #             QPoint(int(nodes[i+1][0] * fact + self.pad),
    #                    int(nodes[i+1][1] * fact + self.nn)))
    
    #     pen.setWidth(5)
    #     pen.setColor(QColor('red'))
    #     painter.setPen(pen)
    
    #     for i, co in enumerate(nodes): 
    #         painter.drawPoint(co[0] * fact + self.pad,
    #                           self.nn + co[1] * fact)
    
    #     pen.setWidth(1)
    #     pen.setColor(QColor('gray'))
    #     painter.setPen(pen)
    #     painter.drawLin
    #         QPoint(int(nodes[0][0] * fact + self.pad),
    #                 int(nodes[0][1] * fact + selfn)),
    #         QPoint(int(nodes[-1][0] * fact + self.pad),
    #                 int(nodes[-1][1] * fact + self.nn))
    #     )

    #     painter.end()


class GCrosssection(QWidget):

    def __init__(self):
        super().__init__()

        self.w = 600
        self.h = 300

        self.color = 'black'


    def sizeHint(self):
        return QSize(self.w,self.h)

    def paintEvent(self, e):

        self.painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')#
        font.setPointSize(10)
        self.painter.setFont(font)

        rect = QRect(0, 0, self.painter.device().width(),
                          self.painter.device().height())

        self.painter.fillRect(rect, brush)
        self.painter.drawText(5, 20, "Überbau Querschnitt")
        self.painter.end()

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

        self.painter = QPainter(self)

        brush = QBrush()
        brush.setColor(QColor(self.color))
        brush.setStyle(Qt.SolidPattern)

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')#
        font.setPointSize(10)
        self.painter.setFont(font)

        rect = QRect(0, 0, self.painter.device().width(),
                          self.painter.device().height())

        self.painter.fillRect(rect, brush)
        self.painter.drawText(5, 20, "System Längsschnitt")
        self.painter.end()

    def _triger_refresher(self):
        self.update()