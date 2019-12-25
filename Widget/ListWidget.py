import csv

from Build.Ui_ListWidget import Ui_Form

from Widget.NewContactWindow import NewContactWindow
from Widget.ContactWindow import ContactWindow
from Widget.ContactButton import ContactButton

from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

# Window that contain all the clips in annotation buffer with the correlated preferencies
class ListWidget(QDialog):

    def __init__(self, model, controller):
        super().__init__()
        
        # Connect model and controller
        self._model = model
        self._controller = controller

        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Define Add Button
        self.ui.addButton.clicked.connect(lambda : NewContactWindow(self._controller).exec_())

        # connect list to the model
        self._model.insertElementSygnal.connect(self.add_annotation)
    
    # Add new anotation to QTreeWidget
    @pyqtSlot(list)#QTreeWidgetItem
    def add_annotation(self, newContact):
        item = QTreeWidgetItem()
        item.setCheckState(0, Qt.Unchecked)
        item.setText(1, newContact[0])
        self.ui.annotationList.addTopLevelItem(item)
        self.ui.annotationList.setItemWidget(item, 1, ContactButton(newContact[0], newContact[0]))

    #@pyqtSignal(int)
    #def delete_contact(self, contact_id):
    #    pass