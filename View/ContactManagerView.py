from Build.Ui_ContactManagerWindow import Ui_ContactManager

from Model.model import Model
from Controller.controller import Controller

from Widget.ListWidget import ListWidget

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget


class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define model and conroller 
        self._model = Model()
        self._controller = Controller(self._model)

        # Set up the user interface from Designer.
        self.ui = Ui_ContactManager()
        self.ui.setupUi(self)

        # Connect model signal with the view   
        self._model.changeCentralWidgetSignal.connect(self.changeCentralWidget)

        # Set starting central widget
        self.setCentralWidget(ListWidget(self._model, self._controller))

    @pyqtSlot(object)
    def changeCentralWidget(self, widget):
        self.setCentralWidget(widget)