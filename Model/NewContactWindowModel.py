from PyQt5.Qt import QObject, pyqtSignal

class NewContactWindowModel(QObject):
    resetSignal = pyqtSignal()
    contactChangedSignal = pyqtSignal(list)

    def __init__(self, currentContactList):
        super().__init__()

        # Take the current element.
        self._currentContactList = currentContactList

        # Define the contact information and the default image.
        self._contactInfo = { 'photo' : 'Build/contact_2.png', 'name' : '', 'secondName' : '', 'phone' : '', 'mail' : '', 'notes' : '', 'tags' : []}

        # Defie a variable that controll if something is changed or not
        self._is_changed = False

    @property
    def is_changed(self):
        return self._is_changed

    @property
    def currentContactList(self):
        return self._currentContactList

    @property
    def contactInfo(self):
        return self._contactInfo

    @property
    def foto(self):
        return self._contactInfo['photo']
  
    
    @property
    def name(self):
        return self._contactInfo['name']

    
    @property
    def secondName(self):
        return self._contactInfo['secondName']

    
    @property
    def phone(self):
        return self._contactInfo['phone']


    @property
    def mail(self):
        return self._contactInfo['mail']


    @property
    def note(self):
        return self._newContactInfo['notes']

    @property
    def tags(self):
        return self._contactInfo['tags']

    @is_changed.setter
    def is_changed(self, slot):
        self._is_changed = slot

    @contactInfo.setter
    def contactInfo(self, slot):
        self._contactInfo = slot
        self.resetSignal.emit()
    
    @foto.setter
    def foto(self, foto):
        self._contactInfo['foto'] = foto
        self.contactChangedSignal.emit(['foto', foto])
    
    @name.setter
    def name(self, name):
        self._contactInfo['name'] = name
        self.contactChangedSignal.emit(['name'])

    @secondName.setter
    def secondName(self, secondName):
        self._contactInfo['secondName'] = secondName
        self.contactChangedSignal.emit(['secondName'])
    
    @phone.setter
    def phone(self, phone):
        self._contactInfo['phone'] = phone
        self.contactChangedSignal.emit(['phone'])
        

    @mail.setter
    def mail(self, mail):
        self._contactInfo['mail'] = mail
        self.contactChangedSignal.emit(['mail'])

    @note.setter
    def note(self, notes):
        self._contactInfo['notes'] = notes
        self.contactChangedSignal.emit(['notes'])
    

    @tags.setter
    def tags(self, tags):
        if 'tags' not in self._contactInfo.keys():
            self._contactInfo['tags'] = [tags]
            
        else: 

            if tags in self._contactInfo['tags']:
                self._contactInfo['tags'].remove(tags)
            else:
                self._contactInfo['tags'].append(tags)
        

        self.contactChangedSignal.emit(['tags'])