import cv2

from Build.Ui_NewContactWidget import Ui_NewContactWidget

from PyQt5.Qt import pyqtSlot, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, currentContactList, controller):
        super().__init__()

        # connect controller and model
        self._model = NewContactWindowModel(currentContactList)
        self._controller = controller

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)

        # Connect button
        self.ui.saveButton.clicked.connect(self.insertContact)
        self.ui.resetButton.clicked.connect(self.resetButton)
        self.ui.backButton.clicked.connect(lambda : self.backButtonFunc())
        self.ui.setPhoto.clicked.connect(lambda : self.changeImage())

        # Set default image. In this case is easier to put toghether thw controller and the view
        # and have a model that have inside the contact image.
        self.ui.photo.setPixmap(QPixmap(self._model.contactImage))

    def backButtonFunc(self):
        self._controller.changeCentralWidget('list')

    def insertContact(self):

        if self.ui.nameLine.text() == '' and self.ui.seconNameLine.text() == '':

            text = 'Name and second name are empty. Please specify the contact name and second name before save it.'
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()  

        elif [idx for idx in self._model.currentContactList.keys() if self.ui.nameLine.text() in self._model.currentContactList[idx]['name'] and self.ui.seconNameLine.text() in self._model.currentContactList[idx]['secondName']]:
            text= "Another contact with same name and second name still already exist. Press ok to modify the existing contact with these new information. Press cancel to go back in new contact window."
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self.close()
        
        else:

            contactInfo = {}
            contactInfo['photo'] = self._model.contactImage
            contactInfo['name'] = self.ui.nameLine.text()
            contactInfo['secondName'] = self.ui.seconNameLine.text()
            contactInfo['phone'] = self.ui.telephoneLine.text()
            contactInfo['mail'] = self.ui.emailLine.text()
            contactInfo['notes'] = self.ui.noteBox.toPlainText()
            contactInfo['tags'] = []
            for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
                if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
                    contactInfo['tags'].append(self.ui.tagsList.invisibleRootItem().child(i).text(0))
            
            self._controller.insertNewContact(contactInfo)
            self._controller.changeCentralWidget('list')
        
    def resetButton(self):
        
        self.ui.nameLine.setText('')
        self.ui.seconNameLine.setText('')
        self.ui.telephoneLine.setText('')
        self.ui.emailLine.setText('')
        self.ui.noteBox.setText('')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
               self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)

    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if fileName[0] != '':
            self._model.contactImage = fileName[0]
            self.ui.photo.setPixmap(QPixmap(self._model.contactImage))

class NewContactWindowModel(QObject):

    def __init__(self, currentContactList):
        super().__init__()

        # Define the image path
        self._contactImage = 'Build/contact_2.png'
        self._currentContactList = currentContactList

    @property
    def currentContactList(self):
        return self._currentContactList

    @property
    def contactImage(self):
        return self._contactImage
    
    @contactImage.setter
    def contactImage(self, image):
        self._contactImage = image

