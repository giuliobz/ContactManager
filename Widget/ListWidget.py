import csv

from Build.Ui_ListWidget import Ui_Form

from Widget.ContactButton import ContactButton

from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem

def createContactInfo(contact):
    contactInfo = {}

    contactInfo['id'] = int(contact[0])
    contactInfo['photo'] = (contact[1])
    contactInfo['name'] = contact[2]
    contactInfo['secondName'] = contact[3]
    contactInfo['phone'] = contact[4]
    contactInfo['mail'] = contact[5]
    contactInfo['notes'] = contact[6]
    contactInfo['tags'] = contact[7].split('/')

    return contactInfo

# Window that contain all the clips in annotation buffer with the correlated preferencies
class ListWidget(QDialog):

    def __init__(self, model, changeCentralWidget):
        super().__init__()
        
        # Connect model and controller
        self._model = model

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
        self.ui.addButton.clicked.connect(lambda : changeCentralWidget(1))
        self.ui.editButton.clicked.connect(lambda : self.enableEdit())
        self.ui.deleteButton.clicked.connect(lambda : self.enableEdit())
        self.ui.searchButton.clicked.connect(lambda : self._model.searchContacts())

        # Connect list to item change signal
        self.ui.contactList.itemChanged.connect(self.upload_selected_element)
        self.ui.nameLine.textChanged.connect(self.setTextualSearch)
        self.ui.tagSearch.currentTextChanged.connect(self.setTagSearch)
        self.ui.orderBox.currentTextChanged.connect(self._model.setCurrentOrder)

        # connect list to the model
        self._model.refreshListSignal.connect(self.refresh)
        self._model.searchDoneSignal.connect(lambda slot: self.changeSearchStatus(slot))
        self._model.addContactSignal.connect(self.add_contact)

        # Load the current contact in list
        self._model.loadListContact()
    
    # Function to change the QTreeWidget column visibility and the delete button visibility.
    # When the user click edit he can delete multiple contacts by selecting them
    # and clicking the delete button. If no one contacts is selected it only 
    # change the QTreeWidget column visibility and delete button visibility.
    @pyqtSlot()
    def enableEdit(self):
        if self._selected:
            self._model.deleteContacts(self._selected)
            self._selected = {}
        self.ui.deleteButton.setEnabled(not self.ui.deleteButton.isEnabled())
        self.ui.editButton.setEnabled(not self.ui.editButton.isEnabled())
        self.ui.contactList.setColumnHidden(0, not self.ui.contactList.isColumnHidden(0))

    # Memorize the lineSearch variable change
    @pyqtSlot(str)
    def setTextualSearch(self, text):
        self._lineSearch = text

    # Memorize the tagearch variable change 
    @pyqtSlot(str)
    def setTagSearch(self, tag):
        self._tagsSearch = tag

    # Function that change the search button text in case the user is making a search.
    # After the user makes his contact search, tapping the Cancel search button 
    # he resets the view to the original one (if he does not make change).
    def changeSearchStatus(self, slot):
        if slot:
            self.ui.searchButton.setText('Cancel search')

        else:
            self.ui.searchButton.setText('Search')
            self.ui.nameLine.setText('')
            self.ui.tagSearch.setCurrentIndex(0)


    # Add new anotation to QTreeWidget
    # NewContaact is a list where the first element is the name and the second element is 
    # a ContactWindow associated with the contact...
    @pyqtSlot(dict)
    def add_contact(self, newContact):
        contact = QTreeWidgetItem()
        contact.setCheckState(0, Qt.Unchecked)
        contact.setData(0, Qt.UserRole, newContact['id'])
        self.ui.contactList.addTopLevelItem(contact)
        self.ui.contactList.setItemWidget(contact, 1, ContactButton(newContact['name'] + ' ' + newContact['secondName'], self._model, newContact['id']))

    # When a element is selected or deselected the 
    # selected_element variable is updated.
    @pyqtSlot(QTreeWidgetItem, int)
    def upload_selected_element(self, item, column):
        self._selected[item.data(0, Qt.UserRole)] =  [True if item.checkState(0) == Qt.Checked else False]

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

        