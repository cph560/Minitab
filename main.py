# coding=gbk
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import numpy as np
from pandas.core.common import temp_setattr
from tkinter import filedialog, Widget
import math

# 自定义Widget
from mytablewidget import MyTableWidget
from PyQt5.Qt import QTableWidgetItem
from designer import Ui_GUI
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
from PyQt5.QtWidgets import *
import random
import re
from PyQt5.QtWidgets import QMessageBox


# 主函数
# 除#可修改项以外均为QtDesigner生成
class Ui_Main(Ui_GUI):
    def __init__(self):
        self.windows = []

    def setupUi(self, GUI):
        super().setupUi(GUI)
        self.WidgetRowCount = 5000  # 可修改项
        self.WidgetColCount = 25  # 可修改项
        self.GUI = GUI  # 可修改项

        self.tableWidget = MyTableWidget(self.centralwidget)  # 可修改项
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(self.WidgetColCount)  # 修改项
        self.tableWidget.setRowCount(self.WidgetRowCount + 1)  # 修改项
        GUI.setCentralWidget(self.tableWidget)

        GUI.setObjectName("GUI")
        GUI.resize(834, 697)
        GUI.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        GUI.setMouseTracking(False)

        ################################
        '''修改行名列名'''
        self.reset_col_row_name()

        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        # for num in range(col_num):
        #         self.tableWidget.setHorizontalHeaderItem(num,QTableWidgetItem("C"+str(num+1)))
        ''' 修改所有 Cell 值到“” '''

        '''修改颜色'''
        color = Qt.lightGray
        for i in range(row_num):
            for j in range(col_num):
                if i == 0:
                    item = ColorDelegate(color)
                else:
                    item = QTableWidgetItem()
                item.setText("")
                self.tableWidget.setItem(i, j, item)
        ###############################
        self.tableWidget.init = 'yes'
        # self.actionKAPPA_2.triggered.connect(self.clear)
        self.action_5.triggered.connect(self.Pareto)
        self.action_6.triggered.connect(self.Indiviplt)
        self.action_7.triggered.connect(self.boxplt)
        self.action.triggered.connect(self.Time_serires_plt)
        self.action_3.triggered.connect(self.Scatter_plt)
        self.action_4.triggered.connect(self.Histogram_plt)
        self.actionsearch.triggered.connect(self.set_random_data)
        self.actionRandom_Int.triggered.connect(self.random_int)
        self.actionNew.triggered.connect(self.resize_setting)
        self.action_statistics.triggered.connect(self.calculate_statistics)
        self.action_equation.triggered.connect(self.equation)
        self.actionSave.triggered.connect(self.SaveToExcel)
        self.actionLoad.triggered.connect(self.LoadExcel)
        self.actionQuit.triggered.connect(self.closeall)

    def show_message_box(self, title, message, icon):
        msg_box = QMessageBox(icon, title, message)
        msg_box.exec_()
    def resize_setting(self):
        from GUI_Dialog_New import Ui_Dialog as Dialog_New
        self.new_window_resize = QtWidgets.QWidget()
        self.resize_setting = Dialog_New()
        self.resize_setting.setupUi(self.new_window_resize)
        self.resize_setting.lineEdit_Row.setText(str(self.WidgetRowCount))
        self.resize_setting.lineEdit_Col.setText(str(self.WidgetColCount))
        self.resize_setting.pushButton_OK.clicked.connect(self.resize_Widget)
        self.resize_setting.pushButton_Cancel.clicked.connect(self.close_resize_setting_window)
        self.new_window_resize.show()
        # 没做窗口，目前是默认值
    def resize_Widget(self):
        row_input=self.resize_setting.lineEdit_Row.text()
        col_input=self.resize_setting.lineEdit_Row.text()
        clean_flag=self.resize_setting.checkBox_clean.isChecked()
        if not row_input.isdigit() or int(row_input) <= 1 or not col_input.isdigit() or int(col_input) <= 1:
            self.show_message_box("错误", "行列数请输入大于1的正整数。", QMessageBox.Critical)
            return
        row=int(self.resize_setting.lineEdit_Row.text())
        col=int(self.resize_setting.lineEdit_Col.text())

        self.rebuild(row + 1, col,clean_flag)
        self.WidgetRowCount=row
        self.WidgetColCount=col
        self.close_resize_setting_window()

    def close_resize_setting_window(self):
        try:
            self.new_window_resize.close()
        except:
            pass
    def rebuild(self, newRowCount, newColumnCount,clean=True):
        self.tableWidget.init = 'no'

        col_num_ori = self.tableWidget.columnCount()
        self.tableWidget.setRowCount(newRowCount)
        self.tableWidget.setColumnCount(newColumnCount)
        color = Qt.lightGray

        if clean:
            self.tableWidget.clearContents()
            col_num_ori=0
        for j in range(col_num_ori,newColumnCount):
            item = ColorDelegate(color)
            item.setText("")
            self.tableWidget.setItem(0,j,item)

        self.reset_col_row_name()
        self.tableWidget.init = 'yes'

    def reset_col_row_name(self):
        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        Column_List = ["C" + str(x) for x in range(1, col_num + 1)]
        Row_List = [str(x) for x in range(1, row_num + 1)]
        Row_List.insert(0, "Title")
        self.tableWidget.setHorizontalHeaderLabels(Column_List)
        self.tableWidget.setVerticalHeaderLabels(Row_List)

    # def clear(self):
    #     # 移除tableWidget控件
    #     self.horizontalLayout.removeWidget(self.tableWidget)
    #     # 删除tableWidget控件
    #     del self.tableWidget
    #
    #     # 创建新的tableWidget控件
    #     self.tableWidget = MyTableWidget(self.centralwidget)
    #     # 设置控件对象名称
    #     self.tableWidget.setObjectName("tableWidget")
    #     # 设置列数
    #     self.tableWidget.setColumnCount(10)
    #     # 设置行数
    #     self.tableWidget.setRowCount(10)
    #     # 将控件添加到布局中
    #     self.horizontalLayout.addWidget(self.tableWidget)
    #
    #     # 设置主窗口的中央控件
    #     self.GUI.setCentralWidget(self.centralwidget)
    #
    #     self.reset_col_row_name()

    # 随机数接口
    def random_int(self):
        from Random import Random_interface

        interface = Random_interface()
        interface.random_res.connect(self.update_random)

        if interface.exec_() == QDialog.Accepted:
            # print(interface.results)
            self.update_random(interface.col_name, result=interface.results)

    def adjust_column_width(self):
        # 自动调整列宽，并维持列宽在设定最小值之上
        min_column_width = 100
        for column in range(self.tableWidget.columnCount()):
            # print(self.tableWidget.columnWidth(column))
            self.tableWidget.resizeColumnToContents(column)
            if self.tableWidget.columnWidth(column) < min_column_width:
                self.tableWidget.setColumnWidth(column, min_column_width)

    def update_random(self, name="C1", result=[]):

        # 默认名不生效，暂未排查原因
        if name == "":
            name = "C1"
        # 以上为临时解决方案
        name_list = name.split()

        for lis_num in range(len(name_list)):
            res_set = [float(i) for i in result[lis_num].flatten()]
            self.tableWidget.import_col(name_list[lis_num], res_set)

        self.reset_col_row_name()
        self.adjust_column_width()

    # Equation 接口
    def equation(self):
        from Equation import Ui_Equation
        Table_data = self.tableWidget.transfer_data()
        line_1_title = {}

        for col in range(self.WidgetColCount):
            if self.tableWidget.item(0, col).text() != "":

                line_1_title[self.tableWidget.item(0, col).text()] = "C" + str(col + 1)
            

        for key in line_1_title.keys():
            
            Table_data[line_1_title[key]] = Table_data.pop(key)
        print(Table_data)        
        try:
            current_col = self.tableWidget.selectedItems()[0].column()
            # print(current_col)
            Table_data["*C" + str(current_col + 1)] = []
        except:
            pass

        try:
            self.r = self.tableWidget.selectedItems()[0].row()
            content = self.tableWidget.selectedItems()[0].text()
            value = float(content) if content else 1
            # print([self.r, current_col+1, value])
            interface = Ui_Equation(Table_data, [self.r, current_col + 1, value])
            interface.eq_res.connect(self.Update_equation)

            if interface.exec_() == QDialog.Accepted:

                if "*" in interface.select:
                    print(interface.select)
                    # out_col = interface.select.lstrip("*")
                    # print(out_col, interface.row_num)
                    self.Update_equation(interface.select, result=interface.result, row=interface.row_num)
                else:
                    print(interface.select)
                    self.Update_equation(name=interface.outputcolumn, result=interface.result, row=interface.row_num)

        except BaseException as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Error")
            error_dialog.showMessage(str(e))
            error_dialog.exec_()

    def Update_equation(self, name="C1", result=[], row=1):
        # 默认名不生效，暂未排查原因
        if name == "":
            name = "C1"
        # 以上为临时解决方案
        # print(name)
        if "*" in name:
            name = name.lstrip("*")

        name_list = name.split()

        for lis_num in range(len(name_list)):
            res_set = [float(i) for i in result]
            self.tableWidget.import_col(name_list[lis_num], res_set, row)

        self.reset_col_row_name()
        self.adjust_column_width()


    def SaveToExcel(self):
        # 尝试保存数据到Excel文件
        try:
            # 获取表格数据
            df = self.get_table_data()[0]
            # 打印数据
            print(df)
            # 弹出文件夹选择对话框
            folder_path = filedialog.askdirectory()
            # 将数据保存到Excel文件
            df.to_excel(f"{folder_path}/Saved_data.xlsx", index=False)
        except BaseException as e:
            # 如果出现异常，弹出错误对话框
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Error")
            error_dialog.showMessage(str(e))
            error_dialog.exec_()

    def LoadExcel(self):
        try:
            folder_path = filedialog.askopenfilenames()
            # print(folder_path)
            dataframe = pd.read_excel(folder_path[0])
            LoadData = dataframe.to_dict(orient='list')
            # print(LoadData)

            for key in LoadData.keys():
                new_list = [item for item in LoadData[key] if not (math.isnan(item)) == True]

                self.tableWidget.import_col(key, new_list, 1)
        except BaseException as e:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Error")
            error_dialog.showMessage(str(e))
            error_dialog.exec_()

    def save_editing_data(self):
        try:
            current_row = self.tableWidget.selectedItems()[0].row()
            current_col = self.tableWidget.selectedItems()[0].column()

            temp_row = 0
            temp_col = 0
            if current_row == 0 and current_col == 0:
                temp_row = 1
            self.tableWidget.setCurrentCell(temp_row, temp_col)

            self.tableWidget.setCurrentCell(current_row, current_col)
        except:
            pass
    def print_time(self):
        from datetime import datetime
        # 获取当前时间
        current_time = datetime.now()
        # 格式化时间为字符串，精确到秒
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        # 输出当前时间
        print(formatted_time)
    def get_table_data(self):
        # 保存编辑中的位置数据
        self.save_editing_data()
        # 获取表格数据
        col_data = []
        col_title=[]
        Title_matrix = {}
        type_matrix = {}
        for col in range(self.WidgetColCount):
            data = []
            for row in range(1, self.WidgetRowCount + 1):
                item = self.tableWidget.item(row, col)

                if item is None: break
                value = item.text()
                if value == '': break

                if self.is_number(value):
                    data.append(float(value))
                elif value != "" and value != np.nan:
                    data.append(value)
                else:
                    data.append(np.nan)
            if len(data) > 0:
                if self.tableWidget.horizontalHeaderItem(col) is not None:
                    C_title = self.tableWidget.horizontalHeaderItem(col).text()
                    if self.tableWidget.item(0, col) is not None and self.tableWidget.item(0, col).text() != '':
                        Title_matrix[C_title]=self.tableWidget.item(0, col).text()
                    else:
                        Title_matrix[C_title]=''
                    col_title.append(C_title)
                    type_matrix[C_title]=self.data_classification(data)
                    col_data.append(data)
        # 转换为pandas的DataFrame格式
        df = pd.DataFrame(col_data).transpose()
        df.columns = col_title
        # df=df.fillna('')  #填充nan
        return df,Title_matrix,type_matrix
    
    def data_classification(self,list):
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
            r'\d{4}\.\d{2}\.\d{2}',  # YYYY.MM.DD
            r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
        ]
        has_date = False
        has_text = False

        for item in list:
            if isinstance(item, str):
                # Check if the string matches any date pattern
                if any(re.match(pattern, item) for pattern in date_patterns):
                    has_date = True
                else:
                    has_text = True
            elif isinstance(item, (int, float)):
                continue
            else:
                has_text = True

            # If both date and text are found, we can stop early
            if has_date and has_text:
                return 'T'

        if has_date:
            return 'D'
        elif has_text:
            return 'T'
        else:
            return ''

    def is_number(self, s):
        pattern = r'^-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?$'
        return re.match(pattern, s) is not None

    def set_random_data(self):
        for i in range(1, 60):
            for j in range(8):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(random.randint(0, 20))))
        for i in range(63, 90):
            for j in range(5):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(random.randint(0, 20))))

    def Time_serires_plt(self):
        from Plot_Window_Time_Series import Time_series_plot
        # 结束编辑状态
        table_data,title_matrix,type_matrix= self.get_table_data()
        pl = Time_series_plot(table_data,title_matrix,type_matrix)
        self.windows.append(pl)

    def Scatter_plt(self):
        from Plot_Window_Scatter import Scatter_plot
        table_data,title_matrix,type_matrix= self.get_table_data()
        pl = Scatter_plot(table_data,title_matrix,type_matrix)
        self.windows.append(pl)

    def Histogram_plt(self):
        from Plot_Window_Histogram import Histogram_plot
        table_data,title_matrix,type_matrix = self.get_table_data()
        pl = Histogram_plot(table_data,title_matrix,type_matrix)
        self.windows.append(pl)

    # Pareto图接口
    def Pareto(self):
        from Plot_interface import Ui_Plot_interface
        pareto_data = self.tableWidget.transfer_data()
        interface = Ui_Plot_interface('Pareto', pareto_data)
        interface.exec_()

    # Individual图接口
    def Indiviplt(self):
        from Plot_interface import Ui_Plot_interface
        Individual_data = self.tableWidget.transfer_data()

        interface = Ui_Plot_interface('Individual', Individual_data)
        interface.exec_()

    # Box图接口
    def boxplt(self):
        from Plot_interface import Ui_Plot_interface
        box_data = self.tableWidget.transfer_data()
        interface = Ui_Plot_interface('box', box_data)
        interface.exec_()

    def calculate_statistics(self):
        if len(self.tableWidget.selectedItems()) == 0:
            QMessageBox.about(MainWindow, 'Error', 'No cells selected')
            return
        selected_items = []
        total_selected_count = 0  # 选中的项的个数
        valid_selected_count = 0  # 被统计的有效量的数量
        # 获取选中的单元格
        for item in self.tableWidget.selectedItems():
            total_selected_count += 1
            try:
                value = float(item.text())
                selected_items.append(value)
                valid_selected_count += 1
            except ValueError:
                continue

        if not selected_items:
            Result = {
                "Mean": None,
                "Max": None,
                "Min": None,
                "Variance": None,
                "Median": None,
                "Sum": None,

            }
        else:
        # 计算统计量
            mean = np.mean(selected_items)
            max_value = np.max(selected_items)
            min_value = np.min(selected_items)
            variance = np.var(selected_items)
            median = np.median(selected_items)
            sum = np.sum(selected_items)

            Result = {"Mean": mean,
                      "Max": max_value,
                      "Min": min_value,
                      "Variance": variance,
                      "Median": median,
                      "Sum": sum,
                      }

        def format_value(value, precision=5):
            if value is None:
                return "None"
            return f"{value:.{precision}g}"
        formatted_result = {key: format_value(value) for key, value in Result.items()}
        result_str = "Count:\t%s\n" %  str(valid_selected_count)
        cal_result = "\n".join([f"{key}:\t {value}" for key, value in formatted_result.items()])
        result_str += cal_result
        from GUI_Window_Statistics import Ui_Dialog as Statistics_window
        self.new_window_statistics = QtWidgets.QWidget()
        self.setting = Statistics_window()
        self.setting.setupUi(self.new_window_statistics)
        self.setting.text_Browser.setText(result_str)
        self.setting.pushButton_copy.clicked.connect(self.copy_result)
        self.setting.pushButton_close.clicked.connect(self.close_statistics_window)
        self.new_window_statistics.show()



        # QMessageBox.about(MainWindow, 'Statistic Results', result_str)
    def close_statistics_window(self):
        try:
            self.new_window_statistics.close()
        except :
            pass
    def copy_result(self):
        window = self.new_window_statistics
        result_str = self.setting.text_Browser.toPlainText()
        import pyperclip
        pyperclip.copy(result_str)
        QMessageBox.about(window, '提示', '已复制到剪贴板')
    def closeall(self):
        # 添加自定义逻辑
        sys.exit()


class ColorDelegate(QTableWidgetItem):
    def __init__(self, color):
        super(ColorDelegate, self).__init__()
        self.setBackground(QBrush(color))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Main()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
