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

        # Define list variable, is a dictonary where a id correspond a contact.
        self._currentContactList = {}

        # Map to connect QTreeWigetItem id with contact database id
        self._indexTable = {}

        # Define database where we can save all contatct
        self._database = Database()
    
    @property
    def currentContactList(self):
        return self._currentContactList
    
    @currentContactList.setter
    def currentContactList(self, newContact):

        if isinstance(newContact, list):

            self._currentContactList[newContact[0]] = newContact[1]
            self._database.saveContact(newContact[0], newContact[1][0], newContact[1][1], newContact[1][2], newContact[1][3], newContact[1][4], newContact[1][5])
            self.insertElementSygnal.emit(newContact[1])

        else:
            del self._currentContactList[newContact]
            self._database.deleteContact(newContact)
            self.deleteElementSygnal.emit(newContact)
