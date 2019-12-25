from Build.Ui_NewContactWidget import Ui_NewContactWidget


from PyQt5.Qt import pyqtSlot, Qt
from PyQt5.QtWidgets import QDialog

# Window that contain all the clips in annotation buffer with the correlated preferencies
class NewContactWindow(QDialog):

    def __init__(self, controller):
        super().__init__()

        # connect controller 
        self._controller = controller

        # Set up the user interface from Designer.
        self.ui = Ui_NewContactWidget()
        self.ui.setupUi(self)

        # Connect button
        self.ui.saveButton.clicked.connect(self.insertContact)


    def insertContact(self):
        name = self.ui.nameLine.text()
        secondName = self.ui.seconNameLine.text()
        phone = self.ui.telephoneLine.text()
        mail = self.ui.emailLine.text()
        notes = self.ui.noteBox.toPlainText()
        tags = []
        for i in range(self.ui.tagsList.invisibleRootItem().childCount()):
            if(self.ui.tagsList.invisibleRootItem().child(i).checkState(0) == Qt.Checked):
                tags.append(self.ui.tagsList.invisibleRootItem().child(i).text(0))
        
        self._controller.insertNewContact([name, secondName, phone, mail, notes, tags])
        #self.close()
            