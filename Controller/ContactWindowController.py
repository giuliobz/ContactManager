import collections

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

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
        
        self._model.tags = item.text(0)


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
    def deleteContact(self):
        self._model

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
        
        else:
            
            self._model.closeWindowSignal.emit()
        

    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._model.photo = fileName[0]

    @pyqtSlot()
    def resetImage(self):
        self._model.photo = self._model.currentContactInfo['photo']
    

    @pyqtSlot()
    def deleteImage(self):
        self._model.photo = 'Build/contact_2.png'

    @pyqtSlot()
    def changeContactInfo(self):
        contactInfo = {}
        if self._model.is_changed:
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
        
        if self._model.is_changed:
            self._model.currentContactInfo = contactInfo
        else:
            self._model.currentContactInfo = self._model.currentContactInfo