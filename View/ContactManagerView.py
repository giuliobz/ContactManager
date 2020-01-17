from Build.Ui_ContactManagerWindow import Ui_ContactManagerWindow

from Model.model import Model
from Controller.controller import Controller

from Widget.AboutDialog import AboutDialog
from Widget.ListWidget import ListWidget

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication


class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define model and conroller 
        self._model = Model()
        self._controller = Controller(self._model)

        # Set up the user interface from Designer.
        self.ui = Ui_ContactManagerWindow()
        self.ui.setupUi(self)

        # Create about dialog and wire actions.
        self._aboutDialog = AboutDialog()
        self.ui.action_About.triggered.connect(self._aboutDialog.exec_)

        # Connect action
        self.ui.action_Quit.triggered.connect(QApplication.exit)

        # Connect model signal with the view   
        self._model.changeCentralWidgetSignal.connect(self.changeCentralWidget)

        # Set starting central widget
        self.setCentralWidget(ListWidget(self._model, self._controller))

    @pyqtSlot(list)
    def changeCentralWidget(self, widget):
        self.setWindowTitle(widget[1])
        self.setCentralWidget(widget[0])