# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContactManagerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ContactManager(object):
    def setupUi(self, ContactManager):
        ContactManager.setObjectName("ContactManager")
        ContactManager.resize(891, 1465)
        self.centralwidget = QtWidgets.QWidget(ContactManager)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        ContactManager.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(ContactManager)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 891, 34))
        self.menuBar.setObjectName("menuBar")
        self.menu_File = QtWidgets.QMenu(self.menuBar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        ContactManager.setMenuBar(self.menuBar)
        self.action_About = QtWidgets.QAction(ContactManager)
        self.action_About.setObjectName("action_About")
        self.action_New_Contact = QtWidgets.QAction(ContactManager)
        self.action_New_Contact.setObjectName("action_New_Contact")
        self.action_Quit = QtWidgets.QAction(ContactManager)
        self.action_Quit.setObjectName("action_Quit")
        self.action_Add = QtWidgets.QAction(ContactManager)
        self.action_Add.setObjectName("action_Add")
        self.action_Quit_2 = QtWidgets.QAction(ContactManager)
        self.action_Quit_2.setObjectName("action_Quit_2")
        self.action_Edit = QtWidgets.QAction(ContactManager)
        self.action_Edit.setObjectName("action_Edit")
        self.action_About_2 = QtWidgets.QAction(ContactManager)
        self.action_About_2.setObjectName("action_About_2")
        self.menu_File.addAction(self.action_Add)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Edit)
        self.menu_Help.addAction(self.action_About_2)
        self.menuBar.addAction(self.menu_File.menuAction())
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(ContactManager)
        QtCore.QMetaObject.connectSlotsByName(ContactManager)

    def retranslateUi(self, ContactManager):
        _translate = QtCore.QCoreApplication.translate
        ContactManager.setWindowTitle(_translate("ContactManager", "Contact Manger"))
        self.menu_File.setTitle(_translate("ContactManager", "&File"))
        self.menu_Help.setTitle(_translate("ContactManager", "&Help"))
        self.action_About.setText(_translate("ContactManager", "&About"))
        self.action_New_Contact.setText(_translate("ContactManager", "&New Contact"))
        self.action_Quit.setText(_translate("ContactManager", "&Quit"))
        self.action_Add.setText(_translate("ContactManager", "&Add"))
        self.action_Quit_2.setText(_translate("ContactManager", "&Quit"))
        self.action_Edit.setText(_translate("ContactManager", "&Quit"))
        self.action_About_2.setText(_translate("ContactManager", "&About"))
