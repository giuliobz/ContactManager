import os 
import sys

from Widget.ContactWindow import ContactWindow

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QTreeWidgetItem


DIR_NAME = os.path.dirname(os.path.abspath('__file__'))


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        # Connect the model
        self._model = model

    @pyqtSlot(dict)
    def insertNewContact(self, newContact):
        contact = QTreeWidgetItem()
        contact.setCheckState(0, Qt.Unchecked)
        contact.setText(1, newContact['name'] + ' ' + newContact['secondName'])
        contactWindow = ContactWindow(newContact, self)
        newContact['tags'] = '/'.join(newContact['tags'])
        identifier = str(id(contact))
        self._model.currentContactList = [newContact, contactWindow, contact]
        self._model.indexTable = [identifier, self._model.id] if 'id' not in newContact.keys() else [identifier, newContact['id']]
    
    @pyqtSlot()
    def loadContact(self):
        contacts = self._model._database.getContacts()
        
        contactInfo = {}
        for i in range(len(contacts)):
            idx = contacts[i][0]
            
            if self._model.id < int(idx):
                self._model.id = contacts[i][0]
            contactInfo['id'] = contacts[i][0]
            contactInfo['name'] = contacts[i][1]
            contactInfo['secondName'] = contacts[i][2]
            contactInfo['phone'] = contacts[i][3]
            contactInfo['mail'] = contacts[i][4]
            contactInfo['notes'] = contacts[i][5]
            contactInfo['tags'] = contacts[i][6].split('/')
            self.insertNewContact(contactInfo)
            
    @pyqtSlot(QTreeWidgetItem)
    def upload_selected_element(self, item):
            self._model.selected_element = item

    @pyqtSlot()
    def deleteContacts(self):
        print(self._model.indexTable)
        for item in self._model.selected_element:
            print(str(id(item)))
            idx = self._model.indexTable[str(id(item))]
            self._model.currentContactList(item)
        
            
                
        
            
