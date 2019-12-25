import os 
import sys

from Model.model import Model
from Controller.controller import Controller

from View.ContactManagerView import ContactManager

from PyQt5.QtWidgets import QApplication

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))


app = QApplication(sys.argv)
model = Model()
controller = Controller(model)
window = ContactManager(model, controller)
window.show()
app.exec_()
sys.exit()
