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
        self._controller = controller

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

        # Connect function to controller    
        self.ui.backButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.changeContactInfo)
        self.ui.resetImgButton.clicked.connect(self.resetImage)
        self.ui.changeImgButton.clicked.connect(self.changeImage)

        # Connect line 

    def backFunc(self):
        
        text= "You are changing a contact. Press ok to modify the existing contact with these new information. Press cancel to go back in new contact window."
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    
    def changeContactInfo(self):
        contactInfo = {}

        text= "You are changing a contact. Press ok to modify the existing contact with these new information. Press cancel to go back in new contact window."
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if (msgBox.exec_() == QMessageBox.Ok):
            contactInfo['idx'] = self._id
            contactInfo['photo'] = self._photo
            contactInfo['name'] = self.ui.nameLine.text()
            contactInfo['secondName'] = self.ui.seconNameLine.text()
            contactInfo['phone'] = self.ui.telephoneLine.text()
            contactInfo['mail'] = self.ui.emailLine.text()
            contactInfo['notes'] = self.ui.noteBox.toPlainText()
            contactInfo['tags'] = []
            for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
                if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
                    contactInfo['tags'].append(self.ui.tagsList.invisibleRootItem().child(i).text(0))

            self._controller.updateContact(contactInfo)
            self.close()

    
    def resetImage(self):
        self._contactInfo['photo'] = 'Build/contact_2.png'
        self.ui.photo.setPixmap(QPixmap(self._contactInfo['photo']))

    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self, caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if fileName[0] != '':
            self._photo = fileName[0]
            self.ui.photo.setPixmap(QPixmap(self._contactInfo['photo']))

