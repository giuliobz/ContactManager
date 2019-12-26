import os
import sys

from Database.database import Database

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

class Model(QObject):
    insertElementSygnal = pyqtSignal(list)
    deleteElementSygnal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # Define the variable of selected element in edit mode
        self._selected_element = []

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
       self._id = id

    @selected_element.setter
    def selected_element(self, slot):
        if slot in self._selected_element:
            self._selected_element.remove(slot)
        else:
            self._selected_element.append(slot)

    # In this case slot[0] is the item identifier and slot[1] is the id
    @indexTable.setter
    def indexTable(self, slot):
        self._indexTable[slot[0]] = slot[1]

    # New Contact is a list where the first element is the id associated with the contact 
    # and the second element is a list of all information
    @currentContactList.setter
    def currentContactList(self, newContact):

        if isinstance(newContact, list) and 'id' not in newContact[0].keys():

            self._currentContactList[self._id] = newContact[0]
            self._database.saveContact(self._id, newContact[0]['name'], newContact[0]['secondName'], newContact[0]['phone'], newContact[0]['mail'], newContact[0]['notes'], newContact[0]['tags'])
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])
            self._id += 1

        elif isinstance(newContact, list) and 'id' in newContact[0].keys():
            
            self._currentContactList[self._id] = newContact[0]
            self.insertElementSygnal.emit([newContact[0]['name'] + ' ' + newContact[0]['secondName'], newContact[1], newContact[2]])

        else:

            #del self._currentContactList[newContact]
            #self._database.deleteContact(newContact)
            self.deleteElementSygnal.emit(newContact)
            self._selected_element = []

