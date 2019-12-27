import os
import sys

from Database.database import Database


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

class Model(QObject):
    insertElementSygnal = pyqtSignal(list)
    changeCentralWidgetSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # Define the current central widget
        self._currentCentralWidget = None

        # Define list variable, is a dictonary where a id correspond a contact.
        self._currentContactList = {}

        # Map to connect QTreeWigetItem id with contact database id
        self._indexTable = {}

        # Define database where we can save all contatct
        self._database = Database()

        # Define the id counter
        self._id = 0
    
    @property
    def currentCentralWidget(self):
        return self._currentCentralWidget
    
    @property
    def currentContactList(self):
        return self._currentContactList

    @property
    def indexTable(self):
        return self._indexTable

    @property
    def id(self):
        return self._id

    @currentCentralWidget.setter
    def currentCentralWidget(self, slot):
        self._currentCentralWidget = slot
        self.changeCentralWidgetSignal.emit(slot)
        

    @id.setter
    def id(self, slot):
       self._id = slot

    # In this case slot[0] is the item identifier and slot[1] is the id
    @indexTable.setter
    def indexTable(self, slot):
        self._indexTable[slot[0]] = slot[1]

    # New Contact is a list where the first element is the id associated with the contact 
    # and the second element is a list of all information
    @currentContactList.setter
    def currentContactList(self, newContact):

        if isinstance(newContact[0], dict) and 'id' not in newContact[0].keys():

            newContact[0]['photo'] = self._database.saveContact(self._id, newContact[0]['photo'], newContact[0]['name'], newContact[0]['secondName'], newContact[0]['phone'], newContact[0]['mail'], newContact[0]['notes'], newContact[0]['tags'])
            self._currentContactList[self._id] = newContact[0]
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])
            self._id += 1

        elif isinstance(newContact[0], dict) and 'id' in newContact[0].keys() and  newContact[0]['id'] not in self._currentContactList.keys():

            self._currentContactList[newContact[0]['id']] = newContact[0]
            newContact[0] = {i : newContact[0][i] for i in newContact[0].keys() if i != 'id'}
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])

        elif isinstance(newContact[0], dict) and 'id' in newContact[0].keys() and newContact[0]['id'] in self._currentContactList.keys():
            
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])

        else:
            
            for contact in newContact[0]:
                
                self._database.deleteContact(contact, self._currentContactList[contact]['photo'])
                self._currentContactList = {i:self._currentContactList[i] for i in self._currentContactList.keys() if i!=int(contact)}
                



