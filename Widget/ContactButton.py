from PyQt5.QtWidgets import QPushButton, QSizePolicy


class ContactButton(QPushButton):
    ''' Choose button to decide the clips you prefer '''

    def __init__(self, name, model, id, **kwargs):
        super().__init__(**kwargs)

        self._name = name 
        self._model = model
        self._id = id
        self.setText('{}'.format(self._name))
        self.clicked.connect(lambda : self.getInformation())
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))

    def getInformation(self):
        self._model.getInformation(self._id)