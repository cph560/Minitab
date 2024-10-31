# coding=gbk
# ����ָ�������ͷֲ����������ݣ����÷ֲ�Ϊ����̬��������̬���������ֲ���F�ֲ���T�ֲ�������ֲ������ɷֲ���ָ���ֲ�
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.Qt import *
import sys
import numpy as np  
import logging


class Random_interface(QWidget):

    def __init__(self, name = 'Default', size = 1000, para1 = 1, para2 = 1):          
        
        super(Random_interface,self).__init__()
        self.setupUi(self)
        self.size = size
        self.para1 = para1
        self.para2 = para2
        
        self.select = name
        ### ���ݲ�ͬ��ͼ�����޸Ľ�������İ�ť
        # if self.select == 'Pareto':
        #     self.pareto()

        # if self.select == 'Individual':
            
        #     self.Individual_p()

        # if self.select == 'box':
            
        #     self.box()
        ###     
        
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        file_handler = logging.FileHandler('test.log')
        file_handler.setLevel(level=logging.INFO)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        
        logger.info("This is an info message")
        logger.addHandler(file_handler)
        logger.addHandler(logging.StreamHandler())
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(327, 292)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(220, 250, 81, 23))
        self.pushButton.setObjectName("pushButton")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(40, 30, 251, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 90, 251, 121))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Random Number"))
        self.pushButton.setText(_translate("Form", "OK"))
        self.comboBox.setItemText(0, _translate("Form", "Default"))
        self.comboBox.setItemText(1, _translate("Form", "Normal Distribution"))
        self.comboBox.setItemText(2, _translate("Form", "Lognormal Distribution"))
        self.comboBox.setItemText(3, _translate("Form", "Weibull Distribution"))
        self.comboBox.setItemText(4, _translate("Form", "Standard_F Distribution"))
        self.comboBox.setItemText(5, _translate("Form", "Standard_T Distribution"))
        self.comboBox.setItemText(6, _translate("Form", "Binomial Distribution"))
        self.comboBox.setItemText(7, _translate("Form", "Poisson Distribution"))
        self.comboBox.setItemText(8, _translate("Form", "Exponential Distribution"))
        self.comboBox.setItemText(9, _translate("Form", "Uniform Distribution"))
        self.comboBox.setItemText(10, _translate("Form", "Chisquare Distribution"))
        self.comboBox.setItemText(11, _translate("Form", "Gamma"))
        self.comboBox.setItemText(12, _translate("Form", "Beta"))
        self.comboBox.setItemText(13, _translate("Form", "Cauchy Distribution"))
        self.comboBox.setItemText(14, _translate("Form", "Pareto Distribution"))
        self.label_2.setText(_translate("Form", "Not Available:"))
        self.label.setText(_translate("Form", "Size:"))
        self.label_3.setText(_translate("Form", "Not Available:"))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setCursor(Qt.ForbiddenCursor)
        # ����lineEdit_3Ϊֻ��
        self.lineEdit_3.setReadOnly(True)
        # ����lineEdit_3�Ĺ��Ϊ��ֹ
        self.lineEdit_3.setCursor(Qt.ForbiddenCursor)

        # ����comboBox��currentIndexChanged�źŵ�comboBoxSelect�ۺ���
        self.comboBox.currentIndexChanged.connect(self.comboBoxSelect)
        self.pushButton.clicked.connect(self.exec)

    def comboBoxSelect(self):
        # ��ȡ��ǰѡ�е�ѡ��    
        currentT = self.comboBox.currentText()
        if currentT == "Default":
            self.label_2.setText("Not Available:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit_2.setCursor(Qt.ForbiddenCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)

        elif currentT == "Normal Distribution":
            self.label_2.setText("loc:")
            self.label_3.setText("scale:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)

        elif currentT == "Lognormal Distribution":
            self.label_2.setText("Mean:")
            self.label_3.setText("Sigma:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)
        elif currentT == "Weibull Distribution":
            self.label_2.setText("a:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)
        elif currentT == "Standard_F Distribution":
            self.label_2.setText("dfnum:")
            self.label_3.setText("dfden:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)
        elif currentT == "Standard_T Distribution":
            self.label_2.setText("df:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)
        elif currentT == "Binomial Distribution":
            self.label_2.setText("n:")
            self.label_3.setText("p:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)
        elif currentT == "Poisson Distribution":
            self.label_2.setText("lam:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)

        elif currentT == "Exponential Distribution":
            self.label_2.setText("Scale:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)

        elif currentT == "Uniform Distribution":
            self.label_2.setText("low:")
            self.label_3.setText("high:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)

        elif currentT == "Chisquare Distribution":
            self.label_2.setText("df:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)
        elif currentT == "Beta":
            self.label_2.setText("a:")
            self.label_3.setText("b:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)
        elif currentT == "Gamma":
            self.label_2.setText("Shape:")
            self.label_3.setText("Scale:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(False)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.IBeamCursor)
        elif currentT == "Pareto Distribution":
            self.label_2.setText("a:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(False)
            self.lineEdit_2.setCursor(Qt.IBeamCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)
        elif currentT == "Cauchy Distribution":
            self.label_2.setText("Not Available:")
            self.label_3.setText("Not Available:")
            self.lineEdit_2.setReadOnly(True)
            self.lineEdit_2.setCursor(Qt.ForbiddenCursor)
            # ����lineEdit_3Ϊֻ��
            self.lineEdit_3.setReadOnly(True)
            # ����lineEdit_3�Ĺ��Ϊ��ֹ
            self.lineEdit_3.setCursor(Qt.ForbiddenCursor)
        self.select = currentT
        return currentT
    
    def exec(self):
        
        try:
            print(self.lineEdit.text())
            self.size = int(self.lineEdit.text())
            if self.select == "Default":
            # ��������� 
                random_data = np.random.rand(self.size)
                print(random_data)
            elif self.select == "Normal Distribution":
            # ������̬�ֲ��������  
                loc = int(self.lineEdit_2.text())
                scale = int(self.lineEdit_3.text())
                normal_data = np.random.normal(loc, scale, self.size)

            elif self.select == "Lognormal Distribution":
            # ���ɶ�����̬�ֲ�������� 
                mean = int(self.lineEdit_2.text())
                sigma = int(self.lineEdit_3.text())
                lognormal_data = np.random.lognormal(mean, sigma, self.size)

            elif self.select == "Weibull Distribution":
            # �����������ֲ��������
                a = int(self.lineEdit_2.text())
                weibull_data = np.random.weibull(a, self.size)

            elif self.select == "Standard_F Distribution":
                # ����F�ֲ��������
                dfnum = int(self.lineEdit_2.text())
                dfden = int(self.lineEdit_3.text())
                f_data = np.random.f(dfnum, dfden, self.size)
            
            elif self.select == "Standard_T Distribution":
                # ����T�ֲ��������
                df = int(self.lineEdit_2.text())
                t_data = np.random.standard_t(df, self.size)

            elif self.select == "Binomial Distribution":
                # ���ɶ���ֲ��������
                n = int(self.lineEdit_2.text())
                p = int(self.lineEdit_3.text())
                binomial_data = np.random.binomial(n, p, self.size)

            elif self.select == "Poisson Distribution":
                # ���ɲ��ɷֲ��������
                lam = int(self.lineEdit_2.text())
                poisson_data = np.random.poisson(lam, self.size)

            elif self.select == "Exponential Distribution":
                # ����ָ���ֲ��������
                scale = int(self.lineEdit_2.text())
                exponential_data = np.random.exponential(scale, self.size)
            elif self.select == "Uniform Distribution":
                # ���ɾ��ȷֲ��������
                low = int(self.lineEdit_2.text())
                high = int(self.lineEdit_3.text())
                uniform_data = np.random.uniform(low, high, self.size)

            elif self.select == "Chisquare Distribution":
                # ���ɿ����ֲ��������
                df = int(self.lineEdit_2.text())
                chisquare_data = np.random.chisquare(df, self.size)
            elif self.select == "Beta":
                # ����Beta�ֲ��������
                a = int(self.lineEdit_2.text())
                b = int(self.lineEdit_3.text())
                beta_data = np.random.beta(a, b, self.size)
            elif self.select == "Gamma":
                # ����Gamma�ֲ��������
                shape = int(self.lineEdit_2.text())
                scale = int(self.lineEdit_3.text())
                gamma_data = np.random.gamma(shape, scale, self.size)
            elif self.select == "Pareto Distribution":
                # ����Pareto�ֲ��������
                a = int(self.lineEdit_2.text())
                pareto_data = np.random.pareto(a, self.size)
            elif self.select == "Cauchy Distribution":
                # ����Cauchy�ֲ��������
                cauchy_data = np.random.standard_cauchy (self.size)
                print(cauchy_data)
        except BaseException as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Error")
            error_dialog.showMessage(str(e))
            error_dialog.exec_()
            
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Random_interface()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())

