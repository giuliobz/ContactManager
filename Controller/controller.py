import os 
import sys

from Widget.NewContactWindow import NewContactWindow
from Widget.ContactWindow import ContactWindow

from PyQt5.QtCore import QObject, pyqtSlot, Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget


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
        contactWindow = ContactWindow(newContact, self)
        newContact['tags'] = '/'.join(newContact['tags'])
        identifier = str(id(contact))
        self._model.indexTable = [identifier, self._model.id] if 'id' not in newContact.keys() else [identifier, newContact['id']]
        self._model.currentContactList = [newContact, contactWindow, contact]
    
    @pyqtSlot()
    def loadContact(self):

        contacts = self._model._database.getContacts()
        contactInfo = {}
        for contact in contacts:

            if self._model.id < int(contact[0]):
                self._model.id = int(contact[0])

            
            contactInfo['id'] = int(contact[0])
            contactInfo['photo'] = (contact[1])
            contactInfo['name'] = contact[2]
            contactInfo['secondName'] = contact[3]
            contactInfo['phone'] = contact[4]
            contactInfo['mail'] = contact[5]
            contactInfo['notes'] = contact[6]
            contactInfo['tags'] = contact[7].split('/')
            self.insertNewContact(contactInfo)
        
        self._model.id = self._model.id + 1
            
    @pyqtSlot(list)
    def upload_selected_element(self, selected):
            self._model.selected_element = selected

    @pyqtSlot()
    def deleteContacts(self):
        
        identifier = [identifier for identifier in self._model.selected_element.keys() if self._model.selected_element[identifier][0]]
        idx = [self._model.indexTable[i] for i in identifier]
        self._model.currentContactList = [idx]

    @pyqtSlot()
    def refreshList(self):
        for id in self._model.currentContactList.keys():
            contact = QTreeWidgetItem()
            contact.setCheckState(0, Qt.Unchecked)
            contactWindow = ContactWindow(self._model.currentContactList[id], self)
            self._model.insertElementSygnal.emit([self._model.currentContactList[id]['name'] + ' ' + self._model.currentContactList[id]['secondName'], contactWindow, contact])
        
    



        
    
            
                
        
            
