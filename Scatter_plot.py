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
from PyQt5.Qt import QTableWidgetItem, QAbstractItemView
import pandas as pd
import sys

class Scatter_plot(general_window):
    def __init__(self,data):
        super().__init__('Scatter_plot')
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.table_raw_data=None
        self.load_data(data)#载入数据

        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.cancel_btn.clicked.connect(self.quit)
        self.plot.clear_btn.clicked.connect(self.clear_input)
        self.plot.ok_btn.clicked.connect(self.plot_data)
        for i in range(10):  # 初始化
            for j in range(2):
                self.plot.tableWidget.setItem(i, j, QTableWidgetItem(""))
        self.plot.tableWidget.setCurrentCell(0, 0)


    def quit(self):
        self.new_window.close()


    def msgbox_info(self, title, text):
        QMessageBox.about(self.new_window, title, text)


    def load_data(self,data):
        self.table_raw_data = data
        self.model = QStandardItemModel()
        for col in self.table_raw_data.columns:
            self.model.appendRow(QStandardItem(str(col)))
        self.plot.listView.setModel(self.model)
        self.plot.listView.show()


    def add_to_column_list(self):
        selected = self.model.item(self.plot.listView.currentIndex().row()).text()
        select_row = self.plot.tableWidget.selectedItems()[0].row()
        select_column = self.plot.tableWidget.selectedItems()[0].column()
        item=QTableWidgetItem(selected)
        self.plot.tableWidget.setItem(select_row, select_column, QTableWidgetItem(selected))
        next_row=select_row
        next_column = select_column
        if select_column == 1:
            if select_row == 9:
                pass
            else:
                next_column = 0
                next_row = select_row + 1
        else:
            next_column = 1
            next_row = select_row

        self.plot.tableWidget.setCurrentCell(next_row, next_column)


    def clear_input(self):
        for i in range(10):  # 初始化
            for j in range(2):
                self.plot.tableWidget.setItem(i, j, QTableWidgetItem(""))


    def plot_data(self):
        data_list = []

        for i in range(10):
            for j in range(2):
                data_list.append(self.plot.tableWidget.item(i, j).text())

        for i in range(0, 10, 2):
            if bool(data_list[i])!=bool(data_list[i + 1]):
                self.msgbox_info('Error', 'x,y变量不匹配，请检查')
                return

        plot_list=[item for item in data_list if item != ''] #提取画图列


        plot_df=self.table_raw_data[plot_list] #提取画图数据

        for i in range(0, len(plot_df.columns), 2):
            # 确保有足够的列来配对
            if i + 1 < len(plot_df.columns):
                x = plot_df.iloc[:, i+1]  # 第i+1列作为x
                y = plot_df.iloc[:, i ]  # 第i列作为y
                plt.scatter(x, y, label=f'({plot_df.columns[i]}, {plot_df.columns[i + 1]})')
        plt.legend()
        # Giving title to the chart using plt.title
        plt.title('Scatter Plot')
        # plt.xticks(rotation=0, ha='center')
        # Providing x and y label to the chart
        data_count=len(plot_df)
        #y列的最大最小值
        odd_max = plot_df.iloc[:, ::2].max()
        odd_min = plot_df.iloc[:, ::2].min()
        odd_interval=odd_max.iloc[0]-odd_min.iloc[0]

        # 获取偶数列的最大值和最小值
        even_max = plot_df.iloc[:, 1::2].max()
        even_min = plot_df.iloc[:, 1::2].min()
        even_interval=even_max.iloc[0]-even_min.iloc[0]

        x_major_locator = MultipleLocator(even_interval//8)
        ax = plt.gca()  # 实例化坐标轴
        ax.xaxis.set_major_locator(x_major_locator)  # 把x轴的主刻度设置为1的倍数
        plt.xlabel('Index')
        plt.ylabel('data')
        # plt.xlim(0,None)
        plt.show()


    def open_setting(self):
        pass


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
    main_window = Scatter_plot(df)
    app.exec()