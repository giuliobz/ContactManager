import csv

from Build.Ui_ListWidget import Ui_Form

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

        # Hide first column and delete botton
        self.ui.contactList.hideColumn(0)
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())

        # Define Add Button
        self.ui.addButton.clicked.connect(lambda : self._controller.changeWindow('add'))
        self.ui.editButton.clicked.connect(lambda : self.enableEdit())
        self.ui.deleteButton.clicked.connect(lambda : self._controller.deleteContacts())
        self.ui.contactList.itemChanged.connect(self.upload_selected_element)

        # connect list to the model
        self._model.insertElementSygnal.connect(self.add_annotation)
        self._model.deleteElementsSygnal.connect(self.delete_item)

        #self._model._database.deleteContact(0)
        self._controller.loadContact()
    
    def enableEdit(self):
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())
        self.ui.contactList.setColumnHidden(0, not self.ui.contactList.isColumnHidden(0))


    # Add new anotation to QTreeWidget
    # NewContaact is a list where the first element is the name and the second element is 
    # a ContactWindow associated with the contact...
    @pyqtSlot(list)#QTreeWidgetItem
    def add_annotation(self, newContact):
        self.ui.contactList.addTopLevelItem(newContact[2])
        self.ui.contactList.setItemWidget(newContact[2], 1, ContactButton(newContact[0], newContact[1]))

    # When a element is selected or deselected the 
    # selected_element variable is updated.
    @pyqtSlot(QTreeWidgetItem, int)
    def upload_selected_element(self, item, column):
        selected = {}
        for i in range(self.ui.contactList.invisibleRootItem().childCount()):
            item = self.ui.contactList.invisibleRootItem().child(i)
            selected[str(id(item))] =  [True if item.checkState(0) == Qt.Checked else False]
        self._controller.upload_selected_element(selected)


    @pyqtSlot()
    def delete_item(self):
        self.ui.contactList.clear()
        self._controller.refreshList()
        self.enableEdit()