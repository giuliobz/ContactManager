from Model.NewContactWindowModel import NewContactWindowModel

from Controller.NewContactWindowController import NewContactWindowController

from Build.Ui_NewContactWidget import Ui_NewContactWidget

from PyQt5.Qt import pyqtSlot, Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QImage, QPixmap

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, currentContactList, controller):
        super().__init__()

        # connect controller and model
        self._model = NewContactWindowModel(currentContactList)
        self._controller = NewContactWindowController(controller, self._model)

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)

        # Connect button
        self.ui.saveButton.clicked.connect(self._controller.insertContact)
        self.ui.resetButton.clicked.connect(self._controller.resetButton)
        self.ui.backButton.clicked.connect(lambda : self._controller.backButtonFunc())
        self.ui.setPhoto.clicked.connect(self._controller.changeImage)

        # Set default image. 
        self.ui.photo.setPixmap(QPixmap(self._model.contactInfo['photo']))

        # Connect line changes 
        self.ui.nameLine.textChanged.connect(self._controller.change_name) 
        self.ui.seconNameLine.textChanged.connect(self._controller.change_secondName)
        self.ui.telephoneLine.textChanged.connect(self._controller.change_Phone)
        self.ui.emailLine.textChanged.connect(self._controller.change_Email)
        self.ui.noteBox.textChanged.connect(self.change_note)
        self.ui.tagsList.itemChanged.connect(self._controller.tagChanged)

        # Connect model
        self._model.resetSignal.connect(lambda : self.resetButton())
        self._model.contactChangedSignal.connect(self.changeContact)


    def change_note(self):
        self._controller.change_note(self.ui.noteBox.toPlainText())
        
    def resetButton(self):
        
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png'))
        self.ui.nameLine.setText('')
        self.ui.seconNameLine.setText('')
        self.ui.telephoneLine.setText('')
        self.ui.emailLine.setText('')
        self.ui.noteBox.setText('')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
               self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)

    @pyqtSlot(str)
    def changeImage(self, image):
        self.ui.photo.setPixmap(QPixmap(image))

    @pyqtSlot(list)
    def changeContact(self, slot):
        if slot[0] == 'foto':
            self.ui.photo.setPixmap(QPixmap(slot[1]))
        
        self._controller.check_changes()



