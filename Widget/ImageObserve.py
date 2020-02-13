from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class Observable(QObject):
    valueChanged = pyqtSignal(str) # Create a custom signal.
    def __init__(self, val):
        super().__init__()
        self._value = val
    
    def observe(self, slot):    
        self.valueChanged.connect(slot)
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newval):
        self._value = newval
        self.valueChanged.emit(self.value) # Emit signal.