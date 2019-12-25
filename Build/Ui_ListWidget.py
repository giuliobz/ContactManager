# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ListWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(975, 1489)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.nameLabel = QtWidgets.QLabel(self.widget)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout.addWidget(self.nameLabel, 1, 0, 1, 1)
        self.tagLabel = QtWidgets.QLabel(self.widget)
        self.tagLabel.setObjectName("tagLabel")
        self.gridLayout.addWidget(self.tagLabel, 2, 0, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.widget)
        self.searchButton.setObjectName("searchButton")
        self.gridLayout.addWidget(self.searchButton, 2, 4, 1, 1)
        self.editButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editButton.sizePolicy().hasHeightForWidth())
        self.editButton.setSizePolicy(sizePolicy)
        self.editButton.setObjectName("editButton")
        self.gridLayout.addWidget(self.editButton, 0, 3, 1, 1)
        self.nameLine = QtWidgets.QLineEdit(self.widget)
        self.nameLine.setObjectName("nameLine")
        self.gridLayout.addWidget(self.nameLine, 1, 1, 1, 3)
        self.tagsButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagsButton.sizePolicy().hasHeightForWidth())
        self.tagsButton.setSizePolicy(sizePolicy)
        self.tagsButton.setObjectName("tagsButton")
        self.gridLayout.addWidget(self.tagsButton, 0, 0, 1, 2)
        self.addButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy)
        self.addButton.setObjectName("addButton")
        self.gridLayout.addWidget(self.addButton, 0, 2, 1, 1)
        self.tagSearch = QtWidgets.QComboBox(self.widget)
        self.tagSearch.setObjectName("tagSearch")
        self.gridLayout.addWidget(self.tagSearch, 2, 1, 1, 3)
        self.verticalLayout.addWidget(self.widget)
        self.contactList = QtWidgets.QTreeWidget(Form)
        self.contactList.setObjectName("contactList")
        self.verticalLayout.addWidget(self.contactList)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ListWidget"))
        self.nameLabel.setText(_translate("Form", "Search name : "))
        self.tagLabel.setText(_translate("Form", "Search tag : "))
        self.searchButton.setText(_translate("Form", "Search"))
        self.editButton.setText(_translate("Form", "Edit"))
        self.tagsButton.setText(_translate("Form", "Tags"))
        self.addButton.setText(_translate("Form", "Add"))
