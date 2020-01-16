import os
import sys

from Database.database import Database


from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QWidget

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

class Model(QObject):
    updateContactSignal = pyqtSignal()
    refreshListSignal = pyqtSignal()
    searchMadeSignal = pyqtSignal(bool)
    insertElementSignal = pyqtSignal(list)
    changeCentralWidgetSignal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # Define the line and tag search element
        self._lineSearch = ''
        self._tagsSearch = '-- all --'
        self._searchDone = False

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
    def lineSearch(self):
        return self._lineSearch

    @property
    def tagsSearch(self):
        return self._tagsSearch 
    
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

    @property
    def searchDone(self):
        return self._searchDone
    
    @searchDone.setter
    def searchDone(self, slot):
        self._searchDone = slot
        self.searchMadeSignal.emit(slot)

    @lineSearch.setter
    def lineSearch(self, slot):
        self._lineSearch = slot

    @tagsSearch.setter
    def tagsSearch(self, slot):
        self._tagsSearch = slot

    @currentCentralWidget.setter
    def currentCentralWidget(self, slot):
        self._currentCentralWidget = slot[0]
        self.changeCentralWidgetSignal.emit(slot)
        

    @id.setter
    def id(self, slot):
       self._id = slot

    # In this case slot[0] is the item identifier and slot[1] is the id.
    @indexTable.setter
    def indexTable(self, slot):
        self._indexTable[slot[0]] = slot[1]

    # New Contact is a list where the first element is the id associated with the contact 
    # and the second element is a list of all information.
    @currentContactList.setter
    def currentContactList(self, newContact):

        # In this case the model has to update the currentContactList and notify it to the view.
        if 'insert' in newContact[0]:

            newContact[1]['photo'] = self._database.saveContact(self._id, newContact[1]['photo'], newContact[1]['name'], newContact[1]['secondName'], newContact[1]['phone'], newContact[1]['mail'], newContact[1]['notes'], newContact[1]['tags'])
            self._currentContactList[self._id] = newContact[1]
            newContact[1] = {i : newContact[1][i] for i in newContact[1].keys() if i != 'id'}
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])
            self._id += 1

        # This is the case where the model init the list when the user start the application.
        elif 'load' in newContact[0] and 'id' in newContact[1].keys() and  newContact[1]['id'] not in self._currentContactList.keys():

            self._currentContactList[newContact[1]['id']] = newContact[1]
            newContact[1] = {i : newContact[1][i] for i in newContact[1].keys() if i != 'id'}
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])

        # This is simply a utility function used to refresh the list view.
        elif 'load' in newContact[0] and 'id' in newContact[1].keys() and newContact[1]['id'] in self._currentContactList.keys():
     
            newContact[1] = {i : newContact[1][i] for i in newContact[1].keys() if i != 'id'}
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])

        # In this case a contact is updated by the user.
        elif 'update' in newContact[0]:
            
            self._database.updateContact(newContact[1]['photo'], newContact[1]['name'], newContact[1]['secondName'], newContact[1]['phone'], newContact[1]['mail'], newContact[1]['notes'], newContact[1]['tags'], newContact[2])
            self.updateContactSignal.emit()

        # Delete an existing contact.
        elif 'delete' in newContact[0]:
            
            for contact in newContact[1]:
                
                self._database.deleteContact(contact, self._currentContactList[contact]['photo'])
                self._indexTable = {i : self._indexTable[i] for i in self._indexTable.keys() if self._indexTable[i] != int(contact)}
                self._currentContactList = {i:self._currentContactList[i] for i in self._currentContactList.keys() if i!=int(contact)}
                self.refreshListSignal.emit()

        # Search in contact using key words or tag.
        elif 'search' in newContact[0]:
            
            self.insertElementSignal.emit([newContact[1]['name'] + ' ' + newContact[1]['secondName'], newContact[2], newContact[3]])

                



