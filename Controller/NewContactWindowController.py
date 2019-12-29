from PyQt5.QtWidgets import QMessageBox, QTreeWidgetItem, QFileDialog
from PyQt5.Qt import QObject, pyqtSlot, Qt

class NewContactWindowController(QObject):
    def __init__(self, controller, model):
        super().__init__()

        # Connect the model with the controller
        self._model = model

        # Connect this controller with the main controller  
        self._controller = controller

    @pyqtSlot(QTreeWidgetItem, int)
    def tagChanged(self, item, column):
        
        self._model.tags = item.text(0)


    @pyqtSlot(str)
    def change_name(self, name):
        self._model.name = name

    
    @pyqtSlot(str)
    def change_secondName(self, secondName):
        self._model.secondName = secondName

    
    @pyqtSlot(str)
    def change_Phone(self, phone):
        self._model.phone = phone

    
    @pyqtSlot(str)
    def change_Email(self, mail):
        self._model.mail = mail

    
    @pyqtSlot(str)
    def change_note(self, note):
        self._model.note = note

    @pyqtSlot()
    def backButtonFunc(self):
        if self._model.is_changed:
            text= "You are leaving the page with modify fields. Press ok if you want to lost all changes, else press cancel"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self._controller.changeCentralWidget('list')
                
        else:
            self._controller.changeCentralWidget('list')


    @pyqtSlot()
    def insertContact(self):
        
        if self._model.is_changed and self._model.name == '' and self._model.secondName== '':

            text = 'Name and second name are empty. Please specify the contact name and second name before save it.'
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()  

        elif self._model.is_changed and [idx for idx in self._model.currentContactList.keys() if self._model.name in self._model.currentContactList[idx]['name'] and self._model.secondName in self._model.currentContactList[idx]['secondName']]:
            text= "Another contact with same name and second name still already exist. Press ok to modify the existing contact with these new information. Press cancel to go back in new contact window."
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self.close()
        
        elif self._model.is_changed:

            self._controller.insertNewContact(self._model.contactInfo)
            self._controller.changeCentralWidget('list')

    @pyqtSlot()
    def resetButton(self):
        if self._model.is_changed:
            text= "You are resetting the page with modify fields. Press ok if you want to lost all changes, else press cancel"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText(text)
            msgBox.setWindowTitle("Warning")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            if (msgBox.exec_() == QMessageBox.Ok):
                self._model.contactInfo = { 'photo' : 'Build/contact_2.png', 'name' : '', 'secondName' : '', 'phone' : '', 'mail' : '', 'notes' : '', 'tags' : []}
        else:

            self._model.contactInfo = { 'photo' : 'Build/contact_2.png', 'name' : '', 'secondName' : '', 'phone' : '', 'mail' : '', 'notes' : '', 'tags' : []}

    @pyqtSlot()
    def changeImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(caption='Open file', filter="Image files (*.jpg *.gif *.png)", options=options)
        if '.png' in fileName[0] or '.jpg' in fileName[0] or '.gif' in fileName[0]:
            self._model.photo = fileName[0]

    @pyqtSlot()
    def check_changes(self):
        if self._model.photo == 'Build/contact_2.png' and self._model.name == '' and self._model.secondName == '' and self._model.phone == '' and self._model.contactInfo['notes'] == '' and self._model.tags == []:
            self._model.is_changed = False
        else:
            self._model.is_changed = True
            