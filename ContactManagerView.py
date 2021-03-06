from Build.Ui_ContactManagerWindow import Ui_ContactManagerWindow

from ContactListModel import Model

from Widget.ContactWindow import ContactWindow
from Widget.NewContactWindow import NewContactWindow
from Widget.AboutDialog import AboutDialog
from Widget.ListWidget import ListWidget

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QStackedWidget


class ContactManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Define model and conroller 
        self._model = Model()

        # Set up the user interface from Designer.
        self.ui = Ui_ContactManagerWindow()
        self.ui.setupUi(self)

        # Setup the stacked widget to change view
        self._stack = QStackedWidget()
        self._stack.addWidget(ListWidget(self._model, self.changeCentralWidget))
        self._stack.addWidget(NewContactWindow(self._model, self.changeCentralWidget))
        self._stack.addWidget(ContactWindow(self._model, self.changeCentralWidget))

        # Create about dialog and wire actions.
        self._aboutDialog = AboutDialog()
        self.ui.action_About.triggered.connect(self._aboutDialog.exec_)

        # Connect action
        self.ui.action_Quit.triggered.connect(QApplication.exit)

        # Connect model signal with the view   
        self._model.changeCentralWidgetSignal.connect(self.changeCentralWidget)

        # Set starting central widget
        self.setCentralWidget(self._stack)

    # This function changes the user view.
    @pyqtSlot(int)
    def changeCentralWidget(self, widget_id):
        self._stack.setCurrentIndex(widget_id)
        self.setCentralWidget(self._stack)
