import os
import sys

from Database.database import Database


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

class Model(QObject):
    updateContactSignal = pyqtSignal()
    insertElementSignal = pyqtSignal(list)
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

        if 'insert' in newContact[0] and 'id' not in newContact[1].keys():

            newContact[1]['photo'] = self._database.saveContact(self._id, newContact[1]['photo'], newContact[1]['name'], newContact[1]['secondName'], newContact[1]['phone'], newContact[1]['mail'], newContact[1]['notes'], newContact[1]['tags'])
            self._currentContactList[self._id] = newContact[1]
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])
            self._id += 1

        elif 'load' in newContact[0] and 'id' in newContact[1].keys() and  newContact[1]['id'] not in self._currentContactList.keys():

            self._currentContactList[newContact[1]['id']] = newContact[1]
            newContact[1] = {i : newContact[1][i] for i in newContact[1].keys() if i != 'id'}
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])

        elif 'load' in newContact[0] and 'id' in newContact[1].keys() and newContact[1]['id'] in self._currentContactList.keys():
     
            newContact[1] = {i : newContact[1][i] for i in newContact[1].keys() if i != 'id'}
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])

        elif 'update' in newContact[0]:

            self._database.updateContact(newContact[1]['photo'], newContact[1]['name'], newContact[1]['secondName'], newContact[1]['phone'], newContact[1]['mail'], newContact[1]['notes'], newContact[1]['tags'], newContact[2])
            self.updateContactSignal.emit()

        elif 'delete' in newContact[0]:
            
            for contact in newContact[1]:
                
                self._database.deleteContact(contact, self._currentContactList[contact]['photo'])
                self._currentContactList = {i:self._currentContactList[i] for i in self._currentContactList.keys() if i!=int(contact)}
                



