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
        self.button_plot = QtWidgets.QPushButton("Draw")
        self.data = data
        self.items = item
        # 连接事件
        self.button_plot.clicked.connect(self.plot_)
        
        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.canvas)
        layout.addWidget(self.button_plot)
        self.setLayout(layout)
        # 转换数据
    # 连接的绘制的方法
    def plot_(self):
        x = []
        for i in range(len(self.items)):
            x += [[self.items[i]] * len(self.data[i])]
        
        xf = []
        yf = []
        for i in range(len(self.items)):
            xf += x[i]
            yf += self.data[i]
        
        ax1 = self.figure.subplots(1,1)

        color = 'tab:blue'
        ax1.set_title('Individual Value Plot', fontsize=16, color=color)
        ax1.set_xlabel('Item', fontsize=16)
        ax1.set_ylabel('Data', fontsize=16)
        sns.set_style("whitegrid")
    
        ax1 = sns.swarmplot(x=np.array(xf), y=np.array(yf), color="red", alpha=.35)

        # self.canvas.draw()
        plt.show()
        self.closeall()


    def closeall(self):
        self.done(0)
        # self.canvas.close()
# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Indiviplt()
    main_window.show()
    app.exec()