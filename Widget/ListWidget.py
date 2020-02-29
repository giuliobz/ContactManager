import csv

from Build.Ui_ListWidget import Ui_Form

from Widget.ContactButton import ContactButton

from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

class ListWidget(QDialog):

    def __init__(self, model, changeCentralWidget):
        super().__init__()
        
        # Connect model and controller
        self._model = model

        # Set up the user interface from Designer.
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Hide first column and delete button
        self.ui.contactList.hideColumn(0)
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())

        # Connect button behaviour
        self.ui.addButton.clicked.connect(lambda : changeCentralWidget(1))
        self.ui.editButton.clicked.connect(lambda : self.enableEdit())
        self.ui.deleteButton.clicked.connect(lambda : self.deleteContacts())
        self.ui.searchButton.clicked.connect(lambda : self.searchContacts())

        # Connect list to item change signal
        self.ui.orderBox.currentTextChanged.connect(self._model.setCurrentOrder)

        # connect list to the model
        self._model.refreshListSignal.connect(self.refresh)
        self._model.searchDoneSignal.connect(lambda slot: self.changeSearchStatus(slot))
        self._model.addContactSignal.connect(self.add_contact)

        # Load the current contact in list
        self._model.loadListContact()
    
    # Function to change the QTreeWidget column visibility and the delete button visibility.
    @pyqtSlot()
    def enableEdit(self):
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())
        self.ui.editButton.setEnabled(not self.ui.editButton.isEnabled())
        self.ui.contactList.setColumnHidden(0, not self.ui.contactList.isColumnHidden(0))

    # Function to search contacts
    def searchContacts(self):
        self._model.searchContacts(self.ui.nameLine.text(), self.ui.tagSearch.currentText())

    # Function to take the selected contact to delete
    def deleteContacts(self):
        selected = {}
        for i in range(self.ui.contactList.invisibleRootItem().childCount()):
                selected[self.ui.contactList.invisibleRootItem().child(i).data(0, Qt.UserRole)] = True if self.ui.contactList.invisibleRootItem().child(i).checkState(0) else False

        self._model.deleteContacts(selected)
        self.enableEdit()


    # Function that change the search button text in case the user is making a search.
    # After the user makes his contact search, tapping the Cancel search button, 
    # he resets the view to the original one (if he does not make change).
    def changeSearchStatus(self, slot):
        if slot:
            self.ui.searchButton.setText('Cancel search')

        else:
            self.ui.searchButton.setText('Search')
            self.ui.nameLine.setText('')
            self.ui.tagSearch.setCurrentIndex(0)


    # Add new contact to the list. To the contacts are
    # assigned an id, which is used to delete contact 
    # and to set information in contact window when the 
    # user want to see a contact informations.
    @pyqtSlot(dict)
    def add_contact(self, newContact):
        contact = QTreeWidgetItem()
        contact.setCheckState(0, Qt.Unchecked)
        contact.setData(0, Qt.UserRole, newContact['id'])
        self.ui.contactList.addTopLevelItem(contact)
        self.ui.contactList.setItemWidget(contact, 1, ContactButton(newContact['name'] + ' ' + newContact['secondName'], self._model, newContact['id']))

    # Function to refresh the contact list.
    # Is used when: contacts are searched, new contact is insert,
    # contact is changed and contact is deleted.
    # This beacouse we want an ordered list.
    @pyqtSlot(list)
    def refresh(self, contacts):
        self.ui.contactList.clear()

        for contactInfo in contacts:
            contact = QTreeWidgetItem()
            contact.setCheckState(0, Qt.Unchecked)
            contact.setData(0, Qt.UserRole, contactInfo['id'])
            self.ui.contactList.addTopLevelItem(contact)
            self.ui.contactList.setItemWidget(contact, 1, ContactButton(contactInfo['name'] + ' ' + contactInfo['secondName'], self._model, contactInfo['id']))  

        
