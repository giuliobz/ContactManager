from PyQt5.QtWidgets import QPushButton, QSizePolicy


class ContactButton(QPushButton):
    ''' Choose button to decide the clips you prefer '''

    def __init__(self, name, contactWindow, **kwargs):
        super().__init__(**kwargs)

        self._name = name 
        self._window = contactWindow
        self.setText('{}'.format(self._name))
        self.clicked.connect(lambda : self._window.exec_())
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))