# coding=gbk
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from mytablewidget import MyTableWidget
from time_series_plot import Ui_Dialog
import pandas as pd
import numpy as np
from PyQt5.Qt import QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import datetime


class Ui_GUI(object):
    def __init__(self):
        self.windows = []

    def setupUi(self, GUI):
        GUI.setObjectName("GUI")
        GUI.resize(834, 697)
        GUI.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        GUI.setMouseTracking(False)

        self.GUI = GUI  # 修改项
        self.centralwidget = QtWidgets.QWidget(GUI)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = MyTableWidget(self.centralwidget)  # 修改项
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(25)  # 修改项
        self.tableWidget.setRowCount(5000)  # 修改项

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
        self.actionFull_Screen.triggered.connect(GUI.showMaximized)  # type: ignore
        self.actionNormal.triggered.connect(GUI.showNormal)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GUI)
        self.action.triggered.connect(self.open_plot_window)

        # 以下是添加项
        self.actionKAPPA_2.triggered.connect(self.clear)

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

    # ----------------------------------------------------------------自定义项 Example
    def clear(self):
        self.horizontalLayout.removeWidget(self.tableWidget)
        del self.tableWidget
        self.tableWidget = MyTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(10)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.GUI.setCentralWidget(self.centralwidget)

    def open_plot_window(self):
        for i in range(6):
            for j in range(2):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(2 * i + 3 * j)))

        pl = plot_Window()
        self.windows.append(pl)

    def get_table_data(self):
        # 获取表格数据
        data = []
        for row in range(self.tableWidget.rowCount()):
            rowData = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item is not None:
                    rowData.append(item.text())
                else:
                    rowData.append(np.nan)
            data.append(rowData)
        title=[]
        # for x in self.tableWidget.horizontalHeader().:
        #     a=x
        # 转换为pandas的DataFrame格式
        df = pd.DataFrame(data)
        '''待补内容：转移标题进dataframe'''
        '''==========================='''
        df = df.dropna(axis=0, how='all')
        df = df.dropna(axis=1, how='all')
        return df

    # def get_table_value(self, row, column):
    #     try:
    #         data = self.tableWidget.item(row, column).text()
    #         print(data)
    #     except:
    #         pass

    # def cell_changed(self):
    #     try:
    #         self.cell = self.tableWidget.currentItem()
    #         self.triggered = self.cell.text()
    #         print(self.triggered)
    #
    #     except:
    #         pass


class plot_Window(Ui_GUI):
    def __init__(self):
        super().__init__()
        self.table_raw_data = None
        self.model = None
        self.new_window = QtWidgets.QWidget()
        self.plot = Ui_Dialog()
        self.plot.setupUi(self.new_window)
        self.plot_load_data()
        self.plot.ok_btn.clicked.connect(self.plot_data)
        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.cancel_btn.clicked.connect(self.quit)
        self.new_window.show()

    def quit(self):
        self.new_window.close()

    def msgbox_info(self, title, text):
        QMessageBox.about(self.new_window, title, text)

    def plot_load_data(self):
        self.table_raw_data = Ui_GUI.get_table_data(ui)
        self.model = QStandardItemModel()
        for col in self.table_raw_data.columns:
            self.model.appendRow(QStandardItem(str(col)))
        self.plot.listView.setModel(self.model)
        self.plot.listView.show()
        app.exec_()

    def add_to_column_list(self):
        selected = str(self.plot.listView.currentIndex().row())
        text = self.plot.text_input.toPlainText()
        if text != "":
            text += " "
        self.plot.text_input.setText(text + selected)

    def plot_data(self):
        column_text = self.plot.text_input.toPlainText()
        title = column_text  # 目前的列名称的提取需要优化
        column_list = column_text.split(' ')
        for i in range(len(column_list) - 1, -1, -1):
            if column_list[i] == "":
                del column_list[i]
            if column_list[i].isdigit():
                column_list[i] = int(column_list[i])
            else:
                self.msgbox_info('Error', '列名称有误，请检查')
                return
        '''分割位置，single plt/multiple'''
        flag = 'single'
        if flag == 'single':
            if len(column_list) != 1:
                self.msgbox_info('Error', '选取列的数量有误，请检查')
                return
            else:
                plot_data = self.table_raw_data.loc[:, column_list].copy()
                plot_data.columns = ['data']
                plot_data.insert(0, 'order', list(range(1, len(plot_data) + 1)))
            '''完成摘取数据，开始画图'''
            # Plotting the time series of given dataframe
            plt.plot(plot_data.order, plot_data.data)
            # Giving title to the chart using plt.title
            plt.title('Time Series Plot of Time')
            plt.xticks(rotation=0, ha='middle')
            # Providing x and y label to the chart
            plt.xlabel('Index')
            plt.ylabel(title)

            plt.show()

    def test1(self):
        pass

        # print(self.data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
