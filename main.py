# coding=gbk
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import numpy as np
from pandas.core.common import temp_setattr

#�Զ���Widget
from mytablewidget import MyTableWidget
from PyQt5.Qt import QTableWidgetItem
from designer import Ui_GUI
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
from PyQt5.QtWidgets import *
import random
import re
import time
from PyQt5.QtWidgets import QMessageBox



#������
#��#���޸��������ΪQtDesigner����
class Ui_Main(Ui_GUI):
    def __init__(self):
        self.windows = []

    def setupUi(self, GUI):
        super().setupUi(GUI)
        Row_Count = 5000  #���޸���
        Col_Count = 25  #���޸���
        self.GUI = GUI  #���޸���

        self.tableWidget = MyTableWidget(self.centralwidget)  #���޸���
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(Col_Count)  # �޸���
        self.tableWidget.setRowCount(Row_Count + 1)  # �޸���
        GUI.setCentralWidget(self.tableWidget)

        GUI.setObjectName("GUI")
        GUI.resize(834, 697)
        GUI.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        GUI.setMouseTracking(False)

        ################################
        '''�޸���������'''
        self.reset_col_row_name()

        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        # for num in range(col_num):
        #         self.tableWidget.setHorizontalHeaderItem(num,QTableWidgetItem("C"+str(num+1)))
        ''' �޸����� Cell ֵ������ '''

        '''�޸���ɫ'''
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
    def resize_setting(self):
        #û�����ڣ�Ŀǰ��Ĭ��ֵ
        newRowCount=10
        newColumnCount=10
        self.rebuild(newRowCount+1,newColumnCount)
        pass
    def reset_col_row_name(self):
        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        Column_List = ["C" + str(x) for x in range(1, col_num + 1)]
        Row_List = [str(x) for x in range(1, row_num + 1)]
        Row_List.insert(0, "Title")
        self.tableWidget.setHorizontalHeaderLabels(Column_List)
        self.tableWidget.setVerticalHeaderLabels(Row_List)

    # def clear(self):
    #     # �Ƴ�tableWidget�ؼ�
    #     self.horizontalLayout.removeWidget(self.tableWidget)
    #     # ɾ��tableWidget�ؼ�
    #     del self.tableWidget
    #
    #     # �����µ�tableWidget�ؼ�
    #     self.tableWidget = MyTableWidget(self.centralwidget)
    #     # ���ÿؼ���������
    #     self.tableWidget.setObjectName("tableWidget")
    #     # ��������
    #     self.tableWidget.setColumnCount(10)
    #     # ��������
    #     self.tableWidget.setRowCount(10)
    #     # ���ؼ���ӵ�������
    #     self.horizontalLayout.addWidget(self.tableWidget)
    #
    #     # ���������ڵ�����ؼ�
    #     self.GUI.setCentralWidget(self.centralwidget)
    #
    #     self.reset_col_row_name()
    def rebuild(self,newRowCount,newColumnCount):
        self.tableWidget.init = 'no'
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(newRowCount)
        self.tableWidget.setColumnCount(newColumnCount)
        color = Qt.lightGray
        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        for i in range(row_num):
            for j in range(col_num):
                if i == 0:
                    item = ColorDelegate(color)
                else:
                    item = QTableWidgetItem()
                item.setText("")
                self.tableWidget.setItem(i, j, item)
        self.reset_col_row_name()
        self.tableWidget.init = 'yes'

    # ������ӿ�
    def random_int(self):
        from Random import Random_interface
        interface = Random_interface()
        interface.random_res.connect(self.update_random)
        if interface.exec_() == QDialog.Accepted:
            print(interface.results)
            self.update_random(interface.col_name, result=interface.results)

    def adjust_column_width(self):
        #�Զ������п���ά���п����趨��Сֵ֮��
        min_column_width = 100
        for column in range(self.tableWidget.columnCount()):
            print(self.tableWidget.columnWidth(column))
            self.tableWidget.resizeColumnToContents(column)
            if self.tableWidget.columnWidth(column) < min_column_width:
                self.tableWidget.setColumnWidth(column, min_column_width)
    def update_random(self, name="C1", result=[]):
        #Ĭ��������Ч����δ�Ų�ԭ��
        if name == "":
            name = "C1"
        #����Ϊ��ʱ�������
        result = [float(i) for i in result]
        name_list = name.split()
        for i in range(len(name_list)):
            self.tableWidget.random_col(name_list[i], result)
        self.reset_col_row_name()
        self.adjust_column_width()

    def get_table_data(self):
        #����༭�е�λ������
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

        # ��ȡ�������
        data = []
        for row in range(1, self.tableWidget.rowCount()):
            rowData = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    if self.is_number(item.text()):
                        rowData.append(float(item.text()))
                    elif item.text() !="" and item.text()!=np.nan:
                        rowData.append(item.text())
                    else:
                        rowData.append(np.nan)
                    # if item.text().isdigit():
                    #     '''����ʱֻ�������֣����������Ż����Զ��ж���������'''
                    #     rowData.append(float(item.text()))
                    # else:
                    #     rowData.append(np.nan)
                else:
                    rowData.append(np.nan)
            data.append(rowData)
        title = []
        for i in range(self.tableWidget.columnCount()):
            if self.tableWidget.horizontalHeaderItem(i) is not None:
                column_title = self.tableWidget.horizontalHeaderItem(i).text()
                if self.tableWidget.item(0, i) is not None and self.tableWidget.item(0, i).text() != '':
                    column_title = "%s" % self.tableWidget.item(0, i).text()
                title.append(column_title)
            else:
                title.append(str(i + 1))
        # ת��Ϊpandas��DataFrame��ʽ
        df = pd.DataFrame(data)
        df.columns = title
        '''�������ݣ�ת�Ʊ����dataframe'''
        '''==========================='''
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all')
        # df=df.fillna('')  #���nan
        return df

    # Paretoͼ�ӿ�
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
        # �����༭״̬
        from Time_series_plot import Time_series_plot
        table_data = self.get_table_data()
        pl = Time_series_plot(table_data)
        self.windows.append(pl)

    def Scatter_plt(self):
        from Scatter_plot import Scatter_plot
        table_data = self.get_table_data()
        pl = Scatter_plot(table_data)
        self.windows.append(pl)

    def Histogram_plt(self):
        from Histogram_plot import Histogram_plot
        table_data = self.get_table_data()
        pl = Histogram_plot(table_data)
        self.windows.append(pl)

    def Pareto(self):
        from Plot_interface import Ui_Plot_interface
        pareto_data = self.tableWidget.transfer_data()
        interface = Ui_Plot_interface('Pareto', pareto_data)
        interface.exec_()

    # Individualͼ�ӿ�
    def Indiviplt(self):
        from Plot_interface import Ui_Plot_interface
        Individual_data = self.tableWidget.transfer_data()

        interface = Ui_Plot_interface('Individual', Individual_data)
        interface.exec_()

    # Boxͼ�ӿ�
    def boxplt(self):
        from Plot_interface import Ui_Plot_interface
        box_data = self.tableWidget.transfer_data()
        interface = Ui_Plot_interface('box', box_data)
        interface.exec_()

    def calculate_statistics(self):
        selected_items = []
        total_selected_count = 0  # ѡ�е���ĸ���
        valid_selected_count = 0  # ��ͳ�Ƶ���Ч��������
        # ��ȡѡ�еĵ�Ԫ��
        for item in self.tableWidget.selectedItems():
            total_selected_count += 1
            try:
                value = float(item.text())
                selected_items.append(value)
                valid_selected_count += 1
            except ValueError:
                continue

        if not selected_items:
            Result= {
                "Mean": None,
                "Max": None,
                "Min": None,
                "Variance": None,
                "Median": None,
                "Sum": None,

            }
        # ����ͳ����
        mean = np.mean(selected_items)
        max_value = np.max(selected_items)
        min_value = np.min(selected_items)
        variance = np.var(selected_items)
        median = np.median(selected_items)
        sum=np.sum(selected_items)

        Result={"Mean": mean,
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
        result_str="Count: %s (valid:%s)\n"%(str(total_selected_count),str(valid_selected_count))
        cal_result= "\n".join([f"{key}: {value}" for key, value in formatted_result.items()])
        result_str+=cal_result
        QMessageBox.about(MainWindow, 'Statistic Results', result_str)


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
