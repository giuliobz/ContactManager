import os 
import sys

from Widget.ListWidget import ListWidget
from Widget.NewContactWindow import NewContactWindow
from Widget.ContactWindow import ContactWindow

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget


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



class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        # Connect the model
        self._model = model

    def changeCentralWidget(self, widget):
        if widget == 'newContact':
            self._model.currentCentralWidget = NewContactWindow(self._model.currentContactList, self)
        elif widget == 'list':
            self._model.currentCentralWidget = ListWidget(self._model, self)
        else:
            self._model.currentCentralWidget = ContactWindow()


    @pyqtSlot(dict)
    def insertNewContact(self, newContact):
        contact = QTreeWidgetItem()
        contact.setCheckState(0, Qt.Unchecked)
        contactWindow = ContactWindow(self._model.id, newContact, self)
        newContact['tags'] = '/'.join(newContact['tags'])
        identifier = str(id(contact))
        self._model.indexTable = [identifier, self._model.id]
        self._model.currentContactList = ['insert', newContact, contactWindow, contact]
    
    @pyqtSlot()
    def loadContact(self):
        self._model._currentContactList = {}
        self._model._indexTable = {}
        contacts = self._model._database.getContacts()
        idx = 0
        for contact in contacts:

            if idx < int(contact[0]):
                idx = int(contact[0])

            contactInfo = createContactInfo(contact)
            contact = QTreeWidgetItem()
            contact.setCheckState(0, Qt.Unchecked)
            contactWindow = ContactWindow(contactInfo['id'],contactInfo, self)
            contactInfo['tags'] = contactInfo['tags']
            identifier = str(id(contact))
            self._model.indexTable = [identifier, contactInfo['id']]
            self._model.currentContactList = ['load', contactInfo, contactWindow, contact]
        
        self._model.id = idx + 1
            
    @pyqtSlot(dict)
    def deleteContacts(self, selected_element):
        identifier = [identifier for identifier in selected_element.keys() if selected_element[identifier][0]]
        idx = [self._model.indexTable[i] for i in identifier]
        self._model.currentContactList = ['delete', idx]

    
    @pyqtSlot(dict)
    def updateContact(self, contactInfo):
        idx = contactInfo['idx']
        contactInfo = {i : contactInfo[i] for i in contactInfo.keys() if i != 'id'}
        contactInfo['tags'] = '/'.join(contactInfo['tags'])
        self._model.currentContactList = ['update', contactInfo, idx]