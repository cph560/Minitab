from General_Window import  general_window
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
import numpy as np
from histogram_setting import Ui_Dialog as setting_window
import matplotlib.pyplot as plt
import sys
import pandas as pd
from matplotlib.ticker import MaxNLocator
from scipy.stats import norm



class Histogram_plot(general_window):
    def __init__(self,data,title,type):
        super().__init__('Histogram')
        self.plot.ok_btn.clicked.connect(self.open_plot_window)
        self.plot.select_btn.clicked.connect(self.add_to_column_list)
        self.plot.listView.doubleClicked.connect(self.add_to_column_list)
        self.plot.setting_btn.clicked.connect(self.open_setting)
        self.distribution_set = True
        self.bin_set='Auto'
        self.stacked_set= False
        self.load_data(data,title,type)#载入数据
        self.open_windows = []
        self.open_windows.append(self.new_window)
        self.minimum_bins=8
        self.custom_bins = 8
        self.output_plain_text=''
        self.title_matrix = title
        self.swapped_title_matrix = {v: k for k, v in self.title_matrix.items()}
        self.type_matrix = type

        self.open_windows = []
        self.open_windows.append(self.new_window)
    def label_change(self):
        if self.setting.Btn_Bin_Autofit.isChecked():
            self.setting.label_bins.setText('Minimum Bins')
        if self.setting.Btn_Bin_Custom.isChecked():
            self.setting.label_bins.setText('Customized Bins')
    def open_setting(self):
        self.new_window_setting = QtWidgets.QWidget()
        self.setting = setting_window()
        self.setting.setupUi(self.new_window_setting)
        self.setting.Btn_Bin_Autofit.clicked.connect(self.label_change)
        self.setting.Btn_Bin_Custom.clicked.connect(self.label_change)
        self.setting.Btn_OK.clicked.connect(self.get_setting)
        self.setting.Btn_cancel.clicked.connect(self.quit_setting)
        self.new_window_setting.show()
        if self.distribution_set:
            self.setting.radioButton.setChecked(True)
        else:
            self.setting.radioButton_2.setChecked(True)

        if self.stacked_set:
            self.setting.Btn_stacked_yes.setChecked(True)
        else:
            self.setting.Btn_stacked_no.setChecked(True)

        if self.bin_set == 'Auto':
            self.setting.Btn_Bin_Autofit.setChecked(True)
            self.setting.lineEdit.setText(str(self.minimum_bins))
        else:
            self.setting.Btn_Bin_Custom.setChecked(True)
            self.setting.lineEdit.setText(str(self.custom_bins))

        self.open_windows.append(self.new_window_setting)


        # self.windows.append(self.new_window_setting)

    def quit_setting(self):
        self.new_window_setting.close()
    def get_setting(self):
        # distribution setting
        if self.setting.radioButton.isChecked():
            self.distribution_set = True
        elif self.setting.radioButton_2.isChecked():
            self.distribution_set = False
        # stacked setting
        if self.setting.Btn_stacked_yes.isChecked():
            self.stacked_set = True
        elif self.setting.Btn_stacked_no.isChecked():
            self.stacked_set = False
        # Bin setting
        if self.setting.Btn_Bin_Autofit.isChecked():
            self.bin_set = 'Auto'
            if self.data_verify(self.setting.lineEdit.text()):
                self.minimum_bins=int(self.setting.lineEdit.text())
            else:
                QMessageBox.about(self.new_window, 'Error', 'Bins amount invalid')
                return
        elif self.setting.Btn_Bin_Custom.isChecked():
            self.bin_set = 'Custom'
            if self.data_verify(self.setting.lineEdit.text()):
                self.custom_bins = int(self.setting.lineEdit.text())
            else:
                QMessageBox.about(self.new_window, 'Error', 'Bins amount invalid')
                return

        self.new_window_setting.close()
    def data_verify(self,data):
        try:
            result=int(data)
            if result>0:
                return True
            else:
                return False
        except:
            return False
    def copy_result(self):
        import pyperclip
        pyperclip.copy(self.output_plain_text)
        QMessageBox.about(self.new_window_plot,'提示','已复制到剪贴板')
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
    def open_plot_window(self):
        # 尝试关闭窗口
        # try:
        #     self.quit_plot_window()
        # except:
        #     pass
        if self.data_calibration():
            from Result_window import Ui_Plot_window as result_window
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
            from matplotlib.ticker import MaxNLocator

            self.new_window_plot = QtWidgets.QWidget()
            self.result_window = result_window()
            self.result_window.setupUi(self.new_window_plot)
            self.result_window.pushButton_close.clicked.connect(self.quit_plot_window)
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
            self.plot_data(stacked=self.stacked_set)
            self.new_window_plot.show()
            self.open_windows.append(self.new_window_plot)
    def quit_plot_window(self):
        self.new_window_plot.close()

    # def is_number(self,s):
    #     try:
    #         float(s)
    #         return True
    #     except ValueError:
    #         return False
    def plot_data(self,stacked=False):

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        # 设置英文字体
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Times New Roman']

        column_text = self.plot.text_input.toPlainText()
        column_list = column_text.split(' ')
        for i, column in enumerate(column_list):
            if column!='' and column in self.swapped_title_matrix:
                column_list[i] = self.swapped_title_matrix[column]

        for i in range(len(column_list) - 1, -1, -1):
            if column_list[i] == "":
                del column_list[i]
        '''分割位置，single plt/multiple'''
        try:
            #确定y轴标题

            title_list = []
            for x in column_list:
                if self.title_matrix[x] != '':
                    title_list.append(self.title_matrix[x])
                else:
                    title_list.append(x)
            label_y = ','.join(title_list)

            plot_data = self.table_raw_data.loc[:, column_list].copy()
            # 使用斯特奇斯规则确定bin的数量
            if self.bin_set == 'Auto':
                n = len(plot_data)
                bin_count=max(self.minimum_bins,int(np.sqrt(n)))
            else:
                bin_count=self.custom_bins
            #提取画图数据
            colormap = plt.get_cmap('Set1')
            colormap2= plt.get_cmap('Set2')

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.figure.patch.set_facecolor('white')
            self.figure.subplots_adjust(left=0.12, right=0.95, top=0.9, bottom=0.13)
            # 设置字体
            ax.set_xlabel('X-axis', fontdict={'family': 'serif', 'size': 12, 'weight': 'normal'})
            ax.set_ylabel('Y-axis', fontdict={'family': 'serif', 'size': 12, 'weight': 'normal'})
            ax.set_title('Histogram of %s'%label_y, fontdict={'family': 'serif', 'size': 14, 'weight': 'bold'})

            min_val = float('inf')
            max_val = float('-inf')
            data_list = []
            labels = []

            for i,column in enumerate(column_list):
                plot_data_drop=plot_data[column].dropna()#对绘图数据去除nan

                min_val = min(min_val, plot_data_drop.min())
                max_val = max(max_val, plot_data_drop.max())
                data_list.append(plot_data_drop)
                if self.title_matrix[column]!='':
                    labels.append(f'{self.title_matrix[column]}')
                else:
                    labels.append(column)


            if data_list:
                ax.hist(data_list, bins=bin_count, density=True, alpha=0.9,
                        color=[colormap(i) for i in range(len(data_list))], edgecolor='black', label=labels,
                        histtype='bar', stacked=stacked)

                if self.distribution_set:
                    fit_equations = {}
                    static_result={}

                    for i, column in enumerate(column_list):
                        col_label=column
                        if self.title_matrix[column]!='':
                            col_label=self.title_matrix[column]
                        plot_data_drop = plot_data[column].dropna()
                        mu, std = norm.fit(plot_data_drop)
                        x = np.linspace(min_val, max_val, 100)
                        y = norm.pdf(x, mu, std)
                        ax.plot(x, y, '-.', color=colormap2(i), linewidth=2, label=f'{col_label}-Fit')
                        mu_formatted = f"{mu:.4g}"
                        std_formatted = f"{std:.4g}"
                        Data_count=len(plot_data_drop)
                        # 保存拟合线方程
                        static_result[col_label] = f'\nMean: {mu_formatted}, Std: {std_formatted},Count:{Data_count}'
                        fit_equation = f"f(x) = (1 / ({std_formatted} * sqrt(2π))) * exp(-(x - {mu_formatted})^2 / (2 * {std_formatted}^2))"
                        fit_equations[col_label] = fit_equation
                    self.result_window.textBrowser.setText('')
                    # 构建完整的 HTML 字符串
                    html_content = ""
                    for col_label, equation in fit_equations.items():
                        html_content += f"Equation - {col_label}: {equation}<br>"
                        html_content += f"{static_result[col_label]}<br>"
                    plain_content=''
                    for col_label, result in fit_equations.items():
                        plain_content += f"Equation - {col_label}: {equation}\n"
                        plain_content += f"{static_result[col_label]}\n"

                    self.result_window.textBrowser.setHtml(html_content)
                    self.output_plain_text=plain_content
            ax.legend()
            #图标设置
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            # 添加标题和标签
            ax.set_title('Histogram of %s' % label_y)
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            self.canvas.draw()

        except Exception as e:
            print(e)
            QMessageBox.about(self.new_window, 'Error', str(e))

    # def latex_to_image(self, equation):
    #     fig, ax = plt.subplots()
    #     ax.text(0.5, 0.5, f'${equation}$', fontsize=20, ha='center', va='center')
    #     ax.axis('off')
    #
    #     buf = BytesIO()
    #     fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    #     buf.seek(0)
    #
    #     # 将图像数据转换为 base64 编码的字符串
    #     image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    #
    #     # 返回包含 base64 编码图像的 HTML 标签
    #     return f'<img src="data:image/png;base64,{image_base64}">'

if __name__ == '__main__':
    columns = ['C1', 'C2', 'C3', 'C4', 'C5']
    # 定义数据
    data = [
        [19.0, 14.0, 'AA', 'DD', 3.0],
        [3.0, 16.0, 'AA', 'AA', 20.0],
        [19.0, 5.0, 'AA', 'DD', 9.0],
        [18.0, 10.0, 'AA', 'DD', 8.0],
        [6.0, 14.0, 'AA', 'CC', 2.0],
        [0.0, 0.0, 'AA', 'DD', 0.0],
        [9.0, 8.0, 'CC', 'CC', 18.0],
        [5.0, 15.0, 'AA', 'CC', 9.0]
    ]
    title_matrix = {'C1': 'Size', 'C2': 'Amount', 'C3': '', 'C4': 'Test', 'C5': ''}
    type_matrix = {'C1': '', 'C2': '', 'C3': 'T', 'C4': 'T', 'C5': ''}

    # 创建DataFrame
    df = pd.DataFrame(data, columns=columns)
    # df=pd.DataFrame(np.random.randn(1000),columns=['1'])
    # df['2']=np.random.randn(1000)
    app = QtWidgets.QApplication(sys.argv)
    main_window = Histogram_plot(df,title_matrix,type_matrix)
    app.exec()
