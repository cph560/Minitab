# coding=gbk

import matplotlib
# ʹ�� matplotlib�е�FigureCanvas (��ʹ�� Qt5 Backends�� FigureCanvas�̳���QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import numpy as np

class Indiviplt(QtWidgets.QDialog):
    def __init__(self,  data =[[400,500,230,650,780,230,600,300,300],[1200,880,950,230,530,340,110,230,30,20,120]], item = ["A1",'A2']):
        # �����ʼ������
        super(Indiviplt,self).__init__()
        
        # ����QWidgets
        self.figure = plt.figure()
        self.setWindowTitle("Individual Value Graph")
        self.canvas = FigureCanvas(self.figure)
        # self.button_plot = QtWidgets.QPushButton("����")
        self.data = data
        self.items = item
        # �����¼�
        # self.button_plot.clicked.connect(self.plot_)
        
        # ���ò���
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        # layout.addWidget(self.button_plot)
        self.setLayout(layout)
        # ת������
        x = []
        for i in range(len(item)):
            x += [[item[i]] * len(data[i])]
        
        xf = []
        yf = []
        for i in range(len(item)):
            xf += x[i]
            yf += data[i]
        
        ax1 = self.figure.subplots(1,1)

        color = 'tab:blue'
        ax1.set_title('Individual Value Plot', fontsize=16, color=color)
        ax1.set_xlabel('Item', fontsize=16)
        ax1.set_ylabel('Data', fontsize=16)
        sns.set_style("whitegrid")
    
        ax1 = sns.swarmplot(x=np.array(xf), y=np.array(yf), color="red", alpha=.35)

        self.canvas.draw()
        # plt.show()

# ���г���
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Indiviplt()
    main_window.show()
    app.exec()