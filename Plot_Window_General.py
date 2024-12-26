
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class general_window(object):
    def __init__(self,type):
        self.plot_type=type
        if self.plot_type=='Time_series_plot':
            from GUI_Plot_Window_General import Ui_Dialog as plot_window
            self.plot = plot_window(type)
        elif self.plot_type=='Scatter_plot':
            from GUI_Plot_Window_Scatter import Ui_Dialog as plot_window
            self.plot = plot_window()
        elif self.plot_type=='Histogram':
            from GUI_Plot_Window_General import Ui_Dialog as plot_window
            self.plot = plot_window(type)
        super().__init__()
        self.new_window = QtWidgets.QWidget()
        self.plot.setupUi(self.new_window)
        self.new_window.show()
        self.table_raw_data = None
        self.model = None
        self.plot.cancel_btn.clicked.connect(self.quit)
        self.plot.clear_btn.clicked.connect(self.clear_input)
        # self.plot.setting_btn.clicked.connect(self.test1)
        self.new_window.show()
        self.plot_type_dict = {'Time_series_plot': [''], 'Scatter_plot': [''],
                               'Histogram': ['Text','']}

    def quit(self):
        self.new_window.close()
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def msgbox_info(self, title, text):
        QMessageBox.about(self.new_window, title, text)
    def get_col_list_by_type(self,data,title_matrix,type_matrix,type:list):
        col_list=[]
        for col in self.table_raw_data.columns:
            if type_matrix[str(col)] in type:
                if title_matrix[str(col)]!='':
                    col_list.append(f'{str(col)}\t{title_matrix[str(col)]}')
                else:
                    col_list.append(f'{str(col)}')
        return col_list

    def customized_format(self,num):
        from decimal import Decimal, ROUND_HALF_UP
        num=Decimal(num)
        if num < 0:
            rounded_num = num.quantize(Decimal('.0001'), rounding=ROUND_HALF_UP)

            # 将Decimal对象转换为字符串，并去除末尾的无效0
            formatted_num = format(rounded_num, 'f')

            # 去除末尾的无效0
            formatted_num = formatted_num.rstrip('0').rstrip('.')
        elif num < 10:
            rounded_num = num.quantize(Decimal('.001'), rounding=ROUND_HALF_UP)

            # 将Decimal对象转换为字符串，并去除末尾的无效0
            formatted_num = format(rounded_num, 'f')

            # 去除末尾的无效0
            formatted_num = formatted_num.rstrip('0').rstrip('.')
        elif num < 100:
            rounded_num = num.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

            # 将Decimal对象转换为字符串，并去除末尾的无效0
            formatted_num = format(rounded_num, 'f')

            # 去除末尾的无效0
            formatted_num = formatted_num.rstrip('0').rstrip('.')
        elif num < 1000:
            rounded_num = num.quantize(Decimal('.1'), rounding=ROUND_HALF_UP)

            # 将Decimal对象转换为字符串，并去除末尾的无效0
            formatted_num = format(rounded_num, 'f')

            # # 去除末尾的无效0
            formatted_num = formatted_num.rstrip('0').rstrip('.')
        else:
            formatted_num = round(num, 0)

        return formatted_num
    def load_data(self,data,title_matrix,type_matrix):
        self.table_raw_data = data
        self.model = QStandardItemModel()
        import_list=self.get_col_list_by_type(data,title_matrix,type_matrix,self.plot_type_dict[self.plot_type])
        for col in import_list:
            self.model.appendRow(QStandardItem(str(col)))
        self.plot.listView.setModel(self.model)
        self.plot.listView.show()

    def add_to_column_list(self):
        selected = self.model.item(self.plot.listView.currentIndex().row()).text()
        parts = selected.split('\t', 1)
        selected=parts[-1]
        text = self.plot.text_input.toPlainText()
        if text != "":
            text += " "
        self.plot.text_input.setText(text + str(selected))

    def clear_input(self):
        self.plot.text_input.setText('')

    def col_class(self,df,colname):
        try:
            col_index = df.columns.get_loc(colname)  # 获取列名对应的列索引
        except KeyError:
            return False  ## 如果列名不存在，返回 "Text"

        # 遍历该列的所有值
        for row in df.itertuples(index=False):  # 跳过列名行
            value = getattr(row, colname)
            try:
                float(value)  # 尝试将值转换为浮点数
            except (ValueError, TypeError):
                return "Text"  # 如果转换失败，返回 "Text"

        return "Number"  # 如果所有值都能转换为数字，返回 "Number"