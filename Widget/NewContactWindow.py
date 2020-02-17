from Build.Ui_NewContactWidget import Ui_NewContactWidget

from PyQt5.Qt import pyqtSlot, Qt, pyqtSignal, QObject, QRegExp
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QIntValidator, QRegExpValidator

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, model, changeCentralWidget):
        super().__init__()

        # Define variable to memorize the photo
        self._photo = 'Build/contact_2.png'

        # connect the central widget function and model
        self._model = model
        self._changeCentralWidget = changeCentralWidget

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
        self.ui.telephoneLine.setValidator(QRegExpValidator(QRegExp("\\d*"), self))

        # Connect button
        self.ui.saveButton.clicked.connect(self.insertContact)
        self.ui.resetPhoto.clicked.connect(self.resetPhoto)
        self.ui.backButton.clicked.connect(self.back)
        self.ui.setPhoto.clicked.connect(self.changeImage)


    # Funtion to change the contact photo with a selected one
    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._photo = fileName[0]
            self.ui.photo.setPixmap(QPixmap(fileName[0]).scaled(289, 289))
    
    # Funtion to reset the contact photo
    @pyqtSlot() 
    def resetPhoto(self):
        self._photo = 'Build/contact_2.png'
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))


    # Funtion to add the new cntact to the list
    @pyqtSlot()
    def insertContact(self):
        ContactInfo = {}
        ContactInfo['photo'] = self._photo 
        ContactInfo['name'] = self.ui.nameLine.text()
        ContactInfo['secondName'] = self.ui.seconNameLine.text()
        ContactInfo['phone'] = self.ui.telephoneLine.text()
        ContactInfo['mail'] = self.ui.emailLine.text()
        ContactInfo['notes'] = self.ui.noteBox.toPlainText()
        ContactInfo['tags'] = []
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).checkState(0):
                ContactInfo['tags'].append(self.ui.tagsList.invisibleRootItem().child(i).text(0))

        self._model.addNewContact(ContactInfo)
        self.reset()

    # Function to go to the contaact list view. If the user
    # set some infos, the application asck if the user is 
    # sure to go back.
    @pyqtSlot()
    def back(self):
        # check if the user writes some contact informations
        tags = []
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if self.ui.tagsList.invisibleRootItem().child(i).checkState(0):
                tags.append(self.ui.tagsList.invisibleRootItem().child(i).text(0))

        if self.ui.nameLine.text() or self.ui.seconNameLine.text() or self.ui.telephoneLine.text() or self.ui.emailLine.text() or self.ui.noteBox.toPlainText() or tags:
            text= "You are write some information press ok to lose them, else press cancel."
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self.reset()
        else:
            self.reset()
  
    # Simple function to reset the contact window information.
    def reset(self):
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
        self.ui.nameLine.setText('')
        self.ui.seconNameLine.setText('')
        self.ui.telephoneLine.setText('')
        self.ui.emailLine.setText('')
        self.ui.noteBox.setText('')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)

        self._changeCentralWidget(0)


