# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Z0228550\OneDrive - zf-lifetec\Documents\Python_projects\minitab\DataStatus.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
#������
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import sys
import numpy as np
from scipy import stats

class Ui_Dialog(QDialog):
    def __init__(self, data = [1,2,2,4,5,6,7,8,9,10]):          
        
        super(QDialog,self).__init__()
        
        self.input_Data = data
        # self.update_status()
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(488, 272)
        Dialog.setWindowOpacity(1.0)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.AVG = QtWidgets.QLabel(Dialog)
        self.AVG.setObjectName("AVG")
        self.gridLayout_2.addWidget(self.AVG, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.MIN = QtWidgets.QLabel(Dialog)
        self.MIN.setObjectName("MIN")
        self.gridLayout_2.addWidget(self.MIN, 1, 2, 1, 1)
        self.max = QtWidgets.QLabel(Dialog)
        self.max.setObjectName("max")
        self.gridLayout_2.addWidget(self.max, 0, 2, 1, 1)
        self.Variance = QtWidgets.QLabel(Dialog)
        self.Variance.setObjectName("Variance")
        self.gridLayout_2.addWidget(self.Variance, 3, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 1, 3, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 0, 3, 1, 1)
        self.SD = QtWidgets.QLabel(Dialog)
        self.SD.setObjectName("SD")
        self.gridLayout_2.addWidget(self.SD, 1, 0, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_2.addWidget(self.lineEdit_5, 1, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 2, 3, 1, 1)
        self.Sum = QtWidgets.QLabel(Dialog)
        self.Sum.setObjectName("Sum")
        self.gridLayout_2.addWidget(self.Sum, 2, 2, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 2, 1, 1, 1)
        self.lineEdit_mode = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_mode.setObjectName("lineEdit_mode")
        self.gridLayout_2.addWidget(self.lineEdit_mode, 3, 3, 1, 1)
        self.lineEdit_var = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_var.setObjectName("lineEdit_var")
        self.gridLayout_2.addWidget(self.lineEdit_var, 3, 1, 1, 1)
        self.Mode = QtWidgets.QLabel(Dialog)
        self.Mode.setObjectName("Mode")
        self.gridLayout_2.addWidget(self.Mode, 3, 2, 1, 1)
        self.Median = QtWidgets.QLabel(Dialog)
        self.Median.setObjectName("Median")
        self.gridLayout_2.addWidget(self.Median, 2, 0, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 8)

        self.retranslateUi(Dialog)
        self.update_status()
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Status of Data"))
        self.AVG.setText(_translate("Dialog", "Average:"))
        self.MIN.setText(_translate("Dialog", "Minmum:"))
        self.max.setText(_translate("Dialog", "Maximum:"))
        self.SD.setText(_translate("Dialog", "Standard Deviation:"))
        self.Sum.setText(_translate("Dialog", "Sum:"))
        self.Median.setText(_translate("Dialog", "Median:"))
        self.label_7.setText(_translate("Dialog", "Data Status:"))
        self.Variance.setText(_translate("Dialog", "Variance:"))
        self.Mode.setText(_translate("Dialog", "Mode:"))

    def update_status(self):
        self.lineEdit.setText(str(np.average(self.input_Data)))
        self.lineEdit_2.setText(str(np.sum(self.input_Data)))
        self.lineEdit_3.setText(str(np.min(self.input_Data)))
        self.lineEdit_4.setText(str(np.max(self.input_Data)))
        self.lineEdit_5.setText(str(np.std(self.input_Data)))
        self.lineEdit_6.setText(str(np.median(self.input_Data)))
        mod = stats.mode(np.array(self.input_Data))
        # print(mod)
        self.lineEdit_mode.setText(str(mod.mode))
        self.lineEdit_var.setText(str(np.var(self.input_Data)))
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())