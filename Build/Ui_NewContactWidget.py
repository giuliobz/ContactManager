# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewContactWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewContactWidget(object):
    def setupUi(self, NewContactWidget):
        NewContactWidget.setObjectName("NewContactWidget")
        NewContactWidget.resize(963, 1343)
        self.verticalLayout = QtWidgets.QVBoxLayout(NewContactWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.photoWidget = QtWidgets.QWidget(NewContactWidget)
        self.photoWidget.setObjectName("photoWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.photoWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.photo = QtWidgets.QLabel(self.photoWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.photo.sizePolicy().hasHeightForWidth())
        self.photo.setSizePolicy(sizePolicy)
        self.photo.setObjectName("photo")
        self.horizontalLayout.addWidget(self.photo)
        self.verticalLayout.addWidget(self.photoWidget)
        self.setPhoto = QtWidgets.QPushButton(NewContactWidget)
        self.setPhoto.setObjectName("setPhoto")
        self.verticalLayout.addWidget(self.setPhoto)
        self.infoWidget = QtWidgets.QWidget(NewContactWidget)
        self.infoWidget.setObjectName("infoWidget")
        self.formLayout = QtWidgets.QFormLayout(self.infoWidget)
        self.formLayout.setObjectName("formLayout")
        self.nameText = QtWidgets.QLabel(self.infoWidget)
        self.nameText.setObjectName("nameText")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameText)
        self.nameLine = QtWidgets.QLineEdit(self.infoWidget)
        self.nameLine.setText("")
        self.nameLine.setObjectName("nameLine")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameLine)
        self.secondNameText = QtWidgets.QLabel(self.infoWidget)
        self.secondNameText.setObjectName("secondNameText")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.secondNameText)
        self.seconNameLine = QtWidgets.QLineEdit(self.infoWidget)
        self.seconNameLine.setText("")
        self.seconNameLine.setObjectName("seconNameLine")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.seconNameLine)
        self.phoneText = QtWidgets.QLabel(self.infoWidget)
        self.phoneText.setObjectName("phoneText")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.phoneText)
        self.telephoneLine = QtWidgets.QLineEdit(self.infoWidget)
        self.telephoneLine.setText("")
        self.telephoneLine.setObjectName("telephoneLine")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.telephoneLine)
        self.mailText = QtWidgets.QLabel(self.infoWidget)
        self.mailText.setObjectName("mailText")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.mailText)
        self.emailLine = QtWidgets.QLineEdit(self.infoWidget)
        self.emailLine.setText("")
        self.emailLine.setObjectName("emailLine")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.emailLine)
        self.verticalLayout.addWidget(self.infoWidget)
        self.notesWidget = QtWidgets.QWidget(NewContactWidget)
        self.notesWidget.setObjectName("notesWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.notesWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.notesLabel = QtWidgets.QLabel(self.notesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notesLabel.sizePolicy().hasHeightForWidth())
        self.notesLabel.setSizePolicy(sizePolicy)
        self.notesLabel.setObjectName("notesLabel")
        self.verticalLayout_3.addWidget(self.notesLabel)
        self.noteBox = QtWidgets.QTextEdit(self.notesWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noteBox.sizePolicy().hasHeightForWidth())
        self.noteBox.setSizePolicy(sizePolicy)
        self.noteBox.setObjectName("noteBox")
        self.verticalLayout_3.addWidget(self.noteBox)
        self.verticalLayout.addWidget(self.notesWidget)
        self.tagsWidget = QtWidgets.QWidget(NewContactWidget)
        self.tagsWidget.setObjectName("tagsWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tagsWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tagsList = QtWidgets.QTreeWidget(self.tagsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsList.sizePolicy().hasHeightForWidth())
        self.tagsList.setSizePolicy(sizePolicy)
        self.tagsList.setObjectName("tagsList")
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        item_0 = QtWidgets.QTreeWidgetItem(self.tagsList)
        item_0.setCheckState(0, QtCore.Qt.Unchecked)
        self.verticalLayout_2.addWidget(self.tagsList)
        self.verticalLayout.addWidget(self.tagsWidget)
        self.buttonWidget = QtWidgets.QWidget(NewContactWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonWidget.sizePolicy().hasHeightForWidth())
        self.buttonWidget.setSizePolicy(sizePolicy)
        self.buttonWidget.setObjectName("buttonWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.buttonWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.saveButton = QtWidgets.QPushButton(self.buttonWidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.resetButton = QtWidgets.QPushButton(self.buttonWidget)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_2.addWidget(self.resetButton)
        self.backButton = QtWidgets.QPushButton(self.buttonWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.backButton.sizePolicy().hasHeightForWidth())
        self.backButton.setSizePolicy(sizePolicy)
        self.backButton.setObjectName("backButton")
        self.horizontalLayout_2.addWidget(self.backButton)
        self.verticalLayout.addWidget(self.buttonWidget)

        self.retranslateUi(NewContactWidget)
        QtCore.QMetaObject.connectSlotsByName(NewContactWidget)

    def retranslateUi(self, NewContactWidget):
        _translate = QtCore.QCoreApplication.translate
        NewContactWidget.setWindowTitle(_translate("NewContactWidget", "NewContactWidget"))
        self.photo.setText(_translate("NewContactWidget", "<html><head/><body><p><img src=\":/contact_2.png\"/></p></body></html>"))
        self.setPhoto.setText(_translate("NewContactWidget", "Set photo"))
        self.nameText.setText(_translate("NewContactWidget", "First name :"))
        self.secondNameText.setText(_translate("NewContactWidget", "Second name :"))
        self.phoneText.setText(_translate("NewContactWidget", "Telephone :"))
        self.mailText.setText(_translate("NewContactWidget", "E-Mail :"))
        self.notesLabel.setText(_translate("NewContactWidget", "Notes :"))
        self.tagsList.headerItem().setText(0, _translate("NewContactWidget", "Select Tags"))
        __sortingEnabled = self.tagsList.isSortingEnabled()
        self.tagsList.setSortingEnabled(False)
        self.tagsList.topLevelItem(0).setText(0, _translate("NewContactWidget", "cinema"))
        self.tagsList.topLevelItem(1).setText(0, _translate("NewContactWidget", "sport"))
        self.tagsList.topLevelItem(2).setText(0, _translate("NewContactWidget", "university"))
        self.tagsList.topLevelItem(3).setText(0, _translate("NewContactWidget", "friend"))
        self.tagsList.topLevelItem(4).setText(0, _translate("NewContactWidget", "music"))
        self.tagsList.topLevelItem(5).setText(0, _translate("NewContactWidget", "politic"))
        self.tagsList.topLevelItem(6).setText(0, _translate("NewContactWidget", "professor"))
        self.tagsList.topLevelItem(7).setText(0, _translate("NewContactWidget", "work"))
        self.tagsList.setSortingEnabled(__sortingEnabled)
        self.saveButton.setText(_translate("NewContactWidget", "Save"))
        self.resetButton.setText(_translate("NewContactWidget", "Reset"))
        self.backButton.setText(_translate("NewContactWidget", "Back"))

import contact_rc
