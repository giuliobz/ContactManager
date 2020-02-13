import collections

from Build.Ui_ContactWidget import Ui_ContactWidget

from Model.ContactWindowModel import ContactWindowModel

from PyQt5.QtCore import pyqtSlot, Qt, QRegExp
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator

# Window that contain all the clips in annotation buffer with the correlated preferencies
class ContactWindow(QDialog):

    def __init__(self, mainModel):
        super().__init__()

        # The contact id to find it
        self.setWindowTitle('ciao')
        
        # Connect controller
        self._model = ContactWindowModel(mainModel)

        # Set up the user interface from Designer.
        self.ui = Ui_ContactWidget()
        self.ui.setupUi(self)
        self.ui.telephoneLine.setValidator(QRegExpValidator(QRegExp("\\d*"), self))

        # Connect with model signal
        self._model.closeWindowSignal.connect(self.closeWindow)
        self._model.contactChangedSignal.connect(self.changeTextColor)
        self._model.changePhotoSignal.connect(self.changeImage)
        self._model.initializeContactSignal.connect(self.initializeContactInfo)

        # Connect function to controller    
        self.ui.backButton.clicked.connect(self._model.closeWindow)
        self.ui.saveButton.clicked.connect(self._model.changeContactInfo)
        self.ui.resetImgButton.clicked.connect(self._model.resetImage)
        self.ui.deleteButton.clicked.connect(self._model.deleteContact)
        self.ui.changeImgButton.clicked.connect(self._model.changeImage)
        self.ui.deleteImageButton.clicked.connect(self._model.deleteImage)

        # Connect line changes 
        self.ui.nameLine.textChanged.connect(self._model.change_name) 
        self.ui.seconNameLine.textChanged.connect(self._model.change_secondName)
        self.ui.telephoneLine.textChanged.connect(self._model.change_Phone)
        self.ui.emailLine.textChanged.connect(self._model.change_Email)
        self.ui.noteBox.textChanged.connect(lambda : self._model.change_note(self.ui.noteBox.toPlainText()))
        self.ui.tagsList.itemChanged.connect(self._model.tagChanged)

    # function to initialize the contact window with the selected contact.
    @pyqtSlot(dict)
    def initializeContactInfo(self, contactInfo):
        # Set info in window
        self.ui.photo.setPixmap(QPixmap(contactInfo['photo']).scaled(289, 289))
        self.ui.nameLine.setText(contactInfo['name'])
        self.ui.seconNameLine.setText(contactInfo['secondName'])
        self.ui.telephoneLine.setText(contactInfo['phone'])
        self.ui.emailLine.setText(contactInfo['mail'])
        self.ui.noteBox.setText(contactInfo['notes'])

        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).text(0) in contactInfo['tags']:
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Checked)

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

    # change image
    @pyqtSlot(str)
    def changeImage(self, image):
        self.ui.photo.setPixmap(QPixmap(image).scaled(289, 289))

    # Reset the window information
    @pyqtSlot()
    def closeWindow(self):
        self.ui.nameText.setStyleSheet('color: black')
        self.ui.secondNameText.setStyleSheet('color: black')
        self.ui.phoneText.setStyleSheet('color: black')
        self.ui.mailText.setStyleSheet('color: black')
        self.ui.notesLabel.setStyleSheet('color: black')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)




    


    
