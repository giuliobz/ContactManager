import os
import sys

from Database.database import Database


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

class Model(QObject):
    insertElementSygnal = pyqtSignal(list)
    deleteElementsSygnal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Define the variable of selected element in edit mode.
        # the key is the item identifier and the value is
        # the item QCheckBox current value.
        self._selected_element = {}

        # Define list variable, is a dictonary where a id correspond a contact.
        self._currentContactList = {}

        # Map to connect QTreeWigetItem id with contact database id
        self._indexTable = {}

        # Define database where we can save all contatct
        self._database = Database()

        # Define the id counter
        self._id = 0

    @property
    def selected_element(self):
        return self._selected_element
    
    @property
    def currentContactList(self):
        return self._currentContactList

    @property
    def indexTable(self):
        return self._indexTable

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, slot):
       self._id = slot

    @selected_element.setter
    def selected_element(self, slot):
        self._selected_element = slot

    # In this case slot[0] is the item identifier and slot[1] is the id
    @indexTable.setter
    def indexTable(self, slot):
        self._indexTable[slot[0]] = slot[1]

    # New Contact is a list where the first element is the id associated with the contact 
    # and the second element is a list of all information
    @currentContactList.setter
    def currentContactList(self, newContact):

        if isinstance(newContact[0], dict) and 'id' not in newContact[0].keys():

            self._currentContactList[self._id] = newContact[0]
            self._database.saveContact(self._id, newContact[0]['name'], newContact[0]['secondName'], newContact[0]['phone'], newContact[0]['mail'], newContact[0]['notes'], newContact[0]['tags'])
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])
            self._id += 1

        elif isinstance(newContact[0], dict) and 'id' in newContact[0].keys():
            
            id =  int(newContact[0]['id'])
            del newContact[0]['id']
            self._currentContactList[id] = newContact[0]
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])

        else:
            
            for contact in newContact[0]:
                
                del self._currentContactList[contact]
                self._database.deleteContact(contact)
            
            self.deleteElementsSygnal.emit()
            self._selected_element = []


