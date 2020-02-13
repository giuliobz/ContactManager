import collections

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QFileDialog, QMessageBox


class ContactWindowModel(QObject):
    closeWindowSignal = pyqtSignal()
    changePhotoSignal = pyqtSignal(str)
    initializeContactSignal = pyqtSignal(dict)
    contactChangedSignal = pyqtSignal(list)

    def __init__(self, mainModel):
        super().__init__()

        # The two variable that memorize event change.
        # The first take the original information, the second
        # contain the key of the changed element.
        self._currentContactInfo = {}
        self._newContactInfo = {}

        # Connect the model to the main model
        self._mainModel = mainModel

        # Define the id for this contact
        self._id = 0

        # Connect the initialization signal 
        self._mainModel.currentInformationSignal.connect(self.initializeContactInfo)

    # Funtion to inizialize the contact informaton in the 
    # contact window.
    @pyqtSlot(dict)
    def initializeContactInfo(self, contactInfo):
        self._id = contactInfo['id']
        self._currentContactInfo = contactInfo
        self.initializeContactSignal.emit(contactInfo)

    # Simple function to delete current image, setting the default one.
    @pyqtSlot()
    def deleteImage(self):
        self._newContactInfo['photo'] = 'Build/contact_2.png' 
        self.changePhotoSignal.emit('Build/contact_2.png')
    
    # Simple funtion to undo the photo changes
    @pyqtSlot()
    def resetImage(self):
        del self._newContactInfo['photo']
        self.changePhotoSignal.emit(self._currentContactInfo['photo'])

    # Allow the user to change te photo.
    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._newContactInfo['photo'] = fileName[0]
            self.changePhotoSignal.emit(fileName[0])

    # memorize the changes in name
    @pyqtSlot(str)
    def change_name(self, name):
        if name != self._currentContactInfo['name']:
            self._newContactInfo['name'] = name

        if 'name' in self._newContactInfo.keys() and self._newContactInfo['name'] == '':
            del self._newContactInfo['name']
        
        self.contactChangedSignal.emit(['name', 'red' if name != self._currentContactInfo['name'] else 'black'])
    
    # memorize the changes in second name
    @pyqtSlot(str)
    def change_secondName(self, secondName):
        if secondName != self._currentContactInfo['secondName']:
            self._newContactInfo['secondName'] = secondName

        if 'secondName' in self._newContactInfo.keys() and self._newContactInfo['secondName'] == '':
            del self._newContactInfo['secondName']

        self.contactChangedSignal.emit(['secondName', 'red' if secondName != self._currentContactInfo['secondName'] else 'black'])

    # memorize the changes in phone
    @pyqtSlot(str)
    def change_Phone(self, phone):
        if phone != self._currentContactInfo['phone']:
            self._newContactInfo['phone'] = phone

        if 'phone' in self._newContactInfo.keys() and self._newContactInfo['phone'] == '':
            del self._newContactInfo['phone']

        self.contactChangedSignal.emit(['phone', 'red' if phone != self._currentContactInfo['phone'] else 'black'])

    # memorize the changes in mail
    @pyqtSlot(str)
    def change_Email(self, mail):
        if mail != self._currentContactInfo['mail']:
            self._newContactInfo['mail'] = mail

        if 'mail' in self._newContactInfo.keys() and self._newContactInfo['mail'] == '':
            del self._newContactInfo['mail']

        self.contactChangedSignal.emit(['mail', 'red' if mail != self._currentContactInfo['mail'] else 'black'])

    # memorize the changes in note
    @pyqtSlot(str)
    def change_note(self, note):
        if note!= self._currentContactInfo['notes']:
            self._newContactInfo['notes'] = note

        self.contactChangedSignal.emit(['notes', 'red' if note != self._currentContactInfo['notes'] else 'black'])

        if 'notes' in self._newContactInfo.keys() and self._newContactInfo['notes'] == '':
            del self._newContactInfo['notes']

    # memorize the changes in tags
    @pyqtSlot(QTreeWidgetItem, int)
    def tagChanged(self, item, column):
        if not 'tags' in self._newContactInfo.keys():
            self._newContactInfo['tags'] = [item.text(0)]

        elif item.text(0) in self._newContactInfo['tags']:
            self._newContactInfo['tags'].remove(item.text(0))

        else:
            self._newContactInfo['tags'].append(item.text(0))

    # Simple function to delete contacts
    @pyqtSlot()
    def deleteContact(self):
        text= "You are deleting a contact press ok to delete it, else press cancel."
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if (msgBox.exec_() == QMessageBox.Ok):
            self._mainModel.deleteContact(self._id)
            self.closeWindow()

    # Funtion to reset the the contact to the actual information
    @pyqtSlot()
    def closeWindow(self):
        self.closeWindowSignal.emit()
        self._id = 0
        self._currentContactInfo = {}
        self._newContactInfo = {}
        self._mainModel.changeCentralWidgetSignal.emit(0)

    # Function to save the changes
    @pyqtSlot()
    def changeContactInfo(self):
        # We check if the tags are changed and if the user changes more contact info. In this case 
        # the current contact Infos are changed with the new contct infos.
        if collections.Counter(self._newContactInfo['tags']) != collections.Counter(self._currentContactInfo['tags']) or len(self._newContactInfo.keys() > 1):
            text= "Are you sure to change definetly the contact infomrations? Press ok to save the change, else press cancel."
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                for key in self._newContactInfo.keys():
                    self._currentContactInfo[key] = self._newContactInfo[key]
                
                self._mainModel.updateContactInfos(self._currentContactInfo)
                self.closeWindow()
            




        