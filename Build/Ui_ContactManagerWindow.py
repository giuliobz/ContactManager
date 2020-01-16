# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContactManagerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ContactManagerWindow(object):
    def setupUi(self, ContactManagerWindow):
        ContactManagerWindow.setObjectName("ContactManagerWindow")
        ContactManagerWindow.resize(874, 1409)
        self.centralwidget = QtWidgets.QWidget(ContactManagerWindow)
        self.centralwidget.setObjectName("centralwidget")
        ContactManagerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ContactManagerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 874, 34))
        self.menubar.setObjectName("menubar")
        self.menu_File = QtWidgets.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        ContactManagerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ContactManagerWindow)
        self.statusbar.setObjectName("statusbar")
        ContactManagerWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtWidgets.QAction(ContactManagerWindow)
        self.action_Quit.setObjectName("action_Quit")
        self.action_About = QtWidgets.QAction(ContactManagerWindow)
        self.action_About.setObjectName("action_About")
        self.menu_File.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(ContactManagerWindow)
        QtCore.QMetaObject.connectSlotsByName(ContactManagerWindow)

    def retranslateUi(self, ContactManagerWindow):
        _translate = QtCore.QCoreApplication.translate
        ContactManagerWindow.setWindowTitle(_translate("ContactManagerWindow", "Contact Manager"))
        self.menu_File.setTitle(_translate("ContactManagerWindow", "&File"))
        self.menu_Help.setTitle(_translate("ContactManagerWindow", "&Help"))
        self.action_Quit.setText(_translate("ContactManagerWindow", "&Quit"))
        self.action_About.setText(_translate("ContactManagerWindow", "&About"))

