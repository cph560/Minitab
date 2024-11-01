# coding=gbk

import matplotlib
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import numpy as np

class Indiviplt(QtWidgets.QDialog):
    def __init__(self,  data =[[400,500,230,650,780,230,600,300,300],[1200,880,950,230,530,340,110,230,30,20,120]], item = ["A1",'A2']):
        # 父类初始化方法
        super(Indiviplt,self).__init__()
        
        # 几个QWidgets
        self.figure = plt.figure()
        self.setWindowTitle("Individual Value Graph")
        self.canvas = FigureCanvas(self.figure)
        # self.button_plot = QtWidgets.QPushButton("绘制")
        self.data = data
        self.items = item
    
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("Status:")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)

        self.label_2.setText("   ")
        self.label_3.setText("Mean   ")
        self.label_4.setText("StDev   ")
        self.label_5.setText("N   ")
        self.label_6.setText("AD   ")
        self.label_7.setText("P-Value   ")
        # 连接事件
        # self.button_plot.clicked.connect(self.plot_)
        
        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(self.gridLayout)
        # layout.addWidget(self.button_plot)
        self.setLayout(layout)
        # 转换数据
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

# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Indiviplt()
    main_window.show()
    app.exec()