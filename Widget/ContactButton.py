from PyQt5.QtWidgets import QPushButton, QSizePolicy


class ContactButton(QPushButton):
    ''' Button to open a contact to see information '''

    def __init__(self, name, model, id, **kwargs):
        super().__init__(**kwargs)

        self._name = name 
        self._model = model
        self._id = id
        self.setText('{}'.format(self._name))
        self.clicked.connect(lambda : self.getInformation())
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
    
    # This button call the model function to setup the contact that the user 
    # want to see. To do that is used the contact id.
    def getInformation(self):
        self._model.getInformation(self._id)
