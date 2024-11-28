# coding=gbk

import matplotlib
# ʹ�� matplotlib�е�FigureCanvas (��ʹ�� Qt5 Backends�� FigureCanvas�̳���QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import numpy as np

class boxplt(QtWidgets.QDialog):
    def __init__(self,  data =[[400,500,230,650,780,230,600,300,300],[1200,880,950,230,530,340,110,230,30,20,120]], item = ["A1",'A2']):
        # �����ʼ������
        super(boxplt,self).__init__()
        
        # ����QWidgets
        self.figure = plt.figure()
        self.setWindowTitle("Individual Value Graph")
        self.canvas = FigureCanvas(self.figure)
        self.button_plot = QtWidgets.QPushButton("Draw")
        self.data = data
        self.items = item
        # �����¼�
        self.button_plot.clicked.connect(self.plot_)
        
        # ���ò���
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.canvas)
        layout.addWidget(self.button_plot)
        self.setLayout(layout)
    
    # ���ӵĻ��Ƶķ���
    def plot_(self):

        # ת������
        x = []
        for i in range(len(self.items)):
            x += [[self.items[i]] * len(self.data[i])]
        
        xf = []
        yf = []
        for i in range(len(self.items)):
            xf += x[i]
            yf += self.data[i]
        # print(xf, yf)
        ax1 = self.figure.subplots(1,1)

        color = 'tab:blue'
        ax1.set_title('Box Plot', fontsize=16, color=color)
        ax1.set_xlabel('Item', fontsize=16)
        ax1.set_ylabel('Data', fontsize=16)
        sns.set_style("whitegrid")
    
        ax1 = sns.boxplot(x=np.array(xf), y=np.array(yf), color="blue")
        # self.canvas.draw()
        plt.show()
        self.closeall()


    def closeall(self):
        self.done(0)
        # self.canvas.close()
# ���г���
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = boxplt()
    main_window.show()
    app.exec()