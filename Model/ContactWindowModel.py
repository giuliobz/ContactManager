from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class ContactWindowModel(QObject):
    closeWindowSignal = pyqtSignal()
    contactChangedSignal = pyqtSignal(list)

    def __init__(self, idx, contactInfo):
        super().__init__()

        # The two variable that memorize event change.
        # The first take the original information, the second
        # contain the key of the changed element. Important:
        # in new contact window i put the current tags selected for
        # this contact. This permits a better contact update.
        self._currentContactInfo = contactInfo
        self._newContactInfo = {}
        self._newContactInfo['tags'] = [tags for tags in contactInfo['tags']]

        # Define a boolean that is True if in newContactinfo 
        # I have more that one key or if tags list has length 
        # greater that the currentContactInfo tags list.
        self._is_changed = []

        # Define the id f this contact
        self._id = idx

    @property
    def id(self):
        return self._id

    @property
    def newContactInfo(self):
        return self._newContactInfo

    @property
    def currentContactInfo(self):
        return self._currentContactInfo 

    @property
    def is_changed(self):
        return self._is_changed
    
    @property
    def foto(self):
        if 'photo' in self._newContactInfo:
            return self._newContactInfo['foto']
        return ''
    
    @property
    def name(self):
        if 'name' in self._newContactInfo:
            return self._newContactInfo['name']
        return ''
    
    @property
    def secondName(self):
        if 'secondName' in self._newContactInfo:
            return self._newContactInfo['secondName']
        return ''
    
    @property
    def phone(self):
        if 'phone' in self._newContactInfo:
            return self._newContactInfo['phone']
        return ''

    @property
    def mail(self):
        if 'mail' in self._newContactInfo:
            return self._newContactInfo['mail']
        return ''

    @property
    def notes(self):
        if 'notes' in self._newContactInfo:
            return self._newContactInfo['notes']
        return ''

    @property
    def tags(self):
        if 'tags' in self._newContactInfo:
            return self._newContactInfo['tags']
        return []
    
    @foto.setter
    def foto(self, foto):
        self._newContactInfo['foto'] = foto
        if self._newContactInfo['foto'] == self._currentContactInfo['photo']:
            del self._newContactInfo['foto']
        self.contactChangedSignal.emit(['foto', foto])
    
    @name.setter
    def name(self, name):
        self._newContactInfo['name'] = name
        if self._newContactInfo['name'] == self._currentContactInfo['name']:
            del self._newContactInfo['name']
        self.contactChangedSignal.emit(['name', 'red' if name != self._currentContactInfo['name'] else 'black'])

    @secondName.setter
    def secondName(self, secondName):
        self._newContactInfo['secondName'] = secondName
        if self._newContactInfo['secondName'] == self._currentContactInfo['secondName']:
            del self._newContactInfo['secondName']
        self.contactChangedSignal.emit(['secondName', 'red' if secondName != self._currentContactInfo['secondName'] else 'black'])
    
    @phone.setter
    def phone(self, phone):
        self._newContactInfo['phone'] = phone
        if self._newContactInfo['phone'] == self._currentContactInfo['phone']:
            del self._newContactInfo['phone']
        self.contactChangedSignal.emit(['phone', 'red' if phone != self._currentContactInfo['phone'] else 'black'])
        

    @mail.setter
    def mail(self, mail):
        self._newContactInfo['mail'] = mail
        if self._newContactInfo['mail'] == self._currentContactInfo['mail']:
            del self._newContactInfo['mail']
        self.contactChangedSignal.emit(['mail', 'red' if mail != self._currentContactInfo['mail'] else 'mail'])

    @notes.setter
    def notes(self, notes):
        self._newContactInfo['notes'] = notes
        if self._newContactInfo['notes'] == self._currentContactInfo['notes']:
            del self._newContactInfo['notes']
        self.contactChangedSignal.emit(['notes', 'red' if notes != self._currentContactInfo['notes'] else 'notes'])
        

    @tags.setter
    def tags(self, tags):
        if tags in self._newContactInfo['tags']:
            self._newContactInfo['tags'].remove(tags)
        else:
            self._newContactInfo['tags'].append(tags)

        self.contactChangedSignal.emit(['tags'])


    @newContactInfo.setter
    def newContactInfo(self, slot):
        self._newContactInfo = slot

    @currentContactInfo.setter
    def currentContactInfo(self, slot):
        self._currentContactInfo = slot
        self._newContactInfo = {}
        self.closeWindowSignal.emit()

    @is_changed.setter
    def is_changed(self, slot):
        self._is_changed = slot