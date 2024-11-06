from General_Window import  general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QColor, QBrush
import numpy as np
from time_series_setting import Ui_Dialog as time_setting
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
import sys
import seaborn as sns
import pandas as pd

class Time_series_plot(general_window):
    def __init__(self,data):
        super().__init__('Time_series_plot')
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.plot.ok_btn.clicked.connect(self.plot_data)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot_type = 'Single'
        self.load_data(data)#载入数据

    def open_setting(self):
        self.new_window_setting = QtWidgets.QWidget()
        self.setting = time_setting()
        self.setting.setupUi(self.new_window_setting)

        self.new_window_setting.show()

        if self.plot_type == 'Single':
            self.setting.radioButton.setChecked(True)
        elif self.plot_type == 'Multiple':
            self.setting.radioButton_2.setChecked(True)

        self.setting.ok_Btn.clicked.connect(self.get_plot_type)
        # self.windows.append(self.new_window_setting)

    def get_plot_type(self):
        if self.setting.radioButton.isChecked():
            self.plot_type = 'Single'
        elif self.setting.radioButton_2.isChecked():
            self.plot_type = 'Multiple'
        self.new_window_setting.close()

    def plot_data(self):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei'是黑体的意思
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题


        column_text = self.plot.text_input.toPlainText()
        column_list = column_text.split(' ')
        marker_list = [".", "s", "^", "D", 'p', '*', 'h', 'H', "<", ">"]
        marker_size_list = [7, 3, 5, 5, 5, 5, 5, 5, 5, 5]

        for i in range(len(column_list) - 1, -1, -1):
            if column_list[i] == "":
                del column_list[i]
        '''分割位置，single plt/multiple'''
        try:
            title_list = ""
            for x in column_list:
                if title_list != "":
                    title_list += ','
                title_list += x
            if self.plot_type == 'Single' and len(column_list) > 1:
                self.msgbox_info('Info', '选取列的数量大于1，绘图类型修改为Mutiple')
                self.plot_type = "Multiple"
            elif self.plot_type == "Multiple" and len(column_list) ==1:
                self.msgbox_info('Info', '选取列的数量为1，修改类型绘图类型为Single')
                self.plot_type = 'Single'
            if len(column_list) ==0:
                self.msgbox_info('Error', '没有选取列，请检查')
                return

            if self.plot_type == 'Single':
                label_y = title_list
            else:
                label_y = 'Data'

            plot_data = self.table_raw_data.loc[:, column_list].copy()
            # print(plot_data.iloc[0,0])
            # while np.isnan(plot_data.iloc[0, 0]):
            #     plot_data.drop(plot_data.index[0], inplace=True)
            plot_data.insert(0, 'order', list(range(1, len(plot_data) + 1)))
            # plot_data = plot_data.fillna('')

            '''完成摘取数据，开始画图'''

            for i in range(1, plot_data.shape[1]):
                plt.plot(plot_data.order, plot_data.iloc[:, i], marker=marker_list[(i - 1) % len(marker_list)],
                         label=plot_data.columns[i],markersize=marker_size_list[(i - 1) % len(marker_size_list)])


            plt.title('Time Series Plot of %s' % title_list)
            max_data_count = len(plot_data)
            x_major_locator = MultipleLocator(max_data_count//8)
            ax = plt.gca()  # 实例化坐标轴
            ax.xaxis.set_major_locator(x_major_locator)  # 把x轴的主刻度设置为1的倍数
            plt.xlabel('Index')
            plt.ylabel(label_y)
            if self.plot_type == "Multiple":
                plt.legend()
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
    app = QtWidgets.QApplication(sys.argv)
    main_window = Time_series_plot(df)
    app.exec()
