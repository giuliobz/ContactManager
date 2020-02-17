import os 
import sys

from ContactManagerView import ContactManager

from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

window = ContactManager()
window.show()
app.exec_()
sys.exit()
