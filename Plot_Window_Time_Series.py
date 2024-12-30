from Plot_Window_General import  general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from GUI_Plot_Window_Time_Series_Setting import Ui_Dialog as time_setting
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, title
import sys
import pandas as pd
import numpy as np

class Time_series_plot(general_window):
    def __init__(self,data,title,type):
        super().__init__('Time_series_plot')
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.plot.ok_btn.clicked.connect(self.plot_data)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.x_custom=''
        self.x_type='Seq'
        self.load_data(data,title,type)#载入列表数据
        self.load_status=False
        self.title_matrix=title
        self.swapped_title_matrix = {v: k for k, v in self.title_matrix.items()}
        self.type_matrix=type
        self.open_windows = []
        self.open_windows.append(self.new_window)


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
        self.open_windows.append(self.new_window_setting)

    def change_x_column_visible(self, checked):
        # 根据 Btn_X_Specific 的状态设置 x_column 的可见性
        self.setting.X_column.setVisible(self.setting.Btn_X_Specific.isChecked())
        if self.setting.Btn_X_Specific.isChecked() and not self.load_status:
            self.load_data_column_list()


    def get_setting(self):
        if self.setting.Btn_X_Sequence.isChecked():
            self.x_type = 'Seq'
        elif self.setting.Btn_X_Specific.isChecked():
            self.x_type = 'Customized'
            self.x_custom=self.setting.X_column.currentText().split(" ")[0]
        self.new_window_setting.close()
    def load_data_column_list(self):
        self.setting.X_column.clear()  # 清空现有的选项
        column_list=self.get_col_list_by_type(self.table_raw_data,self.title_matrix,self.type_matrix,['T','D',''])
        for i, column in enumerate(column_list):
            item = column_list[i].replace("\t"," ")
            self.setting.X_column.addItem(item)
    def data_calibration(self):
        column_text = self.plot.text_input.toPlainText()
        #校验列数量
        if not column_text:
            column_list = []
        else:
            column_list = column_text.split(' ')
            for i, column in enumerate(column_list):
                if column in self.swapped_title_matrix:
                    column_list[i] = self.swapped_title_matrix[column]

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
        for i, column in enumerate(column_list):
            if column!='' and column in self.swapped_title_matrix:
                column_list[i] = self.swapped_title_matrix[column]

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 'SimHei'是黑体的意思
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题

        marker_list = [".", "s", "^", "D", 'p', '*', 'h', 'H', "<", ">"]
        marker_size_list = [7, 3, 5, 5, 5, 5, 5, 5, 5, 5]


        # try:
        title_list = []
        for x in column_list:
            if self.title_matrix[x]!='':
                title_list.append(self.title_matrix[x])
            else:
                title_list.append(x)
        label_y = ','.join(title_list)

        plot_data = self.table_raw_data.loc[:, column_list].copy()
        plot_data = plot_data.dropna(how='all')
        if self.x_type=='Seq':
            plot_data.insert(0, 'order', list(range(1, len(plot_data) + 1)))
        else:
            x_custom_data = self.table_raw_data[self.x_custom].copy()
            x_custom_data = x_custom_data.apply(lambda x: str(x) if pd.notna(x) else x)
            if len(x_custom_data) > len(plot_data):
                x_custom_data = x_custom_data.iloc[:len(plot_data)]
            plot_data['order'] = x_custom_data


        '''完成摘取数据，开始画图'''
        line_counter=0
        x = plot_data['order'].dropna()

        if len(x) > len(plot_data):
            x = x.iloc[:len(plot_data)]
        elif len(x) < len(plot_data):
            temp_list = []
            for j in range(len(plot_data) - len(x)):
                temp_list.append('no_label_' + str(j))
            x = pd.concat([x, pd.Series(temp_list)], ignore_index=True)



        for i in range(0, plot_data.shape[1]):
            if plot_data.columns[i]!='order':
                y= plot_data.iloc[:, i].dropna()
                x_draw=x[:len(y)]
                plt.plot(x_draw,y, marker=marker_list[(line_counter) % len(marker_list)],
                     label=plot_data.columns[i],markersize=marker_size_list[line_counter % len(marker_size_list)])
                line_counter += 1


        plt.title('Time Series Plot of %s' % label_y)

        data_interval = len(plot_data['order'])
        data_interval = max(data_interval // 8, 1)
        x_major_locator = MultipleLocator(data_interval)

        ax = plt.gca()  # 实例化坐标轴
        ax.xaxis.set_major_locator(x_major_locator)  # 把x轴的主刻度设置为1的倍数
        if self.x_type=='Seq':
            xlabel='Index'
        else:
            if self.title_matrix[self.x_custom]=='':
                xlabel=self.x_custom
            else:
                xlabel=self.title_matrix[self.x_custom]


        filtered_positions = [x[i] for i in range(len(x)) if i % data_interval == 0]


        filtered_labels = [str(x) if 'no_label_' not in str(x) else '' for x in filtered_positions]

        ax.set_xticks(filtered_positions)
        if any(len(label) > 8 for label in filtered_labels):
            plt.subplots_adjust(bottom=0.2)
            ax.set_xticklabels(filtered_labels, rotation=45)
        else:
            ax.set_xticklabels(filtered_labels)
        plt.xlabel(xlabel)
        plt.ylabel(label_y)
        plt.show()

        # except Exception as e:
        #
        #     self.msgbox_info('Error', str(e))


if __name__ == '__main__':
    columns = ['C1', 'C2', 'C3', 'C4', 'C5','C6']
    # 定义数据
    data = [
        [19.0, 14.0, 9.0, 12.0, 1.0,'test1',],
        [3.0, 16.0, 5.0, 20.0, 3.0,'test2'],
        [19.0, 5.0, 14.0, 15.0, 5.0,'test3'],
        [18.0, 10.0, 5.0, 13.0, 8.0,'test4'],
        [6.0, 14.0, 12.0, 10.0, 10.0,'test5123421'],
        [0.0, 0.0, 0.0, 0.0, 11.0,'test6'],
        [9.0, 8.0, 5.0, 11.0, 18.0,np.nan],
        [1, 15.0, 16.0, 5.0, 19.0,np.nan]
    ]
    title_matrix= {'C1':'Size','C2':'Amount','C3':'','C4':'Test','C5':'','C6':'test1'}
    type_matrix= {'C1':'','C2':'','C3':'','C4':'','C5':'','C6':'T'}

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Time_series_plot(df,title_matrix,type_matrix)
    app.exec()
