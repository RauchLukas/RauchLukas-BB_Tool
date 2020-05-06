from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np

class StackOne(QWidget):

    geometryChanged = pyqtSignal(str)

    elementLengthChanged = pyqtSignal()
    elementDistChanged = pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        super(StackOne, self).__init__(*args, **kwargs)

        self.g_model = dict()

        m_boxWidget = QGroupBox("Materialauswahl")
        g_boxWidget = QGroupBox("Geometrieeingabe")

        main = QVBoxLayout()
        m_grid = QVBoxLayout()
        g_grid = QGridLayout()
        g_grid.setColumnMinimumWidth(3, 30)
        m_layoutTrag = QHBoxLayout() 
        m_layoutLaen = QHBoxLayout() 
        g_layoutTrag = QHBoxLayout() 
        g_layoutLaen = QHBoxLayout() 

        self.label_lt_l = QLabel("Überbau Elementlänge")
        self.lt_l = 5.0
        lst = np.arange(3.50, 10.0, 0.50).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_lt_l = QComboBox()
        self.com_lt_l.addItems(lst)
        g_grid.addWidget(self.label_lt_l, 0, 0)
        g_grid.addWidget(self.com_lt_l, 0, 1)
        g_grid.addWidget(QLabel("[m]"), 0, 2)

        self.com_lt_dist = QComboBox()
        self.com_lt_dist.addItems(['symmetrisch', 'linear'])
        mini_layout = QHBoxLayout()
        mini_layout.addWidget(QLabel("[m]"))
        mini_layout.addWidget(self.com_lt_dist)
        g_grid.addLayout(mini_layout, 0, 2)


        self.label_lt_n = QLabel("Anzahl Längsträger")
        self.lt_n = 8
        self.com_lt_n = QComboBox()
        lst = range(2,16)
        lst = ["{:2d}".format(x) for x in lst]
        self.com_lt_n.addItems(lst)
        g_grid.addWidget(self.label_lt_n, 1, 0)
        g_grid.addWidget(self.com_lt_n, 1, 1)
        g_grid.addWidget(QLabel("[-]"), 1, 2)

        self.label_lt_h = QLabel("Querschnittshöhe Längsträger")
        self.lt_h = 0.30
        lst = np.arange(0.12, 0.38, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_lt_h = QComboBox()
        self.com_lt_h.addItems(lst)
        g_grid.addWidget(self.label_lt_h, 2, 0)
        g_grid.addWidget(self.com_lt_h, 2, 1)
        g_grid.addWidget(QLabel("[m]"), 2, 2)

        self.label_lt_b = QLabel("Querschnittsbreite Längsträger")
        self.lt_b = 0.20
        lst = np.arange(0.10, 0.42, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_lt_b = QComboBox()
        self.com_lt_b.addItems(lst)
        g_grid.addWidget(self.label_lt_b, 3, 0)
        g_grid.addWidget(self.com_lt_b, 3, 1)
        g_grid.addWidget(QLabel("[m]"), 3, 2)

        self.label_tb_t = QLabel("Tragbelagdicke")
        self.tb_t = 0.12
        lst = np.arange(0.04, 0.32, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_tb_t = QComboBox()
        self.com_tb_t.addItems(lst)
        g_grid.addWidget(self.label_tb_t, 0, 4)
        g_grid.addWidget(self.com_tb_t, 0, 5)
        g_grid.addWidget(QLabel("[m]"), 0, 6)

        self.label_fb_t = QLabel("Fahrbahnbelagdicke")
        self.fb_t = 0.06
        lst = np.arange(0.02, 0.12, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_fb_t = QComboBox()
        self.com_fb_t.addItems(lst)
        g_grid.addWidget(self.label_fb_t, 1, 4)
        g_grid.addWidget(self.com_fb_t, 1, 5)
        g_grid.addWidget(QLabel("[m]"), 1, 6)

        self.label_rb_h = QLabel("Rödelbalkenhöhe")
        self.rb_h = 0.16
        lst = np.arange(0.10, 0.32, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_rb_h = QComboBox()
        self.com_rb_h.addItems(lst)
        g_grid.addWidget(self.label_rb_h, 2, 4)
        g_grid.addWidget(self.com_rb_h, 2, 5)
        g_grid.addWidget(QLabel("[m]"), 2, 6)

        self.label_rb_b = QLabel("Rödelbalkenbreite")
        self.rb_b = 0.16
        lst = np.arange(0.10, 0.32, 0.02).tolist()
        lst = ["{:.2f}".format(x) for x in lst]
        self.com_rb_b = QComboBox()
        self.com_rb_b.addItems(lst)
        g_grid.addWidget(self.label_rb_b, 3, 4)
        g_grid.addWidget(self.com_rb_b, 3, 5)
        g_grid.addWidget(QLabel("[m]"), 3, 6)

        self.key_list = {
            'lt_l': self.com_lt_l,
            'lt_n': self.com_lt_n,
            'lt_h': self.com_lt_h,
            'lt_b': self.com_lt_b,
            'tb_t': self.com_tb_t,
            'fb_t': self.com_fb_t,
            'rb_h': self.com_rb_h,
            'rb_b': self.com_rb_b,
        }
        
        self.gt_h = 1.00
        self.gt_t = 0.08
        self.gt_d = self.gt_h * 0.7
        self.gt_b = self.gt_t
        self.alpha = 60
        self.gp_h = 0.10
        self.gp_t = 0.04

        self.m_trag = "c14"
        self.m_laen = "c24"

        labelTrag = QLabel("Material Tragbelag: ")
        labelTrag.setFixedWidth(65)
        labelLaen = QLabel("Material Längsträger: ")
        labelLaen.setFixedWidth(65)

        self.com_m_trag = QComboBox()
        self.com_m_laen = QComboBox()
        
        self.com_m_trag.addItems(["c14", "c16", "c20", "c24", "c30"])
        self.com_m_laen.addItems(["c14", "c16", "c20", "c24", "c30"]) # , "s235", "s355"])

        
        self.buttenTrag = QPushButton("Parameter anzeigen")
        self.buttenLaen = QPushButton("Parameter anzeigen")

        m_layoutTrag.addWidget(labelTrag)
        m_layoutTrag.addWidget(self.com_m_trag)
        m_layoutTrag.addStretch(1)
        m_layoutTrag.addWidget(self.buttenTrag,  alignment = Qt.AlignRight)

        m_layoutLaen.addWidget(labelLaen)
        m_layoutLaen.addWidget(self.com_m_laen)
        m_layoutLaen.addStretch(1)
        m_layoutLaen.addWidget(self.buttenLaen, alignment = Qt.AlignRight)

        m_grid.addLayout(m_layoutTrag)
        m_grid.addLayout(m_layoutLaen)

        m_boxWidget.setLayout(m_grid)
        main.addWidget(m_boxWidget)

        g_boxWidget.setLayout(g_grid)
        main.addWidget(g_boxWidget)

        self.setLayout(main)

        # SIGNALS

        self.com_lt_l.currentTextChanged.connect(self.gElementChanged)
        self.com_lt_dist.currentTextChanged.connect(self.gElementDistChanged)
                
        for key, arg in self.key_list.items():
            arg.currentTextChanged.connect(self.gComboboxChanged)

        self.com_m_trag.currentTextChanged.connect(lambda s : self.mComboboxChanged(s, "trag"))
        self.com_m_laen.currentTextChanged.connect(lambda s : self.mComboboxChanged(s, "laen"))

        self.buttenTrag.pressed.connect(lambda : self.show_popup("trag"))
        self.buttenLaen.pressed.connect(lambda : self.show_popup("laen"))

        index = self.com_m_trag.findText("C14", Qt.MatchFixedString)
        self.com_m_trag.setCurrentIndex(index) # Set default material to C14
        index = self.com_m_laen.findText("C24", Qt.MatchFixedString)
        self.com_m_laen.setCurrentIndex(index) # Set default material to C24

        # Set currend Index
        self.com_m_trag.setCurrentIndex(1)
        self.com_m_laen.setCurrentIndex(3)
        self.com_lt_n.setCurrentIndex(6)
        self.com_lt_h.setCurrentIndex(6)
        self.com_lt_b.setCurrentIndex(4)
        self.com_tb_t.setCurrentIndex(3)
        self.com_fb_t.setCurrentIndex(1)
        self.com_rb_h.setCurrentIndex(5)
        self.com_rb_b.setCurrentIndex(5)


    def gElementChanged(self):

        self.elementLengthChanged.emit()

    def gElementDistChanged(self):
        element_dist = self.com_lt_dist.currentText()

        self.elementDistChanged.emit(element_dist)

    def gComboboxChanged(self):

        for key, arg in self.key_list.items():
            self.g_model[key] = arg.currentText()

        self.geometryChanged.emit("geometry changed")

    def mComboboxChanged(self, signal, key):
        
        if key == "trag": 
            self.g_model['m_tb'] = signal
        if key == "laen":
            self.g_model['m_lt'] = signal

        self.geometryChanged.emit("geometry changed")


    def getModel(self):
        
        return self.g_model
    
    def show_popup(self, key):

        name = "default"
        material = "c24"

        if key == "trag":
            name = "Tragbelag"
            material = self.com_m_trag.currentText()
        if key == "laen":
            name = "Längsträger"
            material = self.com_m_laen.currentText()

        dialog = QDialog(self)
        dialog.setWindowTitle("Materialparameter %s" % name)
        layout = QVBoxLayout()
        head = QHBoxLayout() 
        grid = QGridLayout()

        m_label = QLabel("Materialtyp: ")
        m_type = QLabel(material)
        head.addWidget(m_label)
        head.addWidget(m_type)
        head.addStretch(1) 

        for i, s in enumerate(m_key_list):
            n = 0
            if i > 5:
                n = 3
                i -= 6

            grid.addWidget(QLabel((s + " :")), i, n)
            line = QLineEdit()
            line.setReadOnly(True)
            line.setText(str(materialdata[material][s]))
            grid.addWidget(line, i, n + 1)
            grid.addWidget(QLabel(unit_list[s]), i, n + 2)

        layout.addLayout(head)
        layout.addLayout(grid)

        dialog.setLayout(layout)
        dialog.exec()



class TabWidget(QWidget):

    def __init__(self):
        super().__init__()


    def _createStackWidget(self):
        
        self.stack = QTabWidget()

        self.tab_1 = QWidget()
        self.tab_1.layout = QVBoxLayout()
        self.tab_1.setLayout(self.tab_1.layout)

        self.tab_1 = StackOne()

        self.tab_2 = QWidget()
        self.tab_2.layout = QVBoxLayout()
        self.tab_2.setLayout(self.tab_2.layout)
        self.tab_3 = QWidget()
        self.tab_3.layout = QVBoxLayout()
        self.tab_3.setLayout(self.tab_3.layout)

        # self._createMaterialWidget()
        # self._createGeometryTopWidget()
        self._createGeometryBotWidget()
        self._createFoundationWidget()

        self.stack.addTab(self.tab_1, "Überbau")
        self.stack.addTab(self.tab_2, "Unterbau")
        self.stack.addTab(self.tab_3, "Gründung")

    


    def placeWidget(self, layout):
        layout.addWidget(self.stack)

    def _createMaterialWidget(self):
        # Create dummy material widget
        self.tab_1.layout.addWidget(QLabel("Material Dummy Widget"))
        self.tab_2.layout.addWidget(QLabel("Material Dummy Widget"))

    def _createGeometryTopWidget(self):
        # Create dummy Überbau widget
        self.tab_1.layout.addWidget(QLabel("Geomertrie Überbau Dummy Widget"))

    def _createGeometryBotWidget(self):
        # Create dummy Unterbau widget
        self.tab_2.layout.addWidget(QLabel("Geomertrie Unterbau Dummy Widget"))

    def _createFoundationWidget(self):
        # Create dummy Unterbau widget
        self.tab_3.layout.addWidget(QLabel(" Grüngung Dummy Widget"))





m_key_list = [
    "fmk", "ft0k", "ft90k", "fc0k", "fc90k", "fvk", "e0mean", "e005", "e90mean", "gmean", "rok", "romean"
]
unit_list = {
    'fmk': "[N/mm²]", 'ft0k': "[N/mm²]", 'ft90k': "[N/mm²]", 'fc0k': "[N/mm²]", 'fc90k': "[N/mm²]",
    'fvk': "[N/mm²]", 'e0mean': "[kN/mm²]", 'e005': "[kN/mm²]", 'e90mean': "[kN/mm²]", 'gmean': "[kN/mm²]",
    'rok': "[kg/m³]", 'romean': "[kg/m³]"
}
materialdata = {
    'c14': {'fmk': 14, 'ft0k': 8, 'ft90k': 0.4, 'fc0k': 16, 'fc90k': 2.0, 'fvk': 3.0, 'e0mean': 7, 
        'e005': 4.7, 'e90mean': 0.23, 'gmean': 0.44, 'rok': 290, 'romean': 350},
    'c16' :{'fmk': 16, 'ft0k': 10, 'ft90k': 0.4, 'fc0k': 17, 'fc90k': 2.2, 'fvk': 3.2, 'e0mean': 8,
            'e005': 5.4,  'e90mean': 0.27, 'gmean': 0.50, 'rok': 310, 'romean': 370},
    'c20': {'fmk': 20, 'ft0k': 12, 'ft90k': 0.4, 'fc0k': 19, 'fc90k': 2.3, 'fvk': 3.6, 'e0mean': 9.5,
            'e005': 6.4, 'e90mean': 0.32, 'gmean': 0.59, 'rok': 330, 'romean': 390},
    'c24': {'fmk': 24, 'ft0k': 14, 'ft90k': 0.4, 'fc0k': 21, 'fc90k': 2.5, 'fvk': 4.0, 'e0mean': 11,
            'e005': 7.4, 'e90mean': 0.37, 'gmean': 0.69, 'rok': 350, 'romean': 420},
    'c30': {'fmk': 30, 'ft0k': 18, 'ft90k': 0.4, 'fc0k': 23, 'fc90k': 2.7, 'fvk': 4.0, 'e0mean': 12,
            'e005': 8.0, 'e90mean': 0.40, 'gmean': 0.75, 'rok': 380, 'romean': 460},
}
t_dict = {
    '6 cm': 0.06 , '8 cm': 0.08 , '10 cm': 0.10 , '12 cm': 0.12, '14 cm': 0.14 ,
    '16 cm': 0.16 , '18 cm': 0.181 , '20 cm': 0.20
}
a_dict = {
    '0.30 m': 0.30, '0.35 m': 0.35, '0.40 m': 0.40, '0.45 m': 0.45, '0.50 m': 0.50, '0.55 m': 0.55,
    '0.60 m': 0.60, '0.65 m': 0.65, '0.70 m': 0.70, '0.75 m': 0.75, '0.80 m': 0.80, '0.85 m': 0.85, 
    '0.90 m': 0.90, '0.95 m': 0.95, '1.00 m': 1.00, '1.05 m': 1.05, '1.10 m': 1.10, '1.15 m': 1.15, 
    '1.20 m': 1.20, '1.25 m': 1.25, '1.30 m': 1.30, '1.35 m': 1.35, '1.40 m': 1.40, '1.45 m': 1.45,
}
l_str_list = ['3.50 m','4.00 m','4.50 m','5.50 m','6.00 m','7.00 m','7.50 m','8.00 m','8.50 m','9.00 m','9.50 m',]
l_dict = {
    '3.,50 m': 3.50, '4.00 m': 4.00, '4.50 m': 4.50, '5.50 m': 5.50, '6.00 m': 6.50, '7.00 m': 7.00,
    '7.50 m': 7.50, '8.00 m': 8.00, '8.50 m': 8.50, '9.00 m': 9.00, '9.50 m': 9.50,
}

