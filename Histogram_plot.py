from General_Window import  general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QColor, QBrush
import numpy as np
from histogram_setting import Ui_Dialog as setting_window
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
import sys
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator
from scipy.stats import norm


class Histogram_plot(general_window):
    def __init__(self,data):
        super().__init__('Histogram')
        self.plot.ok_btn.clicked.connect(self.plot_data)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.distribution_set = 'Yes'
        self.load_data(data)#载入数据

    def open_setting(self):
        self.new_window_setting = QtWidgets.QWidget()
        self.setting = setting_window()
        self.setting.setupUi(self.new_window_setting)

        self.new_window_setting.show()

        if self.distribution_set == 'Yes':
            self.setting.radioButton.setChecked(True)
        elif self.distribution_set == 'No':
            self.setting.radioButton_2.setChecked(True)

        self.setting.ok_Btn.clicked.connect(self.get_setting)
        # self.windows.append(self.new_window_setting)

    def get_setting(self):
        if self.setting.radioButton.isChecked():
            self.distribution_set = 'Yes'
        elif self.setting.radioButton_2.isChecked():
            self.distribution_set = 'No'
        self.new_window_setting.close()

    def plot_data(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei'是黑体的意思
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题


        column_text = self.plot.text_input.toPlainText()
        column_list = column_text.split(' ')


        for i in range(len(column_list) - 1, -1, -1):
            if column_list[i] == "":
                del column_list[i]
        '''分割位置，single plt/multiple'''
        try:
            if len(column_list) ==0:
                self.msgbox_info('Error', '没有选取列，请检查')
                return
            elif len(column_list) >6:
                self.msgbox_info('Error', '选取列过多，目前最多支持6组数据')
                return
            #确定y轴标题
            title_list = ""
            for x in column_list:
                if title_list != "":
                    title_list += ','
                title_list += x



            plot_data = self.table_raw_data.loc[:, column_list].copy()
            # 使用斯特奇斯规则确定bin的数量
            n = len(plot_data)
            k = 1 + 3.322 * np.log10(n)
            bin=max(6,int(np.sqrt(n)))
            #提取画图数据

            colormap = plt.get_cmap('Set1')
            colormap2= plt.get_cmap('Set2')
            # column_to_plot = ['Size','Amount']


            for i,column in enumerate(column_list):
                histogram_label_added = False
                fit_label_added = False
                plot_data_drop=plot_data[column].dropna()#对绘图数据去除nan
                print(column,len(plot_data_drop))
                plt.hist(plot_data_drop, density=True,bins=bin, alpha=0.9, color=colormap(i) , edgecolor='black',label=f'{column}-Histogram')
                if  self.distribution_set=="Yes":
                    mu, std = norm.fit(plot_data_drop)
                    # 生成拟合的正态分布曲线的数据点
                    x = np.linspace(plot_data_drop.min(), plot_data_drop.max(), 100)
                    y = norm.pdf(x, mu, std)
                    # 绘制拟合的正态分布曲线
                    plt.plot(x, y, '-.', color=colormap2(i),linewidth=2,label=f'{column}-Fit')


            plt.legend()
            #图标设置
            plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
            # 添加标题和标签
            plt.title('Histogram of %s' % title_list)
            plt.xlabel('Value')
            plt.ylabel('Frequency')


            # 显示图形
            plt.show()



        except Exception as e:
            print(e)
            self.msgbox_info('Error', '列信息有误，请检查')


if __name__ == '__main__':
    columns = ['Size', 'Amount', 'C3', 'Test', 'C5']
    # 定义数据
    data = [
        [19.0, 14.0, 9.0, 12.0, 3.0],
        [3.0, 16.0, 5.0, 20.0, 20.0],
        [19.0, 5.0, 14.0, 15.0, 9.0],
        [18.0, 10.0, 5.0, 13.0, 8.0],
        [6.0, 14.0, 12.0, 10.0, 2.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [9.0, 8.0, 5.0, 11.0, 18.0],
        [5.0, 15.0, 16.0, 5.0, 9.0]
    ]

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    df=pd.DataFrame(np.random.randn(1000),columns=['1'])
    df['2']=np.random.randn(1000)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Histogram_plot(df)
    app.exec()
