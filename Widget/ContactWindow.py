from Build.Ui_ContactWidget import Ui_ContactWidget


from PyQt5.QtCore import Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtGui import QImage, QPixmap

# Window that contain all the clips in annotation buffer with the correlated preferencies
class ContactWindow(QDialog):

    def __init__(self, contactInfo, controller):
        super().__init__()
        
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


