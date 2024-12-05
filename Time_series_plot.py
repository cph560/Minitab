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
        self.x_custom=''
        self.x_type='Seq'
        self.load_data(data)#载入数据
        self.load_status=False

    def open_setting(self):
        self.new_window_setting = QtWidgets.QWidget()
        self.setting = time_setting()
        self.setting.setupUi(self.new_window_setting)
        self.new_window_setting.show()
        if self.x_type=='Seq':
            self.setting.Btn_X_Sequence.setChecked(True)
            self.setting.X_column.setVisible(False)
        else:
            self.setting.Btn_X_Specific.setChecked(True)
            self.load_data_column_list()
            self.setting.X_column.setCurrentText(self.x_custom)

        self.setting.Btn_OK.clicked.connect(self.get_setting)
        self.setting.Btn_X_Sequence.toggled.connect(self.change_x_column_visible)
        self.setting.Btn_X_Specific.toggled.connect(self.change_x_column_visible)
        # self.windows.append(self.new_window_setting)

    def change_x_column_visible(self, checked):
        # 根据 Btn_X_Specific 的状态设置 x_column 的可见性
        self.setting.X_column.setVisible(self.setting.Btn_X_Specific.isChecked())
        if self.setting.Btn_X_Specific.isChecked() and not self.load_status:
            self.load_data_column_list()


    def get_setting(self):
        if self.setting.Btn_X_Sequence.isChecked():
            self.x_type = 'Seq'
        elif self.setting.Btn_X_Specific.isChecked():
            self.x_type = 'Cusomized'
            self.x_custom=self.setting.X_column.currentText()
        self.new_window_setting.close()
    def load_data_column_list(self):
        self.setting.X_column.clear()  # 清空现有的选项
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            self.setting.X_column.addItem(item.text())
    def data_calibration(self):
        column_text = self.plot.text_input.toPlainText()
        #校验列数量
        if not column_text:
            column_list = []
        else:
            column_list = column_text.split(' ')
        if len(column_list) == 0:
            QMessageBox.about(self.new_window,'Error', '没有选取列，请检查')
            return False
        elif len(column_list) > 6:
            QMessageBox.about(self.new_window,'Error', '选取列过多，目前最多支持6组数据')
            return False
        #校验列有效性
        column_titles = self.table_raw_data.columns.tolist()
        # 重复性校验
        count_dict = {}
        for column in column_list:
            if column in count_dict:
                count_dict[column] += 1
            else:
                count_dict[column] = 1
        duplicates = [column for column, count in count_dict.items() if count > 1]
        if duplicates:
            QMessageBox.about(self.new_window,'Error',f"存在重复项: {duplicates}")
            return False

        # 有效性校验
        validation_results = {}
        for column in column_list:
            if column in column_titles:
                validation_results[column] = True
            else:
                validation_results[column] = False
        invalid_columns = [column for column, is_valid in validation_results.items() if not is_valid]
        if len(invalid_columns)>0:
            QMessageBox.about(self.new_window,'Error',f"无效的列名: {invalid_columns}")
            return False
        #校验数据类型
        plot_data = self.table_raw_data.loc[:, column_list].copy()
        data_type = [0] * len(column_list)
        for i, column in enumerate(column_list):  # 数据校验
            plot_data_drop = plot_data[column].dropna()  # 对绘图数据去除nan
            for item in plot_data_drop:
                if not self.is_number(item):
                    data_type[i] = 1
                    break
        if sum(data_type) != len(column_list) and sum(data_type) != 0:
            QMessageBox.about(self.new_window, 'Error', '数据类型不一致')
            return False
        return True
    def plot_data(self):
        if not self.data_calibration():
            return
        column_text = self.plot.text_input.toPlainText()
        column_list = column_text.split(' ')

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei'是黑体的意思
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题



        marker_list = [".", "s", "^", "D", 'p', '*', 'h', 'H', "<", ">"]
        marker_size_list = [7, 3, 5, 5, 5, 5, 5, 5, 5, 5]

        for i in range(len(column_list) - 1, -1, -1):
            if column_list[i] == "":
                del column_list[i]

        try:
            title_list = ""
            for x in column_list:
                if title_list != "":
                    title_list += ','
                title_list += x

            if len(column_list) ==0:
                self.msgbox_info('Error', '没有选取列，请检查')
                return

            label_y = title_list

            plot_data = self.table_raw_data.loc[:, column_list].copy()
            if self.x_type=='Seq':
                plot_data.insert(0, 'order', list(range(1, len(plot_data) + 1)))
            else:
                plot_data['order'] = self.table_raw_data[self.x_custom].copy()
            # plot_data = plot_data.fillna('')

            '''完成摘取数据，开始画图'''

            for i in range(0, plot_data.shape[1]):
                if plot_data.columns[i]!='order':
                    x=plot_data['order']
                    y= plot_data.iloc[:, i]
                    plt.plot(x,y, marker=marker_list[(i - 1) % len(marker_list)],
                         label=plot_data.columns[i],markersize=marker_size_list[(i - 1) % len(marker_size_list)])

            plt.title('Time Series Plot of %s' % title_list)

            data_interval = max(plot_data['order'])-min(plot_data['order'])
            data_interval=max(data_interval//8,1)
            x_major_locator = MultipleLocator(data_interval)
            ax = plt.gca()  # 实例化坐标轴
            ax.xaxis.set_major_locator(x_major_locator)  # 把x轴的主刻度设置为1的倍数
            if self.x_type=='Seq':
                xlabel='Index'
            else:
                xlabel=self.x_custom
            plt.xlabel(xlabel)
            plt.ylabel(label_y)
            plt.show()

        except Exception as e:

            self.msgbox_info('Error', str(e))


if __name__ == '__main__':
    columns = ['Size', 'Amount', 'C3', 'Test', 'C5']
    # 定义数据
    data = [
        [19.0, 14.0, 9.0, 12.0, 1.0],
        [3.0, 16.0, 5.0, 20.0, 3.0],
        [19.0, 5.0, 14.0, 15.0, 5.0],
        [18.0, 10.0, 5.0, 13.0, 8.0],
        [6.0, 14.0, 12.0, 10.0, 10.0],
        [0.0, 0.0, 0.0, 0.0, 11.0],
        [9.0, 8.0, 5.0, 11.0, 18.0],
        [5.0, 15.0, 16.0, 5.0, 19.0]
    ]

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Time_series_plot(df)
    app.exec()
