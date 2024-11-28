from General_Window import general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QColor, QBrush
import numpy as np
from Scatter_plot_setting import Ui_Dialog as setting
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import FontProperties
from PyQt5.Qt import QTableWidgetItem, QAbstractItemView
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import MaxNLocator

import pandas as pd
import sys

class Scatter_plot(general_window):
    def __init__(self,data):
        super().__init__('Scatter_plot')
        self.setting = None
        self.new_window_setting = None
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.table_raw_data=None
        self.load_data(data)#载入数据

        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.cancel_btn.clicked.connect(self.quit)
        self.plot.clear_btn.clicked.connect(self.clear_input)
        self.plot.ok_btn.clicked.connect(self.open_plot_window)
        for i in range(10):  # 初始化
            for j in range(2):
                self.plot.tableWidget.setItem(i, j, QTableWidgetItem(""))
        self.plot.tableWidget.setCurrentCell(0, 0)
        self.draw_list = [1]
        self.open_windows = []
        self.open_windows.append(self.new_window)
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


    def open_plot_window(self):
        try:
            plt.close('all')
        except:
            pass
        data_list = []
        for i in range(10):
            for j in range(2):
                data_list.append(self.plot.tableWidget.item(i, j).text())

        for i in range(0, 10, 2):
            if bool(data_list[i]) != bool(data_list[i + 1]):
                self.msgbox_info('Error', 'x,y变量不匹配，请检查')
                return

        plot_list = [item for item in data_list if item != '']  # 提取画图列
        plot_df = self.table_raw_data[plot_list]  # 提取画图数据

        from Result_window import Ui_Plot_window as result_window
        self.new_window_plot = QtWidgets.QWidget()
        self.result_window = result_window()
        self.result_window.setupUi(self.new_window_plot)
        self.result_window.pushButton_close.clicked.connect(self.close)
        self.result_window.pushButton_copy.clicked.connect(self.copy_result)
        self.figure = Figure()
        # 创建一个 FigureCanvas 实例
        self.canvas = FigureCanvas(self.figure)
        # 创建一个 NavigationToolbar 实例
        self.toolbar = NavigationToolbar(self.canvas, self.new_window_plot)
        # 获取 plot_container 的布局
        layout = QtWidgets.QVBoxLayout(self.result_window.plot_container)
        # 将 FigureCanvas 和 NavigationToolbar 添加到布局中
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.plot_data(plot_df)
        self.new_window_plot.show()
        self.open_windows.append(self.new_window_plot)
    def plot_data(self,plot_df):
        self.figure.patch.set_facecolor('white')
        self.figure.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.13)
        ax = self.figure.add_subplot(111)

        # 设置字体
        ax.set_xlabel('X-axis', fontdict={'family': 'serif', 'size': 12, 'weight': 'normal'})
        ax.set_ylabel('Y-axis', fontdict={'family': 'serif', 'size': 12, 'weight': 'normal'})
        ax.set_title('Scatter Plot', fontdict={'family': 'serif', 'size': 14, 'weight': 'bold'})

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 设置英文字体
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman']
        # # 设置中文字体
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
        # plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
        # # 设置英文字体
        # plt.rcParams['font.family'] = 'serif'  # 指定默认字体为serif
        # plt.rcParams['font.serif'] = ['Times New Roman']  # 指定英文字体为Times New Roman


        colormap = plt.get_cmap('Set1')
        colormap2 = plt.get_cmap('Set2')


        formula=''
        formula_plain=''
        for i in range(0, len(plot_df.columns), 2):
            # 确保有足够的列来配对
            if i + 1 < len(plot_df.columns):
                x = plot_df.iloc[:, i+1]  # 第i+1列作为x
                y = plot_df.iloc[:, i ]  # 第i列作为y
                label = '(%s,%s)'%(plot_df.columns[i], plot_df.columns[i + 1])

                ax.scatter(x, y, color=colormap(i),label=label)

                if 1 in self.draw_list:
                    coefficients_linear = np.polyfit(x, y, 1)
                    # 生成拟合线的y值
                    y_linear = np.polyval(coefficients_linear, x)
                    ax.plot(x, y_linear, label='Linear Fit - %s' % label)
                    linear_equation,linear_plain = self.coefficients_to_equation(coefficients_linear)

                    formula += f'{label} - Linear: y={linear_equation}<br>'
                    formula_plain+=f'{label} - Linear: y={linear_plain}\n'

                if 2 in self.draw_list:

                    coefficients_quadratic = np.polyfit(x, y, 2)
                    y_quadratic = np.polyval(coefficients_quadratic, x)
                    quadratic_equation,quadratic_plain = self.coefficients_to_equation(coefficients_quadratic)
                    ax.plot(x, y_quadratic, label='Quadratic Fit- %s'%label)
                    formula += f'{label} - Quadratic:y= {quadratic_equation}<br>'
                    formula_plain += f'{label} - Quadratic: y= {quadratic_plain}\n'
                if 3 in self.draw_list:
                    coefficients_cubic = np.polyfit(x,y, 3)
                    y_cubic = np.polyval(coefficients_cubic, x)
                    cubic_equation,cubic_plain = self.coefficients_to_equation(coefficients_cubic)
                    ax.plot(x, y_cubic, label='Cubic Fit - %s'%label)
                    formula += f'{label} - Cubic: y= {cubic_equation}<br>'
                    formula_plain+=f'{label} - Cubic: y= {cubic_plain}\n'



        ax.legend()
        # Giving title to the chart using plt.title
        # ax.title('Scatter Plot')

        #y列的最大最小值
        odd_max = plot_df.iloc[:, ::2].max()
        odd_min = plot_df.iloc[:, ::2].min()
        odd_interval=max(odd_max)-min(odd_min.iloc)

        # 获取偶数列的最大值和最小值
        even_max = plot_df.iloc[:, 1::2].max()
        even_min = plot_df.iloc[:, 1::2].min()
        even_interval=max(even_max)-min(even_min)


        # ax = plt.gca()  # 实例化坐标轴
        ax.xaxis.set_major_locator(MaxNLocator(nbins=12))
        # bx = plt.gca()  # 实例化坐标轴
        ax.yaxis.set_major_locator(MaxNLocator(nbins=9))  # y轴的主刻度设置
        self.plain_text=formula_plain
        self.canvas.draw()
        if formula!='':
            self.result_window.textBrowser.setHtml(f'<html><body>{formula}</body></html>')

    def coefficients_to_equation(self,coefficients):
        # 将系数和对应的指数配对，并按照指数降序排列
        terms = []
        for i, c in enumerate(coefficients):
            if i == 0:
                terms.append([f'{c:.2g}', i])
            elif i == 1:
                terms.append([f'{c:.2g}x', i])
            else:
                terms.append([f'{c:.2g}x<sup>{i}</sup>', i])
            # 按照指数降序排列
        terms.sort(key=lambda x: -x[1])

        # 将排序后的项转换为方程字符串
        equation_parts = []
        for term in terms:
            coefficient_str = term[0].split('x')[0]
            if coefficient_str.startswith('-'):
                coefficient = float(coefficient_str)
                if coefficient != -1:
                    equation_parts.append(f' - {abs(coefficient):.2g}{term[0][len(coefficient_str):]}')
                else:
                    equation_parts.append(f' - x{term[0][len(coefficient_str) + 1:]}')
            elif coefficient_str != '0':
                coefficient = float(coefficient_str)
                if coefficient != 1:
                    equation_parts.append(f' + {coefficient:.2g}{term[0][len(coefficient_str):]}')
                else:
                    equation_parts.append(f' + x{term[0][len(coefficient_str) + 1:]}')
        # 去掉第一个加号
        if equation_parts and equation_parts[0].startswith(' + '):
            equation_parts[0] = equation_parts[0][3:]

        equation = ''.join(equation_parts) if equation_parts else '0'

        terms = []
        for i, c in enumerate(coefficients):
            if i == 0:
                terms.append([f'{c:.2g}', i])
            elif i == 1:
                terms.append([f'{c:.2g}x', i])
            else:
                terms.append([f'{c:.2g}x^{i}', i])
            # 按照指数降序排列
        terms.sort(key=lambda x: -x[1])

        equation_parts = []
        for term in terms:
            coefficient_str = term[0].split('x')[0]
            if coefficient_str.startswith('-'):
                coefficient = float(coefficient_str)
                if coefficient != -1:
                    equation_parts.append(f' - {abs(coefficient):.2g}{term[0][len(coefficient_str):]}')
                else:
                    equation_parts.append(f' - x{term[0][len(coefficient_str) + 1:]}')
            elif coefficient_str != '0':
                coefficient = float(coefficient_str)
                if coefficient != 1:
                    equation_parts.append(f' + {coefficient:.2g}{term[0][len(coefficient_str):]}')
                else:
                    equation_parts.append(f' + x{term[0][len(coefficient_str) + 1:]}')

        # 去掉第一个加号
        if equation_parts and equation_parts[0].startswith(' + '):
            equation_parts[0] = equation_parts[0][3:]

        equation_plain = ''.join(equation_parts) if equation_parts else '0'

        # 将方程字符串包裹在LaTeX的数学模式符号中
        return f'{equation}',equation_plain
    def open_setting(self):
        self.new_window_setting = QtWidgets.QWidget()
        self.setting = setting()
        self.setting.setupUi(self.new_window_setting)
        self.new_window_setting.show()
        if 1 in self.draw_list:
            self.setting.checkBox_1.setChecked(True)
        else:
            self.setting.checkBox_1.setChecked(False)
        if 2 in self.draw_list:
            self.setting.checkBox_2.setChecked(True)
        else:
            self.setting.checkBox_2.setChecked(False)
        if 3 in self.draw_list:
            self.setting.checkBox_3.setChecked(True)
        else:
            self.setting.checkBox_3.setChecked(False)

        self.setting.ok_Btn.clicked.connect(self.get_setting)
    def get_setting(self):
        self.draw_list=[]
        if self.setting.checkBox_1.isChecked():
            self.draw_list.append(1)
        if self.setting.checkBox_2.isChecked():
            self.draw_list.append(2)
        if self.setting.checkBox_3.isChecked():
            self.draw_list.append(3)
        self.new_window_setting.close()

    def copy_result(self):
        import pyperclip
        pyperclip.copy(self.plain_text)
    def close(self):
        self.new_window_plot.close()



if __name__ == '__main__':
    # columns = ['Size', 'Amount', 'C3', 'Test', 'C5']
    # # 定义数据
    # data = [
    #     [19.0, 14.0, 9.0, 12.0, 3.0],
    #     [3.0, 16.0, 5.0, 20.0, 20.0],
    #     [19.0, 5.0, 14.0, 15.0, 9.0],
    #     [18.0, 10.0, 5.0, 13.0, 8.0],
    #     [6.0, 14.0, 12.0, 10.0, 2.0],
    #     [0.0, 0.0, 0.0, 0.0, 0.0],
    #     [9.0, 8.0, 5.0, 11.0, 18.0],
    #     [5.0, 15.0, 16.0, 5.0, 9.0]
    # ]
    np.random.seed(0)
    x = np.random.rand(50) * 10  # 生成50个随机x值
    y = 3 * x + 2 + np.random.randn(50) * 5  # 生成对应的y值，包含一些噪声
    df=pd.DataFrame({'Size':x,'Amount':y})

    #
    # # 创建DataFrame
    # df = pd.DataFrame(data, columns=columns)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Scatter_plot(df)
    app.exec()