# coding=gbk

import matplotlib
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys
import seaborn as sns

class Paretoplt(QtWidgets.QDialog):
    def __init__(self,  data =[400,500,230,650,780,230,600,300,300,1200,880,950,230,530,340,110,230,30,20.22,120.1], item = ["A1",'A2','A3','A4','A5','A6','A7','A8','A9','A10','A11','A12','A13','A14','A15','A16','A17', 'A18','A19','A20']):
        # 父类初始化方法
        super(Paretoplt,self).__init__()
        
        # 几个QWidgets
        self.figure = plt.figure()
        self.setWindowTitle("Pareto Graph")
        self.canvas = FigureCanvas(self.figure)
        self.button_plot = QtWidgets.QPushButton("Draw")
        self.data = data
        self.items = item
        
        # 设置布局
        layout = QtWidgets.QVBoxLayout()
        # layout.addWidget(self.canvas)
        layout.addWidget(self.button_plot)
        self.setLayout(layout)
        # 连接事件
        self.button_plot.clicked.connect(self.plot_)
    # 连接的绘制的方法
    def plot_(self):
        # ax = self.figure.add_axes([0.1,0.1,0.8,0.8])
        # ax.plot([1,2,3,4,5,6,7,8,9,10])
        # self.canvas.draw()
        # plt.show()
        
        sets = []
        sum_data = sum(self.data)
        sum_percent = 0
        scope = len(self.data) if len(self.data)<= len(self.items) else len(self.items)
        for i in range(scope):
            
            sets.append([self.items[i], self.data[i], 0, 0])

        sets = sorted(sets, key = lambda sets: sets[1], reverse = True)

        for i in range(len(sets)):
            sum_percent += sets[i][1]/sum_data
            sets[i][2] = sets[i][1]/sum_data
            sets[i][3] = sum_percent

        ax1 = self.figure.subplots(1,1)

        color = 'tab:blue'
        ax1.set_title('Pareto Chart', fontsize=16, color=color)
        ax1.set_xlabel('Item', fontsize=16)
        ax1.set_ylabel('Data', fontsize=16, color=color)
        #第一图条形图
        ax1 = sns.barplot(x=[x[0] for x in sets], y=[x[1] for x in sets], legend = True)
        ax1.tick_params(axis='y', labelcolor=color)
        #twinx共享x轴(类似的语法，如共享y轴twiny)
        ax2 = ax1.twinx()
        color = 'tab:red'
        #第二个图，折线图
        ax2.set_ylabel('Sum', fontsize=16, color=color)
        ax2 = sns.lineplot(x=[x[0] for x in sets], y=[x[3] for x in sets], sort=False, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        # self.canvas.draw()

        plt.show()

        self.closeall()


    def closeall(self):
        self.done(0)
        # self.canvas.close()
        
# 运行程序
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = Paretoplt()
    main_window.show()
    app.exec()