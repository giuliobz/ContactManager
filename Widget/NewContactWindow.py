import cv2

from Build.Ui_NewContactWidget import Ui_NewContactWidget

from PyQt5.Qt import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QImage, QPixmap

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, controller):
        super().__init__()

        # connect controller and model
        self._controller = controller

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)

        # Connect button
        self.ui.saveButton.clicked.connect(self.insertContact)
        self.ui.resetButton.clicked.connect(self.resetButton)
        self.ui.backButton.clicked.connect(lambda : self.close())

        # Set default image
        h, w, ch = cv2.imread('Build/contact_2.png').shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(cv2.imread('Build/contact_2.png'), w, h, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
        self.ui.photo.setPixmap(QPixmap.fromImage(convertToQtFormat))

    def insertContact(self):
        contactInfo = {}
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
        self.close()
        
    def resetButton(self):
        
        self.ui.nameLine.setText('')
        self.ui.seconNameLine.setText('')
        self.ui.telephoneLine.setText('')
        self.ui.emailLine.setText('')
        self.ui.noteBox.setText('')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
               self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)
            