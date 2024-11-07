# coding=gbk
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import numpy as np
from pandas.core.common import temp_setattr

#自定义Widget
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


#主函数
#除#可修改项以外均为QtDesigner生成
class Ui_Main(Ui_GUI):
    def __init__(self):
        self.windows = []

    def setupUi(self, GUI):
        super().setupUi(GUI)
        Row_Count = 5000  #可修改项
        Col_Count = 25  #可修改项
        self.GUI = GUI  #可修改项

        self.tableWidget = MyTableWidget(self.centralwidget)  #可修改项
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(Col_Count)  # 修改项
        self.tableWidget.setRowCount(Row_Count + 1)  # 修改项
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
    def resize_setting(self):
        #没做窗口，目前是默认值
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

    # 随机数接口
    def random_int(self):
        from Random import Random_interface
        interface = Random_interface()
        interface.random_res.connect(self.update_random)
        if interface.exec_() == QDialog.Accepted:
            print(interface.results)
            self.update_random(interface.col_name, result=interface.results)

    def adjust_column_width(self):
        #自动调整列宽，并维持列宽在设定最小值之上
        min_column_width = 100
        for column in range(self.tableWidget.columnCount()):
            print(self.tableWidget.columnWidth(column))
            self.tableWidget.resizeColumnToContents(column)
            if self.tableWidget.columnWidth(column) < min_column_width:
                self.tableWidget.setColumnWidth(column, min_column_width)
    def update_random(self, name="C1", result=[]):
        #默认名不生效，暂未排查原因
        if name == "":
            name = "C1"
        #以上为临时解决方案
        result = [float(i) for i in result]
        name_list = name.split()
        for i in range(len(name_list)):
            self.tableWidget.random_col(name_list[i], result)
        self.reset_col_row_name()
        self.adjust_column_width()

    def get_table_data(self):
        #保存编辑中的位置数据
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

        # 获取表格数据
        data = []
        for row in range(1, self.tableWidget.rowCount()):
            rowData = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    if self.is_number(item.text()):
                        rowData.append(float(item.text()))
                    else:
                        rowData.append(np.nan)
                    # if item.text().isdigit():
                    #     '''导入时只导入数字，后续可以优化成自动判断数据类型'''
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
        # 转换为pandas的DataFrame格式
        df = pd.DataFrame(data)
        df.columns = title
        '''待补内容：转移标题进dataframe'''
        '''==========================='''
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all')
        # df=df.fillna('')  #填充nan
        return df

    # Pareto图接口
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
        # 结束编辑状态
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
# coding=gbk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys

#自定义Widget
from mytablewidget import MyTableWidget
from PyQt5.Qt import QTableWidgetItem

#主函数
#除#可修改项以外均为QtDesigner生成
class Ui_GUI(object):
    def setupUi(self, GUI):
        GUI.setObjectName("GUI")
        GUI.resize(834, 697)
        GUI.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        GUI.setMouseTracking(False)

        self.GUI = GUI #可修改项
        self.centralwidget = QtWidgets.QWidget(GUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = MyTableWidget(self.centralwidget) #可修改项
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(25) #可修改项
        self.tableWidget.setRowCount(5000)  #可修改项

        ################################
        # 修改所有 Default 列名到C?(Ex. C1,C2)
        col_num = self.tableWidget.columnCount()
        row_num = self.tableWidget.rowCount()
        for num in range(col_num):
                self.tableWidget.setHorizontalHeaderItem(num,QTableWidgetItem("C"+str(num+1)))
        # 修改所有 Cell 值到“”
        for i in range(row_num):
            for j in range(col_num):
                item = QTableWidgetItem()
                item.setText("")
                self.tableWidget.setItem(i, j, item)
        ################################
        
        self.horizontalLayout.addWidget(self.tableWidget)
        GUI.setCentralWidget(self.centralwidget)

        self.menuBar = QtWidgets.QMenuBar(GUI)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 834, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuview = QtWidgets.QMenu(self.menuBar)
        self.menuview.setObjectName("menuview")
        self.menuSet = QtWidgets.QMenu(self.menuBar)
        self.menuSet.setObjectName("menuSet")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFormula = QtWidgets.QMenu(self.menuBar)
        self.menuFormula.setObjectName("menuFormula")
        self.menuMenu = QtWidgets.QMenu(self.menuBar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuplot = QtWidgets.QMenu(self.menuBar)
        self.menuplot.setObjectName("menuplot")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menuDOE = QtWidgets.QMenu(self.menu)
        self.menuDOE.setObjectName("menuDOE")
        self.menuQuality_Tool = QtWidgets.QMenu(self.menuBar)
        self.menuQuality_Tool.setObjectName("menuQuality_Tool")
        self.menuControl_Chart = QtWidgets.QMenu(self.menuQuality_Tool)
        self.menuControl_Chart.setObjectName("menuControl_Chart")
        GUI.setMenuBar(self.menuBar)
        self.actionNew = QtWidgets.QAction(GUI)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(GUI)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtWidgets.QAction(GUI)
        self.actionQuit.setObjectName("actionQuit")
        self.actionFull_Screen = QtWidgets.QAction(GUI)
        self.actionFull_Screen.setCheckable(False)
        self.actionFull_Screen.setObjectName("actionFull_Screen")
        self.actionNormal = QtWidgets.QAction(GUI)
        self.actionNormal.setObjectName("actionNormal")
        self.actionperference = QtWidgets.QAction(GUI)
        self.actionperference.setObjectName("actionperference")
        self.actionPID = QtWidgets.QAction(GUI)
        self.actionPID.setObjectName("actionPID")
        self.actionPareto = QtWidgets.QAction(GUI)
        self.actionPareto.setObjectName("actionPareto")
        self.actionsearch = QtWidgets.QAction(GUI)
        self.actionsearch.setObjectName("actionsearch")
        self.action = QtWidgets.QAction(GUI)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(GUI)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(GUI)
        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(GUI)
        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(GUI)
        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(GUI)
        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(GUI)
        self.action_7.setObjectName("action_7")
        self.actionKAPPA = QtWidgets.QAction(GUI)
        self.actionKAPPA.setObjectName("actionKAPPA")
        self.action_T = QtWidgets.QAction(GUI)
        self.action_T.setObjectName("action_T")
        self.action_T_2 = QtWidgets.QAction(GUI)
        self.action_T_2.setObjectName("action_T_2")
        self.action_T_3 = QtWidgets.QAction(GUI)
        self.action_T_3.setObjectName("action_T_3")
        self.actionANOVA = QtWidgets.QAction(GUI)
        self.actionANOVA.setObjectName("actionANOVA")
        self.action_8 = QtWidgets.QAction(GUI)
        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(GUI)
        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(GUI)
        self.action_10.setObjectName("action_10")
        self.action_11 = QtWidgets.QAction(GUI)
        self.action_11.setObjectName("action_11")
        self.action_12 = QtWidgets.QAction(GUI)
        self.action_12.setObjectName("action_12")
        self.action_13 = QtWidgets.QAction(GUI)
        self.action_13.setObjectName("action_13")
        self.actionType_I_Gage_Study = QtWidgets.QAction(GUI)
        self.actionType_I_Gage_Study.setObjectName("actionType_I_Gage_Study")
        self.actionGage_R_R = QtWidgets.QAction(GUI)
        self.actionGage_R_R.setObjectName("actionGage_R_R")
        self.actionKAPPA_2 = QtWidgets.QAction(GUI)
        self.actionKAPPA_2.setObjectName("actionKAPPA_2")
        self.actionProcess_Capability_Analysis = QtWidgets.QAction(GUI)
        self.actionProcess_Capability_Analysis.setObjectName("actionProcess_Capability_Analysis")
        self.actionI_MR_Chart = QtWidgets.QAction(GUI)
        self.actionI_MR_Chart.setObjectName("actionI_MR_Chart")
        self.actionX_Bar_Chart = QtWidgets.QAction(GUI)
        self.actionX_Bar_Chart.setObjectName("actionX_Bar_Chart")
        self.actionProbability_Plot = QtWidgets.QAction(GUI)
        self.actionProbability_Plot.setObjectName("actionProbability_Plot")
        self.actionRandom_Int = QtWidgets.QAction(GUI)
        self.actionRandom_Int.setObjectName("actionRandom_Int")
        self.menuview.addAction(self.actionFull_Screen)
        self.menuview.addAction(self.actionNormal)
        self.menuSet.addAction(self.actionperference)
        self.menuHelp.addAction(self.actionsearch)
        self.menuFormula.addAction(self.actionRandom_Int)
        self.menuMenu.addAction(self.actionNew)
        self.menuMenu.addAction(self.actionSave)
        self.menuMenu.addAction(self.actionQuit)
        self.menuplot.addAction(self.action)
        self.menuplot.addAction(self.action_3)
        self.menuplot.addAction(self.action_4)
        self.menuplot.addAction(self.action_5)
        self.menuplot.addAction(self.action_6)
        self.menuplot.addAction(self.action_7)
        self.menuplot.addAction(self.actionProbability_Plot)
        self.menuDOE.addAction(self.action_12)
        self.menuDOE.addAction(self.action_13)
        self.menu.addAction(self.action_T)
        self.menu.addAction(self.action_T_2)
        self.menu.addAction(self.action_T_3)
        self.menu.addAction(self.actionANOVA)
        self.menu.addAction(self.action_8)
        self.menu.addAction(self.action_9)
        self.menu.addAction(self.action_10)
        self.menu.addAction(self.action_11)
        self.menu.addAction(self.menuDOE.menuAction())
        self.menuControl_Chart.addAction(self.actionI_MR_Chart)
        self.menuControl_Chart.addAction(self.actionX_Bar_Chart)
        self.menuQuality_Tool.addAction(self.actionType_I_Gage_Study)
        self.menuQuality_Tool.addAction(self.actionGage_R_R)
        self.menuQuality_Tool.addAction(self.actionKAPPA_2)
        self.menuQuality_Tool.addAction(self.actionProcess_Capability_Analysis)
        self.menuQuality_Tool.addAction(self.menuControl_Chart.menuAction())
        self.menuBar.addAction(self.menuMenu.menuAction())
        self.menuBar.addAction(self.menuFormula.menuAction())
        self.menuBar.addAction(self.menuplot.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menuQuality_Tool.menuAction())
        self.menuBar.addAction(self.menuview.menuAction())
        self.menuBar.addAction(self.menuSet.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(GUI)
        self.actionFull_Screen.triggered.connect(GUI.showMaximized) # type: ignore
        self.actionNormal.triggered.connect(GUI.showNormal) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GUI)

        #以下是添加项（连接Function)
        self.actionKAPPA_2.triggered.connect(self.clear) 
        self.actionRandom_Int.triggered.connect(self.random_int) 
        self.action_5.triggered.connect(self.Pareto) 
        self.action_6.triggered.connect(self.Indiviplt)
        self.action_7.triggered.connect(self.boxplt)
    #修改名字
    #除#可修改项以外均为QtDesigner生成                               
    def retranslateUi(self, GUI):
        _translate = QtCore.QCoreApplication.translate
        GUI.setWindowTitle(_translate("GUI", "Test demo"))
        self.menuview.setTitle(_translate("GUI", "View"))
        self.menuSet.setTitle(_translate("GUI", "Settings"))
        self.menuHelp.setTitle(_translate("GUI", "Help"))
        self.menuFormula.setTitle(_translate("GUI", "Formula"))
        self.menuMenu.setTitle(_translate("GUI", "File"))
        self.menuplot.setTitle(_translate("GUI", "Plots"))
        self.menu.setTitle(_translate("GUI", "Statistic"))
        self.menuDOE.setTitle(_translate("GUI", "DOE"))
        self.menuQuality_Tool.setTitle(_translate("GUI", "Quality Tool"))
        self.menuControl_Chart.setTitle(_translate("GUI", "Control Chart"))
        self.actionNew.setText(_translate("GUI", "New"))
        self.actionNew.setShortcut(_translate("GUI", "`"))
        self.actionSave.setText(_translate("GUI", "Save       Ctrl+S"))
        self.actionQuit.setText(_translate("GUI", "Quit"))
        self.actionFull_Screen.setText(_translate("GUI", "Full Screen"))
        self.actionNormal.setText(_translate("GUI", "Normal"))
        self.actionperference.setText(_translate("GUI", "Perference"))
        self.actionPID.setText(_translate("GUI", "PID"))
        self.actionPareto.setText(_translate("GUI", "Pareto"))
        self.actionsearch.setText(_translate("GUI", "Search"))
        self.action.setText(_translate("GUI", "Time Series Plot"))
        self.action_2.setText(_translate("GUI", "控制图"))
        self.action_3.setText(_translate("GUI", "Scatter Plot"))
        self.action_4.setText(_translate("GUI", "Histogram"))
        self.action_5.setText(_translate("GUI", "Pareto Chart"))
        self.action_6.setText(_translate("GUI", "Individual Plot"))
        self.action_7.setText(_translate("GUI", "Box Plot"))
        self.actionKAPPA.setText(_translate("GUI", "KAPPA"))
        self.action_T.setText(_translate("GUI", "1 Sample T Test"))
        self.action_T_2.setText(_translate("GUI", "2 Sample T Test"))
        self.action_T_3.setText(_translate("GUI", "Paired T Test"))
        self.actionANOVA.setText(_translate("GUI", "ANOVA"))
        self.action_8.setText(_translate("GUI", "Chi-SQ Test"))
        self.action_9.setText(_translate("GUI", "2 Variances Test"))
        self.action_10.setText(_translate("GUI", "Simple Linear Regression"))
        self.action_11.setText(_translate("GUI", "Regression"))
        self.action_12.setText(_translate("GUI", "Full Factorial"))
        self.action_13.setText(_translate("GUI", "Partial Factorial"))
        self.actionType_I_Gage_Study.setText(_translate("GUI", "Type I Gage Study"))
        self.actionGage_R_R.setText(_translate("GUI", "Gage R&&R"))
        self.actionKAPPA_2.setText(_translate("GUI", "KAPPA"))
        self.actionProcess_Capability_Analysis.setText(_translate("GUI", "Process Capability Analysis"))
        self.actionI_MR_Chart.setText(_translate("GUI", "I-MR Chart"))
        self.actionX_Bar_Chart.setText(_translate("GUI", "X-Bar R Chart"))
        self.actionProbability_Plot.setText(_translate("GUI", "Probability Plot "))
        self.actionRandom_Int.setText(_translate("GUI", "Random Int"))

#----------------------------------------------------------------以下自定义项 Example
    #清空
    def clear(self):
        # 移除tableWidget控件
        self.horizontalLayout.removeWidget(self.tableWidget)
        # 删除tableWidget控件
        del self.tableWidget
        
        
        # 创建新的tableWidget控件
        self.tableWidget = MyTableWidget(self.centralwidget)
        # 设置控件对象名称
        self.tableWidget.setObjectName("tableWidget")
        # # 设置列数
        # self.tableWidget.setColumnCount(10)
        # # 设置行数
        # self.tableWidget.setRowCount(10)
        # 将控件添加到布局中
        self.horizontalLayout.addWidget(self.tableWidget)
        
        # 设置主窗口的中央控件
        self.GUI.setCentralWidget(self.centralwidget)
    # 随机数接口
    def random_int(self):
        from Random import Random_interface
        
        interface = Random_interface()
        interface.random_res.connect(self.update_random)
        if interface.exec_() == QDialog.Accepted:
            print(interface.results)
            self.update_random(interface.col_name, result=interface.results)
        

    def update_random(self, name= "c1", result=[]):
        
        result = [float(i) for i in result]
        name_list = name.split()
        for i in range(len(name_list)):
            self.tableWidget.random_col(name_list[i], result)

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
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())