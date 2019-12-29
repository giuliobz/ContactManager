import collections

from Build.Ui_ContactWidget import Ui_ContactWidget


from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

# Window that contain all the clips in annotation buffer with the correlated preferencies
class ContactWindow(QDialog):

    def __init__(self, idx, contactInfo, controller):
        super().__init__()

        # The contact id to find it 
        self._id = idx
        self._contactInfo = contactInfo
        
        # Connect controller
        self._model = ContactWindowModel(idx, contactInfo)
        self._controller = ContactWindowController(controller, self._model)

        # Set up the user interface from Designer.
        self.ui = Ui_ContactWidget()
        self.ui.setupUi(self)

        # Set info in window
        self.ui.photo.setPixmap(QPixmap(contactInfo['photo']))
        self.ui.nameLine.setText(contactInfo['name'])
        self.ui.seconNameLine.setText(contactInfo['secondName'])
        self.ui.telephoneLine.setText(contactInfo['phone'])
        self.ui.emailLine.setText(contactInfo['mail'])
        self.ui.noteBox.setText(contactInfo['notes'])
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).text(0) in contactInfo['tags']:
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Checked)

        # Connect with model signal
        self._model.closeWindowSignal.connect(lambda : self.closeWindow())
        self._model.contactChangedSignal.connect(self.changeTextColor)

        # Connect function to controller    
        self.ui.backButton.clicked.connect(self._controller.backFunc)
        #self.ui.saveButton.clicked.connect(self._controller.changeContactInfo)
        self.ui.resetImgButton.clicked.connect(self._controller.resetImage)
        self.ui.changeImgButton.clicked.connect(self._controller.changeImage)
        self.ui.deleteImageButton.clicked.connect(self._controller.deleteImage)

        # Connect line changes 
        self.ui.nameLine.textChanged.connect(self._controller.change_name) 
        self.ui.seconNameLine.textChanged.connect(self._controller.change_secondName)
        self.ui.telephoneLine.textChanged.connect(self._controller.change_Phone)
        self.ui.emailLine.textChanged.connect(self._controller.change_Email)
        self.ui.noteBox.textChanged.connect(self.change_note)
        self.ui.tagsList.itemChanged.connect(self._controller.tagChanged)

    @pyqtSlot(list)
    def changeTextColor(self, slot):

        if slot[0] == 'name':
            self.ui.nameText.setStyleSheet('color: ' + slot[1])
        
        if slot[0] == 'secondName':
            self.ui.secondNameText.setStyleSheet('color: ' + slot[1])
        
        if slot[0] == 'phone':
            self.ui.phoneText.setStyleSheet('color: ' + slot[1])
        
        if slot[0] == 'mail':
            self.ui.mailText.setStyleSheet('color: ' + slot[1])
        
        if slot[0] == 'notes':
            
            self.ui.notesLabel.setStyleSheet('color: ' + slot[1])

        if slot[0] == 'foto':

            self.ui.photo.setPixmap(QPixmap(slot[1]))

        self._controller.checkChanges()


    def change_note(self):
        self._controller.change_note(self.ui.noteBox.toPlainText())

    def closeWindow(self):
        self.ui.photo.setPixmap(QPixmap(self._model.currentContactInfo['photo']))
        self.ui.nameLine.setText(self._model.currentContactInfo['name'])
        self.ui.nameText.setStyleSheet('color: black')
        self.ui.seconNameLine.setText(self._model.currentContactInfo['secondName'])
        self.ui.secondNameText.setStyleSheet('color: black')
        self.ui.telephoneLine.setText(self._model.currentContactInfo['phone'])
        self.ui.phoneText.setStyleSheet('color: black')
        self.ui.emailLine.setText(self._model.currentContactInfo['mail'])
        self.ui.mailText.setStyleSheet('color: black')
        self.ui.noteBox.setText(self._model.currentContactInfo['notes'])
        self.ui.notesLabel.setStyleSheet('color: black')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).text(0) in self._model.currentContactInfo['tags']:
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Checked)
        
        self.close()

    

class ContactWindowModel(QObject):
    closeWindowSignal = pyqtSignal()
    contactChangedSignal = pyqtSignal(list)

    def __init__(self, idx, contactInfo):
        super().__init__()

        # The two variable that memorize event change.
        # The first take the original information, the second
        # contain the key of the changed element. Important:
        # in new contact window i put the current tags selected for
        # this contact. This permits a better contact update.
        self._currentContactInfo = contactInfo
        self._newContactInfo = {}
        self._newContactInfo['tags'] = contactInfo['tags']

        # Define a boolean that is True if in newContactinfo 
        # I have more that one key or if tags list has length 
        # greater that the currentContactInfo tags list.
        self._is_changed = []

        # Define the id f this contact
        self._id = idx

    @property
    def id(self):
        return self._id

    @property
    def newContactInfo(self):
        return self._newContactInfo

    @property
    def currentContactInfo(self):
        return self._currentContactInfo 

    @property
    def is_changed(self):
        return self._is_changed
    
    @property
    def foto(self):
        if 'photo' in self._newContactInfo:
            return self._newContactInfo['foto']
        return ''
    
    @property
    def name(self):
        if 'name' in self._newContactInfo:
            return self._newContactInfo['name']
        return ''
    
    @property
    def secondName(self):
        if 'secondName' in self._newContactInfo:
            return self._newContactInfo['secondName']
        return ''
    
    @property
    def phone(self):
        if 'phone' in self._newContactInfo:
            return self._newContactInfo['phone']
        return ''

    @property
    def mail(self):
        if 'mail' in self._newContactInfo:
            return self._newContactInfo['mail']
        return ''

    @property
    def notes(self):
        if 'notes' in self._newContactInfo:
            return self._newContactInfo['notes']
        return ''

    @property
    def tags(self):
        if 'tags' in self._newContactInfo:
            return self._newContactInfo['tags']
        return []
    
    @foto.setter
    def foto(self, foto):
        self._newContactInfo['foto'] = foto
        if self._newContactInfo['foto'] == self._currentContactInfo['photo']:
            del self._newContactInfo['foto']
        self.contactChangedSignal.emit(['foto', foto])
    
    @name.setter
    def name(self, name):
        self._newContactInfo['name'] = name
        if self._newContactInfo['name'] == self._currentContactInfo['name']:
            del self._newContactInfo['name']
        self.contactChangedSignal.emit(['name', 'red' if name != self._currentContactInfo['name'] else 'black'])

    @secondName.setter
    def secondName(self, secondName):
        self._newContactInfo['secondName'] = secondName
        if self._newContactInfo['secondName'] == self._currentContactInfo['secondName']:
            del self._newContactInfo['secondName']
        self.contactChangedSignal.emit(['secondName', 'red' if secondName != self._currentContactInfo['secondName'] else 'black'])
    
    @phone.setter
    def phone(self, phone):
        self._newContactInfo['phone'] = phone
        if self._newContactInfo['phone'] == self._currentContactInfo['phone']:
            del self._newContactInfo['phone']
        self.contactChangedSignal.emit(['phone', 'red' if phone != self._currentContactInfo['phone'] else 'black'])
        

    @mail.setter
    def mail(self, mail):
        self._newContactInfo['mail'] = mail
        if self._newContactInfo['mail'] == self._currentContactInfo['mail']:
            del self._newContactInfo['mail']
        self.contactChangedSignal.emit(['mail', 'red' if mail != self._currentContactInfo['mail'] else 'mail'])

    @notes.setter
    def notes(self, notes):
        self._newContactInfo['notes'] = notes
        if self._newContactInfo['notes'] == self._currentContactInfo['notes']:
            del self._newContactInfo['notes']
        self.contactChangedSignal.emit(['notes', 'red' if notes != self._currentContactInfo['notes'] else 'notes'])
        

    @tags.setter
    def tags(self, tags):
        self._newContactInfo['tags'].append(tags)


    @newContactInfo.setter
    def newContactInfo(self, slot):
        self._newContactInfo = slot

    @currentContactInfo.setter
    def currentContactInfo(self, slot):
        self._currentContactInfo = slot
        self._newContactInfo = {}
        self.closeWindowSignal.emit()

    @is_changed.setter
    def is_changed(self, slot):
        self._is_changed = slot

class ContactWindowController(QObject):

    def __init__(self, controller, model):
        super().__init__()

        # Connect this controller with the main controller.
        # This is made because this function is used by others widget.
        # This on_configure function is the updateContact function in 
        # the main controller.
        self._controller = controller

        # Connnect controller with the model
        self._model = model

    @pyqtSlot()
    def checkChanges(self):
        if len(self._model.newContactInfo.keys()) == 1 and collections.Counter(self._model.newContactInfo['tags']) == collections.Counter(self._model.currentContactInfo['tags']):
            self._model.is_changed = False
        else:
            self._model.is_changed = True


    # When a element is selected or deselected the 
    # selected_element variable is updated.
    @pyqtSlot(QTreeWidgetItem, int)
    def tagChanged(self, item, column):
        if item.text(0) in self._model.tags:
            self._model.tags.remove(item.text(0))
        else:
            self._model.tags = item.text(0)

        print(self._model.tags)

    @pyqtSlot(str)
    def change_name(self, name):
        self._model.name = name

    
    @pyqtSlot(str)
    def change_secondName(self, secondName):
        self._model.secondName = secondName

    
    @pyqtSlot(str)
    def change_Phone(self, phone):
        self._model.phone = phone

    
    @pyqtSlot(str)
    def change_Email(self, mail):
        self._model.mail = mail

    
    @pyqtSlot(str)
    def change_note(self, note):
        self._model.notes = note

    @pyqtSlot()
    def backFunc(self):
        if self._model.is_changed:
            text= "You are exing with modify field. Press ok if you want to lost all changes, else press cancel"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self._model.closeWindowSignal.emit()
        

    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._model.foto = fileName[0]

    @pyqtSlot()
    def resetImage(self):
        self._model.foto = self._model.currentContactInfo['photo']
    

    @pyqtSlot()
    def deleteImage(self):
        self._model.foto = 'Build/contact_2.png'

    @pyqtSlot()
    def changeContactInfo(self):
        contactInfo = {}
        if len(self._model.newContactInfo.keys()) > 0:
            text = "You are changing a contact. Press ok to modify the existing contact with these new information. Press cancel to go back in new contact window."
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                contactInfo = self._model.currentContactInfo
                for key in self._model.newContactInfo.keys():
                    contactInfo[key] = self._model.newContactInfo[key]
                contactInfo['idx'] = self._model.id
                
                self._controller.updateContact(contactInfo)
        
        if len(contactInfo.keys()) > 0:
            self._model.currentContactInfo = contactInfo
        
        else:

            self._model.currentContactInfo = self._model.currentContactInfo

    


    
