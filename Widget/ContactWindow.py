from Build.Ui_ContactWidget import Ui_ContactWidget

from PyQt5.QtCore import pyqtSlot, Qt, QRegExp
from PyQt5.QtWidgets import QDialog,QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator


class ContactWindow(QDialog):

    def __init__(self, model, changeCentralWidget):
        super().__init__()

        # The two variable that memorize event change.
        # The first take the original information, the second
        # contain the key of the changed element.
        self._currentContactInfo = {}
        self._new_photo = ''
        
        # Connect model and to the change central widget funtion
        self._model = model
        self._changeCentralWidget = changeCentralWidget 

        # Set up the user interface from Designer.
        self.ui = Ui_ContactWidget()
        self.ui.setupUi(self)
        self.ui.telephoneLine.setValidator(QRegExpValidator(QRegExp("\\d*"), self))

        # Connect with model signal
        self._model.currentInformationSignal.connect(self.initializeContactInfo)

        # Define button function   
        self.ui.backButton.clicked.connect(self.closeWindow)
        self.ui.saveButton.clicked.connect(self.changeContactInfo)
        self.ui.resetImgButton.clicked.connect(self.resetImage)
        self.ui.deleteButton.clicked.connect(self.deleteContact)
        self.ui.changeImgButton.clicked.connect(self.changeImage)
        self.ui.deleteImageButton.clicked.connect(self.deleteImage)

        # Connect line changes 
        self.ui.nameLine.textChanged.connect(self.change_name) 
        self.ui.seconNameLine.textChanged.connect(self.change_secondName)
        self.ui.telephoneLine.textChanged.connect(self.change_Phone)
        self.ui.emailLine.textChanged.connect(self.change_Email)
        self.ui.noteBox.textChanged.connect(lambda : self.change_note(self.ui.noteBox.toPlainText()))

    # Function to initialize the contact window with the selected contact.
    @pyqtSlot(dict)
    def initializeContactInfo(self, contactInfo):
        self._currentContactInfo = contactInfo

        self.ui.photo.setPixmap(QPixmap(contactInfo['photo']).scaled(289, 289))
        self.ui.nameLine.setText(contactInfo['name'])
        self.ui.seconNameLine.setText(contactInfo['secondName'])
        self.ui.telephoneLine.setText(contactInfo['phone'])
        self.ui.emailLine.setText(contactInfo['mail'])
        self.ui.noteBox.setText(contactInfo['notes'])

        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).text(0) in contactInfo['tags']:
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Checked)

    # Simple function to delete current image, setting the default one.
    @pyqtSlot()
    def deleteImage(self):
        self._new_photo = 'Build/contact_2.png' 
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
    
    # Simple funtion to undo the photo changes
    @pyqtSlot()
    def resetImage(self):
        self._new_photo = ''
        self.ui.photo.setPixmap(QPixmap(self._currentContactInfo['photo']).scaled(289, 289))

    # Allow the user to change the photo.
    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png *.jpeg)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0] or '.jpeg' in fileName[0]:
            self._new_photo = fileName[0]
            self.ui.photo.setPixmap(QPixmap(fileName[0]).scaled(289, 289))

    # Function to display name field changes
    @pyqtSlot(str)
    def change_name(self, name):
        if name != self._currentContactInfo['name']:
            self.ui.nameText.setStyleSheet('color: red')
        else:
            self.ui.nameText.setStyleSheet('color: black')
    
    # Function to display second name field changes
    @pyqtSlot(str)
    def change_secondName(self, secondName):
        if secondName != self._currentContactInfo['secondName']:
            self.ui.secondNameText.setStyleSheet('color: red')
        else:
            self.ui.secondNameText.setStyleSheet('color: black')
            
    # Function to display phone field changes
    @pyqtSlot(str)
    def change_Phone(self, phone):
        if phone != self._currentContactInfo['phone']:
            self.ui.phoneText.setStyleSheet('color: red')
        else:
            self.ui.phoneText.setStyleSheet('color: black')

    # Function to display mail field changes
    @pyqtSlot(str)
    def change_Email(self, mail):
        if mail != self._currentContactInfo['mail']:
            self.ui.mailText.setStyleSheet('color: red')
        else:
            self.ui.mailText.setStyleSheet('color: black')

    # Function to display notes field changes
    @pyqtSlot(str)
    def change_note(self, note):
        if note!= self._currentContactInfo['notes']:
            self.ui.notesLabel.setStyleSheet('color: red')
        else:
            self.ui.notesLabel.setStyleSheet('color: black')

    # Function to change contact info 
    @pyqtSlot()
    def changeContactInfo(self):
        newContactInfo = {}
        newContactInfo['photo'] = self._new_photo if self._new_photo != '' else self._currentContactInfo['photo']
        newContactInfo['name'] = self.ui.nameLine.text()
        newContactInfo['secondName'] = self.ui.seconNameLine.text()
        newContactInfo['phone'] = self.ui.telephoneLine.text()
        newContactInfo['mail'] = self.ui.emailLine.text()
        newContactInfo['notes'] = self.ui.noteBox.toPlainText()
        newContactInfo['tags'] = []
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).checkState(0):
                newContactInfo['tags'].append(self.ui.tagsList.invisibleRootItem().child(i).text(0))
        
        # In a real case we controll if the contact updates is made or not.
        self._model.updateContactInfos(newContactInfo, self._currentContactInfo)
        self.closeWindow()
    
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
            self._model.deleteContacts({self._currentContactInfo['id'] : True})
            self.closeWindow()
        

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

        self._currentContactInfo = {}
        self._newContactInfo = {}

        self._changeCentralWidget(0)



    


    
