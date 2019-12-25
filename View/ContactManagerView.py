from Build.Ui_ContactManagerWindow import Ui_ContactManager

from Widget.ListWidget import ListWidget

from PyQt5.QtWidgets import QMainWindow


class ContactManager(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()

        # Define model and conroller 
        self._model = model
        self._controller = controller

        # Set up the user interface from Designer.
        self.ui = Ui_ContactManager()
        self.ui.setupUi(self)

        self.setCentralWidget(ListWidget(self._model, self._controller))
        
