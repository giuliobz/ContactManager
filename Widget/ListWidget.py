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

        # Define the variable of selected element in edit mode.
        # the key is the item identifier and the value is
        # the item QCheckBox current value.
        self._selected = {}

        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Hide first column and delete button
        self.ui.contactList.hideColumn(0)
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())

        # Connect button behaviour
        self.ui.addButton.clicked.connect(lambda : self.addButtonFunc())
        self.ui.editButton.clicked.connect(lambda : self.enableEdit())
        self.ui.deleteButton.clicked.connect(lambda : self.delete_item())
        self.ui.searchButton.clicked.connect(lambda : self.searchContact())

        # Connect list to item change signal
        self.ui.contactList.itemChanged.connect(self.upload_selected_element)
        self.ui.nameLine.textChanged.connect(self._controller.changeLineSearch)
        self.ui.tagSearch.currentTextChanged.connect(self._controller.changeTagsSearch)

        # connect list to the model
        self._model.insertElementSignal.connect(self.add_contact)
        self._model.updateContactSignal.connect(self.refresh)
        self._model.searchMadeSignal.connect(self.changeSearchButtonName)

        # Load the current contact in list
        self._controller.loadContact()

    @pyqtSlot(bool)
    def changeSearchButtonName(self, search):
        if search:

            self.ui.searchButton.setText('Cancel search')

        else:

            self.ui.searchButton.setText('Search')
            self.ui.nameLine.setText('')
            self.ui.tagSearch.setCurrentIndex(0)
            self._controller.loadContact()


    def searchContact(self):
        self.ui.contactList.clear()
        self._controller.search()

        '''
        if self.ui.searchButton.text() != 'Cancel search':
        
            if self.ui.nameLine.text() != '' and self.ui.tagSearch.currentText() != '-- all --':
                self.ui.contactList.clear()
                self._controller.search(['both', self.ui.nameLine.text(), self.ui.tagSearch.currentText()])
                self.ui.searchButton.setText('Cancel search')
            elif self.ui.nameLine.text() != '' and self.ui.tagSearch.currentText() == '-- all --':
                self.ui.contactList.clear()
                self._controller.search(['string', self.ui.nameLine.text()])
                self.ui.searchButton.setText('Cancel search')
            elif self.ui.nameLine.text() == '' and self.ui.tagSearch.currentText() != '-- all --':
                self.ui.contactList.clear()
                self._controller.search(['tag', self.ui.tagSearch.currentText()])
                self.ui.searchButton.setText('Cancel search')
        
        else:

            self.ui.contactList.clear()
            self.ui.nameLine.setText('')
            self.ui.tagSearch.setCurrentIndex(0)
            self._controller.loadContact()
        '''
            

    def addButtonFunc(self):
        self._controller.changeCentralWidget('newContact')

    def enableEdit(self):
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())
        self.ui.contactList.setColumnHidden(0, not self.ui.contactList.isColumnHidden(0))

    # Add new anotation to QTreeWidget
    # NewContaact is a list where the first element is the name and the second element is 
    # a ContactWindow associated with the contact...
    @pyqtSlot(list)
    def add_contact(self, newContact):
        self.ui.contactList.addTopLevelItem(newContact[2])
        self.ui.contactList.setItemWidget(newContact[2], 1, ContactButton(newContact[0], newContact[1]))

    # When a element is selected or deselected the 
    # selected_element variable is updated.
    @pyqtSlot(QTreeWidgetItem, int)
    def upload_selected_element(self, item, column):
        self._selected[str(id(item))] =  [True if item.checkState(0) == Qt.Checked else False]


    @pyqtSlot()
    def delete_item(self):
        self._controller.deleteContacts(self._selected)
        self.refresh()
        self.enableEdit()
        self._selected = {}

    @pyqtSlot()
    def refresh(self):
        self.ui.contactList.clear()
        self._controller.loadContact()