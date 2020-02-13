import os
import sys

from Database.database import Database

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, pyqtProperty
from PyQt5.QtWidgets import QWidget,QTreeWidgetItem

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

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

class Model(QObject):
    deleteDoneSignal = pyqtSignal()
    currentInformationSignal = pyqtSignal(dict)
    changeCentralWidgetSignal = pyqtSignal(int)
    searchDoneSignal = pyqtSignal(bool)
    refreshListSignal = pyqtSignal(list)
    addContactSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # Define the line and tag search element
        self._lineSearch = ''
        self._tagsSearch = '-- all --'
        self._searchDone = False  

        # Define the current central widget
        self._currentCentralWidget = None

        # Define a list to memorize the selected
        # contact that the user want delete
        self._selected_contacts = {}

        # Define database where we can save all contatct
        self._database = Database()

        # Define the id counter
        self._id = 0

    # This function changes the apllication view and set the contact information
    @pyqtSlot()
    def getInformation(self, id):
        contacts = [createContactInfo(c) for c in self._database.getContacts()]
        selected_contact = [contact for contact in contacts if id == contact['id']][0]
        self.currentInformationSignal.emit(selected_contact)
        self.changeCentralWidgetSignal.emit(2)

    # Function use only when the application start. It load all the contact 
    # stored in the database by the user
    @pyqtSlot()
    def loadListContact(self):
        contact_info = [createContactInfo(contact) for contact in self._database.getContacts()]
        for contact in contact_info:
            if int(contact['id']) > self._id:
                self._id = int(contact['id'])
            self.addContactSignal.emit(contact)
        
        self._id += 1

    @pyqtProperty(bool, notify = searchDoneSignal)
    def searchDone(self):
        return self._searchDone
    
    @searchDone.setter
    def searchDone(self, slot):
        self._searchDone = slot
        self.searchDoneSignal.emit(slot)

    # This function emit the signal to change the user view.
    # This is the cause that the main view has a list widget.
    # In this implemetation the listWidget has id = 0, NewContactWidget
    # has id=1.
    @pyqtSlot()
    def changeWidget(self, window_id):
        self.changeCentralWidgetSignal.emit(window_id)

    # Memorize the lineSearch variable change
    @pyqtSlot(str)
    def setTextualSearch(self, text):
        self._lineSearch = text

    # Memorize the tagearch variable change 
    @pyqtSlot(str)
    def setTagSearch(self, tag):
        self._tagsSearch = tag

    # Simple function to delete contact in list. In this
    # cas we refresh the contact list becaouse is faster
    # than to delete the single contact.
    @pyqtSlot()
    def deleteContacts(self):
        for idx in self._selected_contacts.keys():
            if self._selected_contacts[idx]:
                self._database.deleteContact(idx)
        
        self._selected_contacts = {}       
        self.deleteDoneSignal.emit()
        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts() ])

    # When a element is selected or deselected the 
    # selected_element variable is updated.
    @pyqtSlot(QTreeWidgetItem, int)
    def upload_selected_element(self, item, column):
        self._selected_contacts[item.data(0, Qt.UserRole)] =  [True if item.checkState(0) == Qt.Checked else False]

    # Define a function to add new contact in the database
    @pyqtSlot(dict)
    def addNewContact(self, newContact):
        contact = {}
        contact['id'] = self._id
        contact['photo'] = newContact['photo'] if 'photo' in newContact.keys() else 'Build/contact_2.png'
        contact['name'] = newContact['name'] if 'name' in newContact.keys() else ''
        contact['secondName'] = newContact['secondName'] if 'secondName' in newContact.keys() else ''
        contact['phone'] = newContact['phone'] if 'phone' in newContact.keys() else ''
        contact['mail'] = newContact['mail'] if 'mail' in newContact.keys() else ''
        contact['notes'] = newContact['notes'] if 'notes' in newContact.keys() else ''
        contact['tags'] = newContact['tags'] if 'tags' in newContact.keys() else []

        # If the user doesn't specify the name and second name of the 
        # contact, the name is setted like Unknown_ + id of the contact.
        if contact['name'] == '' and contact['secondName'] == '':
            contact['name'] = 'Unknown_' + str(self._id)

        # We check if the user already insert the contact in the list.
        # If it true we put the id in the surname. The user can change 
        # after the information.
        current_cotact = [ createContactInfo(contact) for contact in self._database.getContacts() ]
        if [c for c in current_cotact if contact['name'] == c['name'] and contact['secondName'] == c['secondName']]:
            contact['secondName'] += '_' + str(self._id)
        
        self._database.saveContact(self._id, contact['photo'], contact['name'], contact['secondName'], contact['phone'], contact['mail'], contact['notes'], '/'.join(contact['tags']))
        self.changeCentralWidgetSignal.emit(0)
        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts() ])
        self._id += 1
        

    # Simple function to search contact inside the list
    @pyqtSlot()
    def searchContacts(self):
        current_contact_list = [ createContactInfo(contact) for contact in self._database.getContacts() ]

        # Is checked if the user make a search or not
        if not self._searchDone:
            selected_contact = []
            
            # In this case the user makes tag and text search
            if self._lineSearch != '' and self._tagsSearch != '-- all --':

                # If there is a space in lineSearch, is sure that 
                # the user want to search a contact using the contact name and surname.
                if ' ' in self._lineSearch:
                    lineText = self._lineSearch.split(' ')
                
                    for contact in current_contact_list:
                        if lineText[0].lower() in contact['name'].lower() and lineText[1].lower() in contact['secondName'].lower() and self._tagsSearch in contact['tags']:
                            selected_contact.append(contact)

                # If the space doesn't appear in lineSearch, the user can be use, for example, the mail, 
                # phone number or other contact info to search a contact in the list.
                else:

                    lineText = self._lineSearch.lower()
                    for contact in current_contact_list:
                        if lineText.lower() in contact['name'].lower() or lineText in contact['secondName'].lower() or lineText in contact['mail'] or lineText == contact['phone'] and self._tagsSearch in contact['tags']:
                            selected_contact.append(contact)

            # In this case the user makes  text search
            elif self._lineSearch != '' and self._tagsSearch == '-- all --':

                if ' ' in self._lineSearch:
                    lineText = self._lineSearch.split(' ')

                    for contact in current_contact_list:
                        if lineText[0].lower() in contact['name'].lower() and lineText[1].lower() in contact['secondName'].lower():
                            selected_contact.append(contact)
                
                else:

                    lineText = self._lineSearch.lower()
                    for contact in current_contact_list:
                        if lineText.lower() in contact['name'].lower() or lineText in contact['secondName'].lower() or lineText in contact['mail'] or lineText == contact['phone']:
                            selected_contact.append(contact)

            # In this case the user makes tag search
            elif self._lineSearch == '' and self._tagsSearch != '-- all --':

                for contact in current_contact_list:
                    if self._tagsSearch in contact['tags']:
                        selected_contact.append(contact)

            self.searchDone = True
            self.refreshListSignal.emit(selected_contact)
        
        # if the user make a search, when he finish, the 
        # search variables (lineSearch and tagSearch) are reseted.
        else:

            self.searchDone = False
            self._tagsSearch = '-- all --'
            self._lineSearch = ''
            self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts() ])

    # Funtion to delete a single contact
    @pyqtSlot(int)
    def deleteContact(self, id):
        self._database.deleteContact(id)
        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts() ])
    
    # Function to update contact informations
    @pyqtSlot(dict)
    def updateContactInfos(self, contact_info):
        self._database.updateContact(contact_info['photo'], contact_info['name'], contact_info['secondName'], contact_info['phone'], contact_info['mail'], contact_info['notes'], '/'.join(contact_info['tags']), contact_info['id'])