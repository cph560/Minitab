from General_Window import general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import numpy as np
from Scatter_plot_setting import Ui_Dialog as setting
import matplotlib.pyplot as plt
from PyQt5.Qt import QTableWidgetItem
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import MaxNLocator
import pandas as pd
import sys



class Scatter_plot(general_window):
    def __init__(self, data,title,type):
        super().__init__('Scatter_plot')
        self.setting = None
        self.new_window_setting = None
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.table_raw_data = None
        self.load_data(data,title,type)  #载入数据
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
        self.title_matrix = title
        self.swapped_title_matrix = {v: k for k, v in self.title_matrix.items()}
        self.type_matrix = type
        self.open_windows = []
        self.open_windows.append(self.new_window)

    def msgbox_info(self, title, text):
        QMessageBox.about(self.new_window, title, text)

    # def load_data(self, data,title_matrix,type_matrix):
    #     self.table_raw_data = data
    #     self.model = QStandardItemModel()
    #     for col in self.table_raw_data.columns:
    #         self.model.appendRow(QStandardItem(str(col)))
    #     self.plot.listView.setModel(self.model)
    #     self.plot.listView.show()

    def add_to_column_list(self):
        selected = self.model.item(self.plot.listView.currentIndex().row()).text()
        parts = selected.split('\t', 1)
        selected = parts[-1]
        select_row = self.plot.tableWidget.selectedItems()[0].row()
        select_column = self.plot.tableWidget.selectedItems()[0].column()
        item = QTableWidgetItem(selected)
        self.plot.tableWidget.setItem(select_row, select_column, QTableWidgetItem(selected))
        next_row = select_row
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

        for i, column in enumerate(data_list):
            if column!='' and column in self.swapped_title_matrix:
                data_list[i] = self.swapped_title_matrix[column]

        plot_list = [item for item in data_list if item != '']  # 提取画图列

        #校验数据有效性
        for item in plot_list:
            if item not in self.table_raw_data.columns:
                self.msgbox_info('Error', '列名%s不存在，请检查'%str(item))
                return
        plot_df = self.table_raw_data[plot_list]  # 提取画图数据

        cur=0
        #数据校验
        x_name=[]
        y_name=[]
        for i in range(0, 20, 2):
            if bool(data_list[i]) != bool(data_list[i + 1]):
                self.msgbox_info('Error', 'x,y变量不匹配，请检查')
                return
        if all(item=='' for item in data_list):
            self.msgbox_info('Error', '列表全为空值，请检查')
            return


        for i in range(0, 20, 2):
            if data_list[i] == '' and data_list[i + 1] == '':
                continue
            slice=plot_df.iloc[:, [cur, cur + 1]].copy().isnull()
            any_nan=slice.any(axis=1)
            all_nan = slice.all(axis=1)
            result =(~(~any_nan| all_nan)).any()
            cur+=2

            if result:
                self.msgbox_info('Error', 'Row %s : %s 与 %s 列数据长度不一致，请检查'%(str(int((i/2+1))),str(data_list[i]),str(data_list[i + 1])))
                return
            if data_list[i]!='':
                y_name.append(data_list[i])
            if data_list[i+1]!='':
                x_name.append(data_list[i + 1])

        for i,x in enumerate(x_name):
            if self.title_matrix[x]!='' and x in self.title_matrix:
                x_name[i]=self.title_matrix[x]
        for i,y in enumerate( y_name):
            if self.title_matrix[y] !='' and y in self.title_matrix:
                y_name[i]=self.title_matrix[y]


        x_axis='X-axis'
        y_axis='Y_axis'
        title='Scatter Plot'

        if len(x_name) > 1:
            x_axis+= '(' + ', '.join(map(str, x_name)) + ')'
        elif len(x_name)==1:
            x_axis= str(x_name[0])

        if len(y_name) > 1:
            y_axis+= '(' + ', '.join(map(str, y_name)) + ')'
        elif len(y_name)==1:
            y_axis= str(y_name[0])

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
        self.plot_data(plot_df,x_axis,y_axis,title)
        self.new_window_plot.show()
        self.open_windows.append(self.new_window_plot)

    def plot_data(self, plot_df,x_axis,y_axis,title):
        self.figure.patch.set_facecolor('white')
        self.figure.subplots_adjust(left=0.13, right=0.95, top=0.9, bottom=0.13)
        ax = self.figure.add_subplot(111)

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei','Times New Roman']
        plt.rcParams['axes.unicode_minus'] = False
        # #
        # # 设置英文字体
        # plt.rcParams['font.family'] = 'serif'
        # plt.rcParams['font.serif'] = ['SimHei','Times New Roman']

        # 设置字体
        ax.set_xlabel(x_axis, fontdict={'family': 'sans-serif', 'size': 12, 'weight': 'normal'})
        ax.set_ylabel(y_axis, fontdict={'family': 'sans-serif', 'size': 12, 'weight': 'normal'})
        ax.set_title(title, fontdict={'family': 'sans-serif', 'size': 14, 'weight': 'bold'})


        colormap = plt.get_cmap('Set1')
        colormap2 = plt.get_cmap('Set2')

        formula = ''
        formula_plain = ''
        # fit_lines = []
        # labels = []
        for i in range(0, len(plot_df.columns), 2):
            # 确保有足够的列来配对
            if i + 1 < len(plot_df.columns):
                x = plot_df.iloc[:, i + 1].dropna(how='all')  # 第i+1列作为x
                y = plot_df.iloc[:, i].dropna(how='all')  # 第i列作为y-----------------<

                x_name = self.title_matrix[plot_df.columns[i+1]]
                if x_name=="":
                    x_name=plot_df.columns[i+1]
                y_name=self.title_matrix[plot_df.columns[i]]
                if y_name=="":
                    y_name=plot_df.columns[i]
                label = '%s vs %s' % (y_name,x_name)

                ax.scatter(x, y, color=colormap(i), label=label)

                sorted_indices = np.argsort(x)
                x_sorted = x[sorted_indices]
                if 1 in self.draw_list:
                    coefficients_linear = np.polyfit(x, y, 1)
                    # 生成拟合线的y值
                    y_linear = np.polyval(coefficients_linear, x_sorted)
                    line,=ax.plot(x_sorted, y_linear, label='Linear Fit - %s' % label)
                    linear_equation, linear_plain = self.coefficients_to_equation(coefficients_linear)
                    # fit_lines.append(line)
                    # labels.append(label)
                    formula += f'{label} - Linear: y={linear_equation}<br>'
                    formula_plain += f'{label} - Linear: y={linear_plain}\n'

                if 2 in self.draw_list:
                    coefficients_quadratic = np.polyfit(x, y, 2)
                    y_quadratic = np.polyval(coefficients_quadratic, x_sorted)
                    quadratic_equation, quadratic_plain = self.coefficients_to_equation(coefficients_quadratic)
                    ax.plot(x_sorted, y_quadratic, label='Quadratic Fit- %s' % label)
                    formula += f'{label} - Quadratic:y= {quadratic_equation}<br>'
                    formula_plain += f'{label} - Quadratic: y= {quadratic_plain}\n'
                if 3 in self.draw_list:
                    coefficients_cubic = np.polyfit(x, y, 3)
                    y_cubic = np.polyval(coefficients_cubic, x_sorted)
                    cubic_equation, cubic_plain = self.coefficients_to_equation(coefficients_cubic)
                    ax.plot(x_sorted, y_cubic, label='Cubic Fit - %s' % label)
                    formula += f'{label} - Cubic: y= {cubic_equation}<br>'
                    formula_plain += f'{label} - Cubic: y= {cubic_plain}\n'

        ax.legend()
        # Giving title to the chart using plt.title
        # ax.title('Scatter Plot')

        #y列的最大最小值
        odd_max = plot_df.iloc[:, ::2].max()
        odd_min = plot_df.iloc[:, ::2].min()
        odd_interval = max(odd_max) - min(odd_min.iloc)

        # 获取偶数列的最大值和最小值
        even_max = plot_df.iloc[:, 1::2].max()
        even_min = plot_df.iloc[:, 1::2].min()
        even_interval = max(even_max) - min(even_min)

        # ax = plt.gca()  # 实例化坐标轴
        ax.xaxis.set_major_locator(MaxNLocator(nbins=12))
        # bx = plt.gca()  # 实例化坐标轴
        ax.yaxis.set_major_locator(MaxNLocator(nbins=9))  # y轴的主刻度设置
        self.plain_text = formula_plain
        self.canvas.draw()
        if formula != '':
            self.result_window.textBrowser.setHtml(f'<html><body>{formula}</body></html>')

    #     # 添加鼠标移动事件
    #     self.canvas.mpl_connect('motion_notify_event', lambda event: self.on_move(ax,event, fit_lines, labels))
    #
    # def on_move(self, ax,event, fit_lines, labels):
    #     if event.inaxes is None:
    #         return
    #
    #     x, y = event.xdata, event.ydata
    #     distances = []
    #     nearest_points = []
    #
    #     for line, label in zip(fit_lines, labels):
    #         xdata = line.get_xdata()
    #         ydata = line.get_ydata()
    #         distances_to_line = np.sqrt((xdata - x) ** 2 + (ydata - y) ** 2)
    #         nearest_idx = np.argmin(distances_to_line)
    #         distances.append(distances_to_line[nearest_idx])
    #         nearest_points.append((xdata[nearest_idx], ydata[nearest_idx], label))
    #
    #     nearest_distance_idx = np.argmin(distances)
    #     nearest_point = nearest_points[nearest_distance_idx]
    #
    #     # 显示最近点的数值
    #     annotation_text = f"Label: {nearest_point[2]}\nX: {nearest_point[0]:.2f}\nY: {nearest_point[1]:.2f}"
    #     annotation = ax.annotate(annotation_text,
    #                              xy=(nearest_point[0], nearest_point[1]),
    #                              xytext=(20, 20),
    #                              textcoords="offset points",
    #                              bbox=dict(boxstyle="round", fc="w"),
    #                              arrowprops=dict(arrowstyle="->"))
    #     annotation.set_visible(True)
    #     self.canvas.draw_idle()
    #
    #     # 清除之前的注释
    #     annotations = [child for child in ax.get_children() if isinstance(child, plt.Annotation)]
    #     if len(annotations) > 1:
    #         for ann in annotations[:-1]:
    #             ann.remove()
    def terms_2_equation(self, terms):
        equation_parts = []
        for term in terms:
            coefficient_str = term[0].split('x')[0]
            coefficient = float(coefficient_str)
            if coefficient==0:
                continue
            result=''

            if coefficient_str.startswith('-'):
                result+=f' - {abs(coefficient):.2g}'
                offset=int(0)
            else:
                result+=f' + {coefficient:.2g}'
                offset=int(0)

            mid = term[0][len(coefficient_str) + offset:]
            if term[0][len(coefficient_str) +offset:] != "":
                if abs(coefficient)==1:
                    result=result[:len(result)-1]
                else:
                    result+='*'

                result+=f'{term[0][len(coefficient_str)+offset:]}'
            equation_parts.append(result)
        # 去掉第一个加号
        if equation_parts and equation_parts[0].startswith(' + '):
            equation_parts[0] = equation_parts[0][3:]
        return equation_parts
    def coefficients_to_equation(self, coefficients):
        # 将系数和对应的指数配对，并按照指数降序排列
        terms = []
        for i, c in enumerate(coefficients):
            power=len(coefficients)-i-1
            if power == 0:
                terms.append([f'{c:.2g}', power])
            elif power == 1:
                terms.append([f'{c:.2g}x', power])
            else:
                terms.append([f'{c:.2g}x<sup>{power}</sup>', power])
            # 按照指数降序排列
        # terms.sort(key=lambda x: -x[1])

        # 将排序后的项转换为Latex字符串 start
        parts_latex=self.terms_2_equation(terms)

        equation = ''.join(parts_latex) if parts_latex else '0'
        # 将排序后的项转换为方程字符串 end
        # 将排序后的项转换为方程字符串 start
        terms = []
        for i, c in enumerate(coefficients):
            power = len(coefficients) - i - 1
            if power == 0:
                terms.append([f'{c:.2g}', power])
            elif power == 1:
                terms.append([f'{c:.2g}x', power])
            else:
                terms.append([f'{c:.2g}x^{power}', power])
            # 按照指数降序排列
        # terms.sort(key=lambda x: -x[1])
        parts_plain= self.terms_2_equation(terms)
        equation_plain = ''.join(parts_plain) if parts_plain else '0'

        # 将方程字符串包裹在LaTeX的数学模式符号中
        return f'{equation}', equation_plain

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
        self.open_windows.append(self.new_window_setting)
    def get_setting(self):
        self.draw_list = []
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
        QMessageBox.about(self.new_window_plot,'提示','已复制到剪贴板')


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
    x1 = np.random.rand(100) * 10  # 生成50个随机x值
    y1 = 3 * x1 + 2 + np.random.randn(100) * 5  # 生成对应的y值，包含一些噪声

    x2 = np.random.rand(30) * 10  # 生成50个随机x值
    y2 = x2*x2*x2+10*x2*x2+5 * x2 + 2   # 生成对应的y值，包含一些噪声

    x22 = np.pad(x2, (0, 70), mode='constant', constant_values=np.nan)
    y22 = np.pad(y2, (0, 70), mode='constant', constant_values=np.nan)
    x5 = np.random.rand(100) * 10  # 生成50个随机x值
    df = pd.DataFrame({'C1': x1, 'C2': y1, 'C3': x22, 'C4': y22,'C5':x5})

    title_matrix = {'C1': 'Size', 'C2': 'Amount', 'C3': '', 'C4': 'Test','C5':"Wrong"}
    type_matrix = {'C1': '', 'C2': '', 'C3': '', 'C4': '','C5':'D'}
    # # 创建DataFrame
    # df = pd.DataFrame(data, columns=columns)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Scatter_plot(df,title_matrix,type_matrix)
    app.exec()
