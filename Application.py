import os 
import sys

from Model.model import Model
from Controller.controller import Controller

from View.ContactManagerView import ContactManager

from PyQt5.QtWidgets import QApplication

DIR_NAME = os.path.dirname(os.path.abspath('__file__'))


app = QApplication(sys.argv)

window = ContactManager()
window.show()
app.exec_()
sys.exit()
