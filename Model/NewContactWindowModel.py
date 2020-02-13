from PyQt5.Qt import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTreeWidgetItem, QFileDialog

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

class NewContactWindowModel(QObject):
    resetSignal = pyqtSignal()
    changePhotoSignal = pyqtSignal(str)

    def __init__(self, mainModel):
        super().__init__()

        # Connect the model with the main model
        self._mainModel = mainModel

        # Define the variable that contain the contact info.
        self._contactInfo = {}

    # memorize the changes in name
    @pyqtSlot(str)
    def change_name(self, name):
        if name != '':
            self._contactInfo['name'] = name
        elif 'name' in self._contactInfo.keys():
            del self._contactInfo['name']
    
    # memorize the changes in second name
    @pyqtSlot(str)
    def change_secondName(self, secondName):
        if secondName != '':
            self._contactInfo['secondName'] = secondName
        elif 'secondName' in self._contactInfo.keys():
            del self._contactInfo['secondName']
    
    # memorize the changes in phone
    @pyqtSlot(str)
    def change_Phone(self, phone):
        if phone != '':
            self._contactInfo['phone'] = phone
        elif 'phone' in self._contactInfo.keys():
            del self._contactInfo['phone']
  
    # memorize the changes in mail
    @pyqtSlot(str)
    def change_Email(self, mail):
        if mail != '':
            self._contactInfo['mail'] = mail

        elif 'mail' in self._contactInfo.keys():
            del self._contactInfo['mail']
    
    # memorize the changes in note
    @pyqtSlot(str)
    def change_note(self, note):
        if note != '':
            self._contactInfo['note'] = note

        elif 'note' in self._contactInfo.keys():
            del self._contactInfo['note']

             
    # memorize the changes in tags
    @pyqtSlot(QTreeWidgetItem, int)
    def tagChanged(self, item, column):
        if 'tags' not in self._contactInfo.keys():
            self._contactInfo['tags'] = [item.text(0)]

        elif item.text(0) in self._contactInfo['tags']:
            self._contactInfo['tags'].remove(item.text(0))

        else:
            self._contactInfo['tags'].append(item.text(0))
        
        if not self._contactInfo['tags']:
            del self._contactInfo['tags']

    # Function to insert the new contact in the Contact list 
    # and save it in the database. If the contact already exists
    # the user has to modify the name and second name infos.
    # If not, the existing contact will be changed.
    @pyqtSlot()
    def insertContact(self):
        # Is controlled if the user really create a new contact.
        # If not the user return to previews view.
        if self._contactInfo.keys():
            self._mainModel.addNewContact(self._contactInfo)
        
        else:
            self._mainModel.changeWidget(0)
        
        self.resetSignal.emit()

    #Funtion to reset photo
    @pyqtSlot()
    def resetPhoto(self):
        self._contactInfo['photo'] = 'Build/contact_2.png'
        self.changePhotoSignal.emit('Build/contact_2.png')

    # Funtion to set photo
    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._contactInfo['photo'] = fileName[0]
            self.changePhotoSignal.emit(fileName[0])
    
    # Funtion to change the view with the contact
    # list main view
    @pyqtSlot()
    def changeView(self):
        self.resetSignal.emit()
        self._mainModel.changeCentralWidgetSignal.emit(0)