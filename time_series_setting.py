# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'time_series_setting.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(386, 113)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 281, 80))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 46, 101, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.ok_Btn = QtWidgets.QPushButton(Dialog)
        self.ok_Btn.setGeometry(QtCore.QRect(300, 50, 75, 31))
        self.ok_Btn.setObjectName("ok_Btn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Setting"))
        self.groupBox.setTitle(_translate("Dialog", "Choose a Time Series Plot:"))
        self.radioButton.setText(_translate("Dialog", "Single"))
        self.radioButton_2.setText(_translate("Dialog", "Multiple"))
        self.ok_Btn.setText(_translate("Dialog", "OK"))