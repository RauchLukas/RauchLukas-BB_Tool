from PyQt5.QtWidgets import *

class TabWidget(QWidget):

    def __init__(self):
        super().__init__()


    def _createStackWidget(self):
        
        self.stack = QTabWidget()

        self.tab_1 = QWidget()
        self.tab_1.layout = QVBoxLayout()
        self.tab_1.setLayout(self.tab_1.layout)

        self.tab_2 = QWidget()
        self.tab_2.layout = QVBoxLayout()
        self.tab_2.setLayout(self.tab_2.layout)
        self.tab_3 = QWidget()
        self.tab_3.layout = QVBoxLayout()
        self.tab_3.setLayout(self.tab_3.layout)

        self._createMaterialWidget()
        self._createGeometryTopWidget()
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
