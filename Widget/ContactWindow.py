import collections

from Build.Ui_ContactWidget import Ui_ContactWidget

from Model.ContactWindowModel import ContactWindowModel

from Controller.ContactWindowController import ContactWindowController

from PyQt5.QtCore import pyqtSlot, Qt, QRegExp
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator

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
        self.ui.telephoneLine.setValidator(QRegExpValidator(QRegExp("\\d*"), self))

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
        self.ui.saveButton.clicked.connect(self._controller.changeContactInfo)
        self.ui.resetImgButton.clicked.connect(self._controller.resetImage)
        self.ui.deleteButton.clicked.connect(self._controller.deleteContact)
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

        if slot[0] == 'photo':

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

    




    


    
