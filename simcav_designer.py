from PyQt5 import QtWidgets, QtGui, QtCore

class SolutionsTab(QtWidgets.QWidget):
    def __init__(self, elementList, conditionList, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setStyleSheet(open('style_designerSolutions.css').read())
        
        numElements = len(elementList)
        numConditions = len(conditionList)
        
        layout = QtWidgets.QGridLayout(self)
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # Table title: Items, Stability and Conditions
        #font = QtGui.QFont()
        #font.setWeight(QtGui.QFont.Bold)
        self.title = {
        'item': LabelTitle(self, text='Items'),
        'stability': LabelTitle(self, text='Stability'),
        'conditions': LabelTitle(self, text='Conditions')
        }
        
        layout.addWidget(self.title['item'], 0, 0, 1, numElements)
        layout.addWidget(QVLine(), 0, numElements, 1, 1)
        layout.addWidget(self.title['stability'], 0, numElements + 1, 1, 2)
        layout.addWidget(QVLine(), 0, numElements + 3, 1, 1)
        layout.addWidget(self.title['conditions'], 0, numElements + 4, 1, numConditions)
        
        # ACTUALLY, ADD THE SEPARATOR AT THE END, SPANNING THE WHOLE VERTICAL.
        
        # Subtitle: 
        # Elements:
        for element in elementList:
            label = LabelSubtitle(self, text=element['Type'])
            layout.addWidget(label, 1, element['Order'], 1, 1)
        # Separator
        layout.addWidget(QVLine(), 1, numElements, 1, 1)
        # Stability
        label = LabelSubtitle(self, text='Tangential')
        layout.addWidget(label, 1, numElements + 1, 1, 1)
        label = LabelSubtitle(self, text='Sagittal')
        layout.addWidget(label, 1, numElements + 2, 1, 1)
        # Separator
        layout.addWidget(QVLine(), 1, numElements + 3, 1, 1)
        # Conditions
        for i, element in enumerate(conditionList):
            name = element['Widget'].columns['condition'].currentText()
            label = LabelSubtitle(self, text=name)
            layout.addWidget(label, 1, numElements + 4 + i, 1, 1)
            
    def addRow(self, combination, stability, results):
        pass
        
    def addCombination(self, combination):
        pass
        
    def addStability(self, stability):
        pass
        
    def addResults(self, results):
        pass
            
class LabelTitle(QtWidgets.QLabel):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, parent, *args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter)
        
        font = QtGui.QFont()
        font.setWeight(QtGui.QFont.Bold)
        font.setStyleHint(QtGui.QFont.Serif)
        self.setFont(font)
        
class LabelSubtitle(QtWidgets.QLabel):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, parent, *args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter)

class LabelCell(QtWidgets.QLabel):
    def __init__(self, parity, group=0, parent=None, *args, **kwargs):
        QtWidgets.QLabel.__init__(self, parent, *args, **kwargs)
        self.setAlignment(QtCore.Qt.AlignCenter)
        
class QVLine(QtWidgets.QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)