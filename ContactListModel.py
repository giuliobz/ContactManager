import os
import sys
import collections

from Database.database import Database

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, pyqtProperty
from PyQt5.QtWidgets import QWidget,QTreeWidgetItem

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))

# Simple utility function to create a dictionary 
#with the contact info.
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
    currentInformationSignal = pyqtSignal(dict)
    changeCentralWidgetSignal = pyqtSignal(int)
    searchDoneSignal = pyqtSignal(bool)
    refreshListSignal = pyqtSignal(list)
    addContactSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # Define the line and tag search element
        self._searchDone = False  

        # Define database where we can save all contatct
        self._database = Database()

        # Define the id counter
        self._id = 0

        # Define the current order method: 0 for name, 1 second name.
        self._currentIdOrder = 'FIRST_NAME'


    @pyqtProperty(bool, notify = searchDoneSignal)
    def searchDone(self):
        return self._searchDone
    
    @searchDone.setter
    def searchDone(self, slot):
        self._searchDone = slot
        self.searchDoneSignal.emit(slot)

    # Function to display the contact in the new Order
    @pyqtSlot(str)
    def setCurrentOrder(self, order_method):
        self._currentIdOrder = '_'.join(order_method.split(' ')).upper()
        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ])

    # This function changes the apllication view and set the contact information
    # for the user visualization.
    @pyqtSlot()
    def getInformation(self, id):
        contacts = [createContactInfo(c) for c in self._database.getContacts(self._currentIdOrder)]
        selected_contact = [contact for contact in contacts if id == contact['id']][0]
        self.currentInformationSignal.emit(selected_contact)
        self.changeCentralWidgetSignal.emit(2)

    # Function use only when the application start. It load all the contact 
    # stored in the database by the user.
    @pyqtSlot()
    def loadListContact(self):
        contact_info = [createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder)]
        for contact in contact_info:
            if int(contact['id']) > self._id:
                self._id = int(contact['id'])
            self.addContactSignal.emit(contact)
        
        self._id += 1

    # Simple function to delete contact in list.
    # This funtion is used also to delete a single contact.
    # In both case the contact list is refreshed .
    @pyqtSlot(dict)
    def deleteContacts(self, selected_contacts):
        for idx in selected_contacts.keys():
            if selected_contacts[idx]:
                self._database.deleteContact(idx)

        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ])

    # Define a function to add new contact in the database
    @pyqtSlot(dict)
    def addNewContact(self, contact):
        contact['id'] = self._id

        # If the user doesn't specify the name and second name of the 
        # contact, the name is setted like Unknown_ + id of the contact.
        if contact['name'] == '' and contact['secondName'] == '':
            contact['name'] = 'Unknown_' + str(self._id)

        # We check if the user already insert the contact in the list.
        # If it true we put the id in the surname. The user can change 
        # after the contact information.
        current_cotact = [ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ]
        if [c for c in current_cotact if contact['name'] == c['name'] and contact['secondName'] == c['secondName']]:
            contact['secondName'] += '_' + str(self._id)
        
        self._database.saveContact(self._id, contact['photo'], contact['name'], contact['secondName'], contact['phone'], contact['mail'], contact['notes'], '/'.join(contact['tags']))
        self._id += 1
        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ])
        

    # Simple function to search contact inside the list
    @pyqtSlot()
    def searchContacts(self, line, tag):
        current_contact_list = [ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ]

        # Is checked if the user make a search or not
        if not self._searchDone:
            selected_contact = []
            
            # In this case the user makes tag and text search
            if line != '' and tag != '-- all --':

                # If there is a space in lineSearch, is sure that 
                # the user want to search a contact using the contact name and surname.
                if ' ' in line:
                    lineText = line.split(' ')
                
                    for contact in current_contact_list:
                        if lineText[0].lower() in contact['name'].lower() and lineText[1].lower() in contact['secondName'].lower() and tag in contact['tags']:
                            selected_contact.append(contact)

                # If the space doesn't appear in lineSearch, the user can be use, for example, the mail, 
                # phone number or other contact info to search a contact in the list.
                else:

                    lineText = line.lower()
                    for contact in current_contact_list:
                        if (lineText.lower() in contact['name'].lower() or lineText in contact['secondName'].lower() or lineText in contact['mail'] or lineText == contact['phone']) and tag in contact['tags']:
                            selected_contact.append(contact)

            # In this case the user makes  text search
            elif line != '' and tag == '-- all --':

                if ' ' in line:
                    lineText = line.split(' ')

                    for contact in current_contact_list:
                        if lineText[0].lower() in contact['name'].lower() and lineText[1].lower() in contact['secondName'].lower():
                            selected_contact.append(contact)
                
                else:

                    lineText = line.lower()
                    for contact in current_contact_list:
                        if lineText.lower() in contact['name'].lower() or lineText in contact['secondName'].lower() or lineText in contact['mail'] or lineText == contact['phone']:
                            selected_contact.append(contact)

            # In this case the user makes tag search
            elif line == '' and tag != '-- all --':

                for contact in current_contact_list:
                    if tag in contact['tags']:
                        selected_contact.append(contact)

            self.searchDone = True
            self.refreshListSignal.emit(selected_contact)
        
        # if the user make a search, when he finish, the 
        # search variables (lineSearch and tagSearch) are reseted.
        else:

            self.searchDone = False
            self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ])

    # Function to update contact informations only if they are changed.
    @pyqtSlot(dict)
    def updateContactInfos(self, newContactInfo, currentContactInfo):
        contact_info = {}
        contact_info['photo'] = newContactInfo['photo'] if newContactInfo['photo'] != currentContactInfo['photo'] else currentContactInfo['photo']
        contact_info['name'] = newContactInfo['name'] if newContactInfo['name'] != currentContactInfo['name'] else currentContactInfo['name']
        contact_info['secondName'] = newContactInfo['secondName'] if newContactInfo['secondName'] != currentContactInfo['secondName'] else currentContactInfo['secondName']
        contact_info['phone'] = newContactInfo['phone'] if newContactInfo['phone'] != currentContactInfo['phone'] else currentContactInfo['phone']
        contact_info['mail'] = newContactInfo['mail'] if newContactInfo['mail'] != currentContactInfo['mail'] else currentContactInfo['mail']
        contact_info['notes'] = newContactInfo['notes'] if newContactInfo['notes'] != currentContactInfo['notes'] else currentContactInfo['notes']
        contact_info['tags'] = newContactInfo['tags'] if collections.Counter(newContactInfo['tags']) != collections.Counter(currentContactInfo['tags']) else currentContactInfo['tags']
        self._database.updateContact(contact_info['photo'], contact_info['name'], contact_info['secondName'], contact_info['phone'], contact_info['mail'], contact_info['notes'], '/'.join(contact_info['tags']), currentContactInfo['id'])

        self.refreshListSignal.emit([ createContactInfo(contact) for contact in self._database.getContacts(self._currentIdOrder) ])
        
