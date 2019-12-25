import os 
import sys

from PyQt5.QtCore import QObject, pyqtSlot, QEventLoop
from PyQt5.QtWidgets import QTreeWidgetItem


DIR_NAME = os.path.dirname(os.path.abspath('__file__'))


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        # Connect the model
        self._model = model

    @pyqtSlot(list)
    def insertNewContact(self, list):
        print(list)
            
        
            
            