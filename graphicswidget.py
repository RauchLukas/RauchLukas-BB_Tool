
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import math
import numpy as np


class Graphics(QWidget):

    def __init__(self, model, *args, **kwargs):
        super(Graphics,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )       

        self.model = model
        self.nodes = model.supports
        self.spacing = model.spacing

        layout = QVBoxLayout()
        
        self.gradient = GGradient(self.model)
        self.crosssec = GCrosssection()
        self.system = GSystem(self.model)
        layout.addWidget(self.gradient)
        layout.addWidget(self.crosssec)
        layout.addWidget(self.system)

        self.setLayout(layout)
        

    def _triger_refresh(self, nodes=None, selection=None):

        if nodes:
            self.nodes = nodes
        if selection:
            self.selected_node = selection

        self.update()

        self.gradient._triger_refresh(self.nodes, selection)
        self.system._triger_refresh()


class GSystem(QWidget):
    '''Class containing all functions for visualization of the static system Qwidget. '''
    
    def __init__(self, model, *args, **kwargs):
        super(GSystem,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )       

        self.model = model
        self.nodes = model.nodes
        self.support = model.supports

        self.b = 600
        self.h = 250
        self.pad = 50

        self.gap = 10
        
        self.span = model.span
        self.spacing = 3.5
        self.krag = model.krag

        self.h_fac = 0.03

    def sizeHint(self):
        return QSize(self.b,self.h)

    def _triger_refresh(self):

        parent = self.parent()

        self.nodes = parent.nodes
        self.spacing = parent.spacing

        self.update()


    def paintEvent(self, event):
        '''Painter function within the GUI loop. Calls all the necessary draw functions.'''

        span = self.model.span
        spacing = self.model.spacing

        col_pos = self.model.col_pos
        col_height = self.model.col_height

        self.b = self.width()
        self.h = self.height()

        self.l = self.b - 2 * self.pad
        self.fact = self.l / self.span
        nn = self.h * 0.15      # TODO 
        self.nn = nn            #TODO fix this

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('black'))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)

        self.drawGradientLines()

        pen = self.painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor('white'))
        self.painter.setPen(pen)

        for i in range(len(col_pos)-1):
            self.painter.drawLine(
                QPoint(int(col_pos[i] * self.fact + self.pad + self.gap/2), nn), 
                QPoint(int(col_pos[i+1] * self.fact + self.pad - self.gap/2), nn))

        pen.setWidth(1)
        pen.setColor(QColor('red'))
        self.painter.setPen(pen)

        for i in range(len(col_pos)):
            self.circle(col_pos[i]* self.fact + self.pad, nn, 3, self.painter)

        self.sliderSupport(col_pos[-1]* self.fact + self.pad, nn, 3, self.h*self.h_fac, self.painter)
        self.fixedSupport(col_pos[0]* self.fact + self.pad, nn, 3, self.h*self.h_fac, self.painter)

        for i in range(len(col_pos)-2):
            self.unterbau(col_pos[i+1]* self.fact + self.pad, nn, col_height[i+1] * self.fact ,3 , self.painter)
        
        self.labelWidget()

        self.painter.end()
    
    def circle(self, x, y, r, painter):

        x0 = x-r
        y0 = y-r

        painter.drawEllipse(x0, y0, 2*r, 2*r)

    def sliderSupport(self, x, y, r, h, painter):

        x0 = x
        y0 = y+r

        painter.drawLine(x0, y0, x0+h/2, y0+h)
        painter.drawLine(x0, y0, x0-h/2, y0+h)
        painter.drawLine(x0+h/2, y0+h, x0-h/2, y0+h)
        painter.drawLine(x0+1.75*h/2, y0+1.50*h, x0-1.75*h/2, y0+h*1.50)

    def fixedSupport(self, x, y, r, h, painter):

        old_painter = painter

        n = 4
        b = 1.75*h/2

        x0 = x
        y0 = y+r

        painter.drawLine(x0, y0, x0+h/2, y0+h)
        painter.drawLine(x0, y0, x0-h/2, y0+h)
        painter.drawLine(x0+h/2, y0+h, x0-h/2, y0+h)
        painter.drawLine(x0+b, y0+1.50*h, x0-b, y0+h*1.50)

        h1 = 0.5 * h
        inc = b / n
        
        for i in range(n):
            painter.drawLine(x0+-b+2*inc*i, y0+1.50*h+h1, x0+-b+2*inc*(i+1), y0+1.50*h)

    def unterbau(self, x, y, h, r, painter): 
        
        painter_old = painter
        pen = painter.pen()        
        
        x1 = x-self.krag * self.fact
        x2 = x+self.krag * self.fact
        y1 = y-r
        y2 = y-r

        pen.setColor(QColor('red'))
        painter.setPen(pen)

        self.circle(x1, y1+2*r, r, painter)
        self.circle(x2, y2+2*r, r, painter)

        if h != 0:
            self.circle(x1, y1+r+h, r, painter)
            self.circle(x2, y2+r+h, r, painter)
            self.sliderSupport(x1, y1+2*r+h, r, self.h_fac*self.h, painter)
            self.sliderSupport(x2, y2+2*r+h, r, self.h_fac*self.h, painter)
        
            pen.setColor(QColor('white'))
            painter.setPen(pen)
            painter.drawLine(x1, y1+r, x1, y1+h-1)
            painter.drawLine(x2, y2+r, x2, y2+h-1)

        else:
            self.sliderSupport(x1, y1, r, self.h_fac*self.h, painter)
            self.sliderSupport(x2, y2, r, self.h_fac*self.h, painter)

    def drawGradientLines(self):
        '''Function to draw the gradient lines of the global geography.'''
                
                
        nodes = self.makeNodes(self.nodes)   

        pen = self.painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(QColor('dark gray')))
        self.painter.setPen(pen)

        for i in range(len(nodes)-1):
            self.painter.drawLine(
                QPoint(int(nodes[i][0] * self.fact + self.pad),
                    int(nodes[i][1] * self.fact + self.nn)),
                QPoint(int(nodes[i+1][0] * self.fact + self.pad),
                    int(nodes[i+1][1] * self.fact + self.nn)))

    ### TODO dont copy this one from GGRadient
    def makeNodes(self, nodelist):
        '''Collecting the actual node list and the support coordinates making one sorted nodelist.'''

        out = [self.support[0]]
        end = self.support[-1]

        # Check if Nodelist is empty 
        #   -> In case: make it [0,0]
        if nodelist == []:
            nodelist = out
        if nodelist == [[]]:
            nodelist = out
        # If nodelist is NOT empty, but dose not has [0,0] in first place
        #   -> Append it to [0,0]
        if nodelist[0][0] != 0: 
            out.extend(nodelist)
        else: 
        #   -> In Case nodelist has [0,0] just copy it
            out = nodelist
        if out[-1][0] != end[0]: 
            out.append(end)

        out = sorted(out, key=lambda x: x[0] )

        return out


    def labelWidget(self):
        '''Prints the label onto the widget.'''

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')
        h = int(self.h / 30)
        font.setPointSize(h)
        self.painter.setFont(font)

        self.painter.drawText(5, 2*h, "Statisches System.")


class GGradient(QWidget):
    '''Class containing all functions for visualization of the gradient Qwidget. '''
    
    def __init__(self, model, *args, **kwargs):
        super(GGradient,self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding,
        )       

        self.model = model

        self.support = model.supports
        self.nodes = model.supports

        self.b = 600
        self.h = 250
        self.pad = 50

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
        '''Painter function within the GUI loop. Calls all the necessary draw functions.'''

        self.b = self.width()
        self.h = self.height()

        self.nodes = self.makeNodes(self.nodes)

        self.span = self.model.span 
        
        self.l = self.b - 2 * self.pad
        self.fact = self.l / self.span
        self.nn = self.h * 0.25

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('black'))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)

        self.labelWidget()
        self.drawGradientIndicater()
        self.drawGradientBridge()
        self.drawGradientPoints()
        self.drawGradientLines()

        # Label Brückenspannweite
        pen = self.painter.pen()
        pen.setWidth(1)
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(8)
        self.painter.setFont(font)

        self.painter.drawLine(
            QPoint(
            self.nodes[0][0] * self.fact + self.pad - self.h/50,
            self.nodes[0][1] * self.fact + self.nn-self.h/15),
            QPoint(
            self.nodes[-1][0] * self.fact + self.pad + self.h/50,
            self.nodes[-1][1] * self.fact + self.nn - self.h/15)
        )

        for i in range(2):
            self.painter.drawLine(
            QPoint(
            (self.nodes[0][0] + self.span * i)  * self.fact + self.pad,
            self.nn - 1.3*self.h/15),
            QPoint(
            (self.nodes[0][0] + self.span * i)  * self.fact + self.pad,
            self.nn - 0.7*self.h/15),
            )

        self.painter.drawText(
            QPointF(self.b/2-12, self.nn-self.h/10),
            (f"{self.span:.2f}")
        )

        self.painter.end()

    def drawGradientIndicater(self):
        '''Function to draw the hightlight effect of the selected node.'''

        if self.selected_node[0]:

            pen = self.painter.pen()
            pen.setWidth(10)
            pen.setColor(QColor('yellow'))
            self.painter.setPen(pen)
            self.painter.drawPoint(QPoint(
                            self.selected_node[0] * self.fact + self.pad,
                            self.nn + self.selected_node[1] * self.fact))

    def drawGradientBridge(self):
        '''Function to draw the bridge gradient between the supports.'''

        pen = self.painter.pen()
        pen.setWidth(3)
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        self.painter.drawLine(
            QPoint(
            self.nodes[0][0] * self.fact + self.pad,
            self.nodes[0][1] * self.fact + self.nn),
            QPoint(
            self.nodes[-1][0] * self.fact + self.pad,
            self.nodes[-1][1] * self.fact + self.nn)
        )

    def drawGradientPoints(self):
        '''Function to draw the gradient points of the global geography.'''
        pen = self.painter.pen()
        pen.setWidth(5)
        pen.setColor(QColor('red'))
        self.painter.setPen(pen)

        for i, co in enumerate(self.nodes): 
            self.painter.drawPoint(QPoint(
                            co[0] * self.fact + self.pad,
                            self.nn + co[1] * self.fact))

    def drawGradientLines(self):
        '''Function to draw the gradient lines of the global geography.'''

        pen = self.painter.pen()
        pen.setWidth(2)
        pen.setColor(QColor(QColor('dark green')))
        self.painter.setPen(pen)

        for i in range(len(self.nodes)-1):
            self.painter.drawLine(
                QPoint(int(self.nodes[i][0] * self.fact + self.pad),
                    int(self.nodes[i][1] * self.fact + self.nn)),
                QPoint(int(self.nodes[i+1][0] * self.fact + self.pad),
                    int(self.nodes[i+1][1] * self.fact + self.nn)))

    def makeNodes(self, nodelist):
        '''Collecting the actual node list and the support coordinates making one sorted nodelist.'''

        out = [self.support[0]]
        end = self.support[-1]

        # Check if Nodelist is empty 
        #   -> In case: make it [0,0]
        if nodelist == []:
            nodelist = out
        if nodelist == [[]]:
            nodelist = out
        # If nodelist is NOT empty, but dose not has [0,0] in first place
        #   -> Append it to [0,0]
        if nodelist[0][0] != 0: 
            out.extend(nodelist)
        else: 
        #   -> In Case nodelist has [0,0] just copy it
            out = nodelist
        if out[-1][0] != end[0]: 
            out.append(end)

        out = sorted(out, key=lambda x: x[0] )

        return out

    def labelWidget(self):
        '''Prints the label onto the widget.'''

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        h = int(self.h / 30)
        b = int(self.b / 120)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(h)
        self.painter.setFont(font)

        self.painter.drawText(b, 2*h, "Geändegradiente.")


class GCrosssection(QWidget):
    '''Class containing all functions for visualization of the crosssection plot Qwidget. '''
    
    def __init__(self, *args, **kwargs):
        super(GCrosssection, self).__init__(*args, **kwargs)

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding,
        )

        self.h = 250
        self.b = 600
        self.hc = self.h * 0.5
        self.bc = self.b * 0.5
        self.pad = 50
        self.nn = self.h * 0.3

        self.lr_b = 4.0

        self.lt_n = 8
        self.lt_h = 0.24
        self.lt_b = 0.18

        self.tb_t = 0.10
        self.fb_t = 0.04

        self.rb_h = 0.20
        self.rb_b = 0.20

        self.ub_krag = 1.0
        self.ub_b = self.lr_b + 2 * self.rb_b + 2 * self.ub_krag
        
        self.gt_h = 1.00
        self.gt_t = 0.08
        self.gt_d = self.gt_h * 0.7
        self.gt_b = self.gt_t
        self.alpha = 60
        self.gp_h = 0.10
        self.gp_t = 0.04

        self.b_tot = self.b - 2 * self.pad
        self.fact = self.b_tot / self.ub_b

        self.model = dict()
        self.model['m_tb'] = "c16"
        self.model['m_lt'] = "c24"

    def _triger_refresh_model(self, model):

        self.model = model

        for key, val in model.items():
            try:
                setattr(self, key, float(val))
            except:
                pass

        self.ub_b = self.lr_b + 2 * self.rb_b + 2 * self.ub_krag

        self.update()

    def paintEvent(self, event):

        self.b = self.width()
        self.h = self.height()

        self.hc = self.h * 0.7
        self.bc = self.b * 0.5

        self.b_tot = self.b - 2 * self.pad

        fct = self.b_tot / self.ub_b
        self.nn = self.h * 0.6

        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor('black'))
        brush.setStyle(Qt.SolidPattern)
        rect = QRect(0, 0, self.painter.device().width(), self.painter.device().height())
        self.painter.fillRect(rect, brush)

        pen = self.painter.pen()
        pen.setWidth(1)
        pen.setColor(QColor('light blue'))
        self.painter.setPen(pen)

        # Draw Tragbelag
        rect = QRectF(
            QPointF(
                (self.bc - (self.ub_b / 2)  * fct),
                (self.hc - (self.tb_t)      * fct),
            ),
            QSizeF(
                (self.ub_b * fct),
                (self.tb_t * fct)
            )
        )
        self.painter.drawRect(rect)

        # Draw Fahrbahnbelag
        b = self.lr_b * fct

        rect = QRectF(
            QPointF(self.bc -b / 2, self.hc - (self.fb_t + self.tb_t) * fct
            ),
            QSizeF(b, self.fb_t * fct
            )
        )
        self.painter.drawRect(rect)

        # Draw Längsträger
        b0 = 0.5 * (self.lr_b + self.rb_b + self.lt_b)
        b = (self.lr_b + self.rb_b)
        dy = b / (self.lt_n-1)

        for i in range(int(self.lt_n)):
            rect = QRectF(
                QPointF(self.bc - (b0 - i * dy) * fct, self.hc,
                ),
                QSizeF(self.lt_b * fct, self.lt_h * fct
                )
            )
            self.painter.drawRect(rect)

        # Draw Rödelbalken
        dy = (self.lr_b + self.rb_b) * fct
        x0 = self.bc - 0.5 * (self.lr_b + 2 * self.rb_b)  * fct
        
        for i in range(2):
            rect = QRectF(
                QPointF(
                    x0 + dy * i,
                    self.hc - (self.tb_t + self.rb_h) * fct,
                ),
                QSizeF(
                    (self.rb_b * fct),
                    (self.rb_h * fct)
                )
            )
            self.painter.drawRect(rect)

        # Draw Geländer
        b = (self.lr_b + 2 * self.rb_b + 2 * self.gt_b) * fct
        dy = b - self.gt_b * fct
       
        for i in range(2):
            rect = QRectF(
                QPointF(
                    self.bc - b / 2 + dy * i,
                    self.hc - (self.tb_t + self.gt_h) * fct,
                ),
                QSizeF(
                    (self.gt_t * fct),
                    (self.gt_h * fct)
                )
            )
            self.painter.drawRect(rect)

        # Draw Abstützung
        alpha = math.radians(self.alpha)
        e_u = (self.gt_b / math.sin(alpha))
        e_o = (self.gt_b / math.cos(alpha))
        do1 = 0.8 * self.gt_h
        do2 = do1 - e_o
        du1 = math.atan(alpha) * do1
        du2 = math.atan(alpha) * do2

        b0u1 = (0.5 * self.lr_b + self.rb_b +self.gt_t + du1) * fct
        b0u2 = (0.5 * self.lr_b + self.rb_b +self.gt_t + du2) * fct
        h0u1 = self.tb_t * fct
        h0u2 = self.tb_t * fct
        b0o1 = (0.5 * self.lr_b + self.rb_b +self.gt_t) * fct
        b0o2 = (0.5 * self.lr_b + self.rb_b +self.gt_t) * fct
        h0o1 = (self.tb_t + do1) * fct
        h0o2 = (self.tb_t + do2) * fct

        self.painter.drawLine(
            self.bc - b0u1, self.hc - h0u1,
            self.bc - b0o1, self.hc - h0o1,
        )
        self.painter.drawLine(
            self.bc - b0u2, self.hc - h0u2,
            self.bc - b0o2, self.hc - h0o2,
        )
        self.painter.drawLine(
            self.bc + b0u1, self.hc - h0u1,
            self.bc + b0o1, self.hc - h0o1,
        )
        self.painter.drawLine(
            self.bc + b0u2, self.hc - h0u2,
            self.bc + b0o2, self.hc - h0o2,
        )

        # Draw Geländerplanke 
        b = (self.lr_b + 2 * self.rb_b) * fct
        dy = (self.lr_b + 2 * self.rb_b - self.gp_t) * fct
       
        for i in range(2):
            rect = QRectF(
                QPointF(
                    self.bc - b / 2 + dy * i,
                    self.hc - (self.tb_t + self.gt_h * 0.95) * fct,
                ),
                QSizeF(
                    (self.gp_t * fct),
                    (self.gp_h * fct)
                )
            )
            self.painter.drawRect(rect)
        for i in range(2):
            rect = QRectF(
                QPointF(
                    self.bc - b / 2 + dy * i,
                    self.hc - (self.tb_t + self.gt_h * 0.55) * fct,
                ),
                QSizeF(
                    (self.gp_t * fct),
                    (self.gp_h * fct)
                )
            )
            self.painter.drawRect(rect)

        # Label Fahrbahnbreite
        pen = self.painter.pen()
        pen.setWidth(1)
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(8)
        self.painter.setFont(font)

        h0 = self.hc - 10 -  (self.tb_t + self.rb_h) * fct
        b0 = 0.5 * self.lr_b * fct

        self.painter.drawLine(
            QPointF(self.bc - b0 -5, h0),
            QPointF(self.bc + b0 +5, h0)
        )

        for i in range(2):
            self.painter.drawLine(
                QPointF(self.bc - b0 + self.lr_b * fct * i, h0-5),
                QPointF(self.bc - b0 + self.lr_b * fct * i, h0+5)
        )

        self.painter.drawText(
            QPointF(self.bc-12, h0-5),
            (f"{self.lr_b:.2f}")
        )

        self.labelWidget("Überbau Querschnitt")        
        self.painter.end()

    
    def sizeHint(self):
        return QSize(self.b,self.h)

    def labelWidget(self, s):
        '''Prints the label onto the widget.'''

        import ctypes
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        h = self.height()
        b = self.width()

        fac = h / screensize[1] 

        h_text = int(0.05 * h)
        h_text2 = int(h_text*0.8)

        pen = self.painter.pen()
        pen.setColor(QColor('gray'))
        self.painter.setPen(pen)

        h = int(self.h / 30)
        b = int(self.b / 120)

        font = self.painter.font()
        font.setFamily('Latin')
        font.setPointSize(h)
        self.painter.setFont(font)

        self.painter.drawText(b, 2*h, s)
       
        font.setPointSize(0.95*h)
        self.painter.setFont(font)
        m_tb = self.model['m_tb']
        m_lt = self.model['m_lt']
        s1 = f"Material Tragbelag:   {m_tb}"
        s2 = f"Material Längsträger: {m_lt}"
        self.painter.drawText(self.b-self.b/4, 1.5*h, s1)
        self.painter.drawText(self.b-self.b/4, 3*h, s2)