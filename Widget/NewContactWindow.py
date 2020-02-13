from Widget.ImageObserve import Observable

from Model.NewContactWindowModel import NewContactWindowModel

from Build.Ui_NewContactWidget import Ui_NewContactWidget

from PyQt5.Qt import pyqtSlot, Qt, pyqtSignal, QObject, QRegExp
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QIntValidator, QRegExpValidator

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, mainModel):
        super().__init__()

        # connect controller and model
        self._model = NewContactWindowModel(mainModel)

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
        self.ui.telephoneLine.setValidator(QRegExpValidator(QRegExp("\\d*"), self))

        # Connect button
        self.ui.saveButton.clicked.connect(self._model.insertContact)
        self.ui.resetPhoto.clicked.connect(self.resetPhoto)
        self.ui.backButton.clicked.connect(lambda : mainModel.changeWidget(0))
        self.ui.setPhoto.clicked.connect(self.changeImage)

        # Connect line changes 
        self.ui.nameLine.textChanged.connect(self._model.change_name) 
        self.ui.seconNameLine.textChanged.connect(self._model.change_secondName)
        self.ui.telephoneLine.textChanged.connect(self._model.change_Phone)
        self.ui.emailLine.textChanged.connect(self._model.change_Email)
        self.ui.noteBox.textChanged.connect(lambda : self._model.change_note(self.ui.noteBox.toPlainText()))
        self.ui.tagsList.itemChanged.connect(self._model.tagChanged)

        # Connect the photo to an Observable. This allow the application
        # to understand when the user set a new photo or not.
        self._photo = Observable('Build/contact_2.png')
        self._photo.observe(self._model.change_photo)

        # Connect Signal model 
        self._model.resetSignal.connect(self.reset)
    
    # Simple function to reset the contact window information.
    def reset(self):
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
        self._photo.value = 'Build/contact_2.png'
        self.ui.nameLine.setText('')
        self.ui.seconNameLine.setText('')
        self.ui.telephoneLine.setText('')
        self.ui.emailLine.setText('')
        self.ui.noteBox.setText('')
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
                self.ui.tagsList.invisibleRootItem().child(i).setCheckState(0, Qt.Unchecked)

    # Allow the user to change te photo.
    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self.ui.photo.setPixmap(QPixmap(fileName[0]).scaled(289, 289))
            self._photo.value = fileName[0]

    # Allow the user to delete the setted photo
    @pyqtSlot()
    def resetPhoto(self):
        self.ui.photo.setPixmap(QPixmap('Build/contact_2.png').scaled(289, 289))
        self._photo.value = 'Build/contact_2.png'


