from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import numpy as np

class TabStack(QWidget):

    def __init__(self, steps=5, *args, **kwargs):
        super(TabStack, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        stack = QTabWidget()

        stack.addTab(_StackOne(), "Überbau")
        stack.addTab(_StackTwo(), "Unterbau")
        stack.addTab(_StackThree(), "Gründung")

        layout.addWidget(stack)


        self.setLayout(layout)


class _StackOne(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.m_trag = "c14"
        self.m_laen = "c24"
        self.a_laen = 5.0
        self.t_trag = 0.12
         
        m_boxWidget = QGroupBox("Materialauswahl")
        g_boxWidget = QGroupBox("Geometrieeingabe")
        
        main = QVBoxLayout()
        m_grid = QVBoxLayout()
        g_grid = QVBoxLayout()
        m_layoutTrag = QHBoxLayout() 
        m_layoutLaen = QHBoxLayout() 
        g_layoutTrag = QHBoxLayout() 
        g_layoutLaen = QHBoxLayout() 


        labelTrag = QLabel("Tragbelag: ")
        labelLaen = QLabel("Längsträger: ")

        self.m_comboBoxTrag = QComboBox()
        self.m_comboBoxLaen = QComboBox()
        
        self.m_comboBoxTrag.addItems(["c14", "c20", "c24", "c30"])


        self.m_comboBoxLaen.addItems(["c20", "c24", "c30"]) # , "s235", "s355"])

        
        self.buttenTrag = QPushButton("Parameter anzeigen")
        self.buttenLaen = QPushButton("Parameter anzeigen")

        m_layoutTrag.addWidget(labelTrag)
        m_layoutTrag.addWidget(self.m_comboBoxTrag)
        m_layoutTrag.addWidget(self.buttenTrag,  alignment = Qt.AlignRight)
        m_layoutTrag.addStretch(1)

        m_layoutLaen.addWidget(labelLaen)
        m_layoutLaen.addWidget(self.m_comboBoxLaen)
        m_layoutLaen.addWidget(self.buttenLaen, alignment = Qt.AlignRight)
        m_layoutLaen.addStretch(1)

        m_grid.addLayout(m_layoutTrag)
        m_grid.addLayout(m_layoutLaen)

        m_boxWidget.setLayout(m_grid)
        main.addWidget(m_boxWidget)



        labelTrag = QLabel("Tragbelag Dicke: ")
        labelLaen = QLabel("Längsträger Abstand: ")

        self.g_comboBoxTrag = QComboBox()
        self.g_comboBoxLaen = QComboBox()
        
        self.g_comboBoxTrag.addItems(["6 cm", "8 cm", "10 cm", "12 cm", "14 cm", "16 cm", "18 cm", "20 cm"])

        float_format = "{:.2f}".format
        list = np.arange(0.30, 1.50, 0.05).tolist()
        s_list = [str(float_format(i) + " m") for i in list]
        self.g_comboBoxLaen.addItems(s_list) # , "s235", "s355"])


        g_layoutTrag.addWidget(labelTrag)
        g_layoutTrag.addWidget(self.g_comboBoxTrag)
        g_layoutTrag.addStretch(1)

        g_layoutLaen.addWidget(labelLaen)
        g_layoutLaen.addWidget(self.g_comboBoxLaen)
        g_layoutLaen.addStretch(1)

        g_grid.addLayout(g_layoutTrag)
        g_grid.addLayout(g_layoutLaen)

        g_boxWidget.setLayout(g_grid)
        main.addWidget(g_boxWidget)


        self.setLayout(main)

        # SIGNALS
        self.m_comboBoxTrag.currentTextChanged.connect(lambda s : self.mComboboxChanged(s, "trag"))
        self.m_comboBoxLaen.currentTextChanged.connect(lambda s : self.mComboboxChanged(s, "laen"))
        self.g_comboBoxTrag.currentTextChanged.connect(lambda s : self.gComboboxChanged(s, "trag"))
        self.g_comboBoxLaen.currentTextChanged.connect(lambda s : self.gComboboxChanged(s, "laen"))
        self.buttenTrag.pressed.connect(lambda : self.show_popup("trag"))
        self.buttenLaen.pressed.connect(lambda : self.show_popup("laen"))

        index = self.m_comboBoxTrag.findText("C14", Qt.MatchFixedString)
        self.m_comboBoxTrag.setCurrentIndex(index) # Set default material to C14
        index = self.m_comboBoxLaen.findText("C24", Qt.MatchFixedString)
        self.m_comboBoxLaen.setCurrentIndex(index) # Set default material to C24
        self.g_comboBoxTrag.setCurrentIndex(2) # Set default index to 0 ( triggers refersh of the model)
        self.g_comboBoxLaen.setCurrentIndex(5) # Set default index to 0 ( triggers refersh of the model)

    def mComboboxChanged(self, signal, key):
        
        if key == "trag": 
            self.m_trag = signal
        if key == "laen":
            self.m_laen = signal

    def gComboboxChanged(self, signal, key):
        
        if key == "trag": 
            self.t_trag = t_dict[signal]
        if key == "laen":
            self.a_laen = a_dict[signal]

    def show_popup(self, key):

        name = "default"
        material = "c24"

        if key == "trag":
            name = "Tragbelag"
            material = self.m_trag
        if key == "laen":
            name = "Längsträger"
            material = self.m_laen

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

        for i, s in enumerate(key_list):
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
        # dialog.show()
        dialog.exec()

        
        # msg = QMessageBox()
        # msg.setWindowTitle("Materialeigenschaften")
        # msg.setText("Butten %s pushed!" % key) 

        # layout = QVBoxLayout()

        # layout.addWidget(QLabel("Widgettext"))

        # msg.setLayout(layout)
        # msg.show()


        # x = msg.exec_()

# class MyPopUp(QWidget):

#     def __init__(self):
#         super().__init__()

#         widget = QLabel("WidgetText")

#         widget.show()

        # self.m_out_grid = QGridLayout()

        # index = comboBox.findText("C24", Qt.MatchFixedString)
        # comboBox.setCurrentIndex(index)            # Set default material to C24




        # grid.addWidget(m_out)


    # def make_widget(self, material):

    #     pass

        # for i, s in enumerate(key_list):
        #     n = 0
        #     if i > 5:
        #         n = 3
        #         i -= 6

        #     self.m_out_grid.addWidget(QLabel((s + " :")), i, n)
        #     line = QLineEdit()
        #     line.setText(str(materialdata[material][s]))
        #     self.m_out_grid.addWidget(line, i, n + 1)
        #     self.m_out_grid.addWidget(QLabel(unit_list[s]), i, n + 2)

        # m_out = QGroupBox("Materialparameter")
        # m_out.setLayout(self.m_out_grid)



class _StackTwo(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        label = QLabel("placeholder : Unterbauten")
        
        layout = QVBoxLayout()
        
        layout.addWidget(label,)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

class _StackThree(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        label = QLabel("placeholder : Gründung")
        
        layout = QVBoxLayout()
        
        layout.addWidget(label,)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)



key_list = [
    "fmk", "ft0k", "ft90k", "fc0k", "fc90k", "fvk", "e0mean", "e005", "e90mean", "gmean", "rok", "romean"
]
unit_list = {
    'fmk': "[N/mm²]", 'ft0k': "[N/mm²]", 'ft90k': "[N/mm²]", 'fc0k': "[N/mm²]", 'fc90k': "[N/mm²]",
    'fvk': "[N/mm²]", 'e0mean': "[kN/mm²]", 'e005': "[kN/mm²]", 'e90mean': "[kN/mm²]", 'gmean': "[kN/mm²]",
    'rok': "[kg/m³]", 'romean': "[kg/m³]"
}
materialdata = {
    'c14': {'fmk': 14, 'ft0k': 8, 'ft90k': 0.4, 'fc0k': 16, 'fc90k': 2.0, 'fvk': 3.0, 'e0mean': 7, 'e005': 4.7,
            'e90mean': 0.23, 'gmean': 0.44, 'rok': 290, 'romean': 350
            },
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
